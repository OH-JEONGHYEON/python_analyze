
import operator
from konlpy.tag import Okt
import math


class Tf_Idsf:
    def __init__(self, sentences, doc_size=3):

        self.sentences = sentences

        # 포스테깅 및 stopword 처리
        word_list = self.postaging()
        print(word_list)

        self.tf_idsf = self.tf_ids(doc_size, word_list)
        self.tf_idsf = list(map(list,sorted(self.tf_idsf.items(), key=operator.itemgetter(1), reverse=True)))

    def get_result(self):
        return self.tf_idsf[:10]

    def tf_ids(self, doc_size, word_list):
        tfds = {}  # 구조 단어:[tf,ids,index]
        for i, word in enumerate(word_list):
            if word in tfds:
                # 이전 index와 비교하여 doc_size 안에있는경우 tf만 추가
                if tfds[word][2] + doc_size >= i:
                    # doc_size 안에서 추가시 tf만 추가
                    tfds[word][0] += 1
                else:
                    # doc_size를 벗어난 경우 모두 변경 및 index는 초기화
                    tfds[word][0] += 1
                    tfds[word][1] += 1
                    tfds[word][2] += i
            else:
                # 단어가 없는경우 새로 등록
                tfds[word] = [1, 1, i]
        # 총 문서 갯수 구하기
        doc_count = int(len(word_list) / doc_size)
        # 이제 각 딕셔너리 곱해서 tf_ids로 변경
        tf_ids = {}

        # print("tfds : ",tfds)

        # http://dev.youngkyu.kr/25 사이트를 참고한 공
        for key, value in tfds.items():
            tf_ids[key] = value[0] * math.log10(doc_count / value[1])

        return tf_ids

    def postaging(self):
        okt = Okt()
        want = ['Noun']
        stopword = ['어어', '넷', '만', '것', '타', '최', '태', '개', '홈', '선', '끼', '각', '번', '하다', '음', '화', '이다', ' ', '다',
                    '더', '포', '제', '저', '여기', '고', '씬', '첨', '난', '면', '으루', '네', '정보', '생각', '시간']
        pos = []
        for sen in self.sentences:
            token = []
            for t in okt.pos(sen.text, norm=True, stem=True):
                if (t[1] in want) and (t[0] not in stopword) and (len(t[0]) > 1):
                    token.append(t[0])

            pos.extend(token)

        return pos

    def save(self, coll, oid):
        coll.update(
            {"_id": oid},
            {"$set": {"keyword": self.get_result()}},
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
    keyword = Tf_Idsf(sentences)
    print(keyword.get_result())

