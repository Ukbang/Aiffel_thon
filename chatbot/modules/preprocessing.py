def get_name():
    first_name = ['김', '이', '박', '최', '방', '정', '구', '황', '장', '선우', '사', '조', '정', '윤', '임', '오', '신', '권', '한']

    last_name = ['영수', '정훈', '지훈', '민준', '도윤', '지은', '은주', '지혜', '유진', '서연', 
                 '서아', '본회', '문규', '우재', '승욱', '평섭', '진영', '준호', '수정', '민규', 
                 '재현', '재헌', '영인', '승룡', '혜수', '규리', '성미', '경선', '아연', '지희', 
                 '지수', '수진', '정희', '성혜', '민지', '윤지', '희연', '다진', '희영', '가람', 
                 '푸른', '혜미', '은별', '희주', '미현', '미지', '정아', '수연', '경애', '남호', 
                 '다혜', '민규', '민수', '민지', '병호', '성문', '소정', '성철', '수민', '수빈', 
                 '예슬', '예은', '예지', '유미', '은수', '은지', '은혜', '은미', '종민', '준영', 
                 '진석', '초롱', '태호', '혜민', '혜영', '홍민', '효준', '다름', '아름', '상우', 
                 '은비', '성일', '동욱', '동현', '민우', '상원', '소희', '영원', '은철', '종연', 
                 '지영', '태성', '상헌', '동철', '주현', '선영', '승훈', '우찬', '성욱', '민정', 
                 '용민', '성우', '한솔', '현승', '유경', '다운', '연화', '예화', '진주', '현정', 
                 '석환', '주연', '은선', '가영', '강훈', '민경', '민규', '은진', '혜경', '재훈', 
                 '종규', '상현', '찬형', '혜선', '효진', '춘호', '다솜', '윤철', '희진', '주영', 
                 '진성', '진철', '선희']

    return first_name, last_name

def make_name():
    import numpy as np
    import random
    
    first_name, last_name = get_name()

    first_number = random.choice(list(range(len(first_name))))
    last_number = random.choice(list(range(len(last_name))))
    p_number = np.random.rand(1)[0]

    if p_number >= 0.5:
        name = first_name[first_number]+last_name[last_number]
    else:
        name = last_name[last_number]

    return name

def clear_sentence(sentence):
    import numpy as np
    import re

    if '#@시스템#사진#' in sentence: # 해시태그 지정된 사진이 있는 행은 NaN 값으로 변경. 대체적으로 사진 하나만 보내는 경우가 많았음.
        sentence = np.NaN
        return sentence
    sentence = sentence.lower()   # 영어 소문자
    sentence = re.sub(r'\([^)]*\)', r'', sentence) # 괄호 안에 든 문구 삭제
    sentence = re.sub(r"([?.!,~])", r" \1 ", sentence) # 특수문자 주변에 공백 생성
    sentence = re.sub("#@이름#", make_name(), sentence) # 해시태그 지정된 이름을 임의의 이름으로 지정
    sentence = re.sub("#@이모티콘#", '', sentence)  # 이모티콘은 삭제
    sentence = re.sub(r'[^0-9a-zA-Z가-힣ㅋㅎㅠ\n?!._ ]+', r'', sentence) # 지정 단어 제외 삭제
    sentence = re.sub("\n", '\n ', sentence) # 문장나눔기준인 줄 바꿈 기호 뒤에 공백 한칸 생성
    sentence = re.sub(r'[ㅋ]{1}[ㅋ]+', r'ㅋㅋㅋ', sentence) # 반복되는 ㅋ 2개로 통일
    sentence = re.sub(r'[ㅎ]{1}[ㅎ]+', r'ㅎㅎ', sentence) # 반복되는 ㅎ 2개로 통일
    sentence = re.sub(r'[ㅠ]{1}[ㅠ]+', r'ㅠㅠ', sentence) # 반복되는 ㅠ 2개로 통일
    sentence = re.sub(r'[.]{1}[.]+', r'..', sentence) # 반복되는 . 2개로 통일
    sentence = re.sub(r'[키]{1}[키키]+', r'ㅋㅋ', sentence) # 반복되는 키키 2개로 통일
    sentence = re.sub(r'["   "]+', " ", sentence) # 여러개의 공백 1개로 변경
    
    return sentence

def word2vec_tokenize(dataframe, single=True):
    from tqdm import tqdm
    from konlpy.tag import Mecab
    
    if single == True:
        tokenizer = []
        mecab = Mecab()

        for i in tqdm(range(len(dataframe))):
            x = mecab.pos(dataframe['Q'][i])
            y = mecab.pos(dataframe['A'][i])
            questiosn_words = []
            answers_words = []
            for word in x:
                if word[1] == 'NNG' or word[1] == 'MAG' or word[1] == 'NP'  or word[1] == 'NR':
                    questiosn_words.append(word[0])
            for word in y:
                if word[1] == 'NNG' or word[1] == 'MAG' or word[1] == 'NP'  or word[1] == 'NR':
                    answers_words.append(word[0])
            tokenizer.append(questiosn_words)
            tokenizer.append(answers_words)

    if single == False:
        tokenizer = []
        mecab = Mecab()
        
        for i in tqdm(range(len(dataframe))):
            x = mecab.pos(dataframe['conversation'][i], stem=True, norm=True)
            words = []
            for word in x:
                if word[1] == 'NNG' or word[1] == 'MAG' or word[1] == 'NP'  or word[1] == 'NR':
                    words.append(word[0])
            tokenizer.append(words)

    return tokenizer