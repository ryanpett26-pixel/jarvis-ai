import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
import speech_recognition as sr
import pyttsx3
import psutil
import threading
import time
import random
from datetime import datetime
import ollama

Window.size = (400, 600)
Window.clearcolor = (0, 0, 0, 1)

class JarvisOrb(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        Clock.schedule_interval(self.update, 1/30.)

    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            for p in self.particles[:]:
                p['life'] -= 1
                p['x'] += p['vx']
                p['y'] += p['vy']
                if p['life'] <= 0:
                    self.particles.remove(p)
                    continue
                Color(0, 1, random.random(), 0.8)
                Ellipse(pos=(p['x']-5, p['y']-5), size=(10,10))
        if len(self.particles) < 50:
            self.particles.append({
                'x': 200, 'y': 300,
                'vx': random.uniform(-3,3),
                'vy': random.uniform(-3,3),
                'life': random.randint(30,60)
            })

class JarvisApp(App):
    def build(self):
        self.root = JarvisOrb()
        threading.Thread(target=self.voice_thread, daemon=True).start()
        return self.root

    def speak(self, text):
        print("JARVIS:", text)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=5)
            try:
                return r.recognize_google(audio).lower()
            except:
                return None

    def process_command(self, cmd):
        if "time" in cmd:
            self.speak(datetime.now().strftime("%I:%M %p"))
        elif "diagnostics" in cmd or "status" in cmd:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            self.speak(f"CPU {cpu}%, Memory {mem}%")
        elif "joke" in cmd:
            self.speak("Why did the AI cross the road? To optimize the other side!")
        else:
            try:
                resp = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': cmd}])
                self.speak(resp['message']['content'])
            except:
                self.speak("I'm here, sir.")

    def voice_thread(self):
        self.speak("Jarvis online. Say Jarvis to activate.")
        while True:
            cmd = self.listen()
            if cmd and "jarvis" in cmd:
                self.speak("At your service.")
                follow = self.listen()
                if follow:
                    self.process_command(follow)
            time.sleep(1)

if __name__ == '__main__':
    JarvisApp().run()