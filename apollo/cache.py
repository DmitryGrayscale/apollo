from apollo.models import Event, EventChannel, Guild
from contextlib import contextmanager


class Cache:

    def __init__(self, Session):
        self.Session = Session
        self.messages_marked_for_deletion = set()
        self.event_message_ids = set()
        self.event_channel_ids = set()
        self.prefixes = {}


    @contextmanager
    def scoped_session(self):
        """Provide a transactional scope around a series of operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


    def create_event_channel(self, event_channel_id):
        self.event_channel_ids.add(event_channel_id)


    def delete_event_channel(self, event_channel_id):
        self.event_channel_ids.remove(event_channel_id)


    def delete_event(self, message_id):
        self.event_message_ids.remove(message_id)


    def delete_prefix(self, guild_id):
        self.prefixes.pop(guild_id)


    def event_channel_exists(self, event_channel_id):
        return event_channel_id in self.event_channel_ids


    def event_exists(self, message_id):
        return message_id in self.event_message_ids


    def get_prefix(self, guild_id):
        return self.prefixes[guild_id]


    def load_event_channel_ids(self):
        with self.scoped_session() as session:
            event_channels = session.query(EventChannel).all()
        for event_channel in event_channels:
            self.event_channel_ids.add(event_channel.id)


    def load_event_message_ids(self):
        with self.scoped_session() as session:
            events = session.query(Event).all()
        for event in events:
            self.event_message_ids.add(event.message_id)


    def load_prefixes(self):
        with self.scoped_session() as session:
            guilds = session.query(Guild).all()
        for guild in guilds:
            self.prefixes[guild.id] = guild.prefix


    def mark_message_for_deletion(self, message_id):
        self.messages_marked_for_deletion.add(message_id)


    def message_marked_for_deletion(self, message_id):
        return message_id in self.messages_marked_for_deletion


    def unmark_message_for_deletion(self, message_id):
        self.messages_marked_for_deletion.remove(message_id)


    def update_event(self, old_message_id, new_message_id):
        try:
            # If the event is new, it won't be in the cache
            self.event_message_ids.remove(old_message_id)
        except:
            pass
        self.event_message_ids.add(new_message_id)


    def update_prefix(self, guild_id, prefix):
        self.prefixes[guild_id] = prefix
