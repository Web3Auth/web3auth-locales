import os
import openai
import json
import pandas as pd

# export api key under: OPENAI_API_KEY
# or alternatively use openai.api_key = ""

# list models
# models = openai.Model.list()

jsonKey = 'home'
fileKey = 'wallet-home'
workingDir = './Openlogin-locale/'
fileToTranslate = f'locales-{fileKey}.json'
outputFile = f'locales-{fileKey}.new.json'
max_tokens_per_minute = 90000


preprompt = """
I am going to provide you with json snippets to which I want you to add dutch translations for me. 
Be consistent with the ordering, keep it as it is provided.
Do not add in [ or ], and be sure to escape " with \"
Make sure it complies with RFC 8259
Return no more than 1 collection
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

    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    # print the chat completion
    retValue = chat_completion.choices[0].message.content
    # print("Response received: " + retValue)
    return retValue


def transformCollection(items):
    for key, value in items.items():
        result = run_model(preprompt+json.dumps(value))
        items[key] = json.loads(result)
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
    saveJson(workingDir+outputFile, collection)


# Batch processes the collection, does not parse results
def batchProcess(collection):
    writeBatch(collection, './batch.jsonl')
    # clear file as it is otherwise appended to
    open('results.jsonl', 'w').close()
    os.system(
        f"python3 ./api_request_parallel_processor.py --requests_filepath=./batch.jsonl --save_filepath=./results.jsonl --request_url=https://api.openai.com/v1/chat/completions --max_tokens_per_minute={max_tokens_per_minute}")


def add_results_to_collection(collection, resultsPath):
    with open(resultsPath, 'r') as json_file:
        json_list = list(json_file)

        for json_str in json_list:
            result = ""
            try:
                result = json.loads(json_str)
                result = result[1]['choices'][0]['message']['content']
                loaded = json.loads(result)
                # print(type(loaded))
                if (isinstance(loaded, dict)):
                    for key, value in loaded.items():
                        collection[jsonKey][key] = value
                else:
                    collection[jsonKey][loaded[0]] = loaded[1]
            except:
                print("Errored")
                print("Error parsing result: " + result)
                pass
        return collection


collection = openJson(workingDir + fileToTranslate)
batchProcess(collection[jsonKey])
print("Done sending requests.")
print("Now processing results...")

collection = add_results_to_collection(
    collection,  "results.jsonl")
saveJson(workingDir + outputFile, collection)
