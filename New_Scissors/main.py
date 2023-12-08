import sys
from PyQt5 import QtWidgets
from gui import ImageWin

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ImageWin()
    window.setMouseTracking(True)
    window.setWindowTitle('Livewire Demo')
    # window.setFixedSize(window.size())
    # window.resize(800, 600) 
    window.show()
    # window.setFixedSize(window.size())
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
