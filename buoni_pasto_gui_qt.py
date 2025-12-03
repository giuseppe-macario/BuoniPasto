# buoni_pasto_gui_qt.py

import os
import sys

from PyQt6 import QtWidgets, QtCore
from buoni_pasto_core import elabora_pdf


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Buoni pasto - estrattore PDF (PyQt6)")
        self.resize(800, 600)

        # ----- widget centrali -----
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)

        # --- Riga selezione file ---
        file_layout = QtWidgets.QHBoxLayout()

        self.label_file = QtWidgets.QLabel("File PDF:", self)
        file_layout.addWidget(self.label_file)

        self.edit_path = QtWidgets.QLineEdit(self)
        self.edit_path.setPlaceholderText("Seleziona un file PDF…")
        file_layout.addWidget(self.edit_path, stretch=1)

        self.btn_browse = QtWidgets.QPushButton("Sfoglia…", self)
        self.btn_browse.clicked.connect(self.scegli_file)
        file_layout.addWidget(self.btn_browse)

        layout.addLayout(file_layout)

        # --- Pulsante Elabora ---
        self.btn_elabora = QtWidgets.QPushButton("Elabora", self)
        self.btn_elabora.clicked.connect(self.esegui_elaborazione)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.btn_elabora)
        layout.addLayout(buttons_layout)

        # --- Area di testo per l'output ---
        self.label_output = QtWidgets.QLabel("Risultato:", self)
        layout.addWidget(self.label_output)

        self.text_output = QtWidgets.QPlainTextEdit(self)
        self.text_output.setReadOnly(True)
        font = self.text_output.font()
        font.setFamily("Menlo")  # o un font monospazio simile
        self.text_output.setFont(font)
        layout.addWidget(self.text_output, stretch=1)

        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Pronto")

    def scegli_file(self):
        dialog = QtWidgets.QFileDialog(self, "Seleziona il PDF")
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("File PDF (*.pdf);;Tutti i file (*.*)")

        if dialog.exec():
            selected_files = dialog.selectedFiles()
            if selected_files:
                path = selected_files[0]
                self.edit_path.setText(path)
                self.status_bar.showMessage(f"Selezionato: {path}", 5000)

    def esegui_elaborazione(self):
        path = self.edit_path.text().strip()

        if not path:
            QtWidgets.QMessageBox.warning(
                self,
                "Attenzione",
                "Seleziona prima un file PDF."
            )
            return

        if not os.path.isfile(path):
            QtWidgets.QMessageBox.critical(
                self,
                "Errore",
                f"File non trovato:\n{path}"
            )
            return

        self.btn_elabora.setEnabled(False)
        self.text_output.clear()
        self.text_output.appendPlainText("Elaborazione in corso...")
        self.status_bar.showMessage("Elaborazione in corso...")

        # Per evitare blocchi pesanti si potrebbe usare un thread, ma
        # per ora teniamo tutto sincrono (è veloce abbastanza nella maggior parte dei casi).
        QtWidgets.QApplication.processEvents()

        try:
            risultato = elabora_pdf(path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Errore",
                f"Si è verificato un errore durante l'elaborazione:\n{e}"
            )
            self.text_output.clear()
            self.status_bar.showMessage("Errore", 5000)
        else:
            self.text_output.clear()
            self.text_output.appendPlainText(risultato or "(nessun output)")
            self.status_bar.showMessage("Elaborazione completata", 5000)
        finally:
            self.btn_elabora.setEnabled(True)


def main():
    app = QtWidgets.QApplication(sys.argv)

    # (opzionale) impostazioni di base
    app.setApplicationName("Buoni pasto - estrattore PDF")
    app.setOrganizationName("Giuseppe")  # o quello che vuoi

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

