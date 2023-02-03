def message_check(message):
    try:
        import aiffel_finder
        import translator_typos
    except:
        import sys
        sys.path.append('~/aiffel/00_aiffel_thon/modules/')
        import aiffel_finder
        import translator_typos        
    
    re_message = message.replace(' ', '').lower()
    
    if re_message.encode().isalpha():
        if 'have' in message or 'you' in message or 'name' in message:
            return message
        else:
            return_text = translator_typos.translator_typos(message)
            return message
    elif '시간 알려줘' in message or '지금 몇시야' in message:
        return_text = aiffel_finder.find_time()
        return return_text
    elif '날씨 어때' in message or '날씨 알려줘' in message:
        return_text = aiffel_finder.find_weather(message)
        return return_text
    elif '주가 알려줘' in message or '주식 얼마야?' in message or '주가 얼마야?' in message:
        return_text = aiffel_finder.find_stock(message)
        return return_text
    else:
        return message
    