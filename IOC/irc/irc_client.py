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

    def on_welcome(self, connection, event):
        # connection.list()
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


def main():
    # ?USAGE irc_bot("server",PORT, CHANNEL,<nick,realname>)
    bot = Irc_bot("192.168.56.107", 6667, "#general")
    # bot.start()
    task = []
    for a in range(10):
        task.append(Irc_bot("192.168.56.107", 6667, "#general"))
    for a in task:
        a.start()


if __name__ == "__main__":
    main()
