import random
import string

from hamper.interfaces import ChatPlugin
from hamper.utils import ude

from whometxt import *


def tyop(c):
    # typo a character
    if " " in c:
        return " "
    kb = [
        "1234567890",  # row 0
        "qwertyuiop",  # row 1
        " asdfghjkl",  # row 2
        "  zxcvbnm "
    ]  # row 3
    digs = "`1234567890-=[]\\;',./"
    updigs = "~!@#$%^&*()_+{}|:\"<>?"
    x = -1
    y = -1
    for row in kb:
        if c in row:
            y = kb.index(row)
            x = row.index(c)

    if y >= 0 and x >= 0:
        if y != 3 and random.random() < .2:
            y += 1
        if y != 0 and random.random() < .2:
            y -= 1
        if x != 9 and random.random() < .2:
            x += 1
        if x != 0 and random.random() < .2:
            x -= 1
        return kb[y][x]
    if c in digs:
        return updigs[digs.index(c)]
    if c in updigs:
        return digs[updigs.index(c)]
    return c.lower() if c.isupper() else c.upper()


def spin(phrase):
    # introduce typographical errors
    thresh = .9
    mood = thresh - random.random() * random.random()
    out = ''
    for c in phrase:
        if mood <= thresh:
            om = mood + random.random()  # increase mood a bit if low
            out += c
        if mood > thresh:
            if random.random() < mood:  # likelier if mood high
                om = mood * random.random()  # diminish mood a bit
            out += tyop(c)
        if mood > 1:
            om = mood - thresh
        mood = om
    return out


def art(noun):
    if noun[0] in ['a', 'e', 'i', 'o', 'u', 'y']:
        return "an " + noun
    return "a " + noun


def punc():
    return random.choice(['.', '...', '!', '?'])


def inger(word):
    if word.endswith("ing"):
        return word.replace("ing", "er")
    return False


class WhoMePlugin(ChatPlugin):
    """ What someone said, and how it harmed you
        Something you did, that failed to be charming """
    name = 'whome'
    priority = 100

    def setup(self, *args):
        pass

    def discusses_me(self, msg):
        founds = []
        parts = str(msg).translate(None, string.punctuation).split()
        for p in parts:
            if p.lower() in whome:
                founds.append(p)
        if len(founds) > 0:
            return random.choice(founds)
        return False

    def composed(self):
        # noun-verb noun-noun, thanks https://creativeswears.livejournal.com/
        ers = [inger(v) for v in verbs if v.endswith("ing")]
        out = '-'.join(random.choice(nouns), random.choice(verbs))
        out += " "
        out = '-'.join(random.choice(nouns), random.choice(nouns + ers))
        return out

    def repa(self, prefix):
        out = prefix + "? "  # vile?
        out += random.choice(mopes)  # gosh
        out += ", I must be "  # , I must be
        out += art(random.choice(bigs))  # a big
        out += " " + random.choice(whome)  # failure
        return out

    def repb(self, prefix):
        out = prefix  # barbaric
        out += "? Only " + art(random.choice(bigs))  # ? Only a massive
        out += " " + random.choice(whome) + "ing "  # failureing
        if random.random() < .5:
            out += self.composed()
        else:
            out += random.choice(whome) + " "  # terrible
            out += random.choice(whome)  # toaster
        out += " would call some"  # would call someone
        out += random.choice(['one ', 'thing ', 'body '])
        out += art(prefix)  # a barbaric
        out += punc()  # !
        return out

    def repc(self, prefix):
        return "no YOU'RE " + art(prefix) + punc()

    def repd(self, prefix):
        return "Who me, " + art(prefix) + "?"

    def repe(self, prefix):
        out = "you " + self.composed()
        # "you hat-wearing food-eater"
        if random.random() < .5:
            out = "Why " + out
            # why you hat-wearing food-eater
        if random.random() < .5:
            if random.random() < .5:
                out += " you " + random.choice("oughtta", "go and", "go",
                                               "better")
                # why you hat-wearing food-eater you better
            out += " " + random.choice(verbs)
            # why you hat-wearing food-eater stinking OR
            # why you hat-wearing food-eater you better stinking
            out += " " + art(self.composed)
        out += punc()

    def whomereply(self, bot, comm, prefix):
        resp = random.choice([
            self.repa, self.repb, self.repc, self.repd, self.repe, self.repe,
            self.repe
        ])(prefix)
        resp = spin(resp)
        bot.reply(comm, '{0}: {1}'.format(comm['user'], resp))

    def manners(self, bot, comm, prefix):
        if "##" in comm['channel']:
            # Offtopic? ANYTHING GOES
            if comm['directed']:
                self.whomereply(bot, comm, prefix)
                return True
            elif random.random() < .85:
                self.whomereply(bot, comm, prefix)
                return True
        elif comm['directed']:
            out = "Now now, " + random.choice(['saying', 'calling me'])
            out += " " + prefix
            out += " isn't very nice."
            bot.reply(comm, '{0}: {1}'.format(comm['user'], out))
            return True
        else:
            # Politely ignore unkind language in on-topic channels
            return False

    def hasu(self, msg):
        idx = -1
        splat = msg.translate(None,
                              '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~').split()
        if "you" in msg:
            idx = splat.index("you")
        if " u " in " " + msg + " ":
            idx = splat.index("u")
        if idx > -1:
            if idx == len(splat) - 1:
                # catch "bleep(0) you(1)", idx=1, len=2
                if idx >= 1:
                    return splat[idx - 1]
                return random.choice(whome)
            if splat[idx + 1].endswith("ing"):
                # "you(0) bleeping(1)!", idx=0, len=2 => "bleeper"
                if len(splat) == idx + 2:
                    return inger(splat[idx + 1])
                # "you bleeping bleep"
                return " ".join(splat[idx + 1], splat[idx + 2])
            # "you blorp" => "blorp"
            return splat[idx + 1]

    def message(self, bot, comm):
        msg = ude(comm['message'].strip())
        if "##" in comm['channel']:
            # Offtopic? ANYTHING GOES
            if comm['directed']:
                hu = self.hasu(msg)
                if hu:
                    self.whomereply(bot, comm, hu)
                    return True
        prefix = self.discusses_me(msg)
        if prefix:
            return self.manners(bot, comm, prefix)
        return False
