import os

import psutil
from PyQt5.QtCore import QSize, QThread, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (
    FluentWindow,
    MessageBox,
    NavigationItemPosition,
    SplashScreen,
)

from app.common.config import cfg
from app.components.DonateDialog import DonateDialog
from app.config import ASSETS_PATH, GITHUB_REPO_URL
from app.thread.version_manager_thread import VersionManager
from app.view.batch_process_interface import BatchProcessInterface
from app.view.home_interface import HomeInterface
from app.view.setting_interface import SettingInterface
from app.view.subtitle_style_interface import SubtitleStyleInterface

LOGO_PATH = ASSETS_PATH / "logo.png"


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        # Create sub-interfaces
        self.homeInterface = HomeInterface(self)
        self.settingInterface = SettingInterface(self)
        self.subtitleStyleInterface = SubtitleStyleInterface(self)
        self.batchProcessInterface = BatchProcessInterface(self)

        # Initialize version manager
        self.versionManager = VersionManager()
        self.versionManager.newVersionAvailable.connect(self.onNewVersion)
        self.versionManager.announcementAvailable.connect(self.onAnnouncement)

        # Create version check thread
        self.versionThread = QThread()
        self.versionManager.moveToThread(self.versionThread)
        self.versionThread.started.connect(self.versionManager.performCheck)
        self.versionThread.start()

        # Initialize navigation interface
        self.initNavigation()
        self.splashScreen.finish()

        # Register exit handler, cleanup processes
        import atexit

        atexit.register(self.stop)

    def initNavigation(self):
        """Initialize navigation bar"""
        # Add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr("Home"))
        self.addSubInterface(self.batchProcessInterface, FIF.VIDEO, self.tr("Batch Processing"))
        self.addSubInterface(self.subtitleStyleInterface, FIF.FONT, self.tr("Subtitle Style"))

        self.navigationInterface.addSeparator()

        # Add custom widgets at the bottom
        self.navigationInterface.addItem(
            routeKey="avatar",
            text="GitHub",
            icon=FIF.GITHUB,
            onClick=self.onGithubDialog,
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            self.tr("Settings"),
            NavigationItemPosition.BOTTOM,
        )

        # Set default interface
        self.switchTo(self.homeInterface)

    def switchTo(self, interface):
        if interface.windowTitle():
            self.setWindowTitle(interface.windowTitle())
        else:
            self.setWindowTitle(self.tr("Kaka Subtitle Assistant -- VideoCaptioner"))
        self.stackedWidget.setCurrentWidget(interface, popOut=False)

    def initWindow(self):
        """Initialize window"""
        self.resize(1050, 800)
        self.setMinimumWidth(700)
        self.setWindowIcon(QIcon(str(LOGO_PATH)))
        self.setWindowTitle(self.tr("Kaka Subtitle Assistant -- VideoCaptioner"))

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # Create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        # Set window position, center
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()
        QApplication.processEvents()

    def onGithubDialog(self):
        """Open GitHub"""
        w = MessageBox(
            self.tr("GitHub Information"),
            self.tr(
                "VideoCaptioner was independently developed by me in my spare time and is currently hosted on GitHub. Stars and Forks are welcome. The project indeed has many areas that need improvement. If you encounter software issues or bugs, please submit Issues.\n\n https://github.com/WEIFENG2333/VideoCaptioner"
            ),
            self,
        )
        w.yesButton.setText(self.tr("Open GitHub"))
        w.cancelButton.setText(self.tr("Support Author"))
        if w.exec():
            QDesktopServices.openUrl(QUrl(GITHUB_REPO_URL))
        else:
            # Open donation dialog when clicking "Support Author" button
            donate_dialog = DonateDialog(self)
            donate_dialog.exec_()

    def onNewVersion(self, version, force_update, update_info, download_url):
        """New version prompt"""
        title = "New Version Found" if not force_update else "Current Version Discontinued"
        content = f"New version found {version}\n\n{update_info}"
        w = MessageBox(title, content, self)
        w.yesButton.setText("Update Now")
        w.cancelButton.setText("Later" if not force_update else "Exit Program")
        if w.exec():
            QDesktopServices.openUrl(QUrl(download_url))
        if force_update:
            QApplication.quit()

    def onAnnouncement(self, content):
        """Show announcement"""
        w = MessageBox("Announcement", content, self)
        w.yesButton.setText("I Understand")
        w.cancelButton.hide()
        w.exec()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "splashScreen"):
            self.splashScreen.resize(self.size())

    def closeEvent(self, event):
        # Close all sub-interfaces
        # self.homeInterface.close()
        # self.batchProcessInterface.close()
        # self.subtitleStyleInterface.close()
        # self.settingInterface.close()
        super().closeEvent(event)

        # Force exit application
        QApplication.quit()

        # Ensure all threads and processes are terminated. Some error exits won't be handled.
        # import os
        # os._exit(0)

    def stop(self):
        # Find FFmpeg processes and close them
        process = psutil.Process(os.getpid())
        for child in process.children(recursive=True):
            child.kill()
