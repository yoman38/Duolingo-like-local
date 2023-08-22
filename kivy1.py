from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
import PyPDF2
from kivy.uix.colorpicker import ColorPicker
from kivy.graphics import Ellipse
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Line, Color
from kivy.uix.popup import Popup
from kivy.uix.label import Label



class LearningPathApp(App):
    def build(self):
        return BoxLayout()



def load_courses_from_file():
    with open('courses.json', 'r') as file:
        return json.load(file)

def save_courses_to_file(courses):
    with open('courses.json', 'w') as file:
        json.dump(courses, file)



class CourseCreation(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.title_input = TextInput(hint_text='Enter course title')
        self.content_input = TextInput(hint_text='Enter course content', multiline=True)
        
        self.add_widget(self.title_input)
        self.add_widget(self.content_input)
        
        save_button = Button(text='Save Topic')
        save_button.bind(on_press=self.save_course)
        self.add_widget(save_button)
    
    def save_course(self, instance):
        # Logic to save course
        pass



class DraggableImage(Scatter):
    source = StringProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.center = touch.pos
            return True
        return super(DraggableImage, self).on_touch_down(touch)



def import_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def insert_youtube_link(video_id, start_time, end_time):
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)
    return f"https://www.youtube.com/watch?v={video_id}&t={start_seconds}&end={end_seconds}"



def choose_color():
    picker = ColorPicker()
    # You can bind to picker's color property to get the selected color
    return picker.color



class BubblePreview(Widget):
    def render_preview(self, x, y, color):
        with self.canvas:
            Color(*color)
            Ellipse(pos=(x, y), size=(50, 50))



class LearningPathApp(App):
    courses = {}  # Assuming courses is a dictionary
    delete_dropdown = DropDown()

    def delete_selected_bubble(self, instance):
        selected_bubble = self.delete_dropdown.text
        if selected_bubble in self.courses:
            del self.courses[selected_bubble]
            # Save and reload courses (this part depends on your implementation)
            self.reload_courses()
            self.render_preview()

    def reload_courses(self):
        # Implement your logic to reload courses
        pass

    def render_preview(self):
        # Implement your logic to render the preview
        pass

    def build(self):
        course_frame = BoxLayout(orientation='vertical')
        delete_button = Button(text="Delete Selected Bubble")
        delete_button.bind(on_press=self.delete_selected_bubble)
        course_frame.add_widget(delete_button)
        return course_frame

    course_title_input = TextInput(hint_text="Course Title")
    course_content_textarea = TextInput(hint_text="Course Content", multiline=True)
    x_coord_input = TextInput(hint_text="X Coordinate")
    y_coord_input = TextInput(hint_text="Y Coordinate")
    # Assuming you have bubble_type_dropdown and main_bubble_dropdown as DropDown widgets

    def clear_course_creation(self, instance):
        self.course_title_input.text = ''
        self.course_content_textarea.text = ''
        self.x_coord_input.text = ''
        self.y_coord_input.text = ''
        self.bubble_type_dropdown.text = 'Select Bubble Type'
        self.main_bubble_dropdown.text = 'Select Main Bubble'

    def build(self):
        course_frame = BoxLayout(orientation='vertical')
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.clear_course_creation)
        course_frame.add_widget(cancel_button)
        return course_frame

    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5



class CourseBubble(Widget):
    def render_preview(self):
        with self.canvas:
            # Draw main bubbles
            for main_bubble in self.courses.get('main_bubbles', []):
                Color(*main_bubble['color'])
                Ellipse(pos=main_bubble['position'], size=(50, 50))
                # Draw sub-courses inside the main bubble
                for sub_course in main_bubble.get('sub_courses', []):
                    Color(*sub_course['color'])
                    Ellipse(pos=sub_course['position'], size=(30, 30))
                    # Draw a line connecting the main bubble and sub-course
                    Line(points=[main_bubble['position'][0], main_bubble['position'][1], sub_course['position'][0], sub_course['position'][1]])



class CourseBubble(Widget):
    course_title_input = TextInput(hint_text="Course Title")
    course_content_textarea = TextInput(hint_text="Course Content", multiline=True)
    # Assuming you have other input fields and dropdowns for position, properties, etc.

    def save_topic(self, instance):
        course_data = {
            'title': self.course_title_input.text,
            'content': self.course_content_textarea.text,
            # Add other properties like position, type, etc.
        }
        if self.bubble_type_dropdown.text == 'Course Bubble':
            # Save as a sub-course inside the selected main bubble
            main_bubble = self.main_bubble_dropdown.text
            self.courses[main_bubble]['sub_courses'].append(course_data)
        else:
            # Save as a main bubble
            self.courses['main_bubbles'].append(course_data)
        
        # Clear the input fields
        self.course_title_input.text = ''
        self.course_content_textarea.text = ''
        # Refresh the preview canvas and dropdown lists
        self.render_preview()
        self.update_dropdowns()


class CourseBubble(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.course_frame = BoxLayout(orientation='vertical')
        save_button = Button(text="Save Topic")
        save_button.bind(on_press=self.save_topic)
        self.course_frame.add_widget(save_button)



class LearningPathApp(BoxLayout):
    courses = {}  # Assuming courses is a dictionary
    course_title_input = TextInput(hint_text="Course Title")
    course_content_textarea = TextInput(hint_text="Course Content", multiline=True)

    def delete_course(self, instance):
        course_title = self.course_title_input.text
        if course_title in self.courses:
            del self.courses[course_title]
            # Save and reload courses (this part depends on your implementation)
            self.reload_courses()
            self.course_title_input.text = ''
            self.course_content_textarea.text = ''


class LearningPathApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        delete_button = Button(text="Delete Course")
        delete_button.bind(on_press=self.delete_course)
        self.add_widget(delete_button)


class LearningPathApp(BoxLayout):
    def display_course_content(self, title, details):
        if details['type'] == 'course':
            popup = Popup(title=title, content=Label(text=details['content']), size_hint=(0.8, 0.8))
            popup.open()
        elif details['type'] == 'main':
            # Implement logic to display sub-courses in a canvas
            pass

class LearningPathApp(BoxLayout):
    def display_learning_path(self):
        # Implement logic to display the entire learning path in a new window
        pass

class LearningPathApp(BoxLayout):
    def bind_bubble(self, title, details):
        # Implement logic to bind a bubble to its content
        pass


class LearningPathApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        view_path_button = Button(text="View Path")
        view_path_button.bind(on_press=self.display_learning_path)
        self.add_widget(view_path_button)


from kivy.app import App

class MainApp(App):
    def build(self):
        return LearningPathApp()

if __name__ == "__main__":
    MainApp().run()
