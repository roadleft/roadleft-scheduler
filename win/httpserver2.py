import sys
import os
import threading
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore

class HttpDaemon(QtCore.QThread):

    def __init__(self, parent):
        super().__init__(self, parent)
        self.window = parent
        self._lock = threading.Lock()
        self.running = False

    def run(self):
        BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
        PROJECT_DIR = os.path.join(BASE_DIR, 'roadleft_clock')
        sys.path.append(PROJECT_DIR)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roadleft_clock.settings")
        from django.core.management import execute_from_command_line
        print("Starting Django Server...")
        execute_from_command_line(["management.py", "runserver", "--noreload", "--nothreading"])

    def stop(self):
        self.running = False
        with
