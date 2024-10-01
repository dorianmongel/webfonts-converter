from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QListWidget, QFileDialog, QHBoxLayout, QListWidgetItem
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPalette, QColor, QPixmap, QPainter, QBrush, QIcon
from PyQt6.QtSvg import QSvgRenderer
import sys
import os
import shutil
from fontTools import ttLib

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertisseur de Webfonts")
        self.setGeometry(100, 100, 400, 400)

        background_path = self.resource_path("background.png")
        self.background = QPixmap(background_path)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        texte = "Glissez vos polices ici"
        self.bouton_texte = "Réinitialiser"
        self.bouton_generer_texte = "Générer"
        self.bouton_retirer_texte = ""
        
        self.label = QLabel(texte)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #2c3e50;")
        self.layout.addWidget(self.label)

        self.liste_fichiers = QListWidget()
        self.liste_fichiers.setStyleSheet("background-color: rgba(255, 255, 255, 50); color: white; border-radius: 5px;") 
        self.layout.addWidget(self.liste_fichiers)

        boutons_layout = QHBoxLayout()

        self.bouton_generer = QPushButton(self.bouton_generer_texte)
        self.bouton_generer.clicked.connect(self.generer_fichiers)
        self.bouton_generer.setStyleSheet("background-color: rgba(46, 204, 113, 200); padding: 10px 0; color: white; border-radius: 5px;")
        boutons_layout.addWidget(self.bouton_generer)

        self.bouton_reinitialiser = QPushButton(self.bouton_texte)
        self.bouton_reinitialiser.clicked.connect(self.reinitialiser)
        self.bouton_reinitialiser.setStyleSheet("background-color: #e74c3c;  padding: 10px 0; color: white; border-radius: 5px;")
        boutons_layout.addWidget(self.bouton_reinitialiser)

        self.layout.addLayout(boutons_layout)

        self.setAcceptDrops(True)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            chemin_fichier = url.toLocalFile()
            if chemin_fichier.lower().endswith(('.ttf', '.woff', '.otf', '.woff2')):
                nom_fichier = os.path.basename(chemin_fichier)
                item_widget = QWidget()
                item_layout = QHBoxLayout(item_widget)
                item_layout.setSpacing(0)
                item_layout.setContentsMargins(0, 0, 0, 0)
                item_label = QLabel(nom_fichier)
                item_label.setStyleSheet("color: #2c3e50; padding: 0 10px; background-color: transparent;")
                item_layout.addWidget(item_label)
                bouton_retirer = QPushButton()
                svg_renderer = QSvgRenderer()
                svg_renderer.load(bytes("""<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="#ffffff" d="M216 48h-36V36a28 28 0 0 0-28-28h-48a28 28 0 0 0-28 28v12H40a12 12 0 0 0 0 24h4v136a20 20 0 0 0 20 20h128a20 20 0 0 0 20-20V72h4a12 12 0 0 0 0-24M100 36a4 4 0 0 1 4-4h48a4 4 0 0 1 4 4v12h-56Zm88 168H68V72h120Zm-72-100v64a12 12 0 0 1-24 0v-64a12 12 0 0 1 24 0m48 0v64a12 12 0 0 1-24 0v-64a12 12 0 0 1 24 0"/></svg>""", 'utf-8'))
                pixmap = QPixmap(24, 24)
                pixmap.fill(QColor(0, 0, 0, 0))
                painter = QPainter(pixmap)
                svg_renderer.render(painter)
                painter.end()
                bouton_retirer.setIcon(QIcon(pixmap))
                bouton_retirer.setFixedWidth(50)
                bouton_retirer.setStyleSheet("background-color: #e74c3c; border: none; padding: 2px; border-radius: 0; border-top-right-radius: 3px;  border-bottom-right-radius: 3px;")
                bouton_retirer.clicked.connect(lambda _, item=item_widget: self.retirer_fichier(item))
                item_layout.addWidget(bouton_retirer, 0, Qt.AlignmentFlag.AlignRight)
                item = QListWidgetItem(self.liste_fichiers)
                item.setSizeHint(item_widget.sizeHint())
                self.liste_fichiers.addItem(item)
                self.liste_fichiers.setItemWidget(item, item_widget)
                item.setData(Qt.ItemDataRole.UserRole, chemin_fichier)
                
                self.liste_fichiers.setSpacing(5)

    def retirer_fichier(self, item):
        for index in range(self.liste_fichiers.count()):
            if self.liste_fichiers.itemWidget(self.liste_fichiers.item(index)) == item:
                self.liste_fichiers.takeItem(index)
                break

    def generer_fichiers(self):
        css_content = ""
        html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test des polices</title>
    <link rel="stylesheet" href="fonts.css">
    <style>
        body {
            font-size: 18px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
"""
        dossier_export = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier d'exportation")
        if not dossier_export:
            return

        for index in range(self.liste_fichiers.count()):
            chemin_fichier = self.liste_fichiers.item(index).data(Qt.ItemDataRole.UserRole)
            css_content += self.convertir_police(chemin_fichier, dossier_export)
            nom_police = os.path.splitext(os.path.basename(chemin_fichier))[0]
            html_content += f"""
<h1 style="font-family: '{nom_police}';">Test de la police {nom_police}</h1>
<p style="font-family: '{nom_police}';">Portez ce vieux whisky au juge blond qui fume sur son île intérieure, à côté de l'alcôve ovoïde, où les bûches se consument dans l'âtre, ce qui lui permet de penser à la cænogenèse de l'être dont il est question dans la cause ambiguë entendue à Moÿ, dans un capharnaüm qui, pense-t-il, diminue çà et là la qualité de son œuvre.</p>
"""

        html_content += """
</body>
</html>"""

        with open(os.path.join(dossier_export, 'fonts.css'), 'w') as f:
            f.write(css_content)
        with open(os.path.join(dossier_export, 'fonts.html'), 'w') as f:
            f.write(html_content)

        self.label.setText(f"Export effectué")

    def convertir_police(self, chemin_fichier, dossier_export):
        try:
            nom_fichier = os.path.basename(chemin_fichier)
            nom_sans_extension = os.path.splitext(nom_fichier)[0]
            
            # Copier le fichier d'origine dans le dossier d'export, sauf pour OTF
            if not chemin_fichier.lower().endswith('.otf'):
                shutil.copy2(chemin_fichier, os.path.join(dossier_export, nom_fichier))
            
            if chemin_fichier.lower().endswith('.ttf'):
                font = ttLib.TTFont(chemin_fichier)
                font.save(os.path.join(dossier_export, f"{nom_sans_extension}.woff"))
                font.save(os.path.join(dossier_export, f"{nom_sans_extension}.woff2"))
            elif chemin_fichier.lower().endswith('.otf'):
                font = ttLib.TTFont(chemin_fichier)
                font.save(os.path.join(dossier_export, f"{nom_sans_extension}.ttf"))
                font.save(os.path.join(dossier_export, f"{nom_sans_extension}.woff"))
                font.save(os.path.join(dossier_export, f"{nom_sans_extension}.woff2"))
            elif chemin_fichier.lower().endswith('.woff'):
                font = ttLib.TTFont(chemin_fichier)
                font.save(os.path.join(dossier_export, f"{nom_sans_extension}.woff2"))
            elif chemin_fichier.lower().endswith('.woff2'):
                font = ttLib.TTFont(chemin_fichier)
                font.save(os.path.join(dossier_export, f"{nom_sans_extension}.woff"))
            else:
                raise ValueError("Format de fichier non pris en charge")
            
            return f"""@font-face {{
    font-family: '{nom_sans_extension}';
    src: url('{nom_sans_extension}.woff2') format('woff2'),
         url('{nom_sans_extension}.woff') format('woff'),
         url('{nom_sans_extension}.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    font-variant: normal;
    font-feature-settings: normal;
    font-variation-settings: normal;
}}
"""
            
        except Exception as e:
            self.label.setText(f"Erreur : {str(e)}")
            return ""

    def reinitialiser(self):
        self.label.setText("Glissez vos polices ici")
        self.liste_fichiers.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())