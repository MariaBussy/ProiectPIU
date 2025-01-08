from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from target.target import update_goal_time_spent, save_reading_end
from controllers.epub_controller import get_epub_content

class BookReaderApp(QWidget):
    # Definirea semnalului pentru a semnala că utilizatorul a apăsat pe Home
    go_home_signal = pyqtSignal()

    def __init__(self, book):
        super().__init__()

        self.setWindowTitle("Minimal Book Reader")
        self.setGeometry(100, 100, 800, 600)

        # Simularea cărții cu texte împărțite în pagini
        content = get_epub_content(book["cale_fisier"])["content"]
        self.pages = split_content_by_word_count(content, 30)

        self.current_page = 0  # Începe de la prima pagină
        self.bookmarks = []  # Lista pentru a salva marcajele

        # Crearea zonei de text pentru a arăta conținutul cărții
        
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setText(self.pages[0])
        self.text_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Crearea butoanelor (Pagina anterioară, Următoare, Acasă, Sfârșit, Marcaj)
        self.prev_button = QPushButton("Previous Page")
        self.next_button = QPushButton("Next Page")
        self.home_button = QPushButton("Home")
        self.end_button = QPushButton("End")
        self.bookmark_button = QPushButton("Bookmark")

        # Crearea combo box-ului pentru a afișa marcajele
        self.bookmark_combobox = QComboBox(self)
        self.bookmark_combobox.addItem("Select Bookmark")  # Placeholder
        self.bookmark_combobox.currentIndexChanged.connect(self.load_bookmark)

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

        self.setLayout(main_layout)
    

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.text_area.setText(self.pages[self.current_page])

    def show_next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.text_area.setText(self.pages[self.current_page])

    def show_end(self):
        self.current_page = len(self.pages) - 1
        self.text_area.setText(self.pages[self.current_page])

    def add_bookmark(self):
        bookmark_name = f"Bookmark {self.current_page + 1}"
        if bookmark_name not in self.bookmarks:
            self.bookmarks.append(bookmark_name)
            self.bookmark_combobox.addItem(bookmark_name)
        print(f"Bookmark added at Page {self.current_page + 1}")

    def load_bookmark(self):
        selected_index = self.bookmark_combobox.currentIndex()
        if selected_index > 0:
            selected_page = selected_index - 1
            self.current_page = selected_page
            self.text_area.setText(self.pages[self.current_page])

    def go_home(self):
        """Salvează timpul de sfârșit, actualizează target-ul și emite semnalul."""
        minutes_spent = save_reading_end()
        if minutes_spent is not None:
            update_goal_time_spent(minutes_spent)
        self.go_home_signal.emit()
        self.close()  # Închide fereastra de citire
    
def split_content_by_word_count(content, words_per_page):
    # Împărțim conținutul în cuvinte
    words = content.split('\n')
    # Grupăm cuvintele în pagini
    pages = [' '.join(words[i:i + words_per_page]) for i in range(0, len(words), words_per_page)]
    return pages
        
