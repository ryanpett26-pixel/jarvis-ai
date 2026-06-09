import speech_recognition as sr
import pyttsx3
import psutil
import pygame
import time
import threading
import requests
import ollama
from datetime import datetime
import random

# Initialize
engine = pyttsx3.init()
recognizer = sr.Recognizer()

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("JARVIS AI")

# Particle simulation for orb
class Particle:
    def __init__(self):
        self.reset()
    def reset(self):
        self.x = 400
        self.y = 300
        self.vx = (random.random() - 0.5) * 4
        self.vy = (random.random() - 0.5) * 4
        self.life = 100

particles = [Particle() for _ in range(200)]

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5)
    try:
        text = recognizer.recognize_google(audio).lower()
        print("You:", text)
        return text
    except:
        return ""

def get_system_diagnostics():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    return f"CPU: {cpu}%, Memory: {mem}%"

def run_diagnostics():
    speak("Running full system diagnostics.")
    diag = get_system_diagnostics()
    speak(diag)
    for i in range(10, 101, 20):
        print(f"Diagnostics: {i}%")
        time.sleep(0.5)
    speak("All systems nominal.")

def main_loop():
    speak("Jarvis online. How can I assist you today?")
    while True:
        command = listen()
        if "jarvis" in command or "you up" in command:
            if "diagnostics" in command:
                run_diagnostics()
            elif "time" in command:
                speak(datetime.now().strftime("%I:%M %p"))
            else:
                try:
                    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': command}])
                    speak(response['message']['content'])
                except:
                    speak("I'm here to help. What would you like?")
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=main_loop, daemon=True).start()
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        for p in particles:
            p.x += p.vx
            p.y += p.vy
            p.life -= 1
            if p.life <= 0:
                p.reset()
            pygame.draw.circle(screen, (0, 255, 255), (int(p.x), int(p.y)), 3)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()