import openai
import json

# export api key under: OPENAI_API_KEY
# or alternatively use openai.api_key = ""

# list models
models = openai.Model.list()

preprompt = """
I am going to provide you with snippets to which I want you to add dutch translations for me. 
Here's a small example snippet from the file to show what you should do: 

Original:
    "share-approval-desc1": {
      "english": "A new login is trying to access your account.",
      "japanese": "新しいログインがあなたのアカウントにアクセスしようとしています。",
      "german": "Ein neuer Login versucht, auf Ihr Konto zuzugreifen.",
      "korean": "새 로그인으로 계정에 액세스하려고합니다.",
      "spanish": "Un nuevo inicio de sesión está intentando acceder a su cuenta.",
      "mandarin": "新的登录名正在尝试登记入您的帐户。",
      "portuguese": "Um novo login está tentando acessar sua conta."
    }


Should become:

    "share-approval-desc1": {
      "english": "A new login is trying to access your account.",
      "japanese": "新しいログインがあなたのアカウントにアクセスしようとしています。",
      "german": "Ein neuer Login versucht, auf Ihr Konto zuzugreifen.",
      "korean": "새 로그인으로 계정에 액세스하려고합니다.",
      "spanish": "Un nuevo inicio de sesión está intentando acceder a su cuenta.",
      "mandarin": "新的登录名正在尝试登记入您的帐户。",
      "portuguese": "Um novo login está tentando acessar sua conta.",
      "dutch": "Een nieuwe login probeert toegang te krijgen tot uw account."
    }

Now do this for:
"""

item = """
"2fa-verify-share-send": {
      "mandarin": "发送请求",
      "spanish": "Enviar petición",
      "english": "Send request",
      "japanese": "リクエストを送信",
      "korean": "요청 보내기",
      "german": "Anfrage senden",
      "portuguese": "Enviar pedido"
    },
"""

content = preprompt + item

print("\n")
print(content)
print("\n")

# create a chat completion
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}])

# print the chat completion
print(chat_completion.choices[0].message.content)
