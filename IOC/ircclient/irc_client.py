from getname import random_name
import irc.bot
import asyncio


class Irc_bot(irc.bot.SingleServerIRCBot):
    def __init__(self, server, port, channel, nick=None, realName=None):
        if not nick:
            nick = random_name("cat")
        if not realName:
            realName = random_name("dog")
        self.server = server
        self.channel = channel
        self.nick = nick
        self.realName = realName
        self.port = port
        irc.bot.SingleServerIRCBot.__init__(
            self, [(self.server, self.port)], self.nick, self.realName
        )

    def on_nicknameinuse(self, c, e):
        c.nick(random_name("cat") + "_")

    def on_welcome(self, connection, event):
        connection.join(self.channel)

    def _on_kick(self, connection, event):
        self.nick = random_name("cat")
        connection.nick(self.nick)
        connection.join(self.channel)

    def on_list(self, connection, event):
        self.ch = event.arguments
        for channel in self.channels:
            # connection.join(channel)
            if "#" in channel:
                print(channel)
                connection.join(channel)
                break

    def on_pubmsg(self, connection, event):
        message = event.arguments[0]
        sender = event.source.nick
        channel = event.target
        print(f"{sender} said in {channel}: {message}")


def reconn():
    print("-----------------")


async def main():
    bot1 = Irc_bot("192.168.56.107", 6667, "#general")
    bot2 = Irc_bot("192.168.56.107", 6667, "#general")
    bot4 = Irc_bot("192.168.56.107", 6668, "#general")
    tasks = await asyncio.gather(bot1.start(), bot2.start(), bot4.start())
    await bot1.start()


if __name__ == "__main__":
    asyncio.run(main())
