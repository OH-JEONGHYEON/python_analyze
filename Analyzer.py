
import pymongo
from bson import ObjectId

from Sentence import Sentence
from Summarize import Summarize
from Time import Time
from Keyword import Tf_Idsf
from Relation import Relation

class Analyzer():
    def __init__(self, mid):

        conn = pymongo.MongoClient('13.209.73.233', 27017)
        db = conn.get_database('test')
        self.collection = db.get_collection('meets')
        self.mid = mid
        self.oid = ObjectId(self.mid)

        ## get talk
        result = self.collection.find({"_id": self.oid}, {"_id":False, "talk":True, "num_cluster":True})
        if result[0]:
            talk = sorted(result[0]['talk'], key=lambda x:x[1])
            self.sentences = [Sentence(i,t) for i,t in enumerate(talk)]
            self.num_cluster = result[0]['num_cluster']
            print(self.num_cluster)
            self.error = False
        else:
            self.error = True

    def start(self):

        ## summarize
        self.sum = Summarize(self.sentences, self.num_cluster)
        self.sum.save(self.collection, self.oid)

        ## time
        self.time = Time(self.sentences, self.sum.clusters)
        self.time.save(self.collection, self.oid)

        ## keyword
        self.keyword = Tf_Idsf(self.sentences)
        self.keyword.save(self.collection, self.oid)

        ## relation

        self.relation = Relation(self.sentences, self.mid)
        self.relation.save(self.collection, self.oid)

if __name__=="__main__":

    an = Analyzer("5bd83ae586c8cd5b4b355db6")
    # an = Analyzer("5bd0652dfbd6df56f060a70d")
    if not an.error:
        an.start()

        ## print for check
        for i,c in enumerate(an.sum.clusters):
            print("cluster{}".format(i+1))
            for s in c.sentences:
                print(s.text)
        for i,s in enumerate(an.sum.summaries):
            print("cluster_summarize{}".format(i + 1))
            for d in s:
                print(d)

        print("all", an.time.all)
        print("per_talker", an.time.per_talker)
        print("per_cluster", an.time.per_cluster)

        print("keword", an.keyword.get_result())

