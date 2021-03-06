from apollo.time_zones import ISO_TIME_ZONES
from apollo.translate import t


class TimeZoneInput:
    def __init__(self, bot):
        self.bot = bot

    async def call(self, user, channel):
        while True:
            resp = (await self.bot.get_next_message(user, channel)).content

            if not self._valid_time_zone_input(resp):
                await channel.send(t("event.invalid_time_zone"))
                continue

            time_zone_index = int(resp) - 1
            return ISO_TIME_ZONES[time_zone_index]

    def _valid_time_zone_input(self, value):
        return value.isdigit() and int(value) in range(1, len(ISO_TIME_ZONES) + 1)
