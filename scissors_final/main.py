import sys
from PyQt5 import QtWidgets
from gui import ImageWin


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ImageWin()
    window.setMouseTracking(True)
    window.setWindowTitle('Livewire Demo')
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
