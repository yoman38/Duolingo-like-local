from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
import sys

class CourseCreation(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Course Creation")

        layout = QVBoxLayout()

        self.title_label = QLabel("Course Title:")
        self.title_input = QLineEdit()
        self.content_label = QLabel("Course Content:")
        self.content_input = QLineEdit()
        self.save_button = QPushButton("Save")

        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(self.content_label)
        layout.addWidget(self.content_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_course)

    def save_course(self):
        title = self.title_input.text()
        content = self.content_input.text()
        print(f"Course Title: {title}")
        print(f"Course Content: {content}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CourseCreation()
    window.show()
    sys.exit(app.exec())
