def json_single_loader(file_path):
    import pandas as pd
    from tqdm import tqdm
    import json

    with open(file_path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    p_01 = []
    p_02 = []

    for i in range(len(data['data'])):
        p_01_list = []
        p_02_list = []
        
        for j in range(len(data['data'][i]['body']['dialogue'])):
            if data['data'][i]['body']['dialogue'][j]['participantID'] == 'P01':
                if len(p_01_list) == 0: 
                    p_01_list.append(data['data'][i]['body']['dialogue'][j]['utterance']) 
                    continue
                if data['data'][i]['body']['dialogue'][j-1]['participantID'] == 'P01':
                    p_01_list[-1] = p_01_list[-1] + ' ' + data['data'][i]['body']['dialogue'][j]['utterance']
                elif data['data'][i]['body']['dialogue'][j-1]['participantID'] != 'P01':
                    p_01_list.append(data['data'][i]['body']['dialogue'][j]['utterance'])

            elif data['data'][i]['body']['dialogue'][j]['participantID'] == 'P02':
                if len(p_02_list) == 0:
                    p_02_list.append(data['data'][i]['body']['dialogue'][j]['utterance']) 
                    continue                
                if data['data'][i]['body']['dialogue'][j-1]['participantID'] == 'P02':
                    p_02_list[-1] = p_02_list[-1] + ' ' + data['data'][i]['body']['dialogue'][j]['utterance']   
                elif data['data'][i]['body']['dialogue'][j-1]['participantID'] != 'P02':
                    p_02_list.append(data['data'][i]['body']['dialogue'][j]['utterance']) 
        if len(p_01_list) - len(p_02_list) == 1:
            p_01_list.pop()
        elif len(p_02_list) - len(p_01_list) == 1:
            p_02_list.pop()
        else:
            pass
        p_01.append(p_01_list)
        p_02.append(p_02_list)

    for i in reversed(range(len(p_01))):
        if len(p_01[i]) == len(p_02[i]):
            pass
        elif len(p_01[i]) != len(p_02[i]):
            del p_01[i]
            del p_02[i]

    t = tqdm(range(len(p_01)))
    t.set_postfix_str('Loading... [{}]'.format(file_path))

    for i in t:
        for j in range(len(p_01[i])):
            p_01_s = pd.DataFrame(pd.Series(p_01[i][j])).rename(columns = {0:'Q'})
            p_02_s = pd.DataFrame(pd.Series(p_02[i][j])).rename(columns = {0:'A'})
            p_03_s = pd.DataFrame(pd.Series(p_02[i][j])).rename(columns = {0:'Q'})
            p_04_s = pd.DataFrame(pd.Series(p_01[i][j])).rename(columns = {0:'A'})

            if i == 0 and j == 0: 
                first_frame = pd.concat([p_01_s, p_02_s], axis=1)
                second_frame = pd.concat([p_03_s, p_04_s], axis=1)
                total_frame = pd.concat([first_frame, second_frame], axis=0)
            else:
                third_frame = pd.concat([p_01_s, p_02_s], axis=1)
                forth_frame = pd.concat([p_03_s, p_04_s], axis=1)
                fifth_frame = pd.concat([third_frame, forth_frame], axis=0)
                total_frame = pd.concat([total_frame, fifth_frame], axis=0)

    total_frame.reset_index(drop=True, inplace=True)
                
    return total_frame


def json_multi_loader(file_path):
    import pandas as pd
    import json
    from tqdm import tqdm

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    p = []

    for i in range(len(data['data'])):
        p_list = []
        for j in range(len(data['data'][i]['body']['dialogue'])):
            if i == 0 and j == 0 or len(p_list) == 0:
                p_list.append(data['data'][i]['body']['dialogue'][j]['utterance'])        
                continue
            if data['data'][i]['body']['dialogue'][j-1]['participantID'] == data['data'][i]['body']['dialogue'][j]['participantID']:
                p_list[-1] = p_list[-1] + ' ' + data['data'][i]['body']['dialogue'][j]['utterance']
            else:
                p_list[-1] = p_list[-1] + '\n' + data['data'][i]['body']['dialogue'][j]['utterance']
        p.append(p_list)

    t = tqdm(p)
    t.set_postfix_str('Loading... [{}]'.format(file_path))

    for corpus in t:
        if corpus == p[0]:
            total_frame = pd.DataFrame(pd.Series(corpus)).rename(columns={0:'conversation'})
        else:
            sub_frame = pd.DataFrame(pd.Series(corpus)).rename(columns={0:'conversation'})
            total_frame = pd.concat([total_frame, sub_frame], axis=0)

    total_frame.reset_index(inplace=True, drop=True)

    return total_frame    


def save_csv(dataframe, save_path, save_file_name):  
    dataframe.to_csv(save_path+save_file_name)
