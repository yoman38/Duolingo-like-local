from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QPushButton, QLabel, QTextEdit, QFontComboBox,
                               QSpinBox, QColorDialog, QCheckBox)
from PySide6.QtGui import QTextCursor, QColor
import sys

class CourseCreation(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Course Creation")

        main_layout = QVBoxLayout()

        # Title Section
        self.title_label = QLabel("Course Title:")
        self.title_input = QLineEdit()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.title_input)

        # Content Section
        self.content_label = QLabel("Course Content:")
        self.content_input = QTextEdit()
        main_layout.addWidget(self.content_label)
        main_layout.addWidget(self.content_input)

        # Style Section
        style_layout = QHBoxLayout()
        self.font_combo = QFontComboBox()
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 48)
        self.color_button = QPushButton("Color")
        self.bold_check = QCheckBox("Bold")
        self.italic_check = QCheckBox("Italic")
        self.underline_check = QCheckBox("Underline")

        style_layout.addWidget(self.font_combo)
        style_layout.addWidget(self.size_spin)
        style_layout.addWidget(self.color_button)
        style_layout.addWidget(self.bold_check)
        style_layout.addWidget(self.italic_check)
        style_layout.addWidget(self.underline_check)

        main_layout.addLayout(style_layout)

        # Save Button
        self.save_button = QPushButton("Save")
        main_layout.addWidget(self.save_button)

        self.setLayout(main_layout)

        # Connect Signals
        self.save_button.clicked.connect(self.save_course)
        self.font_combo.currentFontChanged.connect(self.apply_style)
        self.size_spin.valueChanged.connect(self.apply_style)
        self.color_button.clicked.connect(self.choose_color)
        self.bold_check.stateChanged.connect(self.apply_style)
        self.italic_check.stateChanged.connect(self.apply_style)
        self.underline_check.stateChanged.connect(self.apply_style)

    def apply_style(self):
        cursor = self.content_input.textCursor()
        format = cursor.charFormat()

        format.setFont(self.font_combo.currentFont())
        format.setFontPointSize(self.size_spin.value())
        format.setFontUnderline(self.underline_check.isChecked())
        format.setFontItalic(self.italic_check.isChecked())
        format.setFontWeight(75 if self.bold_check.isChecked() else 50)

        cursor.mergeCharFormat(format)
        self.content_input.setCurrentCharFormat(format)  # Set the current char format for new text

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            cursor = self.content_input.textCursor()
            format = cursor.charFormat()
            format.setForeground(QColor(color))
            cursor.mergeCharFormat(format)

    def save_course(self):
        title = self.title_input.text()
        content = self.content_input.toHtml()
        print(f"Course Title: {title}")
        print(f"Course Content: {content}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CourseCreation()
    window.show()
    sys.exit(app.exec())
