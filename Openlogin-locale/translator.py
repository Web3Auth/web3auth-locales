import os
import openai
import json
import pandas as pd

# export api key under: OPENAI_API_KEY
# or alternatively use openai.api_key = ""

# list models
# models = openai.Model.list()

preprompt = """
I am going to provide you with json snippets to which I want you to add dutch translations for me. 
Be consistent with the ordering, keep it as it is provided.
Do not add in [ or ], and be sure to escape " with \"
Make sure it complies with RFC 8259
Here's a small example snippet from the file thats show what you should do: 

Original:
link-all, {
    {
      "mandarin": "授权应用",
      "japanese": "認定アプリ",
      "spanish": "Aplicaciones autorizadas",
      "english": "Authorized Apps",
      "german": "Autorisierte Apps",
      "korean": "승인 된 앱",
      "portuguese": "Aplicativos autorizados"
    }
}


Should become:
{
"link-all": {
      "mandarin": "授权应用",
      "japanese": "認定アプリ",
      "spanish": "Aplicaciones autorizadas",
      "english": "Authorized Apps",
      "german": "Autorisierte Apps",
      "korean": "승인 된 앱",
      "portuguese": "Aplicativos autorizados",
      "dutch": "Geautoriseerde apps"
    }
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


def openJson(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data


def saveJson(path, items):
    with open(path, 'w') as outfile:
        json.dump(items, outfile, ensure_ascii=False)


def writeBatch(items, outputFilename):
    with open(outputFilename, "w") as f:
        for item in items.items():
            # item = sanitizeItem(item)
            job = {"model": "gpt-3.5-turbo", "temperature": 0,
                   "messages": [{"role": "user", "content": preprompt+json.dumps(item, ensure_ascii=False)}]}
            json_string = json.dumps(job, ensure_ascii=False)
            f.write(json_string + "\n")


def sequentialProcess(collection):
    collection["nav"] = transformCollection(collection["nav"])
    saveJson('./Openlogin-locale/locales-nav.new.json', collection)

# Batch processes the collection, does not parse results


def batchProcess(collection):
    writeBatch(collection, './Openlogin-locale/batch.jsonl')
    # clear file as it is otherwise appended to
    open('./Openlogin-locale/results.jsonl', 'w').close()
    os.system("python3 ./OpenLogin-locale/api_request_parallel_processor.py --requests_filepath=./Openlogin-locale/batch.jsonl --save_filepath=./Openlogin-locale/results.jsonl --request_url=https://api.openai.com/v1/chat/completions")


def add_results_to_collection(collection, resultsPath):

    with open(resultsPath, 'r') as json_file:
        json_list = list(json_file)

        for json_str in json_list:
            result = json.loads(json_str)
            result = result[1]['choices'][0]['message']['content']
            loaded = json.loads(result)
            print(type(loaded))
            if (isinstance(loaded, dict)):
                for key, value in loaded.items():
                    collection['nav'][key] = value
            else:
                collection['nav'][loaded[0]] = loaded[1]
        return collection

    # results = pd.read_json(
    #     path_or_buf=resultsPath, typ='series', lines=True).to_dict()
    # for item in results.items():
    #     result = item[1][1]['choices'][0]['message']['content']
    #     loaded = json.loads(result)
    #     for key, value in loaded.items():
    #         collection['nav'][key] = value
    # return collection


workingDir = './Openlogin-locale/'

collection = openJson('./Openlogin-locale/locales-nav.json')
batchProcess(collection['nav'])
print("Done sending requests.")
print("Now processing results...")

collection = add_results_to_collection(
    collection, "./Openlogin-locale/results.jsonl")
saveJson('./Openlogin-locale/locales-nav.new.json', collection)
