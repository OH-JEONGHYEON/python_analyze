
from gensim.models import Word2Vec
import boto3

class Relation():

    def __init__(self, sentences, mid):

        data = []
        for s in sentences:
            li = []
            for t in s.tokens:
                if t.tag == "Noun":
                    li.append(t.word)
            data.append(li)
        print(data)

        model = Word2Vec(data, iter=1000, sample=0.01)
        model.save("word2vec.model")

        s3 = boto3.client('s3')
        bucket_name = "tensorpath"
        upload_file_name = "word2vec.model"
        self.dest_file_name = mid+"_word2vec.model"

        s3.upload_file(upload_file_name, bucket_name, self.dest_file_name, ExtraArgs={'ACL': 'public-read'})

    def save(self, coll, oid):
        coll.update(
            {"_id": oid},
            {"$set": {"word2vec": "https://s3.ap-northeast-2.amazonaws.com/tensorpath/"+self.dest_file_name}},
            upsert=True
        )


if __name__ == '__main__' :

    from Sentence import Sentence
    from Summarize import Summarize

    import csv

    talk = []
    f = open('script3.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        talk.append(list(line))
    f.close()
    talk[0][0] = 1

    sentences = [Sentence(i, t) for i, t in enumerate(talk)]
    sum = Summarize(sentences, 2)

    # 트레이닝된 word2vec 모델명, tensorboard file path
    relation = Relation(sentences, "test")
