from PyQt5.QtWidgets import QApplication
import sys as _s
import os as _o

class SystemActions():
    def __init__(self):
        status = None

    def exit_gui_thread(self):
        sp = QApplication(_s.argv)
        _s.exit(sp.exec_())       