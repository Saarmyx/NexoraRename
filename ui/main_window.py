from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NexRename Media v0.1")
        self.resize(1000, 650)

        self.folder_path = ""

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        top = QHBoxLayout()

        self.select_btn = QPushButton(
            "Seleccionar carpeta"
        )

        self.select_btn.clicked.connect(
            self.select_folder
        )

        self.path_label = QLabel(
            "Ninguna carpeta seleccionada"
        )

        top.addWidget(self.select_btn)
        top.addWidget(self.path_label)

        layout.addLayout(top)

        self.table = QTableWidget()

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels([
            "Archivo Original",
            "Nuevo Nombre"
        ])

        layout.addWidget(self.table)

        bottom = QHBoxLayout()

        self.scan_btn = QPushButton("Analizar")
        self.rename_btn = QPushButton("Renombrar")
        self.undo_btn = QPushButton("Deshacer")

        bottom.addWidget(self.scan_btn)
        bottom.addWidget(self.rename_btn)
        bottom.addWidget(self.undo_btn)

        layout.addLayout(bottom)

        self.stats = QLabel(
            "Escaneados: 0 | Duplicados: 0"
        )

        layout.addWidget(self.stats)

        central.setLayout(layout)

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta"
        )

        if folder:
            self.folder_path = folder
            self.path_label.setText(folder)