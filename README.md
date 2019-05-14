# python_analyze

인공지능 회의 분석 서비스의 핵심 엔진.
회의 내 개인별 음성의 stt 결과를 분석하여 주제 분류, 핵심문장, 핵심키워드 등 유의미한 정보를 도출하는 엔진.

2018 한이음 공모전 금상 수상 (팀 미피)

## 시작하기 전

### 환경

Flask(python 3.6), mongodb, tensorflow(tensorboard)

### 실행  

`$ python api.py`  


## 기능

### 핵심키워드 분석 - TF-IDSF(자체 개발)

TF-IDF 알고리즘을 활용한 자체 제작 알고리즘.  
(TF-IDF란, 단어빈도수 기반의 임베딩 알고리즘으로, 여러 개의 문서 중, 특정 문서에 많이 나온 단어가 해당 문서에서 중요한 단어라는 개념(TF)와 '하다'와 같이 보편적으로 많이 쓰이는 단어는 제외된다는 개념(IDF)를 종합한 알고리즘.)  
TF-IDF는 여러문서를 입력으로 받지만, 엔진의 입력값인 회의는 하나의 문서로 취급되기 때문에 <u>가상 문서 사이즈를 가정하여</u> 회의의 핵심 키워드를 분석.

### 단어 간 의미 관계 그래프 - Word2Vec + Tensor Board
<img src="https://raw.githubusercontent.com/OH-JEONGHYEON/python_analyze/master/word2vec.png" />  

Word2Vec은 동시에 등장하는 단어 관계를 학습하는 단어 벡터화(임베딩) 알고리즘의 종류.  
단어벡터 사이의 거리가 가까울수록 의미가 깊다.

### 주제분류 - 클러스터링 알고리즘(자체 개발)
논문을 활용한 자체 제작 알고리즘.  
1. 회의 스크립트에서 명사,동사,형용사 형태소만 사용. '하다','이다'와 같은 불필요한 단어 제거. (전처리)
2. 단어들을 일렬로 나열하여 임의의 사이즈로 나눔. 
3. 블록들 사이의 유사도를 계산하고, 유사도가 현저히 낮은 곳을 주제가 나뉘는 경계로 판단.
<img src="https://raw.githubusercontent.com/OH-JEONGHYEON/python_analyze/master/clustering.png" />

