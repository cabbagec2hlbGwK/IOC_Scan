from getname import random_name
from IOC.irc import bot
import asyncio


class Irc_bot(bot.SingleServerIRCBot):
    def __init__(self, server, port, channel, nick=None, realName=None, proxy=None):
        if not nick:
            nick = random_name("cat")
        if not realName:
            realName = random_name("dog")
        self.server = server
        self.channel = channel
        self.nick = nick
        self.realName = realName
        self.port = port
        self.proxy = proxy
        if not proxy:
            connection = (self.server, self.port)
        else:
            connection = (self.server, self.port, self.proxy)
        bot.SingleServerIRCBot.__init__(self, [connection], self.nick, self.realName)

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


async def main(lists):
    bots = []
    for irc in lists:
        bots.append(Irc_bot(irc["server"], irc["port"], irc["channel"]))
    bot_tasks = [b.start() for b in bots]
    await asyncio.gather(*bot_tasks)


if __name__ == "__main__":
    asyncio.run(main())
