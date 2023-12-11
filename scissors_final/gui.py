from __future__ import division
import time
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from threading import Thread
from livewire import Livewire


class ImageWin(QtWidgets.QWidget):
    def __init__(self):
        super(ImageWin, self).__init__()
        self.setupUi()
        self.active = False
        self.anchor_enabled = True
        self.anchor = None
        self.path_map = {}
        self.path = []

    def setupUi(self):
        self.hbox = QtWidgets.QVBoxLayout(self)

        # Placeholder or blank canvas initialization
        self.canvas = QtWidgets.QLabel(self)
        self.canvas.setMouseTracking(True)
        self.canvas.setText(
            "No Image Loaded. Click 'Load New Image' to begin.")
        self.canvas.setAlignment(QtCore.Qt.AlignCenter)  # Center the text

        # Load New Image Button
        self.load_button = QtWidgets.QPushButton('Load New Image', self)
        self.load_button.clicked.connect(self.load_new_image)
        self.hbox.addWidget(self.load_button)

        self.status_bar = QtWidgets.QStatusBar(self)
        self.status_bar.showMessage('Click "Load New Image" to begin')
        self.hbox.addWidget(self.status_bar)
        self.hbox.addWidget(self.canvas)
        self.setLayout(self.hbox)
        self.lw = None

    def load_new_image(self):
        new_image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, '', '', 'Images (*.bmp *.jpg *.png)')
        if new_image_path:
            self.image_path = new_image_path
            self.image = QPixmap(self.image_path)
            self.cv2_image = cv2.imread(str(self.image_path))
            self.lw = Livewire(self.cv2_image)
            self.w, self.h = self.image.width(), self.image.height()
            self.resize(self.w, self.h)
            self.canvas.setPixmap(self.image)
            self.path_map = {}
            self.path = []
            self.anchor = None
            self.status_bar.showMessage('Left click to set first anchor point')

    def mousePressEvent(self, event):
        if self.anchor_enabled:
            self.canvas.unsetCursor()
            pos = event.pos()
            x, y = pos.x()-self.canvas.x(), pos.y()-self.canvas.y()

            if x < 0:
                x = 0
            if x >= self.w:
                x = self.w - 1
            if y < 0:
                y = 0
            if y >= self.h:
                y = self.h - 1

            # Get the mouse cursor position
            p = y, x
            anchor = self.anchor

            # Export bitmap
            if event.buttons() == QtCore.Qt.MidButton:
                filepath = QtWidgets.QFileDialog.getSaveFileName(
                    self, 'Save image audio to', '', '*.bmp\n*.jpg\n*.png')
                image = self.image.copy()

                draw = QtGui.QPainter()
                draw.begin(image)
                draw.setPen(QtCore.Qt.blue)
                if self.path_map:
                    while p != anchor:
                        draw.drawPoint(p[1], p[0])
                        for q in self.lw._get_neighbors(p):
                            draw.drawPoint(q[1], q[0])
                        p = self.path_map[p]
                if self.path:
                    draw.setPen(QtCore.Qt.green)
                    for p in self.path:
                        draw.drawPoint(p[1], p[0])
                        for q in self.lw._get_neighbors(p):
                            draw.drawPoint(q[1], q[0])
                draw.end()

                try:
                    # Saving the image, checking for errors
                    saved = image.save(filepath[0])
                    if not saved:
                        raise Exception("Image save failed.")
                except Exception as e:
                    print(f"Error saving image: {e}")

            else:
                self.anchor = p

                if self.path_map:
                    while p != anchor:
                        p = self.path_map[p]
                        self.path.append(p)

                # Calculate path map
                if event.buttons() == QtCore.Qt.LeftButton:
                    Thread(target=self._cal_path_matrix).start()
                    Thread(target=self._update_path_map_progress).start()

                # Finish current task and reset
                elif event.buttons() == QtCore.Qt.RightButton:
                    self.path_map = {}
                    self.status_bar.showMessage(
                        'Left click to set the anchor point')
                    self.active = False

    def mouseMoveEvent(self, event):
        if self.active and event.buttons() == QtCore.Qt.NoButton:
            pos = event.pos()
            x, y = pos.x()-self.canvas.x(), pos.y()-self.canvas.y()

            if x < 0 or x >= self.w or y < 0 or y >= self.h:
                pass
            else:
                # Draw livewire
                p = y, x
                path = []
                while p != self.anchor:
                    p = self.path_map[p]
                    path.append(p)

                image = self.image.copy()
                draw = QtGui.QPainter()
                draw.begin(image)
                draw.setPen(QtCore.Qt.blue)
                for p in path:
                    draw.drawPoint(p[1], p[0])
                if self.path:
                    draw.setPen(QtCore.Qt.green)
                    for p in self.path:
                        draw.drawPoint(p[1], p[0])
                draw.end()
                self.canvas.setPixmap(image)

    def _cal_path_matrix(self):
        self.anchor_enabled = False
        self.active = False
        self.status_bar.showMessage(
            'Calculating path map from anchor point to other locations...')
        path_matrix = self.lw.get_path_matrix(self.anchor)
        self.status_bar.showMessage(
            r'Left click: new anchor / Right click: finish process/ Middle click: export image')
        self.anchor_enabled = True
        self.active = True

        self.path_map = path_matrix

    def _update_path_map_progress(self):
        while not self.anchor_enabled:
            time.sleep(0.1)
            message = 'Calculating path map... {:.1f}%'.format(
                self.lw.n_processed/self.lw.n_pixs*100.0)
            self.status_bar.showMessage(message)
        self.status_bar.showMessage(
            r'Left click: new anchor / Right click: finish process / Middle click: export image')
