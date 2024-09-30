from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QListWidget, QFileDialog, QHBoxLayout, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from fontTools import ttLib
import sys
import locale
import os
import shutil

langue = locale.getdefaultlocale()[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if langue.startswith('en'):
            self.setWindowTitle("Webfonts Converter")
        else:
            self.setWindowTitle("Convertisseur de Webfonts")
        self.setGeometry(100, 100, 400, 400)

        # Définir la couleur de fond
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e272e"))
        self.setPalette(palette)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        if langue.startswith('en'):
            texte = "Drop your fonts here"
            self.bouton_texte = "Reset"
            self.bouton_generer_texte = "Generate"
            self.bouton_retirer_texte = "Remove"
        else:
            texte = "Glissez vos polices ici"
            self.bouton_texte = "Réinitialiser"
            self.bouton_generer_texte = "Générer"
            self.bouton_retirer_texte = "Retirer"
        
        self.label = QLabel(texte)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white;")  # Texte en blanc pour contraster avec le fond
        self.layout.addWidget(self.label)

        self.liste_fichiers = QListWidget()
        self.liste_fichiers.setStyleSheet("background-color: #15202b; color: white; border-radius: 5px;")  # Fond plus foncé, texte blanc
        self.layout.addWidget(self.liste_fichiers)

        # Création d'un layout horizontal pour les boutons
        boutons_layout = QHBoxLayout()

        self.bouton_generer = QPushButton(self.bouton_generer_texte)
        self.bouton_generer.clicked.connect(self.generer_fichiers)
        self.bouton_generer.setStyleSheet("background-color: #2ecc71; padding: 10px 0; color: white; border-radius: 5px;")  # Bouton bleu avec texte blanc et coins arrondis
        boutons_layout.addWidget(self.bouton_generer)

        self.bouton_reinitialiser = QPushButton(self.bouton_texte)
        self.bouton_reinitialiser.clicked.connect(self.reinitialiser)
        self.bouton_reinitialiser.setStyleSheet("background-color: #e74c3c;  padding: 10px 0; color: white; border-radius: 5px;")  # Bouton rouge avec texte blanc et coins arrondis
        boutons_layout.addWidget(self.bouton_reinitialiser)

        # Ajout du layout horizontal au layout principal
        self.layout.addLayout(boutons_layout)

        self.setAcceptDrops(True)

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
                item_layout.setSpacing(0)  # Réduit l'espace entre les éléments
                item_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges
                item_label = QLabel(nom_fichier)
                item_label.setStyleSheet("color: white; padding: 0 10px")
                item_layout.addWidget(item_label)
                bouton_retirer = QPushButton(self.bouton_retirer_texte)
                bouton_retirer.setStyleSheet("background-color: #e74c3c; color: white; padding: 2px; margin-right: 10px")
                bouton_retirer.clicked.connect(lambda _, item=item_widget: self.retirer_fichier(item))
                item_layout.addWidget(bouton_retirer)
                item = QListWidgetItem(self.liste_fichiers)
                item.setSizeHint(item_widget.sizeHint())
                self.liste_fichiers.addItem(item)
                self.liste_fichiers.setItemWidget(item, item_widget)
                item.setData(Qt.ItemDataRole.UserRole, chemin_fichier)

    def retirer_fichier(self, item):
        for index in range(self.liste_fichiers.count()):
            if self.liste_fichiers.itemWidget(self.liste_fichiers.item(index)) == item:
                self.liste_fichiers.takeItem(index)
                break

    def generer_fichiers(self):
        css_content = ""
        if langue.startswith('en'):
            html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Test</title>
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
            dossier_export = QFileDialog.getExistingDirectory(self, "Select export folder")
            if not dossier_export:
                return

            for index in range(self.liste_fichiers.count()):
                chemin_fichier = self.liste_fichiers.item(index).data(Qt.ItemDataRole.UserRole)
                css_content += self.convertir_police(chemin_fichier, dossier_export)
                nom_police = os.path.splitext(os.path.basename(chemin_fichier))[0]
                html_content += f"""
    <h1 style="font-family: '{nom_police}';">Test of the font {nom_police}</h1>
    <p style="font-family: '{nom_police}';">The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. Sphinx of black quartz, judge my vow. How vexingly quick daft zebras jump! The five boxing wizards jump quickly. Jackdaws love my big sphinx of quartz. Quick zephyrs blow, vexing daft Jim.</p>
"""

            html_content += """
</body>
</html>"""
        else:
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

        if langue.startswith('en'):
            self.label.setText(f"Export completed")
        else:
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
                if langue.startswith('en'):
                    raise ValueError("Unsupported file format")
                else:
                    raise ValueError("Format de fichier non pris en charge")
            
            return f"""@font-face {{
    font-family: '{nom_sans_extension}';
    src: url('{nom_sans_extension}.woff2') format('woff2'),
         url('{nom_sans_extension}.woff') format('woff'),
         url('{nom_sans_extension}.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}}
"""
            
        except Exception as e:
            if langue.startswith('en'):
                self.label.setText(f"Error: {str(e)}")
            else:
                self.label.setText(f"Erreur : {str(e)}")
            return ""

    def reinitialiser(self):
        if langue.startswith('en'):
            self.label.setText("Drop your fonts here")
        else:
            self.label.setText("Glissez vos polices ici")
        self.liste_fichiers.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())