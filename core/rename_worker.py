from PySide6.QtCore import (
    QThread,
    Signal
)

from core.execute_rename import (
    execute_rename
)


class RenameWorker(QThread):

    finished_rename = Signal(dict)

    def __init__(self, files):

        super().__init__()

        self.files = files

    def run(self):

        stats = execute_rename(
            self.files
        )

        self.finished_rename.emit(
            stats
        )