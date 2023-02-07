import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from message_check import message_check
from html_utils import build_html_chat
import re

class ChatBot:
    def __init__(self, model_name='skt/kogpt2-base-v2', model_path='model2.pth'):
        self.bos_token = '<s>'
        self.eos_token = '</s>'
        self.usr_token = '<usr>'
        self.pad_token = '<pad>'
        self.sys_token = '<sys>'
        self.unk_token = '<unk>'
        self.mask_token = '<mask>'
        self.max_length = 256
        self.max_turns = 3
        self.device = torch.device("cpu")
        self.model_name = "skt/kogpt2-base-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name,
                bos_token=self.bos_token, eos_token=self.eos_token, unk_token=self.unk_token,
                pad_token=self.pad_token, mask_token=self.mask_token, model_max_length=self.max_length)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.usr_token_id = self.tokenizer.convert_tokens_to_ids(self.usr_token)
        self.sys_token_id = self.tokenizer.convert_tokens_to_ids(self.sys_token)
        self.history_limit = [self.bos_token]
        self.chat_history = []
        self.bad_words_ids = [self.tokenizer.encode(token) for token in [
                            self.unk_token, 'ㅋ', 'ㅠ', 'ㅠㅠ', 'ㅜㅜ', 'ㅜ', 'ㅎ', 'ㅠㅜ', 'ㅜㅠ', 'ㅋㅎ', 'ㅎㅋ', '.', '하하', '엄마', '아빠', '오빠', '언니', '누나']]

    def get_reply(self, user_message):
        # save message from the user
        if user_message == '초기화':
            self.chat_history = []
            self.history_limit = [self.bos_token]
            return

        if len(self.history_limit) == self.max_turns * 2 + 1:
            self.history_limit = self.history_limit[: 1] + self.history_limit[3: ]

        self.chat_history.append({
            'text':user_message, 
            'time':str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).time().replace(microsecond=0))
        })

        result = message_check(user_message)

        if result == '그건 나쁜말이야 그런말은 쓰면 안돼!':
            self.chat_history.append({
                'text':result, 
                'time':str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).time().replace(microsecond=0))
            })
            return 

        user_message_pull = self.usr_token + user_message + self.sys_token
        self.history_limit.append(user_message_pull)
    
        # encode the new user message to be used by our model
        message_ids = self.tokenizer.encode(''.join(self.history_limit), return_tensors='pt').to(self.device)

        if result == user_message:
            with torch.no_grad():
                reply_ids = self.model.generate(
                            message_ids,
                            early_stopping= True,
                            num_beams=3,
                            temperature=0.8,
                            top_p=0.92,
                            repetition_penalty=1.25,
                            no_repeat_ngram_size=3,
                            max_new_tokens=25,
                            bad_words_ids = self.bad_words_ids,
                            pad_token_id=self.tokenizer.pad_token_id,
                            bos_token_id = self.tokenizer.bos_token_id,
                            eos_token_id = self.usr_token_id
                        )   

            system_ids = reply_ids[0, message_ids.shape[-1]: -1].tolist()
            
            if self.sys_token_id in system_ids:
                system_ids = system_ids[: system_ids.index(self.sys_token_id)]
                
            decoded_ids = system_ids

            decoded_message = self.tokenizer.decode(decoded_ids)
        else:
            decoded_message = result

        decoded_message = self.special_str(decoded_message)

        self.history_limit.append(decoded_message)

        # save reply from the bot
        self.chat_history.append({
            'text':decoded_message, 
            'time':str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).time().replace(microsecond=0))
        })

        return decoded_message

    def special_str(self, message):
        message = re.sub(r"[.]+", r". ", message)
        message = re.sub(r"[?]+", r"? ", message)
        message = re.sub(r"[!]+", r"! ", message)
        
        return message