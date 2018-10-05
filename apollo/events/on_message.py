from apollo.translate import t


class OnMessage:

    def __init__(self, bot):
        self.bot = bot


    async def on_message(self, message):
        # Delete user messages sent to event channels and notify them
        # as to why this is being done.
        #
        # Many users do not initially understand the intention behind
        # event channels, and end up using them as regular channels, only
        # to have a rude awakening when the channel is cleared.
        if (self.bot.cache.event_channel_exists(message.channel.id) and not
            self.bot.cache.event_exists(message.id)):
            await message.delete()

            if message.author.id != self.bot.user.id:
                await message.author.send(
                    t("notify.message_deleted").format(message.channel.mention)
                    )