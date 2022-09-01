from PySide6 import QtCore, QtWidgets, QtGui

# Constants
APP_TITLE = "PydBook"  # Name of the application, on the titles of the windows, for example.


class MainUI(QtWidgets.QMainWindow):
    """This is the main UI, which is the one shown when the app is started, and whereof everything else is son"""

    def __init__(self):
        super().__init__()

        # UI Settings
        self.setWindowTitle(APP_TITLE)

        stylesheet_file = "./style/main.stylesheet"

        with open(stylesheet_file) as file:
            self.setStyleSheet(file.read())

        # UI Widgets

        self.text_editor = QtWidgets.QPlainTextEdit()
        self.setCentralWidget(self.text_editor)

        self.top_toolbar = QtWidgets.QToolBar()
        self.top_toolbar.setMovable(False)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.top_toolbar)

        self.bottom_toolBar = QtWidgets.QToolBar()
        self.top_toolbar.setMovable(False)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.bottom_toolBar)


class ErrorMessage(QtWidgets.QMessageBox):
    """This class is called when a critical error happens. After its button is clicked or it is closed, its parent
    is closed. Normally, the parent is MainUI, except for when an instance of MainUI is formed."""

    def __init__(self, parent=None, exception: Exception = None):
        super().__init__(parent=parent)

        # UI Settings

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle(APP_TITLE)

        error_icon = QtWidgets.QMessageBox.Critical
        self.setIcon(error_icon)

        error_text = "An exception was raised" + "\n" + (f"{exception.__str__()}" if exception else "")
        self.setText(error_text)

    def end_all(self):
        """Called to end all the application"""

        if self.parent():  # If there is a parent
            self.parent().close()
        else:
            self.close()

    def exec(self) -> None:
        """Executes normally, with the addition that, afterwards, it calls the 'end_all()' function."""

        super().exec()
        self.end_all()


def main():
    app = QtWidgets.QApplication([])

    try:
        ui = MainUI()
    except Exception as ex:
        error_box = ErrorMessage(exception=ex)
        error_box.exec()
    else:
        ui.resize(800, 600)
        ui.show()

    app.exec()


if __name__ == "__main__":
    main()
