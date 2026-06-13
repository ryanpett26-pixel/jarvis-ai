[app]

title = Jarvis AI
package.name = jarvisai
package.domain = org.ryanpett26
source.dir = .
version = 0.1.0

requirements = python3,kivy==2.3.0,plyer,speechrecognition,pyttsx3,psutil,ollama,requests

android.permissions = INTERNET,RECORD_AUDIO,WAKE_LOCK,FOREGROUND_SERVICE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 34
android.minapi = 21
android.ndk_api = 24
android.archs = arm64-v8a,armeabi-v7a

p4a.branch = develop

# Signing
android.release = true

# Other optimizations
orientation = portrait
fullscreen = 0
