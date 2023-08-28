from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                               QLineEdit, QPushButton, QLabel, QTextEdit, QFontComboBox,
                               QSpinBox, QColorDialog, QCheckBox, QTabWidget, QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QTextBrowser)
from PySide6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextBlockFormat, QTextFormat, QFont, QBrush, QPen, QTextCursor, QTextDocument
from PySide6.QtCore import Qt, QRectF
import sys
import json

class Bubble:
    def __init__(self, title, content, x=0, y=0, color=Qt.blue, is_holder=False):
        self.title = title
        self.content = content
        self.x = x
        self.y = y
        self.color = color
        self.is_holder = is_holder
        self.children = []

class CourseCreation(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Course Creation")
        self.bubbles = []
        self.main_bubbles = []  # Initialize main_bubbles to keep track of main canvas bubbles
        self.current_holder = None

        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.view_tab = QWidget()

        self.tabs.addTab(self.main_tab, "Main")
        self.tabs.addTab(self.view_tab, "View")

        main_layout = QVBoxLayout(self.main_tab)
        view_layout = QVBoxLayout(self.view_tab)

        # Create a canvas to display bubbles
        self.canvas = QGraphicsView()
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        self.canvas.setFixedWidth(800)
        self.canvas.setFixedHeight(600)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.canvas)
        view_layout.addWidget(scroll_area)

        # Create a fixed-width display zone that is scrollable
        self.display_zone = QTextBrowser()
        self.display_zone.setFixedWidth(680)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.display_zone)
        view_layout.addWidget(scroll_area)

                # Add a combo box to select the type of bubble to create
        self.bubble_type_combo = QComboBox()
        self.bubble_type_combo.addItems(["Course", "Holder"])
        main_layout.addWidget(self.bubble_type_combo)

        # Add a combo box to select a holder under which to store the bubble
        self.holder_combo = QComboBox()
        self.holder_combo.addItem("None")
        main_layout.addWidget(self.holder_combo)

        # Add a button to go back to the main canvas
        self.back_button = QPushButton("Back to Main Canvas")
        self.back_button.clicked.connect(self.back_to_main_canvas)
        view_layout.addWidget(self.back_button)

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

        # New UI elements for x, y coordinates and bubble color
        self.x_label = QLabel("X:")
        self.x_spin = QSpinBox()
        self.x_spin.setRange(0, 800)
        self.y_label = QLabel("Y:")
        self.y_spin = QSpinBox()
        self.y_spin.setRange(0, 600)
        self.color_label = QLabel("Bubble Color:")
        self.color_button = QPushButton("Choose Color")
        coord_layout = QHBoxLayout()
        coord_layout.addWidget(self.x_label)
        coord_layout.addWidget(self.x_spin)
        coord_layout.addWidget(self.y_label)
        coord_layout.addWidget(self.y_spin)
        coord_layout.addWidget(self.color_label)
        coord_layout.addWidget(self.color_button)
        main_layout.addLayout(coord_layout)

        self.save_button = QPushButton("Save")
        main_layout.addWidget(self.save_button)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)

        # Connect mouse click event to canvas
        self.canvas.mousePressEvent = self.canvas_clicked

        self.save_button.clicked.connect(self.save_course)
        self.style_combo.currentIndexChanged.connect(self.apply_predefined_style)
        self.font_combo.currentFontChanged.connect(self.apply_style)
        self.size_spin.valueChanged.connect(self.apply_style)
        self.bold_check.stateChanged.connect(self.apply_style)
        self.italic_check.stateChanged.connect(self.apply_style)
        self.underline_check.stateChanged.connect(self.apply_style)
        self.align_combo.currentIndexChanged.connect(self.apply_alignment)

        self.save_button.clicked.connect(self.save_course)
        self.new_holder_button = QPushButton("New Holder")
        self.color_button.clicked.connect(self.choose_bubble_color)
        main_layout.addWidget(self.new_holder_button)

    def update_holder_combo(self):
        self.holder_combo.clear()
        self.holder_combo.addItem("None")
        holder_set = set()  # Use a set to eliminate duplicates
        for bubble in self.main_bubbles:
            if bubble.is_holder and bubble.title not in holder_set:
                self.holder_combo.addItem(bubble.title)
                holder_set.add(bubble.title)

    def canvas_clicked(self, event):
        x = event.screenPos().x()
        y = event.screenPos().y()

        for bubble in self.bubbles:
            x0, y0 = bubble.x, bubble.y
            x1, y1 = bubble.x + 50, bubble.y + 50  # Assume each bubble is a 50x50 square for now

            if x0 <= x <= x1 and y0 <= y <= y1:
                if bubble.is_holder:
                    self.current_holder = bubble  # Update the current holder
                    self.bubbles = bubble.children  # Switch the view to the children of the clicked holder
                else:
                    # Code to display or edit the course bubble, as in your original version.
                    self.title_input.setText(bubble.title)
                    self.content_input.setHtml(bubble.content)
                    self.current_color = bubble.color

                self.update_bubble_canvas()
                break
        else:
            self.title_input.clear()
            self.content_input.clear()

    def choose_bubble_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = QColor(color)

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

    def save_course(self):
        title = self.title_input.text()
        content = self.content_input.toHtml()
        x = self.x_spin.value()
        y = self.y_spin.value()
        color = self.current_color if hasattr(self, 'current_color') else Qt.blue
        is_holder = self.bubble_type_combo.currentText() == "Holder"
        new_bubble = Bubble(title, content, x=x, y=y, color=color, is_holder=is_holder)

        holder_name = self.holder_combo.currentText()
        if holder_name != "None":
            for bubble in self.main_bubbles:  # Search in main_bubbles to find the holder
                if bubble.title == holder_name:
                    bubble.children.append(new_bubble)
                    self.bubbles = bubble.children  # Update to the current sub-canvas
                    self.current_holder = bubble  # Remember the current holder for back navigation
                    break
        else:
            self.main_bubbles.append(new_bubble)  # Add to main_bubbles only if not under another holder
            self.bubbles = self.main_bubbles  # Update to the main canvas

        self.update_holder_combo()
        self.update_bubble_canvas()


    def back_to_main_canvas(self):
        self.bubbles = self.main_bubbles  # Reset to the main canvas
        self.current_holder = None  # Reset the current holder
        self.update_bubble_canvas()

    def update_bubble_canvas(self):
        self.scene.clear()
        for bubble in self.bubbles:
            ellipse = QGraphicsEllipseItem(QRectF(bubble.x, bubble.y, 100, 100))
            ellipse.setBrush(QBrush(QColor(bubble.color)))
            ellipse.setPen(QPen(Qt.black))
            self.scene.addItem(ellipse)
            ellipse.setData(Qt.UserRole, bubble)  # Store bubble object in the ellipse

            # Add title text
            text = QGraphicsTextItem()
            font = QFont()
            font.setBold(True)
            text.setFont(font)
            
            # Create a QTextDocument to set alignment
            doc = QTextDocument()
            cursor = QTextCursor(doc)
            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignCenter)

            # Modify the block format of the first block directly
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            cursor.mergeBlockFormat(block_format)

            # Insert the text
            cursor.insertText(bubble.title)

            text.setDocument(doc)
            
            # Set text width for line breaking
            text.setTextWidth(100)  # The width of the bubble

            # Calculate the position to center the text
            text_x = bubble.x + (100 - text.boundingRect().width()) / 2
            text_y = bubble.y + (100 - text.boundingRect().height()) / 2

            text.setPos(text_x, text_y)
            text.setTextInteractionFlags(Qt.TextEditorInteraction)
            self.scene.addItem(text)

    def show_bubble_content(self, item):
        bubble = item.data(Qt.UserRole)
        self.display_zone.setHtml(bubble.content)
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