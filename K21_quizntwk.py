from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                               QLineEdit, QPushButton, QLabel, QTextEdit, QFontComboBox,
                               QSpinBox, QColorDialog, QCheckBox, QTabWidget, QScrollArea, 
                               QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, 
                               QTextBrowser, QGraphicsLineItem, QFileDialog, QDialog, QGraphicsPixmapItem,
                               QRadioButton, QMessageBox)
from PySide6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextBlockFormat, QTextFormat, QFont, QBrush, QPen, QTextCursor, QTextDocument, QPixmap, QImage
from PySide6.QtCore import Qt, QRectF, QUrl, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from io import BytesIO
from PIL import Image
import fitz  # PyMuPDF
import shutil  # for copying files
import os
import sys
import base64
import json
import math
import re

class Bubble:
    def __init__(self, title, content, x=0, y=0, color=Qt.blue, is_holder=False, youtube_link=None, youtube_start_time=None, youtube_end_time=None, pdf_path=None, quiz_question=None, quiz_options=None, quiz_answer=None):
        self.title = title
        self.content = content
        self.x = x
        self.y = y
        self.color = color
        self.is_holder = is_holder
        self.children = []
        self.youtube_link = youtube_link
        self.youtube_start_time = youtube_start_time
        self.youtube_end_time = youtube_end_time
        self.pdf_path = pdf_path
        self.is_quiz = is_quiz
        self.quiz_question = quiz_question
        self.quiz_options = quiz_options
        self.quiz_answer = quiz_answer
        self.quiz_performance = {}  # Example: {"question1": {"attempts": 3, "correct": 1}}


    def to_dict(self):
        bubble_dict = {
            'title': self.title,
            'content': self.content,
            'x': self.x,
            'y': self.y,
            'color': self.color.name() if callable(self.color.name) else self.color.name,
            'is_holder': self.is_holder,
            'children': [child.to_dict() for child in self.children],
            'youtube_link': self.youtube_link,
            'youtube_start_time': self.youtube_start_time,
            'youtube_end_time': self.youtube_end_time,
            'pdf_path': self.pdf_path,
        }
        bubble_dict['quiz_question'] = self.quiz_question
        bubble_dict['quiz_options'] = self.quiz_options
        bubble_dict['quiz_answer'] = self.quiz_answer
        return bubble_dict

    @classmethod
    def from_dict(cls, bubble_dict):
        bubble = cls(
            title=bubble_dict['title'],
            content=bubble_dict['content'],
            x=bubble_dict['x'],
            y=bubble_dict['y'],
            color=QColor(bubble_dict['color']),
            is_holder=bubble_dict['is_holder'],
            youtube_link=bubble_dict.get('youtube_link'),
            youtube_start_time=bubble_dict.get('youtube_start_time'),
            youtube_end_time=bubble_dict.get('youtube_end_time'),
            pdf_path=bubble_dict.get('pdf_path')
        )
        quiz_question = bubble_dict.get('quiz_question')
        quiz_options = bubble_dict.get('quiz_options')
        quiz_answer = bubble_dict.get('quiz_answer')
        bubble.quiz_question = quiz_question
        bubble.quiz_options = quiz_options
        bubble.quiz_answer = quiz_answer
        return bubble

class ContentPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bubble Content")
        layout = QVBoxLayout()

        # Create QTextBrowser for Rich Text
        self.text_browser = QTextBrowser()
        layout.addWidget(self.text_browser)

        # Create QWebEngineView for YouTube
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Create QGraphicsView for PDF
        self.pdf_view = QGraphicsView()
        self.pdf_scene = QGraphicsScene()
        self.pdf_view.setScene(self.pdf_scene)
        layout.addWidget(self.pdf_view)

        # Close Button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class CourseCreation(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize member variables
        self.setWindowTitle("Course Creation")
        self.bubbles = []
        self.current_holder = None
        self.current_color = Qt.blue
        self.pdf_path = None  # Initialize pdf_path
        
        # Initialize UI Elements
        self.init_ui()
        
        # Initialize Event Handlers
        self.init_events()

        # Initialize Data
        self.load_from_file()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.view_tab = QWidget()

        self.tabs.addTab(self.main_tab, "Main")
        self.tabs.addTab(self.view_tab, "View")

        main_layout = QVBoxLayout(self.main_tab)
        view_layout = QVBoxLayout(self.view_tab)

        # Initialize Bubble Type UI
        self.init_bubble_type_ui(main_layout)

        # Initialize Canvas UI
        self.init_canvas_ui(view_layout)

        #youtube
        self.youtube_view = QWebEngineView()
        main_layout.addWidget(self.youtube_view)

        # Initialize Multimedia UI
        self.init_multimedia_ui(main_layout, view_layout)

        # Initialize Text and Style UI
        self.init_text_and_style_ui(main_layout)

        # Initialize Position UI
        self.init_position_ui(main_layout)

        # Initialize Save and Delete UI
        self.init_save_and_delete_ui(main_layout, view_layout)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tabs)



    def init_events(self):
        self.canvas.mousePressEvent = self.canvas_clicked
        self.style_combo.currentIndexChanged.connect(self.apply_predefined_style)
        self.font_combo.currentFontChanged.connect(self.apply_style)
        self.size_spin.valueChanged.connect(self.apply_style)
        self.bold_check.stateChanged.connect(self.apply_style)
        self.italic_check.stateChanged.connect(self.apply_style)
        self.underline_check.stateChanged.connect(self.apply_style)
        self.align_combo.currentIndexChanged.connect(self.apply_alignment)
        self.save_button.clicked.connect(self.save_course)
        self.color_button.clicked.connect(self.choose_bubble_color)
        self.back_button.clicked.connect(self.back_to_previous_canvas)
        self.delete_button.clicked.connect(self.delete_course)
        self.insert_image_button.clicked.connect(self.insert_image)
        self.pdf_upload_button.clicked.connect(self.upload_pdf)
        self.insert_youtube_button.clicked.connect(self.insert_youtube_video)


    def init_bubble_type_ui(self, layout):
        self.bubble_type_combo = QComboBox()
        self.bubble_type_combo.addItems(["Course", "Holder", "Quiz"])
        layout.addWidget(QLabel("Bubble Type:"))
        layout.addWidget(self.bubble_type_combo)

    def init_canvas_ui(self, layout):
        self.canvas = QGraphicsView()
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        self.canvas.setFixedWidth(800)
        self.canvas.setFixedHeight(600)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.canvas)
        layout.addWidget(scroll_area)

    def init_multimedia_ui(self, main_layout, view_layout):
        # Image
        self.insert_image_button = QPushButton("Insert Image")
        main_layout.addWidget(self.insert_image_button)

        # Video and PDF
        self.youtube_link_input = QLineEdit()
        main_layout.addWidget(QLabel("YouTube Link:"))
        main_layout.addWidget(self.youtube_link_input)
        self.start_time_input = QLineEdit()
        self.end_time_input = QLineEdit()
        main_layout.addWidget(QLabel("Start Time (s):"))
        main_layout.addWidget(self.start_time_input)
        main_layout.addWidget(QLabel("End Time (s):"))
        main_layout.addWidget(self.end_time_input)
        self.youtube_view = QWebEngineView()
        view_layout.addWidget(self.youtube_view)
        self.pdf_upload_button = QPushButton("Upload PDF")
        main_layout.addWidget(self.pdf_upload_button)
        self.insert_youtube_button = QPushButton("Insert YouTube Video")
        main_layout.addWidget(self.insert_youtube_button)

        # Quiz UI
        self.quiz_question_input = QLineEdit()
        main_layout.addWidget(QLabel("Quiz Question:"))
        main_layout.addWidget(self.quiz_question_input)

        self.quiz_option1_input = QLineEdit()
        self.quiz_option2_input = QLineEdit()
        self.quiz_option3_input = QLineEdit()
        self.quiz_option4_input = QLineEdit()

        main_layout.addWidget(QLabel("Option 1:"))
        main_layout.addWidget(self.quiz_option1_input)
        main_layout.addWidget(QLabel("Option 2:"))
        main_layout.addWidget(self.quiz_option2_input)
        main_layout.addWidget(QLabel("Option 3:"))
        main_layout.addWidget(self.quiz_option3_input)
        main_layout.addWidget(QLabel("Option 4:"))
        main_layout.addWidget(self.quiz_option4_input)

        self.quiz_answer_input = QLineEdit()
        main_layout.addWidget(QLabel("Correct Answer:"))
        main_layout.addWidget(self.quiz_answer_input)

    def insert_youtube_video(self):
        video_id = self.extract_youtube_id(self.youtube_link_input.text())
        youtube_url = f"https://www.youtube.com/embed/{video_id}"
        self.youtube_view.setUrl(QUrl(youtube_url))

    def init_text_and_style_ui(self, layout):
        self.title_label = QLabel("Course Title:")
        self.title_input = QLineEdit()
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)

        self.content_label = QLabel("Course Content:")
        self.content_input = QTextEdit()
        layout.addWidget(self.content_label)
        layout.addWidget(self.content_input)

        style_layout = QHBoxLayout()
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Custom", "TITLE", "SUBTITLE", "IMPORTANT", "NORMAL"])
        self.font_combo = QFontComboBox()
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 48)
        self.color_button = QPushButton("Txt Color")
        self.bold_check = QCheckBox("Bold")
        self.italic_check = QCheckBox("Italic")
        self.underline_check = QCheckBox("Underline")
        self.align_combo = QComboBox()
        self.align_combo.addItems(["Left", "Right", "Center", "Justified"])
        style_layout.addWidget(self.style_combo)
        style_layout.addWidget(self.font_combo)
        style_layout.addWidget(self.size_spin)
        style_layout.addWidget(self.color_button)
        style_layout.addWidget(self.bold_check)
        style_layout.addWidget(self.italic_check)
        style_layout.addWidget(self.underline_check)
        style_layout.addWidget(self.align_combo)
        layout.addLayout(style_layout)

    def init_position_ui(self, layout):
        coord_layout = QHBoxLayout()
        self.x_label = QLabel("X:")
        self.x_spin = QSpinBox()
        self.x_spin.setRange(0, 800)
        self.y_label = QLabel("Y:")
        self.y_spin = QSpinBox()
        self.y_spin.setRange(0, 600)
        self.color_label = QLabel("Bubble Color:")
        self.color_button = QPushButton("Choose Color")
        coord_layout.addWidget(self.x_label)
        coord_layout.addWidget(self.x_spin)
        coord_layout.addWidget(self.y_label)
        coord_layout.addWidget(self.y_spin)
        coord_layout.addWidget(self.color_label)
        coord_layout.addWidget(self.color_button)
        layout.addLayout(coord_layout)

    def init_save_and_delete_ui(self, main_layout, view_layout):
        self.save_button = QPushButton("Save")
        main_layout.addWidget(self.save_button)

        self.canvas_stack = []
        self.holder_combo = QComboBox()
        self.holder_combo.addItem("Main Canvas")
        self.back_button = QPushButton("Back")
        view_layout.addWidget(self.back_button)
        main_layout.addWidget(QLabel("Save under:"))
        main_layout.addWidget(self.holder_combo)

        self.delete_combo = QComboBox()
        main_layout.addWidget(QLabel("Delete Course:"))
        main_layout.addWidget(self.delete_combo)

        self.delete_button = QPushButton("Delete")
        main_layout.addWidget(self.delete_button)

    def show_content_popup(self, html_content):
        # Create a QDialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Bubble Content")
        dialog_layout = QVBoxLayout()

        # Create a QWebEngineView and set the HTML content
        web_view = QWebEngineView()
        web_view.setHtml(html_content)
        dialog_layout.addWidget(web_view)

        # Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        dialog_layout.addWidget(close_button)

        dialog.setLayout(dialog_layout)
        dialog.exec()

        self.youtube_view.page().webChannel().registerObject("my_channel", self)
        
    def upload_pdf(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Upload PDF File", "", "PDF Files (*.pdf)", options=options)
        if filePath:
            new_pdf_path = os.path.join(os.getcwd(), os.path.basename(filePath))
            shutil.copy(filePath, new_pdf_path)
            self.pdf_path = new_pdf_path
            self.display_pdf_as_image(self.pdf_path)
            
            # Write the name of the PDF in the main content zone
            pdf_name = os.path.basename(filePath)
            self.content_input.append(f"Imported PDF: {pdf_name}")

    def convert_pdf_to_html_images(self, pdf_path):
        image_tags = []
        pdf_document = fitz.open(pdf_path)
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pixmap = page.get_pixmap()
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            img_tag = f'<img src="data:image/png;base64,{img_base64}" />'
            image_tags.append(img_tag)
        return image_tags

    def display_pdf_as_image(self, pdf_path):
        self.scene.clear()
        pdf_document = fitz.open(pdf_path)
        y_offset = 0
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pixmap = page.get_pixmap()
            qt_image =   QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
            qt_pixmap = QPixmap.fromImage(qt_image)
            pixmap_item = QGraphicsPixmapItem(qt_pixmap)
            pixmap_item.setPos(0, y_offset)
            self.scene.addItem(pixmap_item)
            y_offset += pixmap.height

    def extract_youtube_id(self, url):
        video_id_match = re.search(r'v=([A-Za-z0-9_\-]+)', url)
        video_id = video_id_match.group(1) if video_id_match else None
        return video_id       
    
    def update_delete_dropdown(self):
        self.delete_combo.clear()
        for bubble in self.bubbles:
            if not bubble.is_holder:  # Only add courses, not holders
                self.delete_combo.addItem(bubble.title)

    def delete_course(self):
        selected_title = self.delete_combo.currentText()
        current_bubbles = self.current_holder.children if self.current_holder else self.bubbles
        for i, bubble in enumerate(current_bubbles):
            if bubble.title == selected_title:
                if bubble.is_holder:
                    self.delete_holder_and_children(bubble)
                del current_bubbles[i]
                break
        self.update_bubble_canvas()
        self.update_delete_dropdown()
        self.save_to_file()  # Save the updated state to the JSON file

    def delete_holder_and_children(self, holder):
        for child in holder.children:
            if child.is_holder:
                self.delete_holder_and_children(child)
        holder.children.clear()

    def insert_image(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if filePath:
            # Set the width to 680 pixels and let the height be automatically adjusted
            self.content_input.insertHtml(f'<img src="{filePath}" width="680" />')

    def back_to_previous_canvas(self):
        if self.canvas_stack:
            self.current_holder = self.canvas_stack.pop()
            self.update_bubble_canvas()
            
    def canvas_clicked(self, event):
        items = self.canvas.items(event.position().toPoint())
        for item in items:
            if isinstance(item, QGraphicsEllipseItem):
                bubble = item.data(Qt.UserRole)
                if bubble.is_holder:
                    self.canvas_stack.append(self.current_holder)
                    self.current_holder = bubble
                    self.update_bubble_canvas()  # Update the canvas to reflect the current holder
                else:
                    self.show_bubble_content(bubble)
                break

    def on_load_finished(self, ok):
        if ok:
            print("Page loaded successfully.")
            js_code = '''
            console.oldLog = console.log;
            console.log = function(message) {
                console.oldLog(message);
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    window.my_channel = channel.objects.my_channel;
                    my_channel.receiveText(message);
                });
            };
            '''
            self.youtube_view.page().runJavaScript(js_code)

    def choose_bubble_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = QColor(color)

    def choose_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            cursor = self.content_input.textCursor()
            format = cursor.charFormat()
            format.setForeground(QColor(color))
            cursor.mergeCharFormat(format)
            self.content_input.setCurrentCharFormat(format)

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

    def load_from_file(self):
        try:
            with open('courses.json', 'r') as f:
                bubble_dicts = json.load(f)
                self.bubbles = [Bubble.from_dict(bubble_dict) for bubble_dict in bubble_dicts]
                self.update_bubble_canvas()
                self.update_delete_dropdown()  # Update the delete dropdown here
        except FileNotFoundError:
            print("File not found. Initializing an empty list.")
            self.bubbles = []
        except json.JSONDecodeError:
            print("Error decoding JSON. Initializing an empty list.")
            self.bubbles = []

    def save_course(self):
        title = self.title_input.text()
        content = self.content_input.toHtml()
        x = self.x_spin.value()
        y = self.y_spin.value()
        color = self.current_color if hasattr(self, 'current_color') else Qt.blue
        is_holder = True if self.bubble_type_combo.currentText() == "Holder" else False
        is_quiz = True if self.bubble_type_combo.currentText() == "Quiz" else False
        quiz_question = self.quiz_question_input.text() if is_quiz else None
        quiz_options = [self.quiz_option1_input.text(), self.quiz_option2_input.text(), self.quiz_option3_input.text(), self.quiz_option4_input.text()] if is_quiz else None
        quiz_answer = self.quiz_answer_input.text() if is_quiz else None

        new_bubble = Bubble(title, content, x=x, y=y, color=color, is_holder=is_holder, youtube_link=self.youtube_link_input.text(), youtube_start_time=self.start_time_input.text(), youtube_end_time=self.end_time_input.text(),pdf_path=self.pdf_path if hasattr(self, 'pdf_path') else None, quiz_question=quiz_question, quiz_options=quiz_options, quiz_answer=quiz_answer) 

        selected_holder_title = self.holder_combo.currentText()\
        
        # Save the PDF locally if available
        if self.pdf_path:
            pdf_folder = os.path.join(os.getcwd(), 'pdfs')
            if not os.path.exists(pdf_folder):
                os.makedirs(pdf_folder)
            new_pdf_path = os.path.join(pdf_folder, f"{new_bubble.title}.pdf")
            shutil.copy(self.pdf_path, new_pdf_path)
            new_bubble.pdf_path = os.path.relpath(new_pdf_path, os.getcwd())  # Update the Bubble object's pdf_path

        if selected_holder_title == "Main Canvas":
            self.bubbles.append(new_bubble)
        else:
            # Find the holder with the selected title
            for bubble in self.bubbles:
                if bubble.title == selected_holder_title and bubble.is_holder:
                    bubble.children.append(new_bubble)
                    break

        self.update_bubble_canvas()
        self.update_holder_dropdown()
        self.update_delete_dropdown()  # Add this line to update the delete dropdown
        self.save_to_file()

    def save_to_file(self):
        # Use relative paths for PDFs
        for bubble in self.bubbles:
            if bubble.pdf_path:
                bubble.pdf_path = os.path.relpath(bubble.pdf_path, os.getcwd())
        
        with open('courses.json', 'w') as f:
            json.dump([bubble.to_dict() for bubble in self.bubbles], f)
        
        # Restore absolute paths after saving
        for bubble in self.bubbles:
            if bubble.pdf_path:
                bubble.pdf_path = os.path.abspath(bubble.pdf_path)

    def update_bubble_canvas(self):
        self.scene.clear()
        current_bubbles = self.current_holder.children if self.current_holder else self.bubbles

        for bubble in current_bubbles:  # Changed from self.bubbles to current_bubbles

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
            self.draw_lines_between_courses()

            special_content_label = None
            if bubble.youtube_link:
                special_content_label = "YouTube"
            elif bubble.pdf_path:
                special_content_label = "PDF"
            
            if special_content_label:
                label_item = QGraphicsTextItem(special_content_label)
                label_item.setPos(bubble.x, bubble.y + 110)
                self.scene.addItem(label_item)
            
    def show_bubble_content(self, bubble):
        # Create the ContentPopup dialog
        dialog = ContentPopup(self)

        # Show the rich text in QTextBrowser
        dialog.text_browser.setHtml(bubble.content)

        # Show YouTube video if available
        if bubble.youtube_link:
            video_id = self.extract_youtube_id(bubble.youtube_link)
            youtube_url = f"https://www.youtube.com/embed/{video_id}"
            dialog.web_view.setUrl(QUrl(youtube_url))

        # Show PDF as images if available
        if bubble.pdf_path:
            self.display_pdf_as_image_in_scene(bubble.pdf_path, dialog.pdf_scene)

        #quiz
        if bubble.is_quiz:
            self.show_quiz(bubble)

        # Show the dialog
        dialog.exec()

    def show_quiz(self, bubble):
        # Create QDialog for the quiz
        quiz_dialog = QDialog(self)
        quiz_dialog.setWindowTitle("Quiz")
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add the question (assuming it may contain HTML for multimedia)
        question_label = QLabel(bubble.quiz_question)
        layout.addWidget(question_label)
        
        # Create radio buttons for options
        radio_buttons = []
        for option in bubble.quiz_options:
            rb = QRadioButton(option)
            layout.addWidget(rb)
            radio_buttons.append(rb)
        
        # Create a Submit button
        submit_btn = QPushButton("Submit")
        layout.addWidget(submit_btn)
        
        # Connect the Submit button to evaluation logic
        submit_btn.clicked.connect(lambda: self.evaluate_quiz(bubble, radio_buttons, quiz_dialog))
        
        # Set layout and show dialog
        quiz_dialog.setLayout(layout)
        quiz_dialog.exec()

    def evaluate_quiz(self, bubble, radio_buttons, quiz_dialog):
        selected_option = None
        for i, rb in enumerate(radio_buttons):
            if rb.isChecked():
                selected_option = bubble.quiz_options[i]
                break
        
        # Update quiz performance data
        if bubble.quiz_question not in bubble.quiz_performance:
            bubble.quiz_performance[bubble.quiz_question] = {"attempts": 0, "correct": 0}
        
        self.quiz_performance[bubble.quiz_question]["attempts"] += 1
        
        # Check if the selected option is correct
        if selected_option == bubble.quiz_answer:
            self.quiz_performance[bubble.quiz_question]["correct"] += 1
            QMessageBox.information(self, "Result", "Correct!")
            quiz_dialog.accept()
        else:
            QMessageBox.warning(self, "Result", "Incorrect. Try again.")
            QTimer.singleShot(3000, lambda: self.show_quiz(bubble))  # Show the question again after 3 seconds

    def display_pdf_as_image_in_scene(self, pdf_path, scene):
        scene.clear()
        pdf_document = fitz.open(pdf_path)
        y_offset = 0
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pixmap = page.get_pixmap()
            qt_image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
            qt_pixmap = QPixmap.fromImage(qt_image)
            pixmap_item = QGraphicsPixmapItem(qt_pixmap)
            pixmap_item.setPos(0, y_offset)
            scene.addItem(pixmap_item)
            y_offset += pixmap.height

        #updating the dropdown
    def update_holder_dropdown(self):
        self.holder_combo.clear()
        self.holder_combo.addItem("Main Canvas")
        for bubble in self.bubbles:
            if bubble.is_holder:
                self.holder_combo.addItem(bubble.title)

    def update_delete_dropdown(self):
        self.delete_combo.clear()
        current_bubbles = self.current_holder.children if self.current_holder else self.bubbles  # Use current holder's children if available
        for bubble in current_bubbles:
            self.delete_combo.addItem(bubble.title)

    def calculate_distance(self, bubble1, bubble2):
        x1, y1 = bubble1.x, bubble1.y
        x2, y2 = bubble2.x, bubble2.y
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def draw_lines_between_courses(self, threshold_distance=200):
        current_bubbles = self.current_holder.children if self.current_holder else self.bubbles  # Use current holder's children if available
        for i, bubble1 in enumerate(current_bubbles):
            for j, bubble2 in enumerate(current_bubbles):
                if i >= j:  # Avoid duplicate pairs and self-connections
                    continue
                distance = self.calculate_distance(bubble1, bubble2)
                if distance <= threshold_distance:
                    line = QGraphicsLineItem(bubble1.x + 50, bubble1.y + 50, bubble2.x + 50, bubble2.y + 50)
                    self.scene.addItem(line)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CourseCreation()
    window.show()
    sys.exit(app.exec())  