import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QMessageBox, QFrame, QFileDialog)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QIcon, QDesktopServices
import qrcode
from PIL import Image

class ClickableLabel(QLabel):
    def __init__(self, text, link, parent=None):
        super().__init__(text, parent)
        self.link = link
        self.setStyleSheet("""
            color: #0066cc;
            font-size: 12px;
            text-decoration: underline;
            cursor: pointer;
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.link))

class QRGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Kod Oluşturucu")
        self.setFixedSize(600, 450)  # Yüksekliği biraz artırdım
        self.save_directory = "qr-images"  # Varsayılan kayıt dizini
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                min-width: 300px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#browse_button {
                min-width: 80px;
                background-color: #2196F3;
            }
            QPushButton#browse_button:hover {
                background-color: #1976D2;
            }
        """)

        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Kayıt dizini seçimi
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Kayıt Konumu:")
        self.dir_input = QLineEdit()
        self.dir_input.setText(self.save_directory)
        self.dir_input.setReadOnly(True)
        browse_button = QPushButton("Gözat")
        browse_button.setObjectName("browse_button")
        browse_button.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(browse_button)
        layout.addLayout(dir_layout)

        # URL girişi
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(" Örn:  https://mehmetc.dev")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Dosya adı girişi
        filename_layout = QHBoxLayout()
        filename_label = QLabel("QR Kod Adı:")
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Örn mehmetcdev")
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename_input)
        layout.addLayout(filename_layout)

        # Oluştur butonu
        create_button = QPushButton("QR Kod Oluştur")
        create_button.clicked.connect(self.generate_qr)
        layout.addWidget(create_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Ayraç çizgisi
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Hakkında bölümü
        about_layout = QVBoxLayout()
        
        developer_label = QLabel("Geliştirici: Mehmet ÇİMEN")
        developer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        developer_label.setStyleSheet("color: #666; font-size: 12px;")
        
        website_label = ClickableLabel("Website: https://mehmetc.dev", "https://mehmetc.dev")
        website_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        email_label = ClickableLabel("E-mail: mehmetcimentr@gmail.com", "mailto:mehmetcimentr@gmail.com")
        email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        about_layout.addWidget(developer_label)
        about_layout.addWidget(website_label)
        about_layout.addWidget(email_label)
        layout.addLayout(about_layout)

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "QR Kodları için Kayıt Konumu Seçin",
            self.save_directory,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        if dir_path:
            self.save_directory = dir_path
            self.dir_input.setText(dir_path)

    def generate_qr(self):
        url = self.url_input.text().strip()
        filename = self.filename_input.text().strip()

        # Boş alan kontrolü
        if not url or not filename:
            QMessageBox.warning(self, "Hata", "URL ve QR kod adı boş bırakılamaz!")
            return

        # .png uzantısı kontrolü
        if not filename.endswith('.png'):
            filename += '.png'

        try:
            # Seçilen klasörün varlığını kontrol et
            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)

            # QR kod oluştur
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Dosyayı kaydet
            file_path = os.path.join(self.save_directory, filename)
            qr_image.save(file_path)

            QMessageBox.information(self, "Başarılı", 
                f"QR kod başarıyla oluşturuldu!\nKonum: {file_path}")

            # Input alanlarını temizle
            self.url_input.clear()
            self.filename_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"QR kod oluşturulurken bir hata oluştu:\n{str(e)}")

def main():
    app = QApplication(sys.argv)
    window = QRGeneratorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()