# These functions help you when things in irc interact with SQA
# When to use uen (unicode encode):
#   - Whenever you are pulling something *FROM THE DB* that will end up on the
#    wire to IRC
def uen(s):
    return s.encode('utf-8')

# When to use ude (unicode decode):
#   - Whenever you are putting something *INTO THE DB* that was user input from
#   IRC. Note: this applies to values used in any SQA statement, including
#   WHERE cluases

def ude(s):
    return s.decode('utf-8')

# When to use art: Whenever you want the thing you put in with a or an in front of it. If you give it None, you'll get "a None" because if you pass None where you should be passing a string you kind of deserve it. 

def art(noun):
    noun = str(noun)
    if noun[0] in ['a', 'e', 'i', 'o', 'u', 'y']:
        return "an " + noun
    return "a " + noun

