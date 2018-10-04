class Sentence(object):
    def __init__(self, index, talk):
        self.index = index
        self.talker = str(talk[0])
        self.start = talk[1]
        self.end = talk[2]
        self.text = talk[3]
        ## self.tokens

    def __str__(self):
        return str(self.index)


    def __repr__(self):
        try:
            return self.text.encode('utf-8')
        except:
            return self.text

    def __ep__(self, another):
        return hasattr(another, 'index') and self.index == another.index

    def __hash__(self):
        return self.index