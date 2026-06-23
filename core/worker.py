from PySide6.QtCore import (
    QThread,
    Signal
)

from core.scanner import scan_folders


class ScanWorker(QThread):

    finished_scan = Signal(list)
    progress = Signal(int)

    def __init__(self, folders):
        super().__init__()

        self.folders = folders

    def run(self):

        files = scan_folders(
            self.folders,
            self.progress.emit
        )

        self.finished_scan.emit(files)