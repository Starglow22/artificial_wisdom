import random
import nltk.tokenize.treebank as tb

"""
Modified based on Markovify github project to include frequencies.
 
Model is represented as  a dict of dicts where the keys of the outer dict represent all possible states,
and point to the inner dicts. The inner dicts represent all possibilities for the "next" item in the chain, 
along with the count of times it appears.
"""

BEGIN = "___BEGIN__"
END = "___END__"

class MarkovChainer(object):
    def __init__(self, order):
        self.state_size = order
        self.beginnings = {}
        self.model = {}

    # pass a string with a terminator to the function to add it to the markov lists.
    def add_sentence(self, string):
        tkn = tb.TreebankWordTokenizer()
        words = tkn.tokenize(string.strip()) + [END]

        buf = []
        if len(words) >= self.state_size:
            begin = tuple(words[0:self.state_size])
            if begin in self.beginnings:
                self.beginnings[begin] += 1
            else:
                self.beginnings[begin] = 1

        for word in words:
            buf.append(word)
            if len(buf) == self.state_size + 1:
                state = tuple(buf[0:self.state_size])
                next_word = buf[-1]
                if state in self.model and next_word in self.model[state]:
                    self.model[state][next_word] += 1
                elif state in self.model:
                    self.model[state][next_word] = 1
                else:
                    self.model[state] = {next_word: 1}

                buf.pop(0)
            else:
                continue
        return

    # def add_text(self, text):
    #     text = re.sub(r'\n\s*\n/m', ".", text)
    #     seps = '([.!?;:])'
    #     pieces = re.split(seps, text)
    #     sentence = ""
    #     for piece in pieces:
    #         if piece != "":
    #             if re.search(seps, piece):
    #                 self.add_sentence(sentence, piece)
    #                 sentence = ""
    #             else:
    #                 sentence = piece

    def generate_sentence(self):
        """
        Return a list representing a single run of the Markov model, either
        starting with a naive BEGIN state, or the provided `init_state` (as a tuple).
        """
        tokens = self.gen()
        dtkn = tb.TreebankWordDetokenizer()
        result = dtkn.detokenize(tokens)
        # Cosmetic punctuation spacing fixed
        result = result.replace(" ’ ", "’").replace('“ ', '“').replace(' ”', '”')

        def find_all(ch, s):
            return [i for i, ltr in enumerate(s) if ltr == ch]

        # Chain rarely closes brackets
        if '“' in result and '”' not in result:
            start_index = result.find('”')
            valid_insert_pos = list(filter(lambda i: i > start_index, find_all(' ', result)))
            selected_pos = random.choice(valid_insert_pos)
            result = result[:selected_pos] + '”' + result[selected_pos:]

        return result

    def gen(self):
        """
        Generate until the chain reaches the END state.
        """

        choices, weights = zip(*self.beginnings.items())
        state = random.choices(choices, weights=weights)[0]
        sent = list(state)
        while True:
            next_word = self.move(state)
            if next_word == END: break
            sent.append(next_word)

            state = tuple(state[1:]) + (next_word,)

        return sent

        # sentence = random.choice(self.beginnings)
        # if len(sentence) == self.state_size:
        #     nw = True
        #     while nw is not None:
        #         state = tuple(sentence[0:self.state_size])
        #         try:
        #             choices, weights = zip(self.model[state].items())
        #             nw = self.next_word_for(state)
        #             if nw is not None:
        #                 sentence.append(nw)
        #             else:
        #                 continue
        #         except Exception:
        #             nw = False
        #     new_res = sentence[0:-2]
        #     if new_res[0].istitle() or new_res[0].isupper():
        #         pass
        #     else:
        #         new_res[0] = new_res[0].capitalize()
        #     sentence = ""
        #     for word in new_res:
        #         sentence += word + " "
        #     sentence += sentence[-2] + ("" if sentence[-1] in ".!?;:" else " ") + sentence[-1]
        #
        # else:
        #     sentence = None
        # return sentence

    def move(self, state):
        """
        Given a state, choose the next item at random.
        """

        # TODO: smooth weights - log? Switch to a single word state for more possibilities?
        choices, weights = zip(*self.model[state].items())
        selection = random.choices(choices, weights=weights)
        return selection[0]



if __name__ == "__main__":
    print("Try running ebooks.py first")
