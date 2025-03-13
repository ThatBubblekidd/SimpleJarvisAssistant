import os
import subprocess
import sys
import time
import requests  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pathfile  # Import the paths from pathfile.py



def idle_jarvis_ui():
    """Set the state to 'idle'."""
    with open(pathfile.STATE_FILE, "w", encoding="utf-8") as f:
        f.write("idle")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_user_input(prompt):
    """Ensure input is clean and fully displayed on a fresh line."""
    sys.stdout.write(prompt + " ")  # ✅ Prevents weird tab artifacts
    sys.stdout.flush()
    with open("/dev/tty") as tty:  # ✅ Forces clean input (prevents tab 1 bug)
        return tty.readline().strip()

def create_main_flag():
    with open(pathfile.JARVIS_UI_FLAG, "w") as f:
        f.write("running")

def remove_main_flag():
    if os.path.exists(pathfile.JARVIS_UI_FLAG):
        os.remove(pathfile.JARVIS_UI_FLAG)

def launch_jarvis_ui():
    """Launch the Jarvis UI in a hidden process if it's not already running."""
    if os.path.exists(pathfile.JARVIS_UI_FLAG):
        return  # Already running.
    try:
        subprocess.Popen(
            ["open", "-a", pathfile.JARVIS_UI_APP],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        with open(pathfile.JARVIS_UI_FLAG, "w") as f:
            f.write("running")
    except Exception as e:
        print("Error launching Jarvis UI:", e)

def start_jarvis_ui():
    """Launch jarvis_ui.py in a new (hidden) Terminal window."""
    # Ensure the "idle" state file exists.
    if not os.path.exists(pathfile.STATE_FILE):
        with open(pathfile.STATE_FILE, "w") as f:
            f.write("idle")

    # AppleScript to open a new Terminal window, run jarvis_ui.py, and minimize that new window only.
    applescript_code = f'''
        tell application "Terminal"
            -- Open a new Terminal window running jarvis_ui.py
            set newTerm to do script "python3 {pathfile.JARVIS_UI_SCRIPT}"
            
            -- Give Terminal a moment to open the new window
            delay 1
            
            -- Use the newly opened window's ID and minimize it
            tell window id (id of newTerm)
                set miniaturized to true
            end tell
        end tell
    '''

    try:
        subprocess.Popen(
            ["osascript", "-e", applescript_code],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Failed to launch Jarvis UI: {e}")

def settings():
    """Display the settings menu and update the settings file."""
    while True:
        clear_screen()
        print("----- Settings Menu -----")
        print("1. Text Input")
        print("2. Voice Input")
        print("3. Return to Main Menu")

        choice = get_user_input("\nChoose an option:")

        if choice == "1":
            with open(pathfile.SETTINGS_FILE, "w") as f:
                f.write("text")
            print("\n✅ Text input selected. \n\nPress Enter to continue.")
            input()
            return
        elif choice == "2":
            with open(pathfile.SETTINGS_FILE, "w") as f:
                f.write("voice")
            print("\n✅ Voice input selected. \n\nPress Enter to continue.\n")
            input()
            return
        elif choice == "3":
            return
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")
            time.sleep(1)

def main_menu_without_ui_launch():
    """Display main menu without re-launching the Jarvis UI."""
    while True:
        clear_screen()
        print("Welcome to the Main Interface (Single-Run)!")
        print("1. Continue to Assistant Script")
        print("2. Quit")
        print("3. Settings")

        choice = get_user_input("\nChoose an option:")

        if choice == "1":
            try:
                with open(pathfile.SETTINGS_FILE, "r") as f:
                    input_method = f.read().strip()
            except FileNotFoundError:
                input_method = "text"
            run_assistant_script(input_method)
            return
        elif choice == "2":
            print("Exiting the program... Goodbye!")
            remove_main_flag()
            clear_screen()
            sys.exit(0)
        elif choice == "3":
            settings()
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")
            time.sleep(1)

def run_assistant_script(input_method):
    """Run assistant_script.py with the given input method, then exit."""
    clear_screen()
    print(f"Running assistant_script.py with '{input_method}' input method...")
    subprocess.run(["python3", pathfile.ASSISTANT_SCRIPT, input_method])
    print("Assistant script has finished. Exiting now.")
    time.sleep(5)
    clear_screen()
    sys.exit(0)

def main():
    """Main interface entry point."""
    clear_screen()
    create_main_flag()

  

    # Launch Jarvis UI once.
    idle_jarvis_ui()
    start_jarvis_ui()
    launch_jarvis_ui()
    
    main_menu_without_ui_launch()

if __name__ == "__main__":
    main()