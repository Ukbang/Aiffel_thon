import uvicorn
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from html_utils import build_html_chat
from model import ChatBot

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time

app = FastAPI()

# initialises the chatbot model and starts the uvicorn app
chatbot = ChatBot()

# mounts the static folder that contains the css file
app.mount("/static", StaticFiles(directory="static"), name="static")

# locates the template files that will be modified at run time
# with the dialog form the user and bot
templates = Jinja2Templates(directory="templates")

@app.post("/", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
async def root(request:Request, message: Optional[str] = Form(None)):
  # if the Form is not None, then get a reply from the bot
  if message is not None:
    print(message)
  
    # gets a response of the AI bot
    _ = chatbot.get_reply(message)

    # converts the chat history into an HTML dialog
    chat_html = '\n'.join([
      build_html_chat(is_me=i%2==0, text=msg['text'], time=msg['time'])
      for i, msg in enumerate(chatbot.chat_history)
    ])
  
  else: # 최초 연결 시 index.html 갱신을 위한 더미 신호이지만 아무것도 입력하지 않은 채팅을 보낼 시 채팅 로그가 사라져보이는 문제 발생
    chat_html = ''
    
  message_dict = {
    "request": request,
    "chat": chat_html
  }
  
  # returns the final HTML
  return templates.TemplateResponse("index.html", message_dict)


# initialises the chatbot model and starts the uvicorn app
if __name__ == "__main__":
    chatbot = ChatBot()
    uvicorn.run(app, host="0.0.0.0", port=8000)