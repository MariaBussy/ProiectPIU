from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QScrollArea, QFrame, QPushButton, QDialog, QLineEdit, QComboBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
from controllers.books_controller import get_books
from target.target import update_goal, validate_time_input, get_current_goal, save_reading_start
from interface.addFile_page import AddFileWindow
from interface.reading_page import BookReaderApp  # Importă aplicația de citire
from recommandation.recomm_system import RecommendationSystem

class GoalPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Reading Goal")
        self.setGeometry(200, 200, 300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.goal_type_label = QLabel("Goal Type:")
        self.goal_type_combo = QComboBox()
        self.goal_type_combo.addItems(["Time", "Pages"])

        self.frequency_label = QLabel("Frequency:")
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(["Day", "Month"])

        self.value_label = QLabel("Value:")
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Enter minutes or pages")

        self.save_button = QPushButton("Save Goal")
        self.save_button.clicked.connect(self.save_goal)

        self.layout.addWidget(self.goal_type_label)
        self.layout.addWidget(self.goal_type_combo)
        self.layout.addWidget(self.frequency_label)
        self.layout.addWidget(self.frequency_combo)
        self.layout.addWidget(self.value_label)
        self.layout.addWidget(self.value_input)
        self.layout.addWidget(self.save_button)

    def save_goal(self):
        goal_type = self.goal_type_combo.currentText().lower()
        frequency = self.frequency_combo.currentText().lower()
        value = self.value_input.text()

        try:
            validated_value = validate_time_input(value)
            message = update_goal(goal_type, frequency, validated_value)
            self.parent().update_goal_display()  
            self.close()  
        except ValueError as e:
            self.parent().show_message(str(e))  

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("All You Can Read")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #555;
            }
            QMainWindow {
                background-color: #f7f5f8;
            }
        """)

        self.main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        top_bar_layout = QHBoxLayout()
        self.new_window_button = QPushButton("Add New Book")
        self.new_window_button.clicked.connect(self.open_addFile_window)
        self.new_window_button.setMinimumSize(100, 40)
        self.new_window_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #ccc;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
        """)
        top_bar_layout.addWidget(self.new_window_button, alignment=Qt.AlignLeft)

        top_bar_widget = QWidget()
        top_bar_widget.setLayout(top_bar_layout)
        self.main_layout.addWidget(top_bar_widget)


        self.title = QLabel("All You Can Read")
        self.title.setFont(QFont("Arial", 20))
        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title)

        books = get_books()
        self.books_section = self.create_horizontal_section("Your Books", books)
        self.main_layout.addWidget(self.books_section)

        self.goal_section = self.create_reading_goal_section()
        self.main_layout.addWidget(self.goal_section)

        self.recommendations_count=5
        self.recommendations_section = self.create_horizontal_section_for_recomandations("You may enjoy...", books)
        self.main_layout.addWidget(self.recommendations_section)

        self.update_goal_display()

        self.current_section = None

    def open_addFile_window(self):
        """Deschide noua fereastră."""
        self.new_window = AddFileWindow(self)
        self.new_window.files_added.connect(self.refresh_books_list)
        self.new_window.show()

    def create_horizontal_section_for_recomandations(self, title, books):
        section_layout = QVBoxLayout()
        section_title = QLabel(title)
        section_title.setFont(QFont("Arial", 16))
        section_layout.addWidget(section_title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)

        self.book_items = []

        try:
            # Extract book titles and generate recommendations
            book_titles = [book["nume"] for book in books]
            system = RecommendationSystem()
            recommended_data = system.recommend_books(book_titles)
            print(recommended_data)

            # If no recommendations returned, handle it
            if not recommended_data:
                raise Exception("No dataset")

            # Create book items based on recommendations
            for book in recommended_data:
                item = QFrame()
                item.setStyleSheet("background-color: #ddd; border-radius: 5px;")
                item.setFixedSize(120, 180)

                layout = QVBoxLayout(item)

                pixmap = QPixmap('./Photos/default.png')
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(100, 140, Qt.KeepAspectRatio))
                layout.addWidget(image_label)

                title_label = QLabel(book["title"])
                title_label.setAlignment(Qt.AlignCenter)
                title_label.setStyleSheet("font-size: 12px;")
                title_label.setWordWrap(True)  # Enable word wrapping
                title_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                layout.addWidget(title_label)

                item.setLayout(layout)
                scroll_layout.addWidget(item)

        except Exception as e:
            if str(e) == "No dataset":
                message_label = QLabel("This functionality is not available at the moment")
                message_label.setFont(QFont("Arial", 18))
                message_label.setStyleSheet("color: gray; font-weight: bold; text-align: center;")
                scroll_layout.addWidget(message_label)
            else:
                print(f"Caught an exception: {e}")

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        section_layout.addWidget(scroll_area)
        section_widget = QWidget()
        section_widget.setLayout(section_layout)
        return section_widget

    def create_horizontal_section(self, title, books):
        section_layout = QVBoxLayout()
        section_title = QLabel(title)
        section_title.setFont(QFont("Arial", 16))
        section_layout.addWidget(section_title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)

        for book in books:  # Renunțăm la enumerate și iterăm direct asupra cărților
            item = QFrame()
            item.setStyleSheet("background-color: #ddd; border-radius: 5px;")
            item.setFixedSize(120, 180)  # Dimensiuni pentru a arăta imaginea

            layout = QVBoxLayout(item)

            # Adăugăm imaginea
            if book.get("cale_poza"):
                print(book["cale_poza"])
                pixmap = QPixmap(book["cale_poza"])
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(100, 140, Qt.KeepAspectRatio))
                layout.addWidget(image_label)

            # Adăugăm titlul cărții
            title_label = QLabel(book["nume"])
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("font-size: 12px;")
            title_label.setWordWrap(True)  # Enable word wrapping
            title_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            layout.addWidget(title_label)

            item.setLayout(layout)
            scroll_layout.addWidget(item)

            # Adăugăm evenimentul de clic
            item.mousePressEvent = lambda event, book=book: self.on_book_click(book)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        section_layout.addWidget(scroll_area)
        section_widget = QWidget()
        section_widget.setLayout(section_layout)
        return section_widget



    def create_reading_goal_section(self):
        goal_widget = QWidget()
        goal_layout = QVBoxLayout(goal_widget)
        goal_label = QLabel("Your Goal")
        goal_label.setFont(QFont("Arial", 16))
        goal_label.setAlignment(Qt.AlignCenter)
        goal_layout.addWidget(goal_label)

        self.goal_time = QLabel("0:00")
        self.goal_time.setFont(QFont("Arial", 32))
        self.goal_time.setAlignment(Qt.AlignCenter)
        goal_layout.addWidget(self.goal_time)

        set_goal_button = QPushButton("Set Goal")
        set_goal_button.clicked.connect(self.open_goal_popup)
        goal_layout.addWidget(set_goal_button)

        goal_layout.setAlignment(Qt.AlignCenter)
        return goal_widget

    def update_goal_display(self):
        """Update the goal details displayed in the UI."""
        goal = get_current_goal()
        if goal:
            goal_type = goal["goal_type"].capitalize()
            frequency = goal["frequency"].capitalize()
            value = goal["value"]
            created_at = goal["created_at"]
            if goal_type == "Time":
                if frequency == "Day":
                    self.goal_time.setText(f"{value} minutes remaining for the day")
                else:
                    self.goal_time.setText(f"{value} minutes remaining for the month")
            else:
                if goal_type == "Pages":
                    if frequency == "Day":
                        self.goal_time.setText(f"{value} pages remaining for the day")
                    else:
                        self.goal_time.setText(f"{value} pages remaining for the month")
                else:
                    self.goal_time.setText(f"{value}  remaining")
            


        else:
            self.goal_time.setText("0:00")
            

    def open_goal_popup(self):
        popup = GoalPopup(self)
        popup.exec_()

    def show_message(self, message):
        dialog = QDialog(self)
        dialog.setWindowTitle("Message")
        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(message_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(ok_button)

        dialog.exec_()


    def on_book_click(self, book):
        """Deschide fereastra de citire, salvează timpul de început și închide fereastra principală."""

        # Salvăm timpul de început
        save_reading_start()

        # Creăm instanța aplicației de citire
        self.book_reader = BookReaderApp(book)  # Transmite obiectul book către aplicația de citire

        # Conectăm semnalul pentru întoarcerea la fereastra principală
        self.book_reader.go_home_signal.connect(self.open_main_window)

        # Arătăm fereastra de citire
        self.book_reader.show()

        # Închidem fereastra principală
        self.close()



    def open_main_window(self):
        """Redeschide fereastra principală."""
        self.main_window = MyMainWindow()
        self.main_window.show()

    def clear_layout(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None and widget != self.title:
                widget.hide()

    def go_back(self):
        if self.current_section == 'book_details':
            self.clear_layout()
            self.main_layout.addWidget(self.title)
            self.main_layout.addWidget(self.books_section)
            self.main_layout.addWidget(self.goal_section)
            self.main_layout.addWidget(self.recommendations_section)
            self.books_section.show()
            self.goal_section.show()
            self.recommendations_section.show()
            self.current_section = None

    def refresh_books_list(self):
            # Închidem fereastra curentă
        self.close()

        # Creăm o instanță nouă a ferestrei și o deschidem
        new_window = MyMainWindow()  # Asigură-te că folosești numele clasei ferestrei tale
        new_window.show()


main_window = None

def create_app():
    global main_window
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    return app

