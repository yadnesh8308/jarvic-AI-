import win32com.client
import speech_recognition as sr
import webbrowser
import os
import datetime
import requests
import subprocess , sys

speaker = win32com.client.Dispatch("SAPI.SpVoice")
def ask_ollama(prompt):
    try:
        url = "http://localhost:11434/api/generate"
        data = {
             "model": "qwen2.5:3b",
             #"prompt": f"You are Jarvis, a helpful AI assistant. Keep replies short.\nUser: {prompt}",
              "prompt": f"{prompt}",
             "stream": False
        }
        response = requests.post(url, json=data)
        return response.json()["response"]
    except Exception as e:
        return "AI service is not available"

def takecomman():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 2
        audio = r.listen(source)
        try:
            print("recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said :{query}")
            return query
        except Exception as e:
            print("some voice error is occured...")
            return ""

while 1:
    print("Listening...")
    text = takecomman()
   #todo : add the thing here which you want to perform
    mains=[["chat","web","https://chatgpt.com/"],["youtube","web", "https://youtube.com"],
           ["google","web", "https://google.com"],["linkedIn","web", "https://www.linkedin.com/jobs/"],
           ["insta","web", "https://www.instagram.com/"],
           ["portal","web", "https://portal.vmedulife.com/public/auth/#/login/kit-kolhapur"],
           ["facebook","web", "https://www.facebook.com/"],["github","web", "https://github.com/"],
           ["wikipedia","web", "https://www.wikipedia.org/"],["setting","syst", "start ms-settings:"],
            ["wifi settings","syst", "start ms-settings:network-wifi"],
           ["open bluetooth settings","syst", "start ms-settings:bluetooth"],["code1","syst", "code"],
           ["file", "syst", "explorer"],["whatsapp", "syst", "start whatsapp:"],
           ["microsoft store", "syst", "start ms-windows-store:"],
           ["music", "path", r"C:\Users\Dell\CrossDevice\Redmi A3x\storage\Music"],
           ["project","syst","start pycharm"],
           ["sleep", "syst", "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"],
           ["lock", "syst", "rundll32.exe user32.dll,LockWorkStation"],
           ["restart", "syst", "shutdown /r /t 0"],["shutdown", "syst", "shutdown /s /t 0"],
           ["powershell", "syst", "powershell"],["camera", "syst", "start microsoft.windows.camera:"]]

    # todo : it check which type of file and how to open it
    found = False
    for main in mains:
        if f"{main[0]}".lower() in text.lower():
            found = True
            speaker.Speak(f"opening {main[0]} sir...")
            if main[1] == "web":
                webbrowser.open(f"{main[2]}")
            elif main[1] == "syst":
                os.system(f"{main[2]}")
            elif main[1] == "path":
                os.startfile(f"{main[2]}")

    if "time".lower() in text.lower():
        found = True
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(now)
        speaker.Speak(now)

    if text== "exit":
        speaker.Speak(f" exit sir...")
        break

    if not found and text.strip() != "":
        print("Jarvis AI thinking...")
        reply = ask_ollama(text)
        print("Jarvis:", reply)
        speaker.Speak(reply)

    if not text:
        continue