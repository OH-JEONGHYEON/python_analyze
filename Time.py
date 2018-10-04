
import datetime

class Time:
    def __init__(self, sentences, clusters):
        self.sentences = sentences
        self.clusters = clusters
        self.all = self.time_all()
        self.per_talker = self.time_per_talker()
        self.per_cluster = self.time_per_cluster()


    def time_all(self):
        all = 0
        for sen in self.sentences:
            all += sen.end-sen.start

        return str(datetime.timedelta(milliseconds=all))

    def time_per_talker(self):
        per_talker = {}
        for sen in self.sentences:
            if sen.talker not in per_talker:
                per_talker[sen.talker] = 0
            per_talker[sen.talker] += sen.end-sen.start

        for k in per_talker.keys():
            per_talker[k] = str(datetime.timedelta(milliseconds=per_talker[k]))

        return per_talker

    def time_per_cluster(self):
        per_cluster = []
        for c in self.clusters:
            time = 0
            for sen in c.sentences:
                time += sen.end - sen.start
            per_cluster.append(str(datetime.timedelta(milliseconds=time)))
        return per_cluster

    def save(self, coll, oid):
        coll.update(
            { "_id": oid },
            { "$set": {"time_all": self.all}},
            upsert=True
        )
        coll.update(
            {"_id": oid},
            {"$set": {"time_per_talker": self.per_talker}},
            upsert=True
        )
        coll.update(
            {"_id": oid},
            {"$set": {"time_per_cluster": self.per_cluster}},
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

    time = Time(sentences)
    print(time.per_talker)
