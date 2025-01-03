import os, openai
from typing import Optional
import gradio as gr


# 프롬프트 읽어오기
with open("prompts/v2.2.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

openai.api_key = os.environ.get('OPENAI_API_KEY')

class Chat:

    def __init__(self, system: Optional[str] = None):
        self.system = system
        self.messages = []
        
        if system is not None:
            self.messages.append({
                "role": "system",
                "content": system
            })

    def prompt(self, content: str) -> str:
          self.messages.append({
              "role": "user",
              "content": content
          })
          try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
          except Exception as e:
            print("OpenAI Error:", e)
            raise e  # 재확인 위해 다시 던지거나, 로그 남기기

          response_content = response["choices"][0]["message"]["content"]
          self.messages.append({
              "role": "assistant",
              "content": response_content
          })
          return response_content
      
chat = Chat(system=system_prompt) # Define the system prompt

def respond(message, chat_history):
    bot_message = chat.prompt(content=message)
    chat_history.append((message, bot_message))
    return "", chat_history # chat 기록을 저장 가능, 추후 활용 가능


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

# 환경변수 PORT가 있으면 그 포트로, 없으면 8080번 포트로 서버 실행
port = int(os.environ.get("PORT", 7860))
demo.launch(server_name="0.0.0.0", server_port=port, debug=True)