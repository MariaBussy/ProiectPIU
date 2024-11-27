from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QScrollArea, QFrame, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

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
            item.mousePressEvent = lambda event, index=i: self.on_book_click(index)
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
        goal_label = QLabel("Today's Reading")
        goal_label.setFont(QFont("Arial", 16))
        goal_label.setAlignment(Qt.AlignCenter)
        goal_layout.addWidget(goal_label)

        goal_time = QLabel("0:00")
        goal_time.setFont(QFont("Arial", 32))
        goal_time.setAlignment(Qt.AlignCenter)
        goal_layout.addWidget(goal_time)

        goal_subtext = QLabel("of your 5-minute goal")
        goal_subtext.setFont(QFont("Arial", 14))
        goal_subtext.setAlignment(Qt.AlignCenter)
        goal_layout.addWidget(goal_subtext)

        goal_layout.setAlignment(Qt.AlignCenter)
        return goal_widget

    def on_book_click(self, index):
        self.clear_layout()
        book_details = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        book_details.setFont(QFont("Arial", 16))
        book_details.setAlignment(Qt.AlignCenter)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)

        self.main_layout.addWidget(book_details)
        self.main_layout.addWidget(back_button)
        self.current_section = 'book_details'

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
