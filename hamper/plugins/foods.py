import random

from hamper.interfaces import ChatPlugin
from hamper.utils import ude

from foods.txt import *


class FoodsPlugin(ChatPlugin):
    """Even robots can get peckish"""

    name = 'foods'
    priority = 0

    def setup(self, *args):
        pass

    def articleize(self, noun):
        if random.random() < .3:
            noun = random.choice(foodunits) + " of " + noun
        if noun[0] in ['a', 'e', 'i', 'o', 'u', 'y']:
            return "an " + noun
        return "a " + noun

    def discusses_food(self, msg):
        for d in discussors:
            if d in msg:
                return d.strip() + "? "
        return False

    def describe_ingredient(self):
        """ apple. tart apple with vinegar. """
        resp = random.choice(ingredients)
        if random.random() < .2:
            resp = random.choice(foodqualities) + " " + resp
        if random.random() < .2:
            resp += " with " + self.describe_additive()
        return resp

    def describe_additive(self):
        """ vinegar. spicy vinegar. a spicy vinegar. """
        resp = random.choice(additives)
        if random.random() < .2:
           resp = random.choice(foodqualities) + ' ' + resp
        if random.random() < .01:
           resp = self.articleize(resp)
        return resp

    def describe_dish(self):
        """a burrito. a lettuce burrito with ketchup and raspberry."""
        resp = random.choice(foodpreparations)
        if random.random() < .85:
            resp = self.describe_ingredient() + ' ' + resp
            if random.random() < .2:
                resp = self.describe_ingredient() + ' and ' + resp
                if random.random() < .2:
                    resp = self.describe_ingredient() + ', ' + resp
        if random.random() < .5:
            resp += " with " + self.describe_additive()
        elif random.random() < .5:
            resp += " with " + self.describe_ingredient()
        return self.articleize(resp)

    def describe_meal(self):
        resp = self.describe_dish()
        if random.random() < .1:
            resp += ", and " + self.describe_meal()
        return resp

    def suggest(self):
        resp = self.describe_meal()
        if random.random() < .7:
            resp = random.choice(foodverbs) + ' ' + resp
            if random.random() < .5:
                resp = random.choice(suggestions) + ' ' + resp
            if random.random() < .3:
                resp += random.choice([' made with ', ' on ', ' using '])
                resp += self.articleize(random.choice(foodtools))
        return resp

    def foodyreply(self, bot, comm, prefix = ""):
        resp = prefix + self.suggest()
        bot.reply(comm, '{0}: {1}'.format(comm['user'], resp))

    def message(self, bot, comm):
        msg = ude(comm['message'].strip())
        prefix = self.discusses_food(msg)
        if prefix:
            if comm['directed']:
                # always reply on question or comment to self about food
                self.foodyreply(bot, comm)
            elif random.random() < .7:
                # often interject anyways
                self.foodyreply(bot, comm, prefix)
            return True
        return False

