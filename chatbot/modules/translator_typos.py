def translator_typos(message):
    import hangul_utils
    
    # 자음-초성/종성
    cons = {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
               'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ'}
    # 모음-중성
    vowels = {'k':'ㅏ', 'i':'ㅑ', 'j':'ㅓ', 'u':'ㅕ', 'o':'ㅐ', 'O':'ㅒ', 'p':'ㅔ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
               'y':'ㅛ', 'n':'ㅜ', 'nj':'ㅝ', 'np':'ㅞ', 'nl':'ㅟ', 'b':'ㅠ',  'm':'ㅡ', 'ml':'ㅢ', 'l':'ㅣ'}
    # 자음-종성
    cons_double = {'rt':'ㄳ', 'sw':'ㄵ', 'sg':'ㄶ', 'fr':'ㄺ', 'fa':'ㄻ', 'fq':'ㄼ', 'ft':'ㄽ', 'fx':'ㄾ', 'fv':'ㄿ', 'fg':'ㅀ', 'qt':'ㅄ'}    
    
    result = ''   # 영 > 한 변환 결과
    
    # 1. 해당 글자가 자음인지 모음인지 확인
    vc = '' 
    for t in message:
        if t in cons:
            vc += 'c'
        elif t in vowels:
            vc += 'v'
        else:
            vc += '!'

    # cvv → fVV / cv → fv / cc → dd 
    vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')

    # 2. 자음 / 모음 / 두글자 자음 에서 검색
    i = 0
    while i < len(message):
        v = vc[i]
        t = message[i]
        j = 1

        if v == 'f' or v == 'c':   # 초성(f) & 자음(c) = 자음
            result += cons[t]

        elif v == 'V':   # 더블 모음
            if message[i: i+2] in vowels:
                result += vowels[message[i: i+2]]
            else:
                result += vowels[t]
                result += vowels[message[i+1]]
            j += 1

        elif v == 'v':   # 모음
            result += vowels[t]

        elif v == 'd':   # 더블 자음
            if message[i: i+2] in cons_double:
                result += cons_double[message[i: i+2]]
            else:
                result += cons[t]
                result += cons[message[i+1]]
            j += 1

        else:
            result += t
        
        i += j
        
    _result = hangul_utils.join_jamos(result)
    
    result_text = f'{_result} 라고 말씀하신게 맞을까요?'

    return result_text  