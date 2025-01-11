from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QScrollArea, QFrame, QPushButton, QDialog, QLineEdit, QComboBox, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sys
from controllers.books_controller import get_books
from target.target import update_goal, validate_time_input, get_current_goal, save_reading_start
from interface.addFile_page import AddFileWindow
from interface.reading_page import BookReaderApp
from recommandation.recomm_system import RecommendationSystem
import webbrowser

class GoalPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Reading Goal")
        self.setGeometry(200, 200, 300, 200)
        self.setStyleSheet("background-color: #1e1e1e; color: #dcdcdc;")

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
        self.save_button.setStyleSheet(self.button_style())

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

    def button_style(self):
        return (
            "QPushButton {"
            "    font-size: 14px; padding: 8px;"
            "    background-color: #007bff; color: #fff;"
            "    border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #0056b3;"
            "}"
        )

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("All You Can Read")
        self.setGeometry(100, 100, 1000, 970)
        self.setStyleSheet("background-color: #121212; color: #dcdcdc;")

        self.main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Top bar
        top_bar_layout = QHBoxLayout()
        self.new_window_button = QPushButton("Add New Book")
        self.new_window_button.clicked.connect(self.open_addFile_window)
        self.new_window_button.setMinimumSize(100, 40)
        self.new_window_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.new_window_button.setStyleSheet(self.button_style())
        top_bar_layout.addWidget(self.new_window_button, alignment=Qt.AlignLeft)

        top_bar_widget = QWidget()
        top_bar_widget.setLayout(top_bar_layout)
        self.main_layout.addWidget(top_bar_widget)

        # Title
        self.title = QLabel("All You Can Read")
        title_font = QFont("Georgia", 32)  # Creează un font de tip Georgia, dimensiunea 24
        title_font.setItalic(True)  # Aplică stilul italic
        self.title.setFont(title_font)  # Setează fontul la QLabel
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #ffffff;")
        self.main_layout.addWidget(self.title)

        # Goal Section
        self.goal_section = self.create_reading_goal_section()
        self.main_layout.addWidget(self.goal_section)

        # Books Section
        books = get_books()
        self.books_section = self.create_horizontal_section("Your Books", books)
        self.main_layout.addWidget(self.books_section)

        # Recommendations Section
        self.recommendations_count = 5
        self.recommendations_section = self.create_horizontal_section_for_recommendations("You may enjoy...", books)
        self.main_layout.addWidget(self.recommendations_section)

        self.update_goal_display()

    def open_addFile_window(self):
        self.new_window = AddFileWindow(self)
        self.new_window.files_added.connect(self.refresh_books_list)
        self.new_window.show()

    def create_horizontal_section_for_recommendations(self, title, books):
        section_layout = QVBoxLayout()
        section_title = QLabel(title)
        section_title.setFont(QFont("Arial", 18))
        section_title.setStyleSheet("color: #f5f5f5;")
        section_layout.addWidget(section_title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        try:
            book_titles = [book["nume"] for book in books]
            system = RecommendationSystem()
            recommended_data = system.recommend_books(book_titles)

            if not recommended_data:
                raise Exception("No dataset")

            for book in recommended_data:
                item = QFrame()
                item.setStyleSheet(self.book_frame_style())
                item.setFixedSize(150, 250)

                layout = QVBoxLayout(item)

                pixmap = QPixmap('./Photos/default.png')
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(130, 200, Qt.KeepAspectRatio))
                layout.addWidget(image_label)

                title_label = QLabel(book["title"])
                title_label.setAlignment(Qt.AlignCenter)
                title_label.setStyleSheet("font-size: 14px; color: #007bff; font-weight: bold;")
                title_label.setWordWrap(True)
                layout.addWidget(title_label)

                item.setLayout(layout)
                scroll_layout.addWidget(item)

                item.mousePressEvent = lambda event, book=book: self.on_recommendation_click(book)

        except Exception as e:
            message_label = QLabel("This functionality is not available at the moment")
            message_label.setFont(QFont("Arial", 18))
            message_label.setStyleSheet("color: gray; font-weight: bold; text-align: center;")
            scroll_layout.addWidget(message_label)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        section_layout.addWidget(scroll_area)
        section_widget = QWidget()
        section_widget.setLayout(section_layout)
        return section_widget

    def on_recommendation_click(self, book):
        webbrowser.open(book['preview_link'])

    def create_horizontal_section(self, title, books):
        section_layout = QVBoxLayout()
        section_title = QLabel(title)
        section_title.setFont(QFont("Arial", 18))
        section_title.setStyleSheet("color: #f5f5f5;")
        section_layout.addWidget(section_title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        for book in books:
            item = QFrame()
            item.setStyleSheet(self.book_frame_style())
            item.setFixedSize(150, 250)

            layout = QVBoxLayout(item)

            if book.get("cale_poza"):
                pixmap = QPixmap(book["cale_poza"])
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(130, 200, Qt.KeepAspectRatio))
                layout.addWidget(image_label)

            title_label = QLabel(book["nume"])
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
            title_label.setWordWrap(True)
            layout.addWidget(title_label)

            item.setLayout(layout)
            scroll_layout.addWidget(item)
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

        # Titlu: "Your Goal"
        goal_label = QLabel("Your Goal")
        goal_label.setFont(QFont("Arial", 18))
        goal_label.setAlignment(Qt.AlignCenter)
        goal_label.setStyleSheet("color: #f5f5f5; padding: 10px;")  # Doar styling pentru text
        goal_layout.addWidget(goal_label)

        # Crearea unui widget separat pentru conținutul cu bordură
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Timpul Obiectivului
        self.goal_time = QLabel("0:00")
        self.goal_time.setFont(QFont("Arial", 12))
        self.goal_time.setAlignment(Qt.AlignCenter)
        self.goal_time.setStyleSheet("color: #ffffff; font-weight: bold; padding: 15px;")
        content_layout.addWidget(self.goal_time)

        # Butonul Set Goal
        set_goal_button = QPushButton("Set Goal")
        set_goal_button.setStyleSheet(self.button_style())
        set_goal_button.clicked.connect(self.open_goal_popup)
        content_layout.addWidget(set_goal_button)

        # Setarea bordurii pentru widget-ul de conținut
        content_widget.setStyleSheet("""
            background-color: #222;
            border: 2px solid #ffffff;
            border-radius: 10px;
            padding: 20px;
        """)

        # Adăugăm widget-ul de conținut în layout-ul principal
        goal_layout.addWidget(content_widget)

        # Alinierea întregului conținut
        goal_layout.setAlignment(Qt.AlignCenter)

        # Setăm layout-ul pe goal_widget
        goal_widget.setLayout(goal_layout)

        return goal_widget



    def update_goal_display(self):
        goal = get_current_goal()
        if goal:
            goal_type = goal["goal_type"].capitalize()
            frequency = goal["frequency"].capitalize()
            value = goal["value"]
            if goal_type == "Time":
                self.goal_time.setText(f"{value} minutes remaining for the {frequency.lower()}")
            elif goal_type == "Pages":
                self.goal_time.setText(f"{value} pages remaining for the {frequency.lower()}")
        else:
            self.goal_time.setText("0:00")

    def open_goal_popup(self):
        popup = GoalPopup(self)
        popup.exec_()

    def show_message(self, message):
        dialog = QDialog(self)
        dialog.setWindowTitle("Message")
        dialog.setStyleSheet("background-color: #1e1e1e; color: #dcdcdc;")
        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(message_label)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet(self.button_style())
        ok_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(ok_button)

        dialog.exec_()

    def on_book_click(self, book):
        save_reading_start()
        self.book_reader = BookReaderApp(book)
        self.book_reader.go_home_signal.connect(self.open_main_window)
        self.book_reader.show()
        self.close()

    def open_main_window(self):
        self.main_window = MyMainWindow()
        self.main_window.show()

    def refresh_books_list(self):
        self.close()
        new_window = MyMainWindow()
        new_window.show()

    def button_style(self):
        return (
            "QPushButton {"
            "    font-size: 14px; padding: 10px;"
            "    background-color: #007bff; color: #fff;"
            "    border: none; border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #0056b3;"
            "}"
        )

    def book_frame_style(self):
        return (
            "background-color: #2a2a2a;"
            "border: 2px solid #444;"
            "border-radius: 8px;"
            "color: #ffffff;"
        )

main_window = None

def create_app():
    global main_window
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    return app

