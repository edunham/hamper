import random

from hamper.interfaces import ChatPlugin
from hamper.utils import ude

from platitudestxt import *

class PlatitudesPlugin(ChatPlugin):
    """If you can't say something nice, don't say anything at all."""

    name = 'platitudes'
    priority = -3

    def setup(self, *args):
        pass

    def contemplate(self, bot, comm):
        resp = random.choice(platitudes)
        bot.reply(comm, resp)
        return True

    def inform(self, bot, comm):
        resp = random.choice(platitudes)
        bot.reply(comm, '{0}: {1}'.format(comm['user'], resp))
        return True

    def message(self, bot, comm):
        msg = ude(comm['message'].strip())
        if comm['directed']:
            if not '?' in msg:
                if random.random() < .3:
                    self.inform(bot, comm)
                else:
                    self.contemplate(bot, comm)
                return True
        elif random.random() < .0001:
            # Occasionally pipe up
            if random.random() < .2:
                self.inform(bot, comm)
            else:
                self.contemplate(bot, comm)
            return True
        return False


