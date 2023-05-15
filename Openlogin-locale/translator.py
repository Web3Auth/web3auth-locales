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
    {
      "english": "A new login is trying to access your account.",
      "japanese": "新しいログインがあなたのアカウントにアクセスしようとしています。",
      "german": "Ein neuer Login versucht, auf Ihr Konto zuzugreifen.",
      "korean": "새 로그인으로 계정에 액세스하려고합니다.",
      "spanish": "Un nuevo inicio de sesión está intentando acceder a su cuenta.",
      "mandarin": "新的登录名正在尝试登记入您的帐户。",
      "portuguese": "Um novo login está tentando acessar sua conta."
    }


Should become:

    {  
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


def run_model(prompt):
    print("Request sent for prompt: " + prompt)
    print("\n")

    # create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    # print the chat completion
    retValue = chat_completion.choices[0].message.content
    print(retValue)
    return retValue


def transformCollection(items):
    for key, value in items.items():
        result = run_model(preprompt+json.dumps(value))
        items[key] = json.loads(result)
        # values = item.items()
        # print(values)
    print("-------------\n")
    return items


def openCollection(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data


def saveCollection(path, items):
    with open(path, 'w') as outfile:
        json.dump(items, outfile, ensure_ascii=False)


collection = openCollection('./Openlogin-locale/locales-nav.json')
collection["nav"] = transformCollection(collection["nav"])
saveCollection('./Openlogin-locale/locales-nav.new.json', collection)
