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
    QHeaderView,
    QListWidget,
    QProgressBar
)

from core.worker import ScanWorker
from core.rename_worker import RenameWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.folders = []
        self.files = []

        self.worker = None
        self.rename_worker = None

        self.init_ui()

    # ==================================================
    # INTERFAZ
    # ==================================================

    def init_ui(self):

        self.setWindowTitle("NexRename Media v0.3")
        self.resize(1200, 750)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # ==================================================
        # BOTONES DE CARPETAS
        # ==================================================

        folder_buttons_layout = QHBoxLayout()

        self.select_btn = QPushButton(
            "Agregar carpeta"
        )

        self.remove_btn = QPushButton(
            "Eliminar seleccionada"
        )

        self.select_btn.clicked.connect(
            self.add_folder
        )

        self.remove_btn.clicked.connect(
            self.remove_folder
        )

        folder_buttons_layout.addWidget(
            self.select_btn
        )

        folder_buttons_layout.addWidget(
            self.remove_btn
        )

        main_layout.addLayout(
            folder_buttons_layout
        )

        # ==================================================
        # LISTA DE CARPETAS
        # ==================================================

        self.folder_list = QListWidget()

        main_layout.addWidget(
            self.folder_list
        )

        # ==================================================
        # TABLA DE PREVISUALIZACIÓN
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

        main_layout.addWidget(
            self.table
        )

        # ==================================================
        # BOTONES DE ACCIÓN
        # ==================================================

        actions_layout = QHBoxLayout()

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

        # Se implementará después
        self.undo_btn.setEnabled(False)

        self.rename_btn.setEnabled(False)

        actions_layout.addWidget(
            self.scan_btn
        )

        actions_layout.addWidget(
            self.rename_btn
        )

        actions_layout.addWidget(
            self.undo_btn
        )

        main_layout.addLayout(
            actions_layout
        )

        # ==================================================
        # BARRA DE PROGRESO
        # ==================================================

        self.progress_bar = QProgressBar()

        self.progress_bar.setValue(0)

        main_layout.addWidget(
            self.progress_bar
        )

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
    # AGREGAR CARPETA
    # ==================================================

    def add_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta"
        )

        if not folder:
            return

        if folder in self.folders:

            QMessageBox.information(
                self,
                "Carpeta duplicada",
                "Esta carpeta ya fue agregada."
            )

            return

        self.folders.append(folder)

        self.folder_list.addItem(folder)

    # ==================================================
    # ELIMINAR CARPETA
    # ==================================================

    def remove_folder(self):

        row = self.folder_list.currentRow()

        if row < 0:
            return

        self.folders.pop(row)

        self.folder_list.takeItem(row)

    # ==================================================
    # ESCANEAR CARPETAS
    # ==================================================

    def start_scan(self):

        if not self.folders:

            QMessageBox.warning(
                self,
                "Sin carpetas",
                "Agregue al menos una carpeta."
            )

            return

        self.progress_bar.setValue(0)

        self.scan_btn.setEnabled(False)
        self.rename_btn.setEnabled(False)

        self.table.setRowCount(0)

        self.stats_label.setText(
            "Analizando archivos..."
        )

        self.worker = ScanWorker(
            self.folders
        )

        self.worker.progress.connect(
            self.update_progress
        )

        self.worker.finished_scan.connect(
            self.load_preview
        )

        self.worker.start()

    # ==================================================
    # ACTUALIZAR PROGRESO
    # ==================================================

    def update_progress(self, value):

        self.progress_bar.setValue(value)

    # ==================================================
    # CARGAR TABLA
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

        self.progress_bar.setValue(100)

        self.stats_label.setText(
            f"Escaneados: {len(files)}"
        )

        self.scan_btn.setEnabled(True)

        if files:
            self.rename_btn.setEnabled(True)

    # ==================================================
    # RENOMBRAR ARCHIVOS
    # ==================================================

    def start_rename(self):

        if not self.files:

            QMessageBox.warning(
                self,
                "Sin archivos",
                "No hay archivos para renombrar."
            )

            return

        response = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Desea renombrar {len(self.files)} archivos?",
            QMessageBox.Yes | QMessageBox.No
        )

        if response != QMessageBox.Yes:
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

        self.scan_btn.setEnabled(True)
        self.rename_btn.setEnabled(False)

        self.stats_label.setText(
            f"Renombrados: {stats['renamed']} | "
            f"Duplicados: {stats['duplicates']} | "
            f"Conflictos: {stats['conflicts']} | "
            f"Errores: {stats['errors']}"
        )

        QMessageBox.information(
            self,
            "Proceso completado",
            "El renombrado finalizó correctamente."
        )

        # Limpiar tabla

        self.table.setRowCount(0)
        self.files = []

        self.progress_bar.setValue(0)