import sys
from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QLabel
from qtconsole.qt import QtGui

from flixify.dataaccess.db_statements import movie_info
from flixify.dataaccess.db_statements import search_movie_by_title


class App(QMainWindow):
    movie_button_list = []

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # --- Window --- #
        self.setMinimumHeight(450)
        self.setMinimumWidth(450)
        self.title = "Flixify"
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 500

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # --- Movie info --- #
        self.selected_movie_title = QLabel("", self)
        title_font = QtGui.QFont()
        title_font.setBold(True)
        self.selected_movie_title.setFont(title_font)

        self.selected_movie_description = QLabel("", self)

        # --- Searching --- #
        self.textbox = QLineEdit(self)
        self.textbox.move(30, 30)
        self.textbox.resize(250, 20)

        self.button = QPushButton("Search", self)
        self.button.setToolTip("Search for a movie by it's title")
        self.button.move(300, 30)
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.find_movies(self.textbox.text())

    def find_movies(self, title):
        self.clear_movie_button_list()
        titles = search_movie_by_title(title)
        count = 0
        for title in titles:
            button = QPushButton(title[0], self)
            button.move(20, 30 * count + 100)
            button.clicked.connect(partial(self.select_movie, title[0]))
            self.movie_button_list.append(button)
            count += 1

        self.fit_window()

    def clear_movie_button_list(self):
        for button in self.movie_button_list:
            button.setParent(None)
        self.movie_button_list.clear()

    def select_movie(self, title):
        movie = movie_info(title)
        for data in movie:
            self.selected_movie_title.setText(data[1])
            self.selected_movie_description.setText(data[2])
            self.fit_window()

    def resizeEvent(self, *args, **kwargs):
        self.fit_window()

    def fit_window(self):
        self.width = QWidget.width(self)
        self.height = QWidget.height(self)

        # --- Movie info --- #
        # Movie title
        self.selected_movie_title.move(self.width / 2, 100)
        self.selected_movie_title.setMinimumWidth(self.width / 2 - 50)
        self.selected_movie_title.setMaximumWidth(self.width / 2 - 50)
        self.selected_movie_title.setWordWrap(True)
        self.selected_movie_title.adjustSize()
        self.selected_movie_title.show()

        # Movie description
        self.selected_movie_description.move(self.width / 2, 125)
        self.selected_movie_description.setMaximumWidth(self.width / 2 - 50)
        self.selected_movie_description.setMinimumWidth(self.width / 2 - 50)
        self.selected_movie_description.setWordWrap(True)
        self.selected_movie_description.adjustSize()
        self.selected_movie_description.show()

        # --- Movie buttons --- #
        for button in self.movie_button_list:
            button.setStyleSheet(
                "QPushButton {{ Padding-left: 10px; Text-align:left; background-color: pink; min-width:{0}px; min-height:28px }}".format(
                    self.width / 2 - 50))
            button.setMaximumWidth(self.width / 2 - 50)
            button.adjustSize()
            button.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
