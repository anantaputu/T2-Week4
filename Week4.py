# Nama  : I Putu Ananta Sugiartha
# NIM   : F1D0230113
# Kelas : D

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedWidth(500)

        self.init_ui()
        self.apply_style()
        self.setup_events()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label1 = QLabel("Angka Pertama")
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Masukkan angka")

        self.labelOp = QLabel("Operasi")
        self.combo = QComboBox()
        self.combo.addItems(["+ Tambah", "- Kurang", "× Kali", "÷ Bagi"])

        self.label2 = QLabel("Angka Kedua")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Masukkan angka")

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 11px;")

        btn_layout = QHBoxLayout()
        self.btn_hitung = QPushButton("Hitung (Enter)")
        self.btn_clear = QPushButton("Clear (Esc)")

        self.btn_hitung.setEnabled(False)

        btn_layout.addWidget(self.btn_hitung)
        btn_layout.addWidget(self.btn_clear)

        self.hasil = QLabel("Hasil: —")
        self.hasil.setAlignment(Qt.AlignCenter)
        self.hasil.setStyleSheet("background:#eee; color:#000; padding:10px; border-radius:6px;")

        self.info = QLabel("Input tidak valid — tombol Hitung dinonaktifkan")
        self.info.setStyleSheet("color: #888; font-size: 11px;")

        layout.addWidget(self.label1)
        layout.addWidget(self.input1)

        layout.addWidget(self.labelOp)
        layout.addWidget(self.combo)

        layout.addWidget(self.label2)
        layout.addWidget(self.input2)
        layout.addWidget(self.error_label)

        layout.addLayout(btn_layout)
        layout.addWidget(self.hasil)
        layout.addWidget(self.info)

        self.setLayout(layout)

    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 13px;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            QPushButton {
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
            QPushButton#clear {
                background-color: #e74c3c;
                color: white;
            }
        """)

    def setup_events(self):
        self.input1.textChanged.connect(self.validate)
        self.input2.textChanged.connect(self.validate)

        self.btn_hitung.clicked.connect(self.hitung)
        self.btn_clear.clicked.connect(self.clear)

    def is_number(self, text):
        try:
            float(text)
            return True
        except:
            return False

    def validate(self):
        val1 = self.is_number(self.input1.text())
        val2 = self.is_number(self.input2.text())

        if not val2 and self.input2.text() != "":
            self.input2.setStyleSheet("border: 2px solid red;")
            self.error_label.setText("⚠ Input harus berupa angka")
        else:
            self.input2.setStyleSheet("")
            self.error_label.setText("")

        valid = val1 and val2
        self.btn_hitung.setEnabled(valid)

    def hitung(self):
        a = float(self.input1.text())
        b = float(self.input2.text())
        op = self.combo.currentIndex()

        try:
            if op == 0:
                hasil = a + b
            elif op == 1:
                hasil = a - b
            elif op == 2:
                hasil = a * b
            elif op == 3:
                if b == 0:
                    raise ZeroDivisionError
                hasil = a / b

            self.hasil.setText(f"Hasil: {hasil}")

        except ZeroDivisionError:
            QMessageBox.warning(self, "Error", "Tidak bisa dibagi dengan 0")

    def clear(self):
        self.input1.clear()
        self.input2.clear()
        self.hasil.setText("Hasil: —")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.btn_hitung.isEnabled():
                self.hitung()
        elif event.key() == Qt.Key_Escape:
            self.clear()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Konfirmasi",
            "Yakin ingin keluar?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())