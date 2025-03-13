import os
import requests
import subprocess
import shutil
import speech_recognition as sr
import sys
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import whisper
import torch
import librosa
import soundfile as sf
import time
import json
import warnings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pathfile  # Import paths from pathfile.py

# ✅ Use Ollama instead of GPT-4All
OLLAMA_MODEL = "llama3"  # Change to "mistral" if needed

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def remove_main_flag():
    if os.path.exists(pathfile.JARVIS_UI_FLAG):
        os.remove(pathfile.JARVIS_UI_FLAG)

def record_live_audio(filename, duration=5, fs=16000):
    """
    Record live audio from the microphone for a given duration and save it as a WAV file.
    """
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, recording)
    print(f"Recording saved to {filename}")

def load_and_preprocess(audio_path, target_sr=16000):
    """
    Load and preprocess the audio file:
      - Load audio using librosa.
      - Resample to target_sr if needed.
      - Normalize the audio.
    Save the processed audio to a temporary file and return its path.
    """
    print("Loading and pre-processing audio...")
    audio, sr = librosa.load(audio_path, sr=None)

    # ✅ Fix: Use correct resampling method
    if sr != target_sr:
        audio = librosa.resample(y=audio, orig_sr=sr, target_sr=target_sr)

    # ✅ Normalize audio
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    preprocessed_path = os.path.join(pathfile.ASSISTANT_FOLDER, "preprocessed_command.wav")
    sf.write(preprocessed_path, audio, target_sr)

    return preprocessed_path

import whisper
import warnings
import os
import sys

def transcribe_with_whisper(audio_path):
    """
    Use Whisper's medium model on CPU to transcribe the audio file.
    Suppresses all logs, warnings, and prints.
    """
    device = "cpu"

    # ✅ Suppress ALL warnings (including FP16 warning)
    warnings.simplefilter("ignore")

    # ✅ Redirect stdout & stderr to suppress all Whisper outputs
    with open(os.devnull, 'w') as f, warnings.catch_warnings():
        sys.stdout = f
        sys.stderr = f
        warnings.simplefilter("ignore")

        model = whisper.load_model("medium", device=device)  # Load model silently

    # ✅ Restore stdout & stderr after loading model
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    # ✅ Process & transcribe audio
    processed_audio = load_and_preprocess(audio_path, target_sr=16000)
    result = model.transcribe(processed_audio)
    
    os.remove(processed_audio)
    return result["text"].lower().strip()

def start_jarvis_ui():
    """Set the state to 'listening'."""
    with open(pathfile.STATE_FILE, "w", encoding="utf-8") as f:
        f.write("listening")

def idle_jarvis_ui():
    """Set the state to 'idle'."""
    with open(pathfile.STATE_FILE, "w", encoding="utf-8") as f:
        f.write("idle")

def is_ollama_running():
    """ Check if Ollama service is running. """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_ollama():
    """ Start Ollama service if it's not running. """
    print("⚡ Jarvis is not running. Starting it now...")
    subprocess.run(["brew", "services", "start", "ollama"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for Ollama to fully start
    for _ in range(10):
        time.sleep(2)
        if is_ollama_running():
            print("✅ Jarvis is now running!")
            return
    print("❌ Failed to start Jarvis. Make sure it's installed and working.")

def print_typing_effect(text, delay=0.05):
    """ Prints text word by word with a delay to create a typing effect. """
    words = text.split()
    for word in words:
        sys.stdout.write(word + " ")
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after typing effect

def ask_ollama(prompt):
    """ Send request to Ollama and process the response correctly. """
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False  # Disable streaming for clean response
        })
        
        try:
            json_response = response.json()
            return json_response.get("response", "No response.").strip()
        except json.JSONDecodeError:
            print("❌ Ollama returned an invalid response. RAW OUTPUT:")
            print(response.text)
            return "No response."

    except requests.exceptions.RequestException:
        print("❌ Could not connect to Ollama API.")
        return "No response."


# ✅ Ensure Ollama is running
if not is_ollama_running():
    start_ollama()

def generate_tts(text, output_path):
    """Generate TTS using macOS 'say' command"""
    text = text.replace("'", "'\\''")  # Escape single quotes
    os.system(f"say -v 'Nathan (Enhanced)' '{text}' -o {output_path}")

def convert_aiff_to_wav(aiff_path, wav_path):
    """Convert .aiff to .wav format using ffmpeg"""
    os.system(f"ffmpeg -i {aiff_path} -acodec pcm_s16le -ac 1 -ar 44100 {wav_path} -loglevel quiet -y")
    os.remove(aiff_path)

def clear_audio_output_tts_folder(folder_path):
    """Clear the folder where TTS files are stored"""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

def call_tts_to_rvc(input_wav_path, output_enhanced_path):
    """Call separate tts_to_rvc.py to process TTS with RVC"""
    print("\n\nLoading Jarvis Speech...\n")
    subprocess.run(["python3", "tts_to_rvc.py", input_wav_path, output_enhanced_path])

def voice_input():
    """
    - Keeps mic ON permanently, always listening for "Jarvis."
    - When "Jarvis" is detected, it **waits for user speech** before recording.
    - If silent for 10s, it resets to wake word detection.
    """

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    recognizer.dynamic_energy_threshold = True  # Auto adjust for noise
    recognizer.pause_threshold = 0.9  # Detects speech quicker

    print("🔹 Always listening for 'Jarvis'... (Mic stays ON)")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Initial calibration

    first_time = True  # Ensures "Listening..." only prints **once**

    while True:
        with microphone as source:
            if first_time:
                print("🎤 Listening For Wake Word (Jarvis)...")
                first_time = False  # Ensures it prints only ONCE

            try:
                # ✅ **Mic STAYS ON, always listening for "Jarvis"**
                audio = recognizer.listen(source, timeout=None)
                wake_word_detected = recognizer.recognize_google(audio).lower().strip()

            except sr.UnknownValueError:
                continue  # Ignore noise, keep listening
            except sr.RequestError as e:
                print(f"[ERROR] Speech recognition request failed: {e}")
                continue

        # ✅ **Wake word detected, now WAIT for user speech**
        if "jarvis" in wake_word_detected:
            print("✅ Wake word 'Jarvis' detected! Waiting for command...")
            subprocess.run(["afplay", pathfile.LISTENING_SOUND])

            # 🎤 **Now actually wait for speech**
            first_time = True  # Reset print flag for next wake word
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                try:
                    print("🎤 Speak now... (Say, 'Quit Program' to stop Jarvis Assistant)")
                    audio = recognizer.listen(source, timeout=10)  # ✅ Waits for actual speech!

                    # ✅ Try recognizing speech to verify if the user actually spoke
                    try:
                        detected_speech = recognizer.recognize_google(audio).strip()
                    except sr.UnknownValueError:
                        print("❌ No speech detected. Returning to wake word listening.")
                        subprocess.run(["afplay", pathfile.NOT_LISTENING_SOUND])
                        continue  # Go back to listening for "Jarvis"

                except sr.WaitTimeoutError:
                    print("❌ User was silent. Returning to wake word listening.")
                    subprocess.run(["afplay", pathfile.NOT_LISTENING_SOUND])
                    clear_screen()
                    continue  # Go back to listening for "Jarvis"

            print("✅ User finished speaking. Transcribing...")

            # ✅ Save recorded command audio
            command_audio_file = pathfile.USER_VOICE_COMMAND
            with open(command_audio_file, "wb") as f:
                f.write(audio.get_wav_data())

            # 🎤 **Now transcribe**
            command_text = transcribe_with_whisper(command_audio_file)
            os.remove(command_audio_file)

            print(f"\n📢 Recognized Command: '{command_text}'")

            if not command_text:
                print("❌ No command detected. Returning to wake word listening.")
                subprocess.run(["afplay", pathfile.NOT_LISTENING_SOUND])
                continue  # Go back to listening for "Jarvis"

            if command_text.strip().lower().rstrip(".") == "quit program":
                idle_jarvis_ui()
                remove_main_flag()
                clear_screen()
                sys.exit(0)

            subprocess.run(["afplay", pathfile.NOT_LISTENING_SOUND])
            idle_jarvis_ui()
            return command_text

def main(input_method):
    """Main function to integrate everything"""
    start_jarvis_ui()
    subprocess.run(["afplay", pathfile.LISTENING_SOUND])
    clear_screen()

    if input_method == "voice":
        user_input = voice_input()
        if not user_input:
            return
    else:
        print("Type 'quit' anytime to exit the program.")
        user_input = input("\nYou: ")
        subprocess.run(["afplay", pathfile.NOT_LISTENING_SOUND])
        idle_jarvis_ui()

    if user_input.lower() == 'quit':
        remove_main_flag()
        clear_screen()
        return

    chatbot_response = ask_ollama(user_input)
    print("\nJarvis:", end=" ")
    print_typing_effect(chatbot_response)

    clear_audio_output_tts_folder(pathfile.AUDIO_OUTPUT_FOLDER)

    generate_tts(chatbot_response, pathfile.TTS_AIFF_OUTPUT)
    convert_aiff_to_wav(pathfile.TTS_AIFF_OUTPUT, pathfile.TTS_WAV_OUTPUT)

    call_tts_to_rvc(pathfile.TTS_WAV_OUTPUT, pathfile.TTS_ENHANCED_OUTPUT)

if __name__ == "__main__":
    input_method = sys.argv[1] if len(sys.argv) > 1 else "text"
    main(input_method)