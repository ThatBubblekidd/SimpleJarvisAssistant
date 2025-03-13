#Jarvis AI Assistant

A personal AI assistant with voice recognition, text input, speech synthesis, and Retrieval-based Voice Conversion (RVC) for enhanced speech quality.

FYI: This was all made by ChatGPT

📌 Features
• Always-Listening Wake Word Detection (Jarvis)
• Voice Command Processing using Whisper
• Ollama Integration for AI responses
• TTS Generation using macOS say with RVC enhancement
• PyQt5 UI for GIF-based interaction
• Modular Path Management (pathfile.py for easy directory customization)

For Path managment, make sure to update the pathfile.py, it's very easy to understand, I left comments! :)


💻 System Requirements

Jarvis AI Assistant has been tested and runs smoothly on the following system:

✅ Tested System:
• Device: MacBook Pro M3 (11-core)
• Memory: 18GB RAM
• OS: macOS

🖥️ Expected Compatibility:
• MacOS: ✅ Fully supported (Tested on macOS with M3 chip)
• Linux: ❓ Haven't Tested so I don't know
• Windows: ❓ Haven't Tested so I don't know

Note: If you’re using a different OS, additional setup or modifications may be required.



📂 RVC Setup Notes - IMPORTANT‼️

Make sure to have RVC Downloaded

FYI - Move the "Move_To_RVC_Folder" to Retrieval-based-Voice-Conversion folder then open the folder up and then move assests folder (Folder is in Assistant), RVC_requirements.txt, and force_cpu.py out of the folder and into Retrieval-based-Voice-Conversion





🔧 Setup Instructions

Install Pyenv (If Not Installed)

Ensure Pyenv is installed on your system:

```bash
brew install pyenv
```

⚙️ Required Environment

Before running/downloading dependencies for Jarvis AI Assistant and RVC, set up the correct environment.

1. Install python 3.10

Run the following commands in your terminal:

```bash
pyenv install 3.10.13
```
2. Run the environment in directory

```bash
pyenv global 3.10.13
```

3. Install Project Dependencies

```bash
pip install -r requirements.txt
```
4. Setting up The Chatbot

```bash
brew install ollama
ollama pull llama3
```
5. To run Assistant command

```bash
python3 main.py
```

✅ You’re all set!

After completing these steps, you should be ready to run Jarvis AI Assistant. 🚀
