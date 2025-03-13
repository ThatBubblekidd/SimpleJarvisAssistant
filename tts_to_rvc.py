import os
import sys
import subprocess
import time

# Ensure the script can find pathfile.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pathfile

def loading_animation(text="Loading", duration=1, delay=0.5):
    """ Display a repeating 'Loading... . .. ...' animation for a given duration. """
    dots = ["", ".", "..", "..."]
    start_time = time.time()

    while time.time() - start_time < duration:
        for dot in dots:
            sys.stdout.write(f"\r{text}{dot}  ")  # Overwrite line with new dots
            sys.stdout.flush()
            time.sleep(delay)

    sys.stdout.write("\r" + " " * len(text + "...") + "\r")  # Clear line
    sys.stdout.flush()

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def run_assistant_script():
    """Run assistant_script.py with the input method from settings.txt (defaulting to 'text')."""
    try:
        with open(pathfile.SETTINGS_FILE, "r") as f:
            input_method = f.read().strip()
    except FileNotFoundError:
        input_method = "text"
    clear_screen()
    loading_animation("Loading", duration=7)
    subprocess.run(["python3", pathfile.ASSISTANT_SCRIPT, input_method])


def start_jarvis_ui():
    """Set the state to 'talking'."""
    with open(pathfile.STATE_FILE, "w", encoding="utf-8") as f:
        f.write("talking")


def idle_jarvis_ui():
    """Set the state to 'idle'."""
    with open(pathfile.STATE_FILE, "w", encoding="utf-8") as f:
        f.write("idle")


def process_with_rvc(input_path, output_path):
    """Process the given audio file with RVC and play the enhanced output."""
    original_directory = os.getcwd()  # Save the current directory (Assistant folder)

    # Change to the RVC directory
    os.chdir(pathfile.RVC_FOLDER)

    # Export required environment variables
    os.environ['index_root'] = ""
    os.environ['hubert_path'] = pathfile.RVC_HUBERT_PATH
    os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = "1"

    # Print environment variables (for debugging)
    # print(f"export index_root={os.environ['index_root']}")
    # print(f"export hubert_path={os.environ['hubert_path']}")
    # print(f"export PYTORCH_ENABLE_MPS_FALLBACK={os.environ['PYTORCH_ENABLE_MPS_FALLBACK']}")

    # RVC command structure (using pathfile.py paths)
    rvc_command = (
        f"python {pathfile.RVC_CLI_SCRIPT} infer "
        f"--modelPath {pathfile.RVC_MODEL_PATH} "
        f"--inputPath {input_path} "
        f"--outputPath {output_path} "
        "--f0method harvest "
        "--protect 0.5"
    )

    # Run the RVC command
    subprocess.run(rvc_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Play the output enhanced audio file
    print("\nJarvis is talking...")
    start_jarvis_ui()
    subprocess.run(["afplay", output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Return to the original directory
    idle_jarvis_ui()
    os.chdir(original_directory)

    # After playing the audio, rerun the assistant_script.py
    run_assistant_script()


def main():
    """Main function to process TTS output with RVC."""
    if len(sys.argv) != 3:
        print("Usage: python tts_to_rvc.py <input_tts_wav> <output_enhanced_wav>")
        sys.exit(1)

    input_tts_path = sys.argv[1]
    output_enhanced_path = sys.argv[2]

    process_with_rvc(input_tts_path, output_enhanced_path)


if __name__ == "__main__":
    main()