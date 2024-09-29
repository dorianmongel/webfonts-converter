from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from fontTools import ttLib
import sys
import locale

langue = locale.getdefaultlocale()[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if langue.startswith('en'):
            self.setWindowTitle("Webfonts Converter")
        else:
            self.setWindowTitle("Convertisseur de Webfonts")
        self.setGeometry(100, 100, 400, 300)

        fond = QPixmap("background.png")
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(fond))
        self.setPalette(palette)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        if langue.startswith('en'):
            texte = "Drop your fonts here"
            self.bouton_texte = "Reset"
        else:
            texte = "Glissez vos polices ici"
            self.bouton_texte = "Réinitialiser"
        
        self.label = QLabel(texte)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.bouton_reinitialiser = None

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            chemin_fichier = url.toLocalFile()
            if chemin_fichier.lower().endswith(('.ttf', '.woff')):
                self.convertir_police(chemin_fichier)

    def convertir_police(self, chemin_fichier):
        try:
            if chemin_fichier.lower().endswith('.ttf'):
                font = ttLib.TTFont(chemin_fichier)
                font.save(chemin_fichier.replace('.ttf', '.woff'))
                font.save(chemin_fichier.replace('.ttf', '.woff2'))
                if langue.startswith('en'):
                    message = f"Conversion successful"
                else:
                    message = f"Conversion réussie" 
            elif chemin_fichier.lower().endswith('.woff'):
                font = ttLib.TTFont(chemin_fichier)
                font.save(chemin_fichier.replace('.woff', '.ttf'))
                font.save(chemin_fichier.replace('.woff', '.woff2'))
                if langue.startswith('en'):
                    message = f"Conversion successful"
                else:
                    message = f"Conversion réussie"
            else:
                if langue.startswith('en'):
                    raise ValueError("Unsupported file format")
                else:
                    raise ValueError("Format de fichier non pris en charge")
            
            nom_fichier = chemin_fichier.split('/')[-1].split('.')[0]
            chemin_css = '/'.join(chemin_fichier.split('/')[:-1]) + '/font.css'
            
            with open(chemin_css, 'w') as f:
                f.write(f"""@font-face {{
                        font-family: '{nom_fichier}';
                        src: url('{nom_fichier}.woff2') format('woff2'),
                            url('{nom_fichier}.woff') format('woff'),
                        url('{nom_fichier}.ttf') format('truetype');
                    font-weight: normal;
                    font-style: normal;
                }}""")
            
            if langue.startswith('en'):
                message += f"\nCSS file generated"
            else:
                message += f"\nFichier CSS généré"
            self.label.setText(message)
            
            if self.bouton_reinitialiser is None:
                self.bouton_reinitialiser = QPushButton(self.bouton_texte)
                self.bouton_reinitialiser.clicked.connect(self.reinitialiser)
                self.layout.addWidget(self.bouton_reinitialiser)
            
            return
           
        except Exception as e:
            if langue.startswith('en'):
                self.label.setText(f"Error: {str(e)}")
            else:
                self.label.setText(f"Erreur : {str(e)}")

    def reinitialiser(self):
        if langue.startswith('en'):
            self.label.setText("Drop your fonts here")
        else:
            self.label.setText("Glissez vos polices ici")
        if self.bouton_reinitialiser:
            self.layout.removeWidget(self.bouton_reinitialiser)
            self.bouton_reinitialiser.deleteLater()
            self.bouton_reinitialiser = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())