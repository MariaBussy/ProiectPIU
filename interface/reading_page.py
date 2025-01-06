import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QSizePolicy, QComboBox
from PyQt5.QtCore import Qt

class BookReaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minimal Book Reader")
        self.setGeometry(100, 100, 800, 600)

        # Simulate a book with text split into pages (for demo purposes)
        self.pages = [
            "Page 1: Once upon a time, there was a small book...",
            "Page 2: It started with a story of adventure...",
            "Page 3: The journey continued through the lands...",
            "Page 4: Finally, the story concluded with a moral lesson."
        ]

        self.current_page = 0  # Start at the first page
        self.bookmarks = []  # List to store saved bookmarks

        # Create the text area for displaying book content
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setText(self.pages[self.current_page])
        # Set the text area to have flexible size policy
        self.text_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create the buttons (Previous, Next, Home, End, Bookmark)
        self.prev_button = QPushButton("Previous Page")
        self.next_button = QPushButton("Next Page")
        self.home_button = QPushButton("Home")
        self.end_button = QPushButton("End")
        self.bookmark_button = QPushButton("Bookmark")

        # Create the combo box to display bookmarks
        self.bookmark_combobox = QComboBox(self)
        self.bookmark_combobox.addItem("Select Bookmark")  # Default placeholder
        self.bookmark_combobox.currentIndexChanged.connect(self.load_bookmark)

        # Connect buttons to functions
        self.prev_button.clicked.connect(self.show_prev_page)
        self.next_button.clicked.connect(self.show_next_page)
        self.home_button.clicked.connect(self.show_home)
        self.end_button.clicked.connect(self.show_end)
        self.bookmark_button.clicked.connect(self.add_bookmark)

        # Layout for the buttons on the left (Previous and Home)
        left_button_layout = QVBoxLayout()
        left_button_layout.addWidget(self.prev_button)

        right_button_layout = QVBoxLayout()
        right_button_layout.addWidget(self.next_button)

        # Layout for the buttons on the right (Bookmark, End, and Next)
        menu_button_layout = QVBoxLayout()
        menu_button_layout.addWidget(self.end_button)
        menu_button_layout.addWidget(self.home_button)
        menu_button_layout.addWidget(self.bookmark_button)

        # Main layout for the window
        main_layout = QVBoxLayout()

        # Create a horizontal layout for centering the text area horizontally
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(menu_button_layout)
        horizontal_layout.addLayout(left_button_layout)  # Add left buttons
        horizontal_layout.addWidget(self.text_area)     # Add the text area in the middle
        horizontal_layout.addLayout(right_button_layout)  # Add right buttons
        horizontal_layout.setAlignment(Qt.AlignCenter)  # Center the content horizontally

        # Add the horizontal layout to the main layout
        main_layout.addLayout(horizontal_layout)

        # Add the combo box for bookmarks at the bottom
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

    def show_home(self):
        self.current_page = 0
        self.text_area.setText(self.pages[self.current_page])

    def show_end(self):
        self.current_page = len(self.pages) - 1
        self.text_area.setText(self.pages[self.current_page])

    def add_bookmark(self):
        # Save the current page as a bookmark
        bookmark_name = f"Bookmark {self.current_page + 1}"
        if bookmark_name not in self.bookmarks:
            self.bookmarks.append(bookmark_name)
            self.bookmark_combobox.addItem(bookmark_name)  # Add to the combo box
        print(f"Bookmark added at Page {self.current_page + 1}")

    def load_bookmark(self):
        # Load the page corresponding to the selected bookmark
        selected_index = self.bookmark_combobox.currentIndex()
        if selected_index > 0:  # Skip the "Select Bookmark" option
            selected_page = selected_index - 1  # Since the first item is a placeholder
            self.current_page = selected_page
            self.text_area.setText(self.pages[self.current_page])


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookReaderApp()
    window.show()
    sys.exit(app.exec_())
