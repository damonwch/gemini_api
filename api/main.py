# -*- coding: utf-8 -*-
# @Author   : Eurkon
# @Date     : 2022/3/8 14:17

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from scrapy.utils.project import get_project_settings
from sse_starlette.sse import EventSourceResponse
import google.generativeai as genai
import json
import time

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

settings = get_project_settings()


@app.post("/gemini/chat", tags=["API"], summary="GEMINI")
def gemini_chat(data: dict):
    prompt = data.get('prompt')
    api_key= data.get('api_key')
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        text=response.text
        response = {"content": text}
        return response
    
    except Exception as e:
        print(e)
        return None

@app.post("/gemini/chat_list", tags=["API"], summary="GEMINI")
def gemini_chat_list(data_list: list):
    #print('chat data:',data)
    return_list=[]
    for data in data_list:
        response=gemini_chat(data)
        return_list.append(response)
    return return_list 
       


@app.post('/gemini/chat_stream', tags=["API"], summary="GEMINI")
async def chat_stream(request: Request):
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    #print('chat_stream json_post_raw:',json_post)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')

    results=call_chat_stream(prompt)


    return EventSourceResponse(results)

async def call_chat_stream(prompt):
    genai.configure(api_key="AIzaSyDO6L-EuN0Nkd2XlhEMTp9O3ERUSQ2vWNg")
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        text=chunk.text
        response = {"content": text}
        #print('response:',response)
        yield json.dumps(response)
        

async def request(session, url):
    async with session.get(url) as response:
        return await response.text()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1",workers=5)
