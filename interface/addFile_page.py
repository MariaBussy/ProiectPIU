from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from controllers.books_controller import insert_book
from controllers.authors_controller import insert_author, get_author_by_name
from controllers.epub_controller import process_epub
from controllers.authors_controller import insert_book_author
from PyQt5.QtCore import Qt,pyqtSignal
import os
import shutil

class AddFileWindow(QDialog):
    files_added = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Files")
        self.setGeometry(300, 300, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        title_label = QLabel("Add Files to Library")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title_label)

        # Buttons Layout
        buttons_layout = QHBoxLayout()

        # Add EPUB button and label
        epub_layout = QVBoxLayout()
        self.add_epub_button = QPushButton("Select EPUB")
        self.add_epub_button.setStyleSheet(self.get_button_style())
        self.add_epub_button.clicked.connect(self.select_epub_file)
        epub_layout.addWidget(self.add_epub_button)

        self.epub_label = QLabel("No EPUB selected")
        self.epub_label.setAlignment(Qt.AlignCenter)
        self.epub_label.setStyleSheet("font-size: 12px; color: #555;")
        epub_layout.addWidget(self.epub_label)

        buttons_layout.addLayout(epub_layout)

        # Add Photo button and label
        photo_layout = QVBoxLayout()
        self.add_photos_button = QPushButton("Select Photo")
        self.add_photos_button.setStyleSheet(self.get_button_style())
        self.add_photos_button.clicked.connect(self.select_photo_file)
        photo_layout.addWidget(self.add_photos_button)

        self.photo_label = QLabel("No Photo selected")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("font-size: 12px; color: #555;")
        photo_layout.addWidget(self.photo_label)

        buttons_layout.addLayout(photo_layout)

        self.layout.addLayout(buttons_layout)

        # ADD button
        self.add_button = QPushButton("ADD")
        self.add_button.setStyleSheet(self.get_add_button_style())
        self.add_button.clicked.connect(self.add_files_to_folders)
        self.add_button.clicked.connect(self.add_file)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        # File paths
        self.selected_epub = None
        self.selected_photo = None

    def select_epub_file(self):
        """Select a single EPUB file."""
        file, _ = QFileDialog.getOpenFileName(self, "Select EPUB File", "", "EPUB Files (*.epub)")
        if file:
            self.selected_epub = file
            self.epub_label.setText(f"Selected: {os.path.basename(file)}")

    def select_photo_file(self):
        """Select a single image file."""
        file, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file:
            self.selected_photo = file
            self.photo_label.setText(f"Selected: {os.path.basename(file)}")

    def add_files_to_folders(self):
        """Add selected files to their respective folders."""
        if self.selected_epub:
            shutil.copy(self.selected_epub, os.path.join("books", os.path.basename(self.selected_epub)))
        if self.selected_photo:
            shutil.copy(self.selected_photo, os.path.join("Photos", os.path.basename(self.selected_photo)))

    def get_button_style(self):
        """Return the style for the buttons."""
        return """
        QPushButton {
            font-size: 14px;
            padding: 8px 16px;
            background-color: #e0e0e0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #d6d6d6;
        }
        QPushButton:pressed {
            background-color: #c8c8c8;
        }
        """

    def get_add_button_style(self):
        """Return the style for the ADD button."""
        return """
        QPushButton {
            font-size: 16px;
            padding: 10px 20px;
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3e8e41;
        }
        """
    def add_file(self):   
        try:
            book_data, author_data = process_epub(self.selected_epub)

            # Verificăm dacă autorul există deja, altfel îl adăugăm
            author = get_author_by_name(author_data["nume"])
            if not author:
                author = insert_author(author_data)

            # Verificăm dacă a fost selectată o poză și o copiem în folderul Photos
            if self.selected_photo:
                photo_filename = os.path.basename(self.selected_photo)
                photo_path = os.path.join("Photos", photo_filename)
                shutil.copy(self.selected_photo, photo_path)  # Copiem fișierul în directorul Photos
                book_data["cale_poza"] = photo_path  # Salvăm calea relativă în baza de date
            else:
                photo_filename = os.path.basename("default.png")
                photo_path = os.path.join("Photos", photo_filename)
                book_data["cale_poza"] = photo_path  # Dacă nu există poză, folosim default.jpg

            # Copiem fișierul EPUB în directorul Books și salvăm calea relativă în baza de date
            epub_filename = os.path.basename(self.selected_epub)
            epub_path = os.path.join("Books", epub_filename)
            shutil.copy(self.selected_epub, epub_path)  # Copiem fișierul EPUB în folderul Books
            book_data["cale_fisier"] = epub_path  # Salvăm calea relativă în baza de date

            # Adăugăm cartea
            inserted_book = insert_book(book_data)
            if inserted_book:
                # Creăm relația între carte și autor
                insert_book_author(inserted_book['id'], author['id'])

            try:
                # Codul pentru procesarea fișierului și adăugarea cărții
                # După ce adaugi cartea, emiți semnalul
                self.files_added.emit()

            except Exception as e:
                print(f"Eroare: {str(e)}") 

        except Exception as e:
            print(f"Eroare: {str(e)}") 

        # Închidem fereastra
        self.close()

