from common import *
import random


def message_check(message):
    
    re_message = message.replace(' ', '').lower()
    
    if re_message.encode().isalpha():
        if 'have' in message or 'you' in message or 'name' in message:
            return message
        else:
            return_text = translator_typos(message) # 번역된 문장
            if return_text == message_check(return_text): # 번역된 문장을 함수에 넣었을 때 어떠한 커맨드에 해당되지 않아서 그대로 출력될 경우
                return f'{return_text} 라고 말씀하신게 맞을까요?' # 번역 문장
            else:
                return message_check(return_text)
    
    elif find_bad_words(re_message):
        return_text = '그건 나쁜말이야 그런말은 쓰면 안돼!'
        return return_text
    elif '시간 알려줘' in message or '지금 몇시야' in message:
        return_text = find_time()
        return return_text
    elif '날씨 어때' in message or '날씨 알려줘' in message:
        return_text = find_weather(message)
        return return_text
    elif '주가 알려줘' in message or '주식 얼마야?' in message or '주가 얼마야?' in message:
        return_text = find_stock(message)
        return return_text
    elif '로또 번호 뽑아줘' in message or '로또 번호 추천해줘' in message or '로또번호 뽑아줘' in message or '로또번호 추천해줘' in message:
        _lotto = random.sample(range(1, 46), 7)
        bonus_lotto = _lotto[-1]
        _lotto = sorted(_lotto[:-1])
        return_text = f"제가 추천드리는 로또 번호는 {' '.join(str(i) for i in _lotto)}에 보너스 번호는 {bonus_lotto} 입니다. 너무 맹신하지는 마세요!"
        return return_text
    else:
        return message


bad_words = ['시발', '씨발', 'ㅅㅂ', 'ㅆㅃ', 'ㅆㅂ', 'ㅅㅃ', '싯빨', '싯발', '시빨', 
                '시팔', '씨팔', '병신', '빙신', '뷩신', '븅신', 'ㅄ', 'ㅂㅅ', 'ㅈ같네', 
                '좆', '개같네', '창녀', '창년', '창놈', '애미', '애비', '느금마', 
                '느금빠', '느금', '빨통', '뻐큐', '뻑큐', 'Fuck', 'fuck', '저능아',
                '좆밥', 'ㅈ밥', '틀딱']

def find_bad_words(message):
    for bad in bad_words:
        if bad in message:
            return True