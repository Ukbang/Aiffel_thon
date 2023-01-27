def find_time(korea=False):
    import datetime
    
    weekend = {'0':'일요일', '1':'월요일', '2':'화요일', '3':'수요일', '4':'목요일', '5':'금요일', '6':'토요일'}
    
    if korea:
        time_zone = datetime.timezone(datetime.timedelta(hours=0))
        now = datetime.datetime.now(time_zone)
        weekend_day = now.strftime('%w')
        today = weekend[weekend_day]
        _time = now.strftime(f'현재 시각은 %Y년 %m월 %d일 %H시 %M분 {today} 입니다.')
        print(f'{_time}')
        
        return _time
    
    else:
        time_zone = datetime.timezone(datetime.timedelta(hours=9))
        now = datetime.datetime.now(time_zone)
        weekend_day = now.strftime('%w')
        today = weekend[weekend_day]
        _time = now.strftime(f'현재 시각은 %Y년 %m월 %d일 %H시 %M분 {today} 입니다.')
        print(f'{_time}')    
        
        return _time