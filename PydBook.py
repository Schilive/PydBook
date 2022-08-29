from PySide6 import QtCore, QtWidgets, QtGui


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PydBook")

        self.initUI()


    def initUI(self):
        with open("./style/main.stylesheet") as file:
            self.setStyleSheet(file.read())

        self.textEditor = QtWidgets.QPlainTextEdit()
        self.setCentralWidget(self.textEditor)

        self.top_toolBar = QtWidgets.QToolBar()
        self.top_toolBar.setMovable(False)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.top_toolBar)

        self.bottom_toolBar = QtWidgets.QToolBar()
        self.top_toolBar.setMovable(False)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.bottom_toolBar)


def main():
    app = QtWidgets.QApplication([])

    ui = MainUI()
    ui.resize(800, 600)
    ui.show()

    app.exec()


if __name__ == "__main__":
    main()


