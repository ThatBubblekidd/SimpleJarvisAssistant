# Retrieval-based-Voice-Conversion


## 💻 System Requirements

Retrieval-based-Voice-Conversion has been tested and runs smoothly on the following system:

✅ Tested System:
• Device: MacBook Pro M3 (11-core)
• Memory: 18GB RAM
• OS: macOS

🖥️ Expected Compatibility:
• MacOS: ✅ Fully supported (Tested on macOS with M3 chip)
• Linux: ❓ Haven't Tested so I don't know
• Windows: ❓ Haven't Tested so I don't know

Note: If you’re using a different OS, additional setup or modifications may be required.



1. Clone the Retrieval-based Voice Conversion (RVC) repository

```bash
git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion.git
cd Retrieval-based-Voice-Conversion
```

2. Download the "Move_To_RVC_Folder" and of course, Move the "Move_To_RVC_Folder" to Retrieval-based-Voice-Conversion folder then open the folder up and then move assests folder (Folder is in Assistant), RVC_requirements.txt, and force_cpu.py out of the folder and into Retrieval-based-Voice-Conversion - (‼️DON'T DO THIS IF YOU HAVE ALREADY DONE IT FROM THE README.md‼️)

```bash
git clone https://huggingface.co/Thatbubblekid/RVC_Necessities_For_Mac
```

3. Install Pyenv (If Not Installed)

Ensure Pyenv is installed on your system:

```bash
brew install pyenv
```




## ⚙️ Required Environment

Before running/downloading dependencies for Jarvis AI Assistant and RVC, set up the correct environment.

4. Install python 3.10

Run the following commands in your terminal:

```bash
pyenv install 3.10.13
```
5. Run the environment in directory

```bash
pyenv global 3.10.13
``` 

6. Install Project Dependencies

```bash
pip install -r requirements.txt
```

7. Next is to run these - Make sure to input hubert_base.pt path which is in the assets folder you move to RVC

```bash
export index_root=""
export hubert_path="/path/to/hubert/directory/Retrieval-based-Voice-Conversion/assets/hubert/hubert_base.pt"
```

8. Test RVC

```bash
python /Path/to/Retrieval-based-Voice-Conversion/force_cpu.py infer \
        --modelPath "/path/to/assests/pth/file/Retrieval-based-Voice-Conversion/assets/pretrained/Jarvis/Jarvis.pth" \
        --inputPath "/path/to/input.wav" \
        --outputPath "/path/for/output.wav" \
        --f0method pm \
        --protect 0.5
```
🚀 You now have RVC installed! If you haven't looked at the README.md (In Assistant folder), please do for next steps!



