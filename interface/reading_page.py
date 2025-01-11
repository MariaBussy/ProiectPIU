from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from target.target import update_goal_time_spent, save_reading_end
from controllers.epub_controller import get_epub_content
from controllers.bookmarks_controller import get_bookmark, insert_bookmark, get_bookmarks_for_book,update_last_bookmark_default_page

class BookReaderApp(QWidget):
    # Definirea semnalului pentru a semnala că utilizatorul a apăsat pe Home
    go_home_signal = pyqtSignal()

    def __init__(self, book):
        super().__init__()

        self.book = book
        self.setWindowTitle(book["nume"])
        self.setGeometry(100, 100, 1000, 970)

        # Simularea cărții cu texte împărțite în pagini
        content = get_epub_content(book["cale_fisier"])["content"]
        self.pages = paginate_content(content, 1500)

        # Obține ultimul bookmark pentru carte
        last_bookmark = get_bookmarks_for_book(book["id"])[-1] if get_bookmarks_for_book(book["id"]) else None
        self.current_page = last_bookmark["pagina_default"] if last_bookmark else 0

        self.bookmarks = []  # Lista pentru a salva marcajele

        # Crearea zonei de text pentru a arăta conținutul cărții
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

        # Crearea butoanelor (Pagina anterioară, Următoare, Acasă, Sfârșit, Marcaj)
        self.prev_button = QPushButton("Previous Page")
        self.next_button = QPushButton("Next Page")
        self.home_button = QPushButton("Home")
        self.end_button = QPushButton("End")
        self.bookmark_button = QPushButton("Bookmark")

        # Setarea stilului pentru butoane
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

        # Crearea combo box-ului pentru a afișa marcajele
        self.bookmark_combobox = QComboBox(self)
        self.bookmark_combobox.addItem("Select Bookmark")  # Placeholder
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

        # Conectarea butoanelor la funcții
        self.prev_button.clicked.connect(self.show_prev_page)
        self.next_button.clicked.connect(self.show_next_page)
        self.home_button.clicked.connect(self.go_home)
        self.end_button.clicked.connect(self.show_end)
        self.bookmark_button.clicked.connect(self.add_bookmark)

        # Layout-ul butoanelor
        left_button_layout = QVBoxLayout()
        left_button_layout.addWidget(self.prev_button)

        right_button_layout = QVBoxLayout()
        right_button_layout.addWidget(self.next_button)

        menu_button_layout = QVBoxLayout()
        menu_button_layout.addWidget(self.end_button)
        menu_button_layout.addWidget(self.home_button)
        menu_button_layout.addWidget(self.bookmark_button)
        menu_button_layout.addWidget(self.bookmark_combobox)

        # Layout-ul principal al ferestrei
        main_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(menu_button_layout)
        horizontal_layout.addLayout(left_button_layout)
        horizontal_layout.addWidget(self.text_area)
        horizontal_layout.addLayout(right_button_layout)
        horizontal_layout.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(horizontal_layout)

        # Adăugarea combo box-ului pentru marcaje
        bookmark_layout = QHBoxLayout()
        bookmark_layout.addWidget(self.bookmark_combobox)
        main_layout.addLayout(bookmark_layout)

        # Aplicarea stilului general
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
            self.bookmark_combobox.setCurrentIndex(0)  # Resetează combo box-ul

    def show_next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.text_area.setText(self.pages[self.current_page])
            self.bookmark_combobox.setCurrentIndex(0)  # Resetează combo box-ul

    def show_end(self):
        self.current_page = len(self.pages) - 1
        self.text_area.setText(self.pages[self.current_page])
        self.bookmark_combobox.setCurrentIndex(0)  # Resetează combo box-ul


    def load_existing_bookmarks(self):
        """Încărcați marcajele pentru cartea curentă din baza de date."""
        bookmarks = get_bookmarks_for_book(self.book["id"])  # ID-ul cărții
        if bookmarks:
            for bookmark in bookmarks:
                self.bookmarks.append(bookmark)
                self.bookmark_combobox.addItem(f"Page {bookmark['pagina_user']}")

    def add_bookmark(self):
        """Adaugă un marcaj în baza de date."""
        existing_bookmarks = get_bookmarks_for_book(self.book["id"])
        if any(b["pagina_user"] == self.current_page + 1 for b in existing_bookmarks):
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
        """Încarcă pagina selectată din marcaj."""
        selected_index = self.bookmark_combobox.currentIndex()
        if selected_index > 0:  # Primul element este placeholder
            bookmark = self.bookmarks[selected_index - 1]  # Index în lista bookmark-urilor
            self.current_page = bookmark["pagina_user"] - 1
            self.text_area.setText(self.pages[self.current_page])

    def go_home(self):
        """Adaugă un bookmark nou dacă nu există sau actualizează ultimul bookmark."""
        # Verifică dacă există un bookmark
        existing_bookmarks = get_bookmarks_for_book(self.book["id"])

        if not existing_bookmarks:
            # Dacă nu există niciun bookmark, adaugă unul nou
            new_bookmark = {
                "id_carte": self.book["id"],
                "pagina_default": self.current_page,
                "pagina_user": self.current_page + 1,
            }
            if insert_bookmark(new_bookmark):
                print(f"Created a new bookmark at page {self.current_page}")
        else:
            # Dacă există, actualizează `pagina_default` al ultimului bookmark
            update_last_bookmark_default_page(self.book["id"], self.current_page)
            print(f"Updated last bookmark to page {self.current_page}")

        # Salvează timpul de citire și actualizează ținta
        minutes_spent = save_reading_end()
        if minutes_spent is not None:
            update_goal_time_spent(minutes_spent)

        # Emiterea semnalului și închiderea ferestrei
        self.go_home_signal.emit()
        self.close()


def paginate_content(content: str, chars_per_page: int) -> list:
    """
    Paginates the content while preserving whitespace and alignment,
    but removes leading and trailing whitespace.

    Args:
        content (str): The text content to paginate.
        chars_per_page (int): The maximum number of characters per page.

    Returns:
        list: A list of strings, where each string represents a page.
    """
    if not content or chars_per_page <= 0:
        raise ValueError("Content must not be empty and chars_per_page must be greater than zero.")

    # Elimina spațiile albe de la începutul și sfârșitul conținutului
    content = content.strip()

    pages = []
    current_page = []
    current_char_count = 0

    for line in content.splitlines(keepends=True):
        if current_char_count + len(line) > chars_per_page:
            # Dacă linia curentă depășește limita paginii, se creează o nouă pagină
            pages.append("".join(current_page))
            current_page = []
            current_char_count = 0
        
        current_page.append(line)
        current_char_count += len(line)

    # Adăugăm ultima pagină dacă are conținut
    if current_page:
        pages.append("".join(current_page))

    return pages
