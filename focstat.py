#!/usr/bin/env python3
import sys
import os
import subprocess
import collections
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import (
    QFileDialog, QListView, QTreeView, QAbstractItemView,
    QProgressDialog, QMenuBar, QDialog, QLabel, QVBoxLayout
)
import exifread
import matplotlib.pyplot as plt

# Version and Author
VERSION = "1.0"
AUTHOR = "Shotokanda"
LICENSE_TEXT = (
    "This software is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.\n"
    "You may not sell it.\n"
    "Attribution to the author \"Shotokanda\" is required."
)

# Texts in multiple languages
texts = {
    'English': {
        'title': 'Focal Length Histogram Generator',
        'description': 'Select one or more photo folders and generate a histogram of the focal lengths used.',
        'select_folders': 'Select Folders…',
        'generate': 'Generate Histogram',
        'scan_progress': 'Scanning images...',
        'no_folder': 'Please select at least one folder.',
        'no_jpg': 'No JPG files found.',
        'no_data': 'No focal lengths found.',
        'about': 'About',
        'language': 'Language',
        'remove_selected': 'Remove Selected',
        'clear_all': 'Clear All',
        'x_label': 'focal length',
        'y_label': 'amount of pictures'
    },
    'Deutsch': {
        'title': 'Brennweiten-Histogramm Generator',
        'description': 'Wähle einen oder mehrere Ordner mit Fotos und erstelle ein Histogramm der verwendeten Brennweiten.',
        'select_folders': 'Ordner auswählen…',
        'generate': 'Histogramm erstellen',
        'scan_progress': 'Scanne Bilder...',
        'no_folder': 'Bitte wähle mindestens einen Ordner aus.',
        'no_jpg': 'Keine JPG-Dateien gefunden.',
        'no_data': 'Keine Brennweiten gefunden.',
        'about': 'Über',
        'language': 'Sprache',
        'remove_selected': 'Auswahl entfernen',
        'clear_all': 'Alle löschen',
        'x_label': 'Brennweite',
        'y_label': 'Anzahl Fotos'
    },
    '日本語': {
        'title': '焦点距離ヒストグラムジェネレータ',
        'description': 'フォトフォルダを1つ以上選択し、使用した焦点距離のヒストグラムを作成します。',
        'select_folders': 'フォルダを選択…',
        'generate': 'ヒストグラム生成',
        'scan_progress': '画像をスキャン中...',
        'no_folder': '少なくとも1つのフォルダを選択してください。',
        'no_jpg': 'JPGファイルが見つかりません。',
        'no_data': '焦点距離が見つかりません。',
        'about': '情報',
        'language': '言語',
        'remove_selected': '選択を削除',
        'clear_all': 'すべてクリア',
        'x_label': '焦点距離',
        'y_label': '写真枚数'
    }
}

def get_focal_length(filepath):
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, stop_tag='EXIF FocalLength')
            fl = tags.get('EXIF FocalLength')
            if fl:
                return fl.values.num / fl.values.den
    except:
        pass
    try:
        out = subprocess.run(
            ['exiftool', '-FocalLength', '-s3', filepath],
            capture_output=True, text=True, check=True
        ).stdout.strip()
        if out:
            return float(out.split()[0])
    except:
        pass
    return None

class FocalApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("app_icon.png"))
        self.current_lang = 'English'
        self.build_ui()

    def build_ui(self):
        self.setWindowTitle(texts[self.current_lang]['title'])
        self.resize(800, 600)

        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.menubar = QMenuBar(self)
        self.lang_menu = self.menubar.addMenu(texts[self.current_lang]['language'])
        self.lang_menu.clear()
        for lang in texts:
            act = self.lang_menu.addAction(lang)
            act.triggered.connect(lambda chk, l=lang: self.change_language(l))
        self.about_act = self.menubar.addAction(texts[self.current_lang]['about'])
        self.about_act.triggered.connect(self.show_about)
        self.main_layout.setMenuBar(self.menubar)

        self.desc_label = QtWidgets.QLabel(texts[self.current_lang]['description'])
        self.desc_label.setWordWrap(True)
        self.main_layout.addWidget(self.desc_label)

        self.btn_layout = QtWidgets.QHBoxLayout()
        self.btn_sel = QtWidgets.QPushButton(texts[self.current_lang]['select_folders'])
        self.btn_sel.clicked.connect(self.select_dirs)
        self.btn_layout.addWidget(self.btn_sel)

        self.btn_remove = QtWidgets.QPushButton(texts[self.current_lang]['remove_selected'])
        self.btn_remove.clicked.connect(self.remove_selected)
        self.btn_layout.addWidget(self.btn_remove)

        self.btn_clear = QtWidgets.QPushButton(texts[self.current_lang]['clear_all'])
        self.btn_clear.clicked.connect(self.clear_all)
        self.btn_layout.addWidget(self.btn_clear)

        self.main_layout.addLayout(self.btn_layout)

        self.listw = QtWidgets.QListWidget()
        self.main_layout.addWidget(self.listw)

        self.btn_gen = QtWidgets.QPushButton(texts[self.current_lang]['generate'])
        self.btn_gen.clicked.connect(self.on_generate)
        self.main_layout.addWidget(self.btn_gen)

    def change_language(self, lang):
        self.current_lang = lang
        self.setWindowTitle(texts[lang]['title'])
        self.menubar.clear()
        self.lang_menu = self.menubar.addMenu(texts[lang]['language'])
        for l in texts:
            act = self.lang_menu.addAction(l)
            act.triggered.connect(lambda chk, ll=l: self.change_language(ll))
        self.about_act = self.menubar.addAction(texts[lang]['about'])
        self.about_act.triggered.connect(self.show_about)
        self.desc_label.setText(texts[lang]['description'])
        self.btn_sel.setText(texts[lang]['select_folders'])
        self.btn_gen.setText(texts[lang]['generate'])
        self.btn_remove.setText(texts[lang]['remove_selected'])
        self.btn_clear.setText(texts[lang]['clear_all'])

    def show_about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(texts[self.current_lang]['about'])
        dlg.setWindowIcon(QtGui.QIcon("app_icon.png"))
        dlg.setFixedSize(400, 300)

        layout = QVBoxLayout(dlg)
        icon_label = QLabel()
        icon_label.setPixmap(QtGui.QPixmap("app_icon.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel(f"<h2>{texts[self.current_lang]['title']}</h2>")
        title_label.setAlignment(Qt.AlignCenter)

        version_label = QLabel(f"Version {VERSION}<br>by {AUTHOR}")
        version_label.setAlignment(Qt.AlignCenter)

        desc_label = QLabel(texts[self.current_lang]['description'])
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)

        license_label = QLabel(LICENSE_TEXT)
        license_label.setAlignment(Qt.AlignCenter)
        license_label.setWordWrap(True)
        license_label.setStyleSheet("font-size: 10px; color: gray;")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addWidget(desc_label)
        layout.addWidget(license_label)

        dlg.exec_()

    def select_dirs(self):
        dlg = QFileDialog(self, texts[self.current_lang]['select_folders'])
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        for view in dlg.findChildren((QListView, QTreeView)):
            view.setSelectionMode(QAbstractItemView.MultiSelection)
        if dlg.exec_():
            self.listw.clear()
            for d in dlg.selectedFiles():
                self.listw.addItem(d)

    def remove_selected(self):
        for item in self.listw.selectedItems():
            self.listw.takeItem(self.listw.row(item))

    def clear_all(self):
        self.listw.clear()

    def on_generate(self):
        folders = [self.listw.item(i).text() for i in range(self.listw.count())]
        if not folders:
            QtWidgets.QMessageBox.warning(self, texts[self.current_lang]['title'], texts[self.current_lang]['no_folder'])
            return

        file_paths = []
        for folder in folders:
            for root, _, files in os.walk(folder):
                for f in files:
                    if f.lower().endswith(('.jpg', '.jpeg')):
                        file_paths.append(os.path.join(root, f))
        total = len(file_paths)
        if total == 0:
            QtWidgets.QMessageBox.information(self, texts[self.current_lang]['title'], texts[self.current_lang]['no_jpg'])
            return

        progress = QProgressDialog(texts[self.current_lang]['scan_progress'], texts[self.current_lang]['about'], 0, total, self)
        progress.setWindowTitle(texts[self.current_lang]['title'])
        progress.setWindowModality(Qt.WindowModal)
        progress.show()

        fls = []
        for i, path in enumerate(file_paths, start=1):
            if progress.wasCanceled():
                break
            fl = get_focal_length(path)
            if fl:
                fls.append(round(fl, 1))
            progress.setValue(i)
        progress.close()

        if not fls:
            QtWidgets.QMessageBox.information(self, texts[self.current_lang]['title'], texts[self.current_lang]['no_data'])
            return

        cnt = collections.Counter(fls)
        xs = sorted(cnt)
        ys = [cnt[x] for x in xs]
        plt.figure(figsize=(10, 5))
        plt.bar(xs, ys)
        plt.xticks(xs, rotation=90)
        plt.xlabel(texts[self.current_lang]['x_label'])
        plt.ylabel(texts[self.current_lang]['y_label'])
        plt.title(texts[self.current_lang]['title'])
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FocalApp()
    window.show()
    sys.exit(app.exec_())
