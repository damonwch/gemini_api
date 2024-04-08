from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

@app.route('/gemini/chat', methods=['POST'])
def gemini_chat():
    data = request.get_json()
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

if __name__ == '__main__':
    app.run()
