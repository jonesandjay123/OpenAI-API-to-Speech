import openai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import speech_recognition as sr
import pyttsx3
import time

# Read API key from file
with open("api_key.txt", "r") as f:
    openai.api_key = f.read().strip()

# Print the API key to verify it's being read correctly
print(f"API Key: {openai.api_key}")

# Initialize the text to speech engine
engine = pyttsx3.init()

def record_audio(duration, fs=16000):
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return myrecording

def save_wav(filename, audio, fs=16000):
    scipy.io.wavfile.write(filename, fs, audio)

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language='zh-CN')
    except:
        print("No question detected.")

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["message"]["content"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    # Speak "Say your question" and start listening immediately after
    speak_text("請說出您的問題")
    
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Adjust these values as needed

    # Save audio to a file
    filename = "input.wav"
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())

    # Transcribe audio to text
    text = transcribe_audio_to_text(filename)
    if text:
        print(f"您說了: {text}")

        # Generate the response
        response = generate_response(text)
        print(f"ChatGPT 回應: {response}")

        # Read response using TTS
        speak_text(response)

try:
    main()
except Exception as e:
    print("An error occurred: {}".format(e))
if __name__ == "__main__":
    main()