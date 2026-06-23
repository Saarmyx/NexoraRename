from PySide6.QtCore import (
    QThread,
    Signal
)

from core.scanner import scan_folder


class ScanWorker(QThread):

    finished_scan = Signal(list)

    def __init__(self, folder):

        super().__init__()

        self.folder = folder

    def run(self):

        files = scan_folder(
            self.folder
        )

        self.finished_scan.emit(
            files
        )