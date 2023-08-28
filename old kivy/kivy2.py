from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color
from kivy.uix.widget import Widget
import json
import os

# File Operations
def load_courses_from_file():
    # Check if the file exists
    if not os.path.exists('courses.json'):
        # If the file doesn't exist, create an empty list and save it to the file
        save_courses_to_file([])
    
    with open('courses.json', 'r') as file:
        return json.load(file)

def save_courses_to_file(courses):
    with open('courses.json', 'w') as file:
        json.dump(courses, file)

# Course Creation Class
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
        course_title = self.title_input.text
        course_content = self.content_input.text
        
        courses = load_courses_from_file()
        courses.append({'title': course_title, 'content': course_content})
        save_courses_to_file(courses)
        
        self.title_input.text = ''
        self.content_input.text = ''

# Canvas Drawing and Interactions
class CourseCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.courses = load_courses_from_file()
        self.draw_courses()
    
    def draw_courses(self):
        for course in self.courses:
            x, y = course.get('x', 0), course.get('y', 0)
            with self.canvas:
                Color(1, 1, 1, 1)
                Ellipse(pos=(x, y), size=(50, 50))

    def on_touch_down(self, touch):
        for course in self.courses:
            x, y = course.get('x', 0), course.get('y', 0)
            if ((touch.x - x) ** 2 + (touch.y - y) ** 2) <= 25**2:
                print(course.get('content', 'No content available'))
                break
        return super().on_touch_down(touch)

class LearningPathApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')
        
        # Add a toggle button to switch between CourseCreation and CourseCanvas views
        toggle_button = Button(text='Toggle View')
        toggle_button.bind(on_press=self.toggle_view)
        main_layout.add_widget(toggle_button)
        
        # Initially show the CourseCreation view
        self.current_view = CourseCreation()
        main_layout.add_widget(self.current_view)
        
        return main_layout
    
    def toggle_view(self, instance):
        # Switch between CourseCreation and CourseCanvas views
        if isinstance(self.current_view, CourseCreation):
            new_view = CourseCanvas()
        else:
            new_view = CourseCreation()
        
        # Replace the current view with the new one
        self.root.remove_widget(self.current_view)
        self.root.add_widget(new_view)
        self.current_view = new_view

if __name__ == "__main__":
    LearningPathApp().run()

