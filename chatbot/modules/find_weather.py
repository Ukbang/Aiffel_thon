def find_weather(location, city=None):
    from urllib.request import urlopen, Request
    import urllib
    import bs4
    
    if city:
        enc_location = urllib.parse.quote(city + location + '+날씨')
    else:
        enc_location = urllib.parse.quote(location + '+날씨')
    
    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location
    
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
        

    print(f'{city_location}의 현재 온도는 {present_weather}도 입니다.')
    print(f'최고 기온은 {maximum_temp}도 최저 기온은 {minimum_temp}도 입니다.')