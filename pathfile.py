import os

# Base Assistant Folder
YOURPATH = "/Users/micahmcduffie/Downloads"  # Change this if needed

ASSISTANT_FOLDER = os.path.join(YOURPATH, "Assistant")
JARVISMAIN_FOLDER = os.path.join(ASSISTANT_FOLDER, "JarvisMain")
AUDIO_FILES_AND_STORAGE_FOLDER = os.path.join(ASSISTANT_FOLDER, "Audio_Files_and_storage")

# RVC Path Access

# Change RVC_MODEL_NAME to your models name
RVC_MODEL_NAME = "Jarvis"

# Change to your RVC directory
YOURPATH_RVC = "/Users/micahmcduffie"

RVC_FOLDER = os.path.join(YOURPATH_RVC, "Retrieval-based-Voice-Conversion")
RVC_HUBERT_PATH = os.path.join(RVC_FOLDER, "assets", "hubert", "hubert_base.pt")
RVC_MODEL_PATH = os.path.join(RVC_FOLDER, "assets", "pretrained", RVC_MODEL_NAME, f"{RVC_MODEL_NAME}.pth")
RVC_CLI_SCRIPT = os.path.join(RVC_FOLDER, "force_cpu.py")









# Core files
STATE_FILE = os.path.join(JARVISMAIN_FOLDER, "state.txt")
JARVIS_UI_FLAG = os.path.join(JARVISMAIN_FOLDER, "main_running.txt")
SETTINGS_FILE = os.path.join(ASSISTANT_FOLDER, "settings.txt")

# Audio files
LISTENING_SOUND = os.path.join(AUDIO_FILES_AND_STORAGE_FOLDER, "SoundEffects", "ListeningSound.mp3")
NOT_LISTENING_SOUND = os.path.join(AUDIO_FILES_AND_STORAGE_FOLDER, "SoundEffects", "NotListening.mp3")

# Assistant Scripts
ASSISTANT_SCRIPT = os.path.join(ASSISTANT_FOLDER, "assistant_script.py")
JARVIS_UI_SCRIPT = os.path.join(JARVISMAIN_FOLDER, "jarvis_ui.py")

# Assistant UI Path
JARVIS_GIF_FOLDER = os.path.join(JARVISMAIN_FOLDER, "JarvisGifs")
IDLE_GIF = os.path.join(JARVIS_GIF_FOLDER, "subtle.gif")
TALKING_GIF = os.path.join(JARVIS_GIF_FOLDER, "energetic.gif")
LISTENING_GIF = os.path.join(JARVIS_GIF_FOLDER, "listening.gif")

# TTS & Audio Output
AUDIO_OUTPUT_FOLDER = os.path.join(AUDIO_FILES_AND_STORAGE_FOLDER, "audio_output_tts")
TTS_AIFF_OUTPUT = os.path.join(AUDIO_OUTPUT_FOLDER, "generated_tts.aiff")
TTS_WAV_OUTPUT = os.path.join(AUDIO_OUTPUT_FOLDER, "generated_tts.wav")
TTS_ENHANCED_OUTPUT = os.path.join(AUDIO_OUTPUT_FOLDER, "output_enhanced.wav")

# User Voice Input Storage
USER_VOICE_COMMAND = os.path.join(ASSISTANT_FOLDER, "command_audio.wav")
CLEANED_AUDIO_FOLDER = os.path.join(AUDIO_FILES_AND_STORAGE_FOLDER, "cleaned_audio")

# Ensure directories exist
os.makedirs(AUDIO_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(CLEANED_AUDIO_FOLDER, exist_ok=True)