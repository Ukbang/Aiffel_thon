def find_stock(stock):    
    from urllib.request import urlopen, Request
    import urllib
    import bs4

    ran_dict = {0: '올라갈 거', 1: '떨어질 거', 2: '유지될 거'}

    stock_name = urllib.parse.quote(stock)

    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='+ stock_name

    try:
        req = Request(url)
        page = urlopen(req)
        html = page.read()
        soup = bs4.BeautifulSoup(html,'html5lib')

        spt_con_up = str(soup.find('span', class_='spt_con')).replace('</em>', '')
        present_price = spt_con_up[spt_con_up.find('<strong>')+8:spt_con_up.rfind('</strong>')]
        present_percent = spt_con_up[spt_con_up.rfind('<em>')+6:spt_con_up.rfind('</span>')-11]
        up_price = spt_con_up[spt_con_up.find('<em>')+4:spt_con_up.rfind('<em>')]

        if '상승' in spt_con_up:
            state = '상승'
        elif '하락' in spt_con_up:
            state = '하락'
        elif '보합' in spt_con_up:
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
            result_text = f'현재 {stock}의 가격은 {present_price}원 입니다. 전일대비 {state} 중 입니다. 제 생각에는 앞으로 {trend} 같아요. 하지만 저를 너무 믿지 마세요!'
        else:
            result_text = f'현재 {stock}의 가격은 {present_price}원 입니다. 전일대비 {up_price}원, {present_percent}% {state} 중 입니다. 제 생각에는 앞으로 {trend} 같아요. 하지만 저를 너무 믿지 마세요!'

        return result_text

    except:
        print(f'{stock}의 주가를 알고싶으신게 맞으실까요? 검색이 안되네요.')