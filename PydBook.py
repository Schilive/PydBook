from PySide6 import QtCore, QtWidgets, QtGui
import math  # Only for floor function
import locale  # For knowing the user's language
import string_changes  # For undoing-redoing actions on the PydEditor


def get_language() -> str:
    """Gets the language to be used. If the user's language is supported, their language code (e.g. "en") is returned,
    otherwise the standard language is returned."""

    supported_languages: set[str] = {"en", "pt"}
    standard_lang: str = "en"

    lang_local: str = locale.getdefaultlocale()[0]  # If the user is in Spain and using English, = en_ES
    lang: str = lang_local.split("_")[0]

    if lang in supported_languages:
        return lang
    else:
        return standard_lang


# Constants
APP_TITLE = "PydBook"  # Name of the application, on the titles of the windows, for example.
LANGUAGE = get_language()


class PydEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.textChanged.connect(self.text_changed)

        self.changes_list = string_changes.ChangesList()  # Ordered list of text-modifying actions
        self.lastText: str = ""  # Temporary variable of the written text after 'text_changed' event finishes
        self.undo_redoing: bool = False  # If the editor is changing the text for a undo-redoing action

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.matches(QtGui.QKeySequence.Undo):
            self.undo()
            return
        elif e.matches(QtGui.QKeySequence.Redo):
            self.redo()
            return

        super().keyPressEvent(e)

    def text_changed(self) -> None:
        if not self.undo_redoing:
            self.changes_list.add_changes(string_changes.get_changes(self.lastText, self.toPlainText()))
        self.lastText = self.toPlainText()

    def undo(self) -> None:
        self.undo_redoing = True

        self.setPlainText(string_changes.remake_str(self.toPlainText(), self.changes_list.get_last_change()))
        self.changes_list.rollback_changes()

        self.undo_redoing = False

    def redo(self) -> None:
        self.undo_redoing = True

        self.setPlainText(string_changes.change_str(self.toPlainText(), self.changes_list.get_next_change()))
        self.changes_list.roll_forward_changes()

        self.undo_redoing = False


class MainUI(QtWidgets.QMainWindow):
    """This is the main UI, which is the one shown when the app is started, and whereof everything else is son."""

    def texts(self):
        """It is generator, containing the texts on the right langauge. This generator is used for naming in the
        __init__ function. It is a generator to save memory."""

        src = f"lang/{LANGUAGE}.txt"

        with open(file=src, mode="r", encoding="utf-8") as file:
            while True:
                text = file.readline()

                if text == "" or text == "\n":
                    break

                yield text[:-1]  # The last character is "\n"

    def __init__(self):
        super().__init__()

        # Application Variables
        self.stylesheet_file = "./style/main.stylesheet"

        self.standard_title = ""  # Standard title, before the text is associated with a file

        self.isSaveFile: bool = False  # Whether there is a saving file
        self.save_file: str = ""

        self.saved: bool = True  # Whether the current text has been saved, or whether it is blank.
        self.saved_text: str = ""  # This is a bad solution, better would be to save the changes done

        self.standard_font_size = 11  # The zoom is done by changing the font size
        self.current_zoom = 100
        self.zoom_percentage_change = 10
        self.maximum_zoom = 500
        self.minimum_zoom = 10

        # Temporary Variable

        # It contains the texts on the right language, which will be used here for naming
        texts = self.texts()
        self.standard_title = next(texts)

        # UI Settings
        self.setWindowTitle(f"{self.standard_title} — {APP_TITLE}")

        self.update_style()

        # UI Widgets

        self.text_editor = PydEditor()
        self.text_editor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.text_editor.textChanged.connect(self.text_changed)
        self.setCentralWidget(self.text_editor)

        # Menu Bar

        self.menuBar_file = self.menuBar().addMenu(next(texts))
        self.menuBar_file.setWindowFlags(self.menuBar_file.windowFlags() | QtCore.Qt.NoDropShadowWindowHint)

        self.open_action = QtGui.QAction(next(texts))
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open)
        self.menuBar_file.addAction(self.open_action)

        self.menuBar_file.addSeparator()

        self.save_action = QtGui.QAction(next(texts))
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.user_save)
        self.menuBar_file.addAction(self.save_action)

        self.save_as_action = QtGui.QAction(next(texts))
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self.save_as)
        self.menuBar_file.addAction(self.save_as_action)

        self.menuBar_file.addSeparator()

        self.exit_action = QtGui.QAction(next(texts))
        self.exit_action.setShortcut("Ctrl+E")
        self.exit_action.triggered.connect(self.close)
        self.menuBar_file.addAction(self.exit_action)

        self.menuBar_edit = self.menuBar().addMenu(next(texts))
        self.menuBar_edit.setWindowFlags(self.menuBar_edit.windowFlags() | QtCore.Qt.NoDropShadowWindowHint)

        self.undo_action = QtGui.QAction(next(texts))
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self.text_editor.undo)
        self.menuBar_edit.addAction(self.undo_action)

        self.redo_action = QtGui.QAction(next(texts))
        self.redo_action.setShortcut("Ctrl+Z")
        self.redo_action.triggered.connect(self.text_editor.redo)
        self.menuBar_edit.addAction(self.redo_action)

        self.menuBar_view = self.menuBar().addMenu(next(texts))
        self.menuBar_file.setWindowFlags(self.menuBar_file.windowFlags() | QtCore.Qt.NoDropShadowWindowHint)

        self.zoomIn_action = QtGui.QAction(next(texts))
        self.zoomIn_action.setShortcut("Ctrl++")
        self.zoomIn_action.triggered.connect(self.zoom_in)
        self.menuBar_view.addAction(self.zoomIn_action)

        self.zoomOut_action = QtGui.QAction(next(texts))
        self.zoomOut_action.setShortcut("Ctrl+-")
        self.zoomOut_action.triggered.connect(self.zoom_out)
        self.menuBar_view.addAction(self.zoomOut_action)

        self.menuBar_view.addSeparator()

        self.noZoom_action = QtGui.QAction(next(texts))
        self.noZoom_action.triggered.connect(self.no_zoom)
        self.menuBar_view.addAction(self.noZoom_action)

        # Status Bar

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)

        self.label_zoom = QtWidgets.QLabel()
        self.label_zoom.setText(f"{self.current_zoom}%")

        self.statusBar.addPermanentWidget(self.label_zoom)

    def update_style(self):
        with open(file=self.stylesheet_file, mode="r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        event.ignore()

        if not self.saved:

            match LANGUAGE:
                case "en":
                    second_text = " Before opening a file."
                case "pt":
                    second_text = " Antes de abrir o arquivo."

            user_will = self.ask_if_wants_to_save(second_text)

            if user_will == 0 or user_will == QtWidgets.QMessageBox.Cancel:  # Canceled
                return
            elif user_will == QtWidgets.QMessageBox.No:  # Not save
                event.accept()
            elif user_will == QtWidgets.QMessageBox.Yes:  # Wants to save
                self.user_save()
                event.accept()
        else:
            event.accept()

    def text_changed(self):
        """Called when the text, of 'self.text_editor', changes."""

        if self.text_editor.toPlainText() != self.saved_text:
            self.saved = False

            if self.isSaveFile:
                file_name = self.save_file.split("/")[-1]
                self.setWindowTitle(f"{file_name}* — {APP_TITLE}")
            else:
                self.setWindowTitle(f"{self.standard_title}* — {APP_TITLE}")
        else:
            self.saved = True

            if self.isSaveFile:
                file_name = self.save_file.split("/")[-1]
                self.setWindowTitle(f"{file_name} — {APP_TITLE}")
            else:
                self.setWindowTitle(f"{self.standard_title} — {APP_TITLE}")

    def set_saving_file(self, file_src: str):
        """Called when saved or a file is opened. It updates whether the application has a file it can save to."""

        self.isSaveFile = True
        self.save_file = file_src
        self.saved_text = self.text_editor.toPlainText()
        self.saved = True

        file_name = file_src.split("/")[-1]
        self.setWindowTitle(f"{file_name} — {APP_TITLE}")

    def ask_if_wants_to_save(self, second_text: str = "") -> int:
        """This is called for the user to decide whether they want to save the file, before some other action;
        for example, opening a file. The variable 'second_text' adds a text to enlight the user. Returns the pressed
        button (Yes, No, Cancel), and 0 if unsuccessful."""

        # Building the Asking Box

        asking_box = QtWidgets.QMessageBox(self)
        asking_box.setWindowModality(QtCore.Qt.WindowModal)
        asking_box.setWindowTitle(APP_TITLE)

        warning_icon = QtWidgets.QMessageBox.Warning
        asking_box.setIcon(warning_icon)

        cancel_button = QtWidgets.QMessageBox.Cancel
        not_save_button = QtWidgets.QMessageBox.No
        save_button = QtWidgets.QMessageBox.Yes
        asking_box.setStandardButtons(cancel_button | not_save_button | save_button)

        asking_text: str
        match LANGUAGE:
            case "en":
                asking_box.button(cancel_button).setText("Cancel")
                asking_box.button(not_save_button).setText("No")
                asking_box.button(save_button).setText("Yes")

                if self.isSaveFile:
                    save_file_name = self.save_file.split("/")[-1]
                    asking_text = f"Would you like to save {save_file_name}?"
                else:
                    asking_text = "Would you like to save this text?"
            case "pt":
                asking_box.button(cancel_button).setText("Cancelar")
                asking_box.button(not_save_button).setText("Não")
                asking_box.button(save_button).setText("Sim")

                if self.isSaveFile:
                    save_file_name = self.save_file.split("/")[-1]
                    asking_text = f"Você gostaria de salvar {save_file_name}?"
                else:
                    asking_text = "Você gostaria de salvar este texto?"

        asking_text += second_text
        asking_box.setText(asking_text)

        # Asking and Interpreting

        pressed_button = asking_box.exec()  # Returns 0 if unsuccessful
        return pressed_button

    def save_warn_if_needed(second_texts: dict[str, str] = ""):
        """This is a decorator with the attribute 'second_text'. If the text has not been saved, tt asks if the user
        wants to save the file before an action, which is the function the decorator wraps.

        The attribute is a dictionary with the languge code (e.g. "EN") pointing to the message on the appropriate
        language; the message is directly concatenated to the asker box. If the user refuses, the action will continue
        normally; if the user accepts, they will be asked to save the file and, then, the action will continue
        normally; if they somehow cancel, nothing shall happen."""

        def decorator(func):
            def wrapper(self, *args, **kwargs):
                if not self.saved:
                    user_will = self.ask_if_wants_to_save(second_texts[LANGUAGE])

                    if user_will == 0 or user_will == QtWidgets.QMessageBox.Cancel:  # Canceled
                        return
                    elif user_will == QtWidgets.QMessageBox.No:  # Not save
                        func(self, *args, **kwargs)
                    elif user_will == QtWidgets.QMessageBox.Yes:  # Wants to save
                        self.user_save()
                        func(self, *args, **kwargs)
                else:
                    func(self, *args, **kwargs)
            return wrapper
        return decorator

    @save_warn_if_needed({"en": " Before opening a file.",
                          "pt": " Antes de abrir o arquivo."})
    def open(self):
        """Called for the user to open a file, altering the text to the text in the selected file, using UTF-8."""

        # File Selection

        file_selector = QtWidgets.QFileDialog(self)
        file_selector.setFileMode(QtWidgets.QFileDialog.ExistingFile)  # Only one file is to be selected

        match LANGUAGE:
            case "en":
                file_selector.setLabelText(file_selector.Accept, "Open")
                file_selector.setLabelText(file_selector.Reject, "Close")
                file_selector.setLabelText(file_selector.FileName, "Name:")
                file_selector.setLabelText(file_selector.LookIn, "Look in:")
                file_selector.setLabelText(file_selector.FileType, "Type:")
                file_selector.setWindowTitle("Open a File")
                text_filter: str = "Text File (*.txt)"
                any_file_filter: str = "Any File (*)"
            case "pt":
                file_selector.setLabelText(file_selector.Accept, "Abrir")
                file_selector.setLabelText(file_selector.Reject, "Fechar")
                file_selector.setLabelText(file_selector.FileName, "Nome:")
                file_selector.setLabelText(file_selector.LookIn, "Em:")
                file_selector.setLabelText(file_selector.FileType, "Tipo:")
                file_selector.setWindowTitle("Abrir um Arquivo")
                text_filter: str = "Documento de Texto (*.txt)"
                any_file_filter: str = "Todos os Arquivos (*)"

        file_selector.setNameFilter(f"{text_filter};;{any_file_filter}")  # Filters are separated by ;;

        result = file_selector.exec()  # Returns 1 if file was selected, 0 otherwise; for example, 'cancel' is pressed

        # Interpretation of the File Selection

        if result == 0:
            return

        file_selected: str = file_selector.selectedFiles()[0]  # As only one file can be selected

        try:
            file = open(file_selected, "r", encoding="utf-8")
            text = file.read()
        except Exception:
            match LANGUAGE:
                case "en":
                    warning_message = f"{APP_TITLE} could not open the file: {file_selected}."
                case "pt":
                    warning_message = f"{APP_TITLE} não pôde abriro o arquivo: {file_selected}."

            warning_box = WarningMessage(self, text=warning_message)
            warning_box.exec()
            return
        else:
            file.close()
            self.text_editor.setPlainText(text)

            self.set_saving_file(file_selected)

    def user_save(self):
        """Called when the users want to 'save' the text."""

        if not self.isSaveFile:
            self.save_as()
        else:
            self.save(self.save_file)

    def save_as(self):
        """Called when the user presses 'save as' button. It asks the user to select a file, where the text shall be
        saved, using UTF-8."""

        # File Selector Widget

        file_selector = QtWidgets.QFileDialog(self)
        file_selector.setFileMode(QtWidgets.QFileDialog.AnyFile)  # Only one file is to be selected, existing or not

        match LANGUAGE:
            case "en":
                file_selector.setLabelText(file_selector.Accept, "Save")
                file_selector.setLabelText(file_selector.Reject, "Close")
                file_selector.setLabelText(file_selector.FileName, "Name:")
                file_selector.setLabelText(file_selector.LookIn, "Look in:")
                file_selector.setLabelText(file_selector.FileType, "Type:")
                file_selector.setWindowTitle("Save As")
                text_filter: str = "Text File (*.txt)"
                any_file_filter: str = "Any File (*)"
            case "pt":
                file_selector.setLabelText(file_selector.Accept, "Salvar")
                file_selector.setLabelText(file_selector.Reject, "Fechar")
                file_selector.setLabelText(file_selector.FileName, "Nome:")
                file_selector.setLabelText(file_selector.LookIn, "Em")
                file_selector.setLabelText(file_selector.FileType, "Tipo:")
                file_selector.setWindowTitle("Salvar Como")
                text_filter: str = "Documento de Texto (*.txt)"
                any_file_filter: str = "Todos os Arquivos (*)"

        file_selector.setNameFilter(f"{text_filter};;{any_file_filter}")  # Filter are separated by ;;
        file_selector.setViewMode(QtWidgets.QFileDialog.List)

        # File Selection

        result = file_selector.exec()  # Returns 1 if file was selected, 0 otherwise; for example, 'cancel' is pressed

        if result == 0:
            return

        files_selected: list[str] = file_selector.selectedFiles()
        filter_selected: str = file_selector.selectedNameFilter()
        file_src: str = files_selected[0]  # As only one file can be selected

        if filter_selected == text_filter:
            file_name = file_src.split("/")[-1]

            if file_name.endswith(".txt"):
                saving_file = file_src
            else:
                saving_file = file_src + ".txt"
        else:  # filter_selected == any_file_filter:
            saving_file = file_src

        self.save(saving_file)

    def save(self, file_src):
        """It saves the text in the file 'file_src'."""

        try:
            file = open(file_src, "w", encoding="utf-8")
            text = self.text_editor.toPlainText()
            file.write(text)
        except Exception:
            match LANGUAGE:
                case "en":
                    warning_text = f"{APP_TITLE} could not save the text at {file_src}."
                case "pt":
                    warning_text = f"{APP_TITLE} não pôde salvar o texto em {file_src}."

            warning_box = WarningMessage(self, text=warning_text)
            warning_box.exec()
        else:
            file.close()
            self.set_saving_file(file_src)

    def update_zoom(self):
        """If the variable of how much to zoom has been altered, this function is called. It alters the text size."""

        zoom_point = math.floor(self.current_zoom / 100 * self.standard_font_size)
        self.text_editor.setStyleSheet(f"QPlainTextEdit {{font-size: {zoom_point}pt;}}")

        self.label_zoom.setText(f"{self.current_zoom}%")

    def zoom_in(self):
        """Zooms in on the text."""

        self.current_zoom = min(self.current_zoom + self.zoom_percentage_change, self.maximum_zoom)

        self.update_zoom()

    def zoom_out(self):
        """Zooms out on the text."""

        self.current_zoom = max(self.current_zoom - self.zoom_percentage_change, self.minimum_zoom)

        self.update_zoom()

    def no_zoom(self):
        """Alters the zoom to none, or to standard size."""

        self.current_zoom = 100
        self.update_zoom()


class WarningMessage(QtWidgets.QMessageBox):
    """This class is called when a warning is needed. As contrast with the ErrorMessage class, this message box
    do not intend to close the program: it is mostly to warn the user. It is only called inside the MainUI class."""

    def __init__(self, parent=None, text=""):
        super().__init__(parent=parent)

        # UI Settings

        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle(APP_TITLE)

        warning_icon = QtWidgets.QMessageBox.Warning
        self.setIcon(warning_icon)

        warning_text = text
        self.setText(warning_text)


class ErrorMessage(QtWidgets.QMessageBox):
    """This class is called when a critical error happens. After its button is clicked, or it is closed, its parent
    is closed. Normally, the parent is MainUI, except for when an instance of MainUI is being formed."""

    def __init__(self, parent=None, exception: Exception = None):
        super().__init__(parent=parent)

        # UI Settings

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle(APP_TITLE)

        error_icon = QtWidgets.QMessageBox.Critical
        self.setIcon(error_icon)

        match LANGUAGE:
            case "en":
                error_text = "An exception was raised" + (f"\n{exception.__str__()}." if exception else "")
            case "pt":
                error_text = "Uma exceção foi gerada" + (f"\n{exception.__str__()}." if exception else "")

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
        raise ex
    else:
        ui.resize(800, 600)
        ui.show()

    app.exec()


if __name__ == "__main__":
    main()
