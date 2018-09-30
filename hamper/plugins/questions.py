# -*- coding: utf-8 -*-

import random
import re
import string

from hamper.interfaces import ChatCommandPlugin, ChatPlugin, Command
from hamper.utils import ude

from questionstxt import *

class YesNoPlugin(ChatPlugin):

    name = 'yesno'
    priority = -1

    def setup(self, *args):
        """
        Set up the list of responses, with weights. If the weight of a response
        is 'eq', it will be assigned a value that splits what is left after
        everything that has a number is assigned. If it's weight is some
        fraction of 'eq' (ie: 'eq/2' or 'eq/3'), then it will be assigned
        1/2, 1/3, etc of the 'eq' weight. All probabilities will add up to
        1.0 (plus or minus any rounding errors).
        """

        # responses came from questions.txt
        resps = responses
        resps += [(i.strip(), 'eq') for i in affirmatives]
        resps += [(i.strip(), 'eq') for i in negatories]
        self.advices = [(x, 1) for x in obliques]
        total_prob = 0
        real_resp = []
        evens = []
        for resp, prob in resps:
            if isinstance(prob, str):
                if prob.startswith('eq'):
                    sp = prob.split('/')
                    if len(sp) == 1:
                        evens.append((resp, 1))
                    else:
                        div = int(sp[1])
                        evens.append((resp, 1.0 / div))

            else:
                real_resp.append((resp, prob))
                total_prob += prob

        # Share is the probability of a "eq" probability. Share/2 would be the
        # probability of a "eq/2" probability.
        share = (1 - total_prob) / sum(div for _, div in evens)
        for resp, divisor in evens:
            real_resp.append((resp, share * divisor))

        self.resps = real_resp
        self.is_question = re.compile('.*\?(\?|!)*$')

    def shouldq(self, bot, comm):
        resp = random.choice(obliques)
        bot.reply(comm, '{0}: {1}'.format(comm['user'], resp))
        return True

    def articleize(self, noun):
        if random.random() < .3:
            noun = random.choice(adjs) + ' ' + noun
        if noun[0] in ['a', 'e', 'i', 'o', 'u', 'y']:
            return "an " + noun
        return "a " + noun

    def canq(self, bot, comm):
        """
        <@person> hamper: pls remind me that i cannot just go around buying tubas kthx
        <hamper> I share your pain.
        <@human> hamper: can person just go around buying tubas?
        <hamper> human: Perhaps try with a false blade and a tongue.
        <@human> hamper: can person just go around buying tubas with a false blade and a tongue?
        <hamper> human: Yes, you'll need a scissors?
        <@human> hamper: can person just go around buying tubas with a false blade, a tongue, and scissors?
        <hamper> human: Nope, there's too much of a spade...
        <@human> hamper: can person just go around buying tubas with a false blade, a tongue, and scissors, but without a spade?
        <hamper> human: Maybe if you had a hollow square?
        <@human> hamper: can person just go around buying tubas with a false blade, a tongue, and scissors, but without a spade, but with a hollow square?
        <hamper> human: Yes, but watch out for a regular floor and a sponge.
        <@person> you found the feature!
        """
        resp = random.choice(canstarts)
        resp += self.articleize(random.choice(nouns))
        if random.random() < .5:
                resp += " and " + self.articleize(random.choice(nouns))
        if random.random() < .1:
                resp += " and " + self.articleize(random.choice(nouns))
        resp += random.choice(['...', '.', '?'])
        bot.reply(comm, '{0}: {1}'.format(comm['user'], resp))
        return True

    def xtoy(self):
        x = str(int(random.random()*10))
        y = str(int(random.random()*10))
        return x + " to " + y

    def manything(self, msg):
        parts = str(msg).translate(None, string.punctuation)
        parts = parts.split()
        quantifiers = ['many', 'much']
        for q in quantifiers:
            if q in msg:
                try:
                    idx = parts.index(q)
                    for i in range(idx, len(parts)):
                        if len(parts[i]) > 4:
                            # Let's pretend to plural.
                            return parts[i].rstrip('s') + 's'
                except ValueError:
                    return "of " + random.choice(['it','them','that'])
        return None

    def howmany(self, bot, comm, msg):
        thing = self.manything(msg)
        resp = random.randint(-5, 100)
        if resp > 80:
            resp = random.randint(80, 1000)
        resp = str(resp)
        if resp == '0':
            if thing:
                resp = "No " + thing + " at all."
            else:
                resp = "None at all."
        if thing:
            if resp == '1':
                resp = "Just a single " + thing.rstrip('s')
            else:
                resp += " " + thing
        if random.random() < .05:
            if thing:
                resp = "All the " + thing + "!"
            else:
                resp = "All of them!"
        bot.reply(comm, resp)
        return True

    def betting(self, bot, comm):
        resp = random.choice(bettings)
        if random.random() < .7:
            resp = random.choice(idcall)
            resp += random.choice(foragainst)
            resp += random.choice(['it ','that ','such nonsense ', 'such a thing '])
            resp += self.xtoy()
        bot.reply(comm, resp)
        return True

    def hamperesque(self, bot, comm, msg):
            whatsay = ""
            if "n't" in msg:
                whatsay = random.choice(negatories)
            for n in negatories:
                if n in msg:
                    whatsay = random.choice(negatories)
            for a in affirmatives:
                if a in msg:
                    whatsay = random.choice(affirmatives)
            if "n't" in msg:
                whatsay = random.choice(negatories)
            if whatsay != "":
                bot.reply(comm, '{0}: {1}'.format(comm['user'], whatsay))
            else:
                r = random.random()
                replies = self.resps
                for resp, prob in replies:
                    r -= prob
                    if r < 0:
                        bot.reply(comm, '{0}: {1}'.format(comm['user'], resp))
                        return True

    def sortq(self, bot, comm, msg):
        if "should " in msg:
            return self.shouldq(bot, comm)
        for b in betwords:
            if b in msg:
                return self.betting(bot, comm)

        if "many" in msg or "much" in msg:
            # TODO handle "much" with units
            return self.howmany(bot, comm, msg)

        if "can " in msg or "could" in msg or " how" in " "+msg:
            return self.canq(bot, comm)
        return self.hamperesque(bot, comm, msg)

    def message(self, bot, comm):
        msg = ude(comm['message'].strip()).lower()
        if self.is_question.search(msg):
            if comm['directed']:
                self.sortq(bot, comm, msg)
            elif random.random() < .1:
                self.sortq(bot, comm, msg)
        return False


class ChoicesPlugin(ChatCommandPlugin):
    """
    Answers questions like "apples or bananas?" "this, that or the other
    things", and "should I do homework or play videogames?"
    """

    name = 'choices'
    priority = 0

    class ChoicesCommand(Command):
        regex = r'^.* or .*\?$'

        name = 'choices'
        short_desc = None
        long_desc = None

        def command(self, bot, comm, groups):
            choices = self.parse(comm['message'])
            print choices
            chance_of_snark = 0.05
            snarks = [
                "I don't know, I'm just a bot",
                ['Neither', 'None of them.'],
                ['Why not both?', 'Why not all of them?'],
                [u'¿Por qué no los dos?', u'¿Por qué no los todos?'],
            ]
            snarks += obliques

            if random.random() < chance_of_snark:
                # snark. ignore choices and choose something funny
                snark = random.choice(snarks)
                if isinstance(snarks, list):
                    conjugation = 0 if len(choices) == 2 else 1
                    choice = snark[conjugation]
                else:
                    choice = snark
            else:
                # no snark, give one of the original choices
                choice = random.choice(choices) + '.'
            print choice
            bot.reply(comm, u'{0}: {1}'.format(comm['user'], choice))
            return True

        @staticmethod
        def parse(question):
            """
            Parses out choices in a 'or' based, possible comma-ed list.

            >>> parse = ChoicesPlugin.ChoicesCommand.parse
            >>> parse('x or y?')
            ['x', 'y']
            >>> parse('x, y or z?')
            ['x', 'y', 'z']
            >>> parse('this thing, that thing or the other thing?')
            ['this thing', 'that thing', 'the other thing']
            >>> parse('door or window?')
            ['door', 'window']
            >>> parse('should i do homework or play video games?')
            ['do homework', 'play video games']
            """
            # Handle things like "should ___ X or Y"
            if question.lower().startswith('should'):
                question = ' '.join(question.split()[2:])

            question = question.strip('?')
            # split on both ',' and ' or '
            choices = question.split(',')
            choices = sum((c.split(' or ') for c in choices), [])
            # Get rid of empty strings
            choices = filter(bool, (c.strip() for c in choices))
            return choices


if __name__ == '__main__':
    import doctest
    doctest.testmod()
