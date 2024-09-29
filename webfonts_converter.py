from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
from fontTools import ttLib
import sys
import locale

langue = locale.getdefaultlocale()[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertisseur de Webfonts")
        self.setGeometry(100, 100, 300, 200)

        if langue.startswith('en'):
            texte = "Déposez vos polices ici"
        else:
            texte = "Glissez vos polices ici"
        self.label = QLabel(texte, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            chemin_fichier = url.toLocalFile()
            if chemin_fichier.lower().endswith('.ttf'):
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
            return
           
        except Exception as e:
            if langue.startswith('en'):
                self.label.setText(f"Error: {str(e)}")
            else:
                self.label.setText(f"Erreur : {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())