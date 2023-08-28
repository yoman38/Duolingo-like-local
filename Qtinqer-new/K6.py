from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                               QLineEdit, QPushButton, QLabel, QTextEdit, QFontComboBox,
                               QSpinBox, QColorDialog, QCheckBox, QTabWidget, QScrollArea, QGraphicsView, QGraphicsScene, QTextBrowser, QListWidget)
from PySide6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextBlockFormat, QTextFormat, QFont, QBrush, QPen
from PySide6.QtCore import Qt, QRectF
import sys
import json

class Bubble:
    def __init__(self, title, content, x=0, y=0, color=Qt.blue, bubble_type='normal', is_holder=False):
        self.title = title
        self.content = content
        self.x = x
        self.y = y
        self.color = color
        self.bubble_type = bubble_type
        self.is_holder = is_holder
        self.children = []

class CourseCreation(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Course Creation")
        self.bubbles = []
        self.current_holder = None

        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.view_tab = QWidget()

        self.tabs.addTab(self.main_tab, "Main")
        self.tabs.addTab(self.view_tab, "View")

        main_layout = QVBoxLayout(self.main_tab)
        view_layout = QVBoxLayout(self.view_tab)

        # Create a QGraphicsView and QGraphicsScene for custom canvas
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        view_layout.addWidget(self.view)


        # Create a fixed-width display zone that is scrollable
        self.display_zone = QTextBrowser()
        self.display_zone.setFixedWidth(400)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.display_zone)
        view_layout.addWidget(scroll_area)

        self.title_label = QLabel("Course Title:")
        self.title_input = QLineEdit()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.title_input)

        self.content_label = QLabel("Course Content:")
        self.content_input = QTextEdit()
        main_layout.addWidget(self.content_label)
        main_layout.addWidget(self.content_input)

        style_layout = QHBoxLayout()
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Custom", "TITLE", "SUBTITLE", "IMPORTANT", "NORMAL"])
        style_layout.addWidget(self.style_combo)

        self.font_combo = QFontComboBox()
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 48)
        self.color_button = QPushButton("Color")
        self.bold_check = QCheckBox("Bold")
        self.italic_check = QCheckBox("Italic")
        self.underline_check = QCheckBox("Underline")

        self.align_combo = QComboBox()
        self.align_combo.addItems(["Left", "Right", "Center", "Justified"])
        style_layout.addWidget(self.align_combo)

        style_layout.addWidget(self.font_combo)
        style_layout.addWidget(self.size_spin)
        style_layout.addWidget(self.color_button)
        style_layout.addWidget(self.bold_check)
        style_layout.addWidget(self.italic_check)
        style_layout.addWidget(self.underline_check)

        main_layout.addLayout(style_layout)

        self.save_button = QPushButton("Save")
        main_layout.addWidget(self.save_button)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)

        # Create a list widget to display bubbles
        self.bubble_list = QListWidget()
        self.bubble_list.itemClicked.connect(self.show_bubble_content)
        view_layout.addWidget(self.bubble_list)

        self.save_button.clicked.connect(self.save_course)
        self.style_combo.currentIndexChanged.connect(self.apply_predefined_style)
        self.font_combo.currentFontChanged.connect(self.apply_style)
        self.size_spin.valueChanged.connect(self.apply_style)
        self.color_button.clicked.connect(self.choose_color)
        self.bold_check.stateChanged.connect(self.apply_style)
        self.italic_check.stateChanged.connect(self.apply_style)
        self.underline_check.stateChanged.connect(self.apply_style)
        self.align_combo.currentIndexChanged.connect(self.apply_alignment)
        #bubble
        self.save_button.clicked.connect(self.save_course)
        self.new_holder_button = QPushButton("New Holder")
        self.new_holder_button.clicked.connect(self.create_new_holder)
        main_layout.addWidget(self.new_holder_button)

        self.save_button.clicked.connect(self.save_course)
        self.new_holder_button = QPushButton("New Holder")
        self.new_holder_button.clicked.connect(self.create_new_holder)
        main_layout.addWidget(self.new_holder_button)

    def apply_predefined_style(self):
        self.apply_style(predefined=True)

    def apply_style(self, predefined=False):
        cursor = self.content_input.textCursor()
        char_format = QTextCharFormat()
        block_format = QTextBlockFormat()

        if predefined:
            style = self.style_combo.currentText()
            if style == "TITLE":
                char_format.setFont(QFont("Tahoma", 16, QFont.Bold))
                char_format.setForeground(QColor("dark blue"))
                char_format.setFontUnderline(True)
                block_format.setAlignment(Qt.AlignCenter)
            elif style == "SUBTITLE":
                char_format.setFont(QFont("Tahoma", 14, QFont.Bold))
                char_format.setForeground(QColor("light blue"))
                char_format.setFontUnderline(True)
                block_format.setAlignment(Qt.AlignCenter)
            elif style == "IMPORTANT":
                char_format.setFont(QFont("Arial", 12, QFont.Bold))
                char_format.setForeground(QColor("dark red"))
                block_format.setAlignment(Qt.AlignJustify)
            elif style == "NORMAL":
                char_format.setFont(QFont("Arial", 11))
                char_format.setForeground(QColor("black"))
                block_format.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)
        else:
            char_format.setFont(self.font_combo.currentFont())
            char_format.setFontPointSize(self.size_spin.value())
            char_format.setFontUnderline(self.underline_check.isChecked())
            char_format.setFontItalic(self.italic_check.isChecked())
            char_format.setFontWeight(75 if self.bold_check.isChecked() else 50)

        cursor.mergeCharFormat(char_format)
        cursor.mergeBlockFormat(block_format)
        self.content_input.setCurrentCharFormat(char_format)

    def apply_alignment(self):
        cursor = self.content_input.textCursor()
        block_format = QTextBlockFormat()
        alignment = self.align_combo.currentText()

        if alignment == "Left":
            block_format.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)
        elif alignment == "Right":
            block_format.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
        elif alignment == "Center":
            block_format.setAlignment(Qt.AlignCenter)
        elif alignment == "Justified":
            block_format.setAlignment(Qt.AlignJustify)

        cursor.mergeBlockFormat(block_format)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            cursor = self.content_input.textCursor()
            format = cursor.charFormat()
            format.setForeground(QColor(color))
            cursor.mergeCharFormat(format)

    def create_new_holder(self):
        title = "New Holder"
        new_holder = Bubble(title, "", is_holder=True)
        self.bubbles.append(new_holder)
        self.current_holder = new_holder
        self.update_bubble_canvas()

    def save_course(self):
        title = self.title_input.text()
        content = self.content_input.toHtml()
        new_bubble = Bubble(title, content, x=100, y=100)  # Example coordinates
        if self.current_holder:
            self.current_holder.children.append(new_bubble)
        else:
            self.bubbles.append(new_bubble)
        self.update_bubble_canvas()
        self.display_zone.setHtml(content)
        print(f"Course Title: {title}")
        print(f"Course Content: {content}")

    def update_bubble_canvas(self):
        self.scene.clear()
        for bubble in self.bubbles:
            x, y = bubble.x, bubble.y
            color = bubble.color
            self.scene.addEllipse(x, y, 50, 50, QPen(color), QBrush(color))
            if bubble.is_holder:
                for child in bubble.children:
                    x, y = child.x, child.y
                    color = child.color
                    self.scene.addEllipse(x, y, 30, 30, QPen(color), QBrush(color))


    def update_bubble_list(self):
        self.bubble_list.clear()
        for bubble in self.bubbles:
            item = QListWidgetItem(bubble.title)
            item.setData(Qt.UserRole, bubble)
            self.bubble_list.addItem(item)
            if bubble.is_holder:
                for child in bubble.children:
                    child_item = QListWidgetItem(f"  - {child.title}")
                    child_item.setData(Qt.UserRole, child)
                    self.bubble_list.addItem(child_item)

    def show_bubble_content(self, item):
        bubble = item.data(Qt.UserRole)
        if bubble.is_holder:
            self.current_holder = bubble
            self.update_bubble_list()
        else:
            self.display_zone.setHtml(bubble.content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CourseCreation()
    window.show()
    sys.exit(app.exec())