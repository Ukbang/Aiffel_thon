# def json_single_loader(file_path):
#     import pandas as pd
#     from tqdm import tqdm
#     import json

#     with open(file_path, 'r', encoding='utf-8') as fp:
#         data = json.load(fp)

#     p_01 = []
#     p_02 = []

#     for i in range(len(data['data'])):
#         p_01_list = []
#         p_02_list = []
        
#         for j in range(len(data['data'][i]['body']['dialogue'])):
#             if data['data'][i]['body']['dialogue'][j]['participantID'] == 'P01':
#                 if len(p_01_list) == 0: 
#                     p_01_list.append(data['data'][i]['body']['dialogue'][j]['utterance']) 
#                     continue
#                 if data['data'][i]['body']['dialogue'][j-1]['participantID'] == 'P01':
#                     p_01_list[-1] = p_01_list[-1] + ' ' + data['data'][i]['body']['dialogue'][j]['utterance']
#                 elif data['data'][i]['body']['dialogue'][j-1]['participantID'] != 'P01':
#                     p_01_list.append(data['data'][i]['body']['dialogue'][j]['utterance'])

#             elif data['data'][i]['body']['dialogue'][j]['participantID'] == 'P02':
#                 if len(p_02_list) == 0:
#                     p_02_list.append(data['data'][i]['body']['dialogue'][j]['utterance']) 
#                     continue                
#                 if data['data'][i]['body']['dialogue'][j-1]['participantID'] == 'P02':
#                     p_02_list[-1] = p_02_list[-1] + ' ' + data['data'][i]['body']['dialogue'][j]['utterance']   
#                 elif data['data'][i]['body']['dialogue'][j-1]['participantID'] != 'P02':
#                     p_02_list.append(data['data'][i]['body']['dialogue'][j]['utterance']) 
#         if len(p_01_list) - len(p_02_list) == 1:
#             p_01_list.pop()
#         elif len(p_02_list) - len(p_01_list) == 1:
#             p_02_list.pop()
#         else:
#             pass
#         p_01.append(p_01_list)
#         p_02.append(p_02_list)

#     for i in reversed(range(len(p_01))):
#         if len(p_01[i]) == len(p_02[i]):
#             pass
#         elif len(p_01[i]) != len(p_02[i]):
#             del p_01[i]
#             del p_02[i]

#     t = tqdm(range(len(p_01)))
#     t.set_postfix_str('Loading... [{}]'.format(file_path))

#     for i in t:
#         for j in range(len(p_01[i])):
#             p_01_s = pd.DataFrame(pd.Series(p_01[i][j])).rename(columns = {0:'Q'})
#             p_02_s = pd.DataFrame(pd.Series(p_02[i][j])).rename(columns = {0:'A'})
#             p_03_s = pd.DataFrame(pd.Series(p_02[i][j])).rename(columns = {0:'Q'})
#             p_04_s = pd.DataFrame(pd.Series(p_01[i][j])).rename(columns = {0:'A'})

#             if i == 0 and j == 0: 
#                 first_frame = pd.concat([p_01_s, p_02_s], axis=1)
#                 second_frame = pd.concat([p_03_s, p_04_s], axis=1)
#                 total_frame = pd.concat([first_frame, second_frame], axis=0)
#             else:
#                 third_frame = pd.concat([p_01_s, p_02_s], axis=1)
#                 forth_frame = pd.concat([p_03_s, p_04_s], axis=1)
#                 fifth_frame = pd.concat([third_frame, forth_frame], axis=0)
#                 total_frame = pd.concat([total_frame, fifth_frame], axis=0)

#     total_frame.reset_index(drop=True, inplace=True)
                
#     return total_frame


def json_loader(file_path, single=False):
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

    if single == True:
        q_list = []
        a_list = []
        for i in tqdm(range(len(total_frame))):
            sub_q_list = []
            sub_a_list = []
            corpus = total_frame['conversation'][i].split('\n')
            for j in range(len(corpus)):
                if j == len(corpus)-1:
                    continue
                elif j == 0:
                    sub_q_list.append(corpus[j])
                    sub_a_list.append(corpus[j+1])
                elif j == 1:
                    continue
                else:
                    sub_q_list.append(corpus[j-1])
                    sub_a_list.append(corpus[j])
            q_list.append(sub_q_list)
            a_list.append(sub_a_list)

        for i in tqdm(range(len(q_list))):
            if i == 0:
                first_frame = pd.DataFrame(pd.Series(q_list[i])).rename(columns={0:'Q'})
                second_frame = pd.DataFrame(pd.Series(a_list[i])).rename(columns={0:'A'})
                total_frame = pd.concat([first_frame, second_frame], axis=1)
            else:
                first_frame = pd.DataFrame(pd.Series(q_list[i])).rename(columns={0:'Q'})
                second_frame = pd.DataFrame(pd.Series(a_list[i])).rename(columns={0:'A'})
                third_frame = pd.concat([first_frame, second_frame], axis=1)
                total_frame = pd.concat([total_frame, third_frame], axis=0)
    
    total_frame.reset_index(inplace=True, drop=True)

    return total_frame    


def social_json_multi_loader(file_path, list_name):
    import os
    import json
    from tqdm import tqdm
    import pandas as pd

    total_list = []

    t = tqdm(range(len(list_name)))

    for i in t:
        t.set_postfix_str('Loading... [{}]'.format(list_name[i][:-1]))
        _dir = os.listdir(file_path+list_name[i])
        for j in range(len(_dir)):
            with open(file_path+list_name[i]+_dir[j], 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except:
                    print(file_path+list_name[i]+_dir[j])
                _list = []
                for k in range(len(data['info'][0]['annotations']['lines'])):
                    if k == 0:
                        _list.append(data['info'][0]['annotations']['lines'][k]['norm_text'])
                    elif k != 0:
                        if data['info'][0]['annotations']['lines'][k-1]['speaker']['id'] == data['info'][0]['annotations']['lines'][k]['speaker']['id']:
                            _list[-1] = _list[-1] + ' ' + data['info'][0]['annotations']['lines'][k]['norm_text']
                        else:
                            _list[-1] = _list[-1] + '\n' + data['info'][0]['annotations']['lines'][k]['norm_text']
                total_list.append(_list)

    t = tqdm(range(len(total_list)))
    t.set_postfix_str('transforming to csv file...')

    for i in t:
        if i == 0:
            total_df = pd.DataFrame(pd.Series(total_list[i])).rename(columns={0:'conversation'})
        elif i != 0:
            first_df = pd.DataFrame(pd.Series(total_list[i])).rename(columns={0:'conversation'})
            total_df = pd.concat([total_df, first_df], axis=0)

    total_df.reset_index(inplace=True, drop=True)

    return total_df

def save_csv(dataframe, save_path, save_file_name):  
    dataframe.to_csv(save_path+save_file_name)
