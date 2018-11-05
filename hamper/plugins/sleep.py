import random

from hamper.interfaces import ChatPlugin
from hamper.utils import ude

from sleeptxt import *


class SleepTalkPlugin(ChatPlugin):
    """*ZZZzzzz*"""

    name = 'sleep'
    priority = 0

    def setup(self, *args):
        pass

    def discusses_sleep(self, msg):
        for d in discussors:
            if d in msg:
                return d.strip() + "? "
        return False

    def sleepyreply(self, bot, comm, prefix = ""):

        resp = prefix + random.choice(sleepfacts)
        bot.reply(comm, '{0}: {1}'.format(comm['user'], resp))

    def message(self, bot, comm):
        msg = ude(comm['message'].strip())
        prefix = self.discusses_sleep(msg)
        if prefix:
            if comm['directed']:
                # always reply on question or comment to self about sleep
                self.sleepyreply(bot, comm)
            elif random.random() < .2:
                # often interject anyways
                self.sleepyreply(bot, comm, prefix)
            return True
        return False

