from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QScrollArea, QFrame, QPushButton, QDialog, QLineEdit, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from target.target import update_goal, validate_time_input, get_current_goal, save_reading_start
from interface.reading_page import BookReaderApp  # Importă aplicația de citire

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

        self.title = QLabel("All You Can Read")
        self.title.setFont(QFont("Arial", 20))
        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title)

        self.books_section = self.create_horizontal_section("Your Books", 10)
        self.main_layout.addWidget(self.books_section)

        self.goal_section = self.create_reading_goal_section()
        self.main_layout.addWidget(self.goal_section)

        self.recommendations_section = self.create_horizontal_section("You may enjoy...", 8)
        self.main_layout.addWidget(self.recommendations_section)

        self.update_goal_display()

        self.current_section = None

    def create_horizontal_section(self, title, num_items):
        section_layout = QVBoxLayout()
        section_title = QLabel(title)
        section_title.setFont(QFont("Arial", 16))
        section_layout.addWidget(section_title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)

        self.book_items = []
        for i in range(num_items):
            item = QFrame()
            item.setStyleSheet("background-color: #ddd; border-radius: 5px;")
            item.setFixedSize(100, 140)
            item.mousePressEvent = lambda event, index=i: self.on_book_click(index)  # Deschide aplicația de citire
            self.book_items.append(item)
            scroll_layout.addWidget(item)

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


    def on_book_click(self, index):
        """Deschide fereastra de citire, salvează timpul de început și închide fereastra principală."""
        save_reading_start()  # Salvează timpul de început
        self.book_reader = BookReaderApp()  # Creează o instanță a aplicației de citire
        self.book_reader.go_home_signal.connect(self.open_main_window)  # Conectează semnalul
        self.book_reader.show()  # Arată fereastra de citire
        self.close()  # Închide fereastra principală


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

main_window = None

def create_app():
    global main_window
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    return app

