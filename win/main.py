"""
Name: roadleft-blog Application
Author: fish走出地球
Date started: 14 Aug 2020
"""

import os
import sys
import webbrowser
from tendo import singleton
from PyQt5 import QtWidgets, QtGui, QtCore
from httpserver import  HttpDaemon


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        open_app = menu.addAction("Open Admin")
        open_app.triggered.connect(self.open_note)
        open_app.setIcon(QtGui.QIcon('icon.png'))

        # open_app = menu.addAction("reload server")
        # open_app.triggered.connect(self.reload_httpserver)
        # open_app.setIcon(QtGui.QIcon('icon.png'))

        menu.addSeparator()

        exit_app = menu.addAction("Exit")
        # exit_app.triggered.connect(lambda: sys.exit())
        exit_app.triggered.connect(self.exit_app)
        exit_app.setIcon(QtGui.QIcon('icon.png'))

        self.setContextMenu(menu)

        self.msg_parent = QtWidgets.QWidget()
        self.server = HttpDaemon()

    def reload_httpserver(self):
        self.server.stop()
        self.server.start()
        # from server_manage import ServerWin
        # self.win = ServerWin()
        # self.win.show()

    def open_note(self):
        webbrowser.open("http://127.0.0.1:8000/admin/", 1)
        # print("closeing django")
        # self.server.terminate()
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.blog.settings")
        # from django.core.wsgi import get_wsgi_application 
        # application = get_wsgi_application()
        # from django.core.management import call_command
        # call_command('runserver',  '127.0.0.1:8000')
        # print("django server start")

    def exit_app(self):
        reply = QtWidgets.QMessageBox.question(
            self.msg_parent, 
            'Confirm exit', 
            'Are you sure you want to exit Persistent laucher?',
            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            QtCore.QCoreApplication.exit(0)  
    


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)
    tray_icon.show()
    tray_icon.server.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    
    try:
        me = singleton.SingleInstance()
    except singleton.SingleInstanceException:
        sys.exit(1)
    main()
