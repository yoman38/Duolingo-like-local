from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color, Line, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooser
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.videoplayer import VideoPlayer
from pdf2image import convert_from_path
from kivy.core.window import Window
import PyPDF2
import json
import os
import math

# File Operations
def load_courses_from_file():
    if not os.path.exists('courses.json'):
        save_courses_to_file([])
    
    with open('courses.json', 'r') as file:
        courses = json.load(file)
        return [course for course in courses if isinstance(course, dict)]

def save_courses_to_file(courses):
    with open('courses.json', 'w') as file:
        json.dump(courses, file)

class ImageDropTarget(Image):  # Removed FileDropEntry
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.4
        self.allow_stretch = True

    def on_dropfile(self, filename):
        # Set the source of the Image widget to the dropped file
        self.source = filename[0]


class PDFImporter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Replace FileChooserIconView with a button
        self.browse_button = Button(text="Browse PDF", size_hint_y=0.2)
        self.browse_button.bind(on_press=self.browse_pdf)
        self.add_widget(self.browse_button)
        
        import_button = Button(text="Import PDF", size_hint_y=0.2)
        import_button.bind(on_press=self.import_pdf)
        self.add_widget(import_button)
        
    def browse_pdf(self, instance):
        filechooser = FileChooser(title="Choose a PDF", filters=['*.pdf'])
        filechooser.bind(on_submit=self.load_pdf)
        popup = Popup(title="Choose a PDF", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()

    def load_pdf(self, instance, selection, touch):
        if selection:
            self.pdf_file = selection[0]
            # Close the file chooser popup
            instance.parent.dismiss()
        
    def import_pdf(self, instance):
        if self.file_chooser.selection:
            pdf_file = self.file_chooser.selection[0]
            # Convert the PDF to an image
            images = convert_from_path(pdf_file)
            # For simplicity, we'll just use the first page of the PDF
            image_path = "temp_image.jpg"
            images[0].save(image_path, "JPEG")
            # Display the converted image in the ImageDropTarget widget
            self.parent.image_drop_target.source = image_path

class YouTubeInserterButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Click here to insert YouTube video"
        self.bind(on_press=self.open_popup)

    def open_popup(self, instance):
        content = YouTubeInserter()
        self.popup = Popup(title="Insert YouTube Video", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def insert_video(self, instance):
        link = self.link_input.text
        start_time = int(self.start_time_input.text or 0)
        end_time = int(self.end_time_input.text or 0)
        # Set the source of the VideoPlayer widget to the YouTube link
        self.video_player.source = link
        # Set the start and end times for the video
        self.video_player.seek(start_time)
        # Note: The VideoPlayer widget doesn't support setting an end time directly,
        # so you might need to implement a custom solution for that

# Course Creation Class
class CourseCreation(BoxLayout):
    def __init__(self, preview_window, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.preview_window = preview_window

        # Spinner for bubble type
        self.bubble_type = Spinner(text='Main', values=('Main', 'Course'), size_hint_y=0.2)
        self.main_bubble_dropdown = Spinner(text='None', values=self.get_main_bubbles(), size_hint_y=0.2)

        #draganddrop
        self.image_drop_target = ImageDropTarget()
        self.add_widget(self.image_drop_target)
        
        #pdf
        self.pdf_importer = PDFImporter()
        self.add_widget(self.pdf_importer)
       
        # Replace YouTubeInserter with YouTubeInserterButton
        self.youtube_button = YouTubeInserterButton(size_hint_y=0.2)
        self.add_widget(self.youtube_button)
        
        self.title_input = TextInput(hint_text='Enter course title', size_hint_y=0.2)
        self.content_input = TextInput(hint_text='Enter course content', multiline=True, size_hint_y=0.4)
        self.x_input = TextInput(hint_text='Enter x position for the bubble', size_hint_y=0.2)
        self.y_input = TextInput(hint_text='Enter y position for the bubble', size_hint_y=0.2)
        self.color_picker = ColorPicker(size_hint_y=0.6)
        
        self.title_input.bind(text=self.update_preview)
        self.x_input.bind(text=self.update_preview)
        self.y_input.bind(text=self.update_preview)
        
        self.title_font_input = TextInput(hint_text='Enter title font', size_hint_y=0.2)
        self.title_color_input = TextInput(hint_text='Enter title color', size_hint_y=0.2)
        self.subtitle_font_input = TextInput(hint_text='Enter subtitle font', size_hint_y=0.2)
        self.subtitle_color_input = TextInput(hint_text='Enter subtitle color', size_hint_y=0.2)

        # Add them to the layout
        self.add_widget(self.title_font_input)
        self.add_widget(self.title_color_input)
        self.add_widget(self.subtitle_font_input)
        self.add_widget(self.subtitle_color_input)

        # Set default values
        self.title_font_input.text = 'Roboto'
        self.title_color_input.text = '0,0,0,1'  # Black color
        self.subtitle_font_input.text = 'Roboto'
        self.subtitle_color_input.text = '0.5,0.5,0.5,1'  # Grey color


        self.add_widget(self.title_input)
        self.add_widget(self.content_input)
        self.add_widget(self.x_input)
        self.add_widget(self.y_input)
        self.add_widget(self.color_picker)
        self.add_widget(self.bubble_type)
        self.add_widget(self.main_bubble_dropdown)
        
        save_button = Button(text='Save Topic', size_hint_y=0.2)
        save_button.bind(on_press=self.save_course)
        self.add_widget(save_button)

    def get_main_bubbles(self):
        main_bubbles = ['None']
        for course in load_courses_from_file():
            if course.get('type') == 'Main':
                main_bubbles.append(course['title'])
            elif course.get('main_bubble'):
                main_bubbles.append('>' + course['title'])
        return main_bubbles


    def save_course(self, instance):
        course_title = self.title_input.text
        course_content = self.content_input.text
        x = int(self.x_input.text)
        y = int(self.y_input.text)
        color = self.color_picker.color[:3]
        bubble_type = self.bubble_type.text
        main_bubble = self.main_bubble_dropdown.text if self.main_bubble_dropdown.text != 'None' else None

        courses = load_courses_from_file()
        courses.append({
            'title': course_title, 'content': course_content, 'x': x, 'y': y, 
            'color': color, 'type': bubble_type, 'main_bubble': main_bubble
        })
        save_courses_to_file(courses)

        # Update the main bubble dropdown options
        self.main_bubble_dropdown.values = self.get_main_bubbles()
        
        self.title_input.text = ''
        self.content_input.text = ''
        self.x_input.text = ''
        self.y_input.text = ''
        
        self.preview_window.draw_courses()

    def update_preview(self, *args):
        # Update the preview window with the current bubble details
        course_title = self.title_input.text
        x = int(self.x_input.text or 0)
        y = int(self.y_input.text or 0)
        color = self.color_picker.color[:3]
        
        # Add the current bubble to the courses list for preview
        courses = load_courses_from_file()
        current_course = {'title': course_title, 'x': x, 'y': y, 'color': color}
        courses.append(current_course)
        
        # Update the preview window
        self.preview_window.courses = courses
        self.preview_window.draw_courses()

# Canvas Drawing and Interactions
class CourseCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.courses = load_courses_from_file()
        self.current_main_bubble = None
        self.draw_courses()

    def draw_courses(self):
        self.canvas.clear()
        courses = self.courses
        
        # Filter courses based on current main bubble
        if self.current_main_bubble:
            courses = [course for course in courses if course.get('main_bubble') == self.current_main_bubble]
        
        # Draw connections between bubbles
        for i, course1 in enumerate(courses):
            for j, course2 in enumerate(courses):
                if i != j and self.distance(course1, course2) < 150:
                    with self.canvas:
                        Color(0.5, 0.5, 0.5)
                        Line(points=[course1['x'], course1['y'], course2['x'], course2['y']])
        
        for course in courses:
            x, y = course.get('x', 0), course.get('y', 0)
            color = course.get('color', (1, 1, 1))
            with self.canvas:
                Color(*color)
                Ellipse(pos=(x-50, y-50), size=(100, 100))
                
                label = Label(text=course['title'], pos=(x-50, y-50), size=(100, 100), color=(0, 0, 0, 1))
                label.texture_update()
                Rectangle(texture=label.texture, pos=label.pos, size=label.texture_size)

    def distance(self, course1, course2):
        return math.sqrt((course1['x'] - course2['x'])**2 + (course1['y'] - course2['y'])**2)

    def on_touch_down(self, touch):
        for course in load_courses_from_file():
            x, y = course.get('x', 0), course.get('y', 0)
            if ((touch.x - x) ** 2 + (touch.y - y) ** 2) <= 50**2:
                if course.get('type') == 'Main':
                    self.current_main_bubble = course['title']
                    self.draw_courses()
                else:
                    popup = Popup(title=course['title'], content=Label(text=course.get('content', 'No content available')), size_hint=(0.8, 0.8))
                    popup.open()
                break
        return super().on_touch_down(touch)


class LearningPathApp(App):
    def build(self):
        # Main layout with tabs
        tab_panel = TabbedPanel(do_default_tab=False)
        
        # Course Creation Tab
        course_creation_tab = TabbedPanelItem(text="Course Creation")
        course_creation_layout = BoxLayout(orientation='vertical')
        
        self.preview_window = CourseCanvas(size_hint_y=0.7)
        course_creation = CourseCreation(preview_window=self.preview_window, size_hint_y=0.6)
        course_creation_layout.add_widget(course_creation)
        
        view_topic_button = Button(text="View Topic", size_hint_y=0.1)
        view_topic_button.bind(on_press=self.toggle_view)
        course_creation_layout.add_widget(view_topic_button)
        
        run_preview_button = Button(text="Run Preview", size_hint_y=0.1)
        run_preview_button.bind(on_press=self.run_preview)
        course_creation_layout.add_widget(run_preview_button)
        
        course_creation_tab.add_widget(course_creation_layout)
        tab_panel.add_widget(course_creation_tab)
        
        # User Version Tab
        user_version_tab = TabbedPanelItem(text="User Version")
        user_version_layout = BoxLayout(orientation='vertical')
        
        user_version_canvas = CourseCanvas(size_hint_y=1)
        user_version_layout.add_widget(user_version_canvas)
        
        user_version_tab.add_widget(user_version_layout)
        tab_panel.add_widget(user_version_tab)
        
        # Bind the on_dropfile event to the handle_file_drop method
        Window.bind(on_dropfile=self.handle_file_drop)
        
        return tab_panel
    
    def handle_file_drop(self, window, file_path):
        # Convert the byte string to a normal string
        file_path = file_path.decode('utf-8')
        # Check if the file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Set the source of the ImageDropTarget widget to the dropped file
            self.root.ids.image_drop_target.source = file_path


    def toggle_view(self, instance):
        if self.preview_window.parent:
            self.root.remove_widget(self.preview_window)
        else:
            self.root.add_widget(self.preview_window)

    def run_preview(self, instance):
        self.preview_window.draw_courses()
        if not self.preview_window.parent:
            self.root.add_widget(self.preview_window)

if __name__ == "__main__":
    LearningPathApp().run()