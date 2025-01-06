from interface.ui_app import create_app
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

if __name__ == "__main__":
    print("Autori: ", get_authors())
    print("Carti: ", get_books())
    app = create_app()
    sys.exit(app.exec_())