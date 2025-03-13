import sys
import os
import signal
import subprocess
import atexit
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QMovie
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pathfile  # Import paths from pathfile.py

# Terminal hiding/closing functions
def set_terminal_title():
    try:
        subprocess.Popen(
            ["osascript", "-e", 'tell application "Terminal" to set custom title of front window to "JarvisUIHidden"'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

def hide_terminal():
    try:
        subprocess.Popen(
            ["osascript", "-e", 'tell application "Terminal" to set visible of front window to false'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

def close_jarvis_terminal():
    try:
        subprocess.Popen(
            ["osascript", "-e", 'tell application "Terminal" to close (first window whose custom title is "JarvisUIHidden")'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

hide_terminal()
atexit.register(close_jarvis_terminal)
set_terminal_title()

class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Interface")
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)

        # Create label for GIFs
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 565, 400)
        self.label.setScaledContents(True)

        # Opacity effect for transitions
        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

        # Load GIFs from `pathfile.py`
        self.idle_movie = QMovie(pathfile.IDLE_GIF)
        self.talking_movie = QMovie(pathfile.TALKING_GIF)
        self.listening_movie = QMovie(pathfile.LISTENING_GIF)
        self.idle_movie.setScaledSize(self.size())
        self.talking_movie.setScaledSize(self.size())
        self.listening_movie.setScaledSize(self.size())

        self.current_state = None
        self.current_movie = None

        # Ensure GIFs restart if they stop
        self.idle_movie.stateChanged.connect(self.movie_state_changed)
        self.talking_movie.stateChanged.connect(self.movie_state_changed)
        self.listening_movie.stateChanged.connect(self.movie_state_changed)

        # Start with idle animation (no transition initially)
        self.set_idle_animation(initial=True)

        # Timer to check state every second
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_state)
        self.timer.start()

        # Timer to check if main is running
        self.main_timer = QTimer(self)
        self.main_timer.setInterval(1000)
        self.main_timer.timeout.connect(self.check_main_flag)
        self.main_timer.start()

        # Make window draggable
        self.oldPos = self.pos()

    def check_main_flag(self):
        """Quit UI if main flag file does not exist."""
        if not os.path.exists(pathfile.JARVIS_UI_FLAG):
            QApplication.quit()

    def movie_state_changed(self, state):
        """Restart GIF if it stops unexpectedly."""
        from PyQt5.QtGui import QMovie
        if self.current_movie and self.current_movie.state() != QMovie.Running:
            self.current_movie.start()

    def transition_to(self, new_movie):
        """Smooth cross-fade transition between animations."""
        fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_out.setDuration(150)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)

        fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_in.setDuration(150)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.InOutQuad)

        def on_fade_out_finished():
            self.label.setMovie(new_movie)
            new_movie.start()
            fade_in.start()

        fade_out.finished.connect(on_fade_out_finished)
        fade_out.start()
        self.fade_out_anim = fade_out
        self.fade_in_anim = fade_in

    def set_idle_animation(self, initial=False):
        """Switch to idle GIF if not already in idle mode."""
        if self.current_state == "idle":
            if self.idle_movie.state() != QMovie.Running:
                self.idle_movie.start()
            return
        if initial or self.current_state is None:
            self.current_state = "idle"
            self.current_movie = self.idle_movie
            self.label.setMovie(self.idle_movie)
            self.idle_movie.start()
        else:
            self.current_state = "idle"
            self.current_movie = self.idle_movie
            self.transition_to(self.idle_movie)

    def set_talking_animation(self):
        """Switch to talking GIF if not already in talking mode."""
        if self.current_state == "talking":
            if self.talking_movie.state() != QMovie.Running:
                self.talking_movie.start()
            return
        self.current_state = "talking"
        self.current_movie = self.talking_movie
        self.transition_to(self.talking_movie)

    def set_listening_animation(self):
        """Switch to listening GIF if not already in listening mode."""
        if self.current_state == "listening":
            if self.listening_movie.state() != QMovie.Running:
                self.listening_movie.start()
            return
        self.current_state = "listening"
        self.current_movie = self.listening_movie
        self.transition_to(self.listening_movie)

    def check_state(self):
        """Read assistant state from state file and update GIF accordingly."""
        try:
            with open(pathfile.STATE_FILE, "r", encoding="utf-8") as f:
                state = f.read().strip().lower()
        except Exception:
            state = "idle"

        if state not in ("idle", "talking", "listening"):
            state = "idle"

        if state != self.current_state:
            if state == "talking":
                self.set_talking_animation()
            elif state == "listening":
                self.set_listening_animation()
            else:
                self.set_idle_animation()
        else:
            if self.current_state == "idle" and self.idle_movie.state() != QMovie.Running:
                self.idle_movie.start()
            elif self.current_state == "talking" and self.talking_movie.state() != QMovie.Running:
                self.talking_movie.start()
            elif self.current_state == "listening" and self.listening_movie.state() != QMovie.Running:
                self.listening_movie.start()

    def mousePressEvent(self, event):
        """Allow dragging the UI window."""
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        """Handle UI dragging."""
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

def main():
    """Launch UI and handle signals."""
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = JarvisWindow()
    window.move(50, 50)
    window.show()
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()