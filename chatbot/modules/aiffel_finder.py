def find_stock(stock):    
    from urllib.request import urlopen, Request
    import urllib
    import bs4

    ran_dict = {0: '올라갈 거', 1: '떨어질 거', 2: '유지될 거'}

    stock_url = urllib.parse.quote(stock)

    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='+ stock_url

    try:
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html,'html5lib')

        stock_name = str(soup.find('span', 'stk_nm'))
        stock_name = stock_name[stock_name.find('>')+1:stock_name.find('</span>')]

        spt_con = str(soup.find('span', class_='spt_con')).replace('</em>', '')
        present_price = spt_con[spt_con.find('<strong>')+8:spt_con.rfind('</strong>')]
        present_percent = spt_con[spt_con.rfind('<em>')+6:spt_con.rfind('</span>')-11]
        up_price = spt_con[spt_con.find('<em>')+4:spt_con.rfind('<em>')-1]

        if '상승' in spt_con:
            state = '상승'
        elif '하락' in spt_con:
            state = '하락'
        elif '보합' in spt_con:
            state = '보합'
        else:
            error
        
        try:
            trendy_num = sum([int(i) for i in present_price.split(',')])
        except:
            trendy_num = sum([int(i) for i in present_price])

        trendy_num = trendy_num % 3

        trend = ran_dict[trendy_num]

        if state == '보합':
            result_text = f'현재 {stock_name}의 가격은 {present_price}원 입니다. 전일대비 {state} 중 입니다. 제 생각에는 앞으로 {trend} 같아요. 하지만 저를 너무 믿지 마세요!'
        else:
            result_text = f'현재 {stock_name}의 가격은 {present_price}원 입니다. 전일대비 {up_price}원, {present_percent}% {state} 중 입니다. 제 생각에는 앞으로 {trend} 같아요. 하지만 저를 너무 믿지 마세요!'

        return result_text

    except:
        result_text = f'{stock_name}의 주가를 알고싶으신게 맞으실까요? 검색이 안되네요.'
        return result_text
        
def find_time(korea=False):
    import datetime
    
    weekend = {'0':'일요일', '1':'월요일', '2':'화요일', '3':'수요일', '4':'목요일', '5':'금요일', '6':'토요일'}
    
    if korea:
        time_zone = datetime.timezone(datetime.timedelta(hours=0))
        now = datetime.datetime.now(time_zone)
        weekend_day = now.strftime('%w')
        today = weekend[weekend_day]
        _time = now.strftime(f'현재 시각은 %Y년 %m월 %d일 %H시 %M분 {today} 입니다.')
        
        return _time
    
    else:
        time_zone = datetime.timezone(datetime.timedelta(hours=9))
        now = datetime.datetime.now(time_zone)
        weekend_day = now.strftime('%w')
        today = weekend[weekend_day]
        _time = now.strftime(f'현재 시각은 %Y년 %m월 %d일 %H시 %M분 {today} 입니다.')
        
        return _time
        
def find_weather(location, city=None):
    from urllib.request import urlopen, Request
    import urllib
    import bs4
    
    if city:
        enc_location = urllib.parse.quote(city + location + '+날씨')
    else:
        enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location
    
    try:
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html,'html5lib')

        city_location = str(soup.find('h2', class_='title'))
        city_location = city_location[city_location.find('"title">'):city_location.rfind('</h2>')][8:]

        temp_text = str(soup.find('div', class_='temperature_text'))
        minimum_temp = str(soup.find('span', class_='temperature_inner').find('span', class_='lowest'))
        maximum_temp = str(soup.find('span', class_='temperature_inner').find('span', class_='highest'))

        present_weather = temp_text[temp_text.find('</span>'):temp_text.find('<span class="celsius">')][7:]
        minimum_temp = minimum_temp[minimum_temp.find('</span>'):minimum_temp.rfind('°</span>')][7:]
        maximum_temp = maximum_temp[maximum_temp.find('</span>'):maximum_temp.rfind('°</span>')][7:]


        if present_weather[:1] == '-': 
            present_weather = present_weather.replace('-', '영하 ') 
        else: 
            pass

        if minimum_temp[:1] == '-': 
            minimum_temp = minimum_temp.replace('-', '영하 ') 
        else: 
            pass

        if maximum_temp[:1] == '-': 
            maximum_temp = maximum_temp.replace('-', '영하 ') 
        else: 
            pass    
        
        result_text = f'{city_location}의 현재 온도는 {present_weather}도 입니다. 최고 기온은 {maximum_temp}도 최저 기온은 {minimum_temp}도 입니다.'
        
        return result_text
        
    except:
        result_text = f'{city} {location}의 날씨를 알고싶으신게 맞을까요? 그런곳은 없어요. 어떤 시의 무슨 동 날씨가 궁금하실까요?'
        return result_text
     