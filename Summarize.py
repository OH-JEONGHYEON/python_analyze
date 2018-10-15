
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from lexrankr import LexRank


class Token(object):
    def __init__(self, index, word, tag):
        self.index = index
        self.word = word
        self.tag = tag

    def __str__(self):
        return self.word

    def __repr__(self):
        return str((self.index, self.word))

    def __ep__(self, another):
        return hasattr(another, 'index') and self.index == another.index

class Cluster(object):
    def __init__(self, index, sentences):
        self.index = index
        self.sentences = sentences

    def sen_with_talker(self):
        result = []
        for sen in self.sentences:
            result.append([sen.talker, sen.text])
        return result

    def sen2txt(self):
        text = ""
        for s in self.sentences:
            text += s.text
            text += ". "
        return text

    def __str__(self):
        return self.index

    def __repr__(self):
        return str(self.index)

    def __ep__(self, another):
        return hasattr(another, 'index') and self.index == another.index

class Summarize():

    def __init__(self, sentences, subject=1):

        self.sentences = sentences
        self.subject = subject
        self.text2token(self.sentences)
        self.tfidfv = TfidfVectorizer(max_df=0.8, min_df=2)   #norm='l2'
        self.token4tf = [" ".join(map(str, sen.tokens)) for sen in self.sentences]
        ## each sentence == each document
        # self.token4tf = []
        # for sen in self.sentences:
        #     self.token4tf.extend(sen.tokens)
        ## all sentences = 1 document
        x = self.tfidfv.fit_transform(self.token4tf)
        self.useful = self.filter_sentences(self.tfidfv.get_feature_names())
        self.clusters = self.clustering()
        lexrank = LexRank(clustering=None)
        self.summaries = []
        for c in self.clusters:
            lexrank.summarize(c.sen2txt())
            self.summaries.append(lexrank.probe())


    def text2token(self, sentences):
        for sen in sentences:
            okt = Okt()
            stopwords=[]
            useful_tags=['Noun', 'Verb', 'Adjective', 'Adverb', 'Alpha', 'Number']
            tokens = []
            for word, tag in okt.pos(sen.text, norm=True, stem=True):
                if(word in stopwords or tag not in useful_tags):
                    continue
                tokens.append(Token(sen.index, word, tag))
            sen.tokens = tokens


    def filter_sentences(self, dict, cnt=2):
        useful_sentences = []
        for sen in self.sentences:
            for t in sen.tokens:
                if t.word not in dict:
                    sen.tokens.remove(t)
            if len(sen.tokens) > cnt:
                useful_sentences.append(sen)

        return useful_sentences

    def clustering(self):
        self.token_list = []
        for sen in self.useful:
            self.token_list.extend(sen.tokens)
        token_len = [len(sen.tokens) for sen in self.useful]
        self.step_size = sum(token_len) // len(token_len)  # sentence per mean token legnth
        self.one_topic = round(len(self.token_list) * 0.2)
        self.window_size = round(self.one_topic / 2)
        similarity = self.cal_similarity()
        num_part = len(self.token_list)//self.one_topic+1
        cnt = len(similarity)//5
        part = [similarity[i*cnt:(i+1)*cnt] for i in range(num_part+1) if i*cnt<len(similarity)]
        min = [sorted(p, key=lambda x:x[1])[0] for p in part]
        boundary_list = sorted(min, key=lambda x:x[1])[:self.subject-1]

        start=0
        tmp_clusters=[]
        for b in boundary_list:
            i = b[0]
            token = self.token_list[i].word
            idx = self.token_list[i].index
            boundary = list(map(str, self.sentences[idx].tokens))
            pos = boundary.index(str(token))
            if(pos<len(boundary)//2):
                tmp_clusters.append(self.sentences[start:idx+1])
                start = idx+1
            else:
                tmp_clusters.append(self.sentences[start:idx])
                start=idx
        if start<len(self.sentences):
            tmp_clusters.append(self.sentences[start:])

        clusters = [Cluster(i,c) for i,c in enumerate(tmp_clusters)]
        return clusters

    def cal_similarity(self):
        start=0
        mid = self.window_size
        end = mid+self.window_size
        similarity = []
        stop = False
        while(not stop):
            if end > len(self.token_list):
                new_win = (len(self.token_list)-start)//2
                mid = start+new_win
                end = mid+new_win
                stop=True
            elif end==len(self.token_list):
                stop=True
            block1 = self.tfidfv.transform([" ".join(map(str, self.token_list[start:mid]))]).toarray()
            block2 = self.tfidfv.transform([" ".join(map(str, self.token_list[mid:end]))]).toarray()

            similarity.append([mid, cosine_similarity(block1, block2)[0][0]])

            start = start+self.step_size
            mid = start+self.window_size
            end = mid+self.window_size

        return similarity

    def matchTalker(self):
        summarize = []
        idx = 0
        for c in self.summaries:
            t = []
            for s in c:
                for i in range(idx, len(self.sentences)):
                    if s == self.sentences[i].text:
                        t.append([self.sentences[i].talker, self.sentences[i].text])
                        idx = i
                        break
            summarize.append(t)
        return summarize

    def save(self, coll, oid):
        ## cluster
        data = [c.sen_with_talker() for c in self.clusters]
        coll.update(
            {"_id": oid},
            {"$set": {"cluster": data}},
            upsert=True
        )

        coll.update(
            {"_id": oid},
            {"$set": {"num_cluster": len(self.clusters)}},
            upsert=True
        )

        ## summarize
        coll.update(
            { "_id": oid },
            { "$set": {"summarize": self.matchTalker()}},
            upsert=True
        )


if __name__=="__main__":
    from Sentence import Sentence

    import csv
    talk = []
    f = open('script3.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        talk.append(list(line))
    f.close()

    sentences = [Sentence(i,t) for i,t in enumerate(talk)]

    sum = Summarize(sentences,2)
    for i,c in enumerate(sum.clusters):
        print("cluster{}".format(i))
        for j,s in enumerate(c.sentences):
            print(j, s.text)

    print(sum.summaries)
    print(sum.matchTalker())