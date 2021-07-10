import json
import asyncio
import discord


class Client(discord.Client):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(
            everyone=False, roles=False, users=True)
        intents = discord.Intents.all()
        super().__init__(
            intents=intents,
            allowed_mentions=allowed_mentions
        )
        self.down = False

    async def on_ready(self):
        print('start')

    async def on_message(self, message):
        for command in commands:
            if message.content.startswith(command):
                if self.down:
                    return await message.channel.send(down_msg)

                def check(m):
                    if m.channel == message.channel and m.author == self.user:
                        return True
                    return False
                try:
                    await self.wait_for("message", timeout=1, check=check)
                except asyncio.TimeoutError:
                    await message.channel.trigger_typing()
                    try:
                        await self.wait_for("message", timeout=3, check=check)
                    except asyncio.TimeoutError:
                        await self.on_down(message)

    async def on_down(self, message):
        self.down = True
        await message.channel.send(down_msg)
        owner = (await self.application_info()).owner
        log_ch = self.get_channel(log_ch_id)

        def owner_check(m):
            if m.author.id == owner.id and m.channel == log_ch:
                return True
            return False
        notice = await log_ch.send(notice_msg)
        mention = await log_ch.send(owner.mention)
        while True:
            try:
                await self.wait_for("message", check=owner_check, timeout=mention_span)
            except asyncio.TimeoutError:
                if mention_span != 0:
                    await mention.delete()
                    mention = await log_ch.send(owner.mention)
                continue
            await log_ch.send("通常運転に移行")
            self.down = False
            break


def main():
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
    TOKEN = config.get("TOKEN")
    global commands, log_ch_id, down_msg, notice_msg, mention_span
    commands = config.get("commands")
    log_ch_id = config.get("log_ch_id")
    down_msg = config.get("down_msg")
    notice_msg = config.get("notice_msg")
    mention_span = config.get("mention_span")
    client = Client()
    client.run(TOKEN)


if __name__ == "__main__":
    main()
