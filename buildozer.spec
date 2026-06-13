[app]

title = Jarvis AI
package.name = jarvisai
package.domain = org.jarvis

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy==2.3.0,speechrecognition,pyttsx3,psutil,ollama,requests

orientation = portrait

osx.python_version = 3

fullscreen = 0

# Android specific
android.permissions = INTERNET,RECORD_AUDIO,WAKE_LOCK
android.api = 34
android.minapi = 21
android.ndk_api = 24
android.archs = arm64-v8a,armeabi-v7a
p4a.branch = develop

# For signing
android.release = true
