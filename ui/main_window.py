from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView
)

from core.worker import ScanWorker
from core.rename_worker import RenameWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.folder_path = ""
        self.files = []

        self.worker = None
        self.rename_worker = None

        self.init_ui()

    # ==================================================
    # INTERFAZ
    # ==================================================

    def init_ui(self):

        self.setWindowTitle("NexRename Media v0.2")
        self.resize(1100, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # ==================================================
        # BARRA SUPERIOR
        # ==================================================

        top_layout = QHBoxLayout()

        self.select_btn = QPushButton(
            "Seleccionar carpeta"
        )

        self.select_btn.clicked.connect(
            self.select_folder
        )

        self.path_label = QLabel(
            "Ninguna carpeta seleccionada"
        )

        top_layout.addWidget(self.select_btn)
        top_layout.addWidget(self.path_label)

        main_layout.addLayout(top_layout)

        # ==================================================
        # TABLA
        # ==================================================

        self.table = QTableWidget()

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels([
            "Archivo Original",
            "Nuevo Nombre"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setAlternatingRowColors(True)

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        main_layout.addWidget(self.table)

        # ==================================================
        # BOTONES INFERIORES
        # ==================================================

        bottom_layout = QHBoxLayout()

        self.scan_btn = QPushButton(
            "Analizar"
        )

        self.rename_btn = QPushButton(
            "Renombrar"
        )

        self.undo_btn = QPushButton(
            "Deshacer"
        )

        self.scan_btn.clicked.connect(
            self.start_scan
        )

        self.rename_btn.clicked.connect(
            self.start_rename
        )

        # Aún no implementado
        self.undo_btn.setEnabled(False)

        self.rename_btn.setEnabled(False)

        bottom_layout.addWidget(
            self.scan_btn
        )

        bottom_layout.addWidget(
            self.rename_btn
        )

        bottom_layout.addWidget(
            self.undo_btn
        )

        main_layout.addLayout(bottom_layout)

        # ==================================================
        # ESTADÍSTICAS
        # ==================================================

        self.stats_label = QLabel(
            "Escaneados: 0"
        )

        main_layout.addWidget(
            self.stats_label
        )

        central_widget.setLayout(
            main_layout
        )

    # ==================================================
    # SELECCIONAR CARPETA
    # ==================================================

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta"
        )

        if folder:

            self.folder_path = folder

            self.path_label.setText(
                folder
            )

            self.table.setRowCount(0)

            self.stats_label.setText(
                "Escaneados: 0"
            )

            self.files = []

            self.rename_btn.setEnabled(
                False
            )

    # ==================================================
    # ESCANEO
    # ==================================================

    def start_scan(self):

        if not self.folder_path:

            QMessageBox.warning(
                self,
                "Carpeta no seleccionada",
                "Seleccione una carpeta primero."
            )

            return

        self.scan_btn.setEnabled(False)

        self.rename_btn.setEnabled(False)

        self.stats_label.setText(
            "Analizando archivos..."
        )

        self.table.setRowCount(0)

        self.worker = ScanWorker(
            self.folder_path
        )

        self.worker.finished_scan.connect(
            self.load_preview
        )

        self.worker.start()

    # ==================================================
    # CARGAR VISTA PREVIA
    # ==================================================

    def load_preview(self, files):

        self.files = files

        self.table.setRowCount(
            len(files)
        )

        for row, file in enumerate(files):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    file["original"]
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    file["new"]
                )
            )

        self.stats_label.setText(
            f"Escaneados: {len(files)}"
        )

        self.scan_btn.setEnabled(True)

        if files:
            self.rename_btn.setEnabled(
                True
            )

    # ==================================================
    # RENOMBRAR
    # ==================================================

    def start_rename(self):

        if not self.files:

            QMessageBox.warning(
                self,
                "Sin archivos",
                "No hay archivos para renombrar."
            )

            return

        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Desea renombrar {len(self.files)} archivos?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        self.rename_btn.setEnabled(False)

        self.scan_btn.setEnabled(False)

        self.stats_label.setText(
            "Renombrando archivos..."
        )

        self.rename_worker = RenameWorker(
            self.files
        )

        self.rename_worker.finished_rename.connect(
            self.finish_rename
        )

        self.rename_worker.start()

    # ==================================================
    # FINALIZAR RENOMBRADO
    # ==================================================

    def finish_rename(self, stats):

        self.stats_label.setText(
            f"Renombrados: {stats['renamed']} | "
            f"Duplicados: {stats['duplicates']} | "
            f"Conflictos: {stats['conflicts']} | "
            f"Errores: {stats['errors']}"
        )

        self.rename_btn.setEnabled(True)

        self.scan_btn.setEnabled(True)

        QMessageBox.information(
            self,
            "Proceso finalizado",
            "El renombrado ha finalizado correctamente."
        )

        # Limpiar tabla tras renombrar

        self.table.setRowCount(0)

        self.files = []

        self.rename_btn.setEnabled(False)