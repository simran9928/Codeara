from django.shortcuts import render,HttpResponse
from django.conf import settings
import json
import requests
import base64

API_ENDPOINT = "https://api.jdoodle.com/v1/execute"

client_id = "aa3c5e94ced8d771cb0a961ce09643e1"
client_secret = "30ed01aa75f848fe6388516339bea7944295cfa0bb8f5983f7302e556c87b9bb"

LANG_CODE = { 'c': 1, 'java': 3, 'cpp14': 3, 'python3': 3,'go': 3,
            'sql': 3,'csharp': 3,'dart': 3,'nodejs': 3,'kotlin': 2,'brainfuck': 0,}

def code_editor(request):
    return render(request,'code_editor.html')

def result(request):
    if request.method == "POST":
        source = request.POST.get("script")
        lang = request.POST.get("lang")
        stdin = request.POST.get("stdin")
        
        data = {'clientId':client_id,
                'clientSecret':client_secret,
                'script':source,
                'stdin':stdin,
                'language':lang,
                'versionIndex':LANG_CODE[lang],
            }
        #if stdin:
            #data.update({'stdin':stdin}) 
        try:
            headers = {'Content-type': 'application/json'}
            r = requests.post(url = API_ENDPOINT, data = json.dumps(data), headers = headers)
            json_data = r.json()
            print(json_data)
            status_code = r.status_code
            #output = Robject(r.json())
            output = json_data['output']
            if not output:
                output = message.replace("\n","<br>")
        except Exception as e:
            print(e)
            output = settings.ERROR_MESSAGE
        print(output)    
        return HttpResponse(json.dumps({'output': json_data['output']}), content_type="application/json")
    else:
        return render(request,'code_editor.html',locals())
'''
class Robject():
    def __init__(self, result):
        self.output = result['output']
        self.memory = result['memory']
        self.time = result['cpuTime']

'''