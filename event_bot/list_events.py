from .embeds import event_embed


async def list_events(bot, event_channel):
    """Clear the given event channel and then populate it with its events"""
    channel = bot.get_channel(event_channel.id)
    await channel.purge()

    for event in event_channel.events:
        organizer = bot.find_guild_member(event_channel.guild_id, event.organizer_id)
        event_msg = await channel.send(embed=event_embed(event, organizer.display_name))
        event.message_id = event_msg.id

    with bot.transaction.new() as session:
        session.add(event_channel)