from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from target.target import update_goal_time_spent, save_reading_end
from controllers.epub_controller import get_epub_content
from controllers.bookmarks_controller import get_bookmark, get_last_page_bookmark, insert_bookmark, get_bookmarks_for_book,update_last_bookmark_default_page

class BookReaderApp(QWidget):
    go_home_signal = pyqtSignal()

    def __init__(self, book):
        super().__init__()

        self.book = book
        self.setWindowTitle(book["nume"])
        self.setGeometry(100, 100, 1000, 970)

        content = get_epub_content(book["cale_fisier"])["content"]
        self.pages = paginate_content(content, 1500)

        last_bookmark=get_last_page_bookmark(self.book["id"]) if get_last_page_bookmark(self.book["id"]) else None
        self.current_page = last_bookmark["pagina_default"] if last_bookmark else 0

        existing_bookmarks = get_bookmarks_for_book(self.book["id"])
        if not existing_bookmarks:
            insert_bookmark({
                    "id_carte": self.book["id"],
                    "pagina_default": self.current_page,
                    "pagina_user": self.current_page + 1,
                })

        self.bookmarks = []

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setText(self.pages[self.current_page])
        self.text_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                font-family: 'Georgia';
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

        self.prev_button = QPushButton("Previous Page")
        self.next_button = QPushButton("Next Page")
        self.home_button = QPushButton("Home")
        self.end_button = QPushButton("End")
        self.bookmark_button = QPushButton("Bookmark")

        button_style = """
            QPushButton {
                font-size: 14px;
                padding: 10px;
                background-color: #6c757d;
                color: #ffffff;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """

        button_vertical_style = """ 
            QPushButton {
                font-size: 14px; padding: 8px;
                background-color: #007bff; color: #fff;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }"""

        for button in [self.prev_button, self.next_button]:
            button.setStyleSheet(button_style)
        for button in [self.home_button, self.end_button, self.bookmark_button]:
            button.setStyleSheet(button_vertical_style)

        self.bookmark_combobox = QComboBox(self)
        self.bookmark_combobox.addItem("Select Bookmark")
        self.bookmark_combobox.currentIndexChanged.connect(self.load_bookmark)
        self.bookmark_combobox.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                background-color: #007bff; color: #fff;
                border: 1px solid #6c757d;
                border-radius: 5px;
            }
        """)

        self.prev_button.clicked.connect(self.show_prev_page)
        self.next_button.clicked.connect(self.show_next_page)
        self.home_button.clicked.connect(self.go_home)
        self.end_button.clicked.connect(self.show_end)
        self.bookmark_button.clicked.connect(self.add_bookmark)

        left_button_layout = QVBoxLayout()
        left_button_layout.addWidget(self.prev_button)

        right_button_layout = QVBoxLayout()
        right_button_layout.addWidget(self.next_button)

        menu_button_layout = QVBoxLayout()
        menu_button_layout.addWidget(self.end_button)
        menu_button_layout.addWidget(self.home_button)
        menu_button_layout.addWidget(self.bookmark_button)
        menu_button_layout.addWidget(self.bookmark_combobox)

        main_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(menu_button_layout)
        horizontal_layout.addLayout(left_button_layout)
        horizontal_layout.addWidget(self.text_area)
        horizontal_layout.addLayout(right_button_layout)
        horizontal_layout.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(horizontal_layout)

        bookmark_layout = QHBoxLayout()
        bookmark_layout.addWidget(self.bookmark_combobox)
        main_layout.addLayout(bookmark_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #212529;
                color: #ffffff;
            }
            QLabel {
                font-family: 'Arial';
                font-size: 14px;
            }
        """)

        self.setLayout(main_layout)
        self.load_existing_bookmarks()


    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.text_area.setText(self.pages[self.current_page])
            self.bookmark_combobox.setCurrentIndex(0)

    def show_next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.text_area.setText(self.pages[self.current_page])
            self.bookmark_combobox.setCurrentIndex(0)

    def show_end(self):
        self.current_page = len(self.pages) - 1
        self.text_area.setText(self.pages[self.current_page])
        self.bookmark_combobox.setCurrentIndex(0)


    def load_existing_bookmarks(self):
        bookmarks = get_bookmarks_for_book(self.book["id"])
        if bookmarks:
            self.bookmarks.append(bookmarks[0])
            self.bookmark_combobox.addItem("Last read page")
            for bookmark in bookmarks[1:]:
                self.bookmarks.append(bookmark)
                self.bookmark_combobox.addItem(f"Page {bookmark['pagina_user']}")

    def add_bookmark(self):
        existing_bookmarks = get_bookmarks_for_book(self.book["id"])
        if any(b["pagina_user"] == self.current_page + 1 for b in existing_bookmarks[1:]):
            print(f"Page {self.current_page + 1} is already bookmarked.")
            return  # Nu adaugă un bookmark duplicat

        bookmark_data = {
            "id_carte": self.book["id"],
            "pagina_default": 0,
            "pagina_user": self.current_page + 1,
        }
        result = insert_bookmark(bookmark_data)
        if result:
            self.bookmarks.append(result)
            self.bookmark_combobox.addItem(f"Page {result['pagina_user']}")
            print(f"Bookmark added at Page {self.current_page + 1}")
        else:
            print("Failed to add bookmark.")

    def load_bookmark(self):
        selected_index = self.bookmark_combobox.currentIndex()
        if selected_index > 0:
            bookmark = self.bookmarks[selected_index - 1]
            self.current_page = bookmark["pagina_user"] - 1
            self.text_area.setText(self.pages[self.current_page])

    def go_home(self):
        existing_bookmarks = get_bookmarks_for_book(self.book["id"])

        update_last_bookmark_default_page(self.book["id"], self.current_page)
        print(f"Updated last bookmark to page {self.current_page}")

        minutes_spent = save_reading_end()
        if minutes_spent is not None:
            update_goal_time_spent(minutes_spent)

        self.go_home_signal.emit()
        self.close()


def paginate_content(content: str, chars_per_page: int) -> list:
    if not content or chars_per_page <= 0:
        raise ValueError("Content must not be empty and chars_per_page must be greater than zero.")

    content = content.strip()

    pages = []
    current_page = []
    current_char_count = 0

    for line in content.splitlines(keepends=True):
        if current_char_count + len(line) > chars_per_page:
            pages.append("".join(current_page))
            current_page = []
            current_char_count = 0
        
        current_page.append(line)
        current_char_count += len(line)

    if current_page:
        pages.append("".join(current_page))

    return pages
