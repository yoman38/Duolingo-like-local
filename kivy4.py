from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.uix.colorpicker import ColorPicker
import json
import os

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

# Course Creation Class
class CourseCreation(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 400
        
        input_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)
        self.title_input = TextInput(hint_text='Enter course title')
        self.content_input = TextInput(hint_text='Enter course content', multiline=True)
        self.x_input = TextInput(hint_text='Enter x position for the bubble')
        self.y_input = TextInput(hint_text='Enter y position for the bubble')
        self.color_picker = ColorPicker()
        
        input_layout.add_widget(self.title_input)
        input_layout.add_widget(self.content_input)
        input_layout.add_widget(self.x_input)
        input_layout.add_widget(self.y_input)
        input_layout.add_widget(self.color_picker)
        
        save_button = Button(text='Save Topic')
        save_button.bind(on_press=self.save_course)
        input_layout.add_widget(save_button)
        
        self.preview = CourseCanvas(preview=True, size_hint_x=0.5)
        self.title_input.bind(text=self.preview.draw_courses)
        self.x_input.bind(text=self.preview.draw_courses)
        self.y_input.bind(text=self.preview.draw_courses)
        
        self.add_widget(input_layout)
        self.add_widget(self.preview)

    def save_course(self, instance):
        course_title = self.title_input.text
        course_content = self.content_input.text
        x = int(self.x_input.text)
        y = int(self.y_input.text)
        color = self.color_picker.color[:3]
        
        courses = load_courses_from_file()
        courses.append({'title': course_title, 'content': course_content, 'x': x, 'y': y, 'color': color})
        save_courses_to_file(courses)
        
        self.title_input.text = ''
        self.content_input.text = ''
        self.x_input.text = ''
        self.y_input.text = ''

# Canvas Drawing and Interactions
class CourseCanvas(Widget):
    def __init__(self, preview=False, **kwargs):
        super().__init__(**kwargs)
        self.courses = load_courses_from_file()
        self.preview = preview
        self.bind(parent=self.draw_courses)
    
    def draw_courses(self, *args):
        self.canvas.clear()
        courses = self.courses
        if self.preview and self.parent:
            x = int(self.parent.x_input.text or 0)
            y = int(self.parent.y_input.text or 0)
            color = self.parent.color_picker.color[:3]
            title = self.parent.title_input.text
            courses.append({'title': title, 'x': x, 'y': y, 'color': color})
        
        for course in courses:
            x, y = course.get('x', 0), course.get('y', 0)
            color = course.get('color', (1, 1, 1))
            with self.canvas:
                Color(*color)
                Ellipse(pos=(x-50, y-50), size=(100, 100))
                
                core_label = CoreLabel(text=course['title'], font_size=14, color=(0, 0, 0, 1))
                core_label.refresh()
                texture = core_label.texture
                texture_size = list(texture.size)
                Rectangle(texture=texture, pos=(x - texture_size[0] / 2, y - texture_size[1] / 2), size=texture_size)

    def on_touch_down(self, touch):
        for course in self.courses:
            x, y = course.get('x', 0), course.get('y', 0)
            if ((touch.x - x) ** 2 + (touch.y - y) ** 2) <= 25**2:
                popup = Popup(title=course['title'], content=Label(text=course.get('content', 'No content available')), size_hint=(0.8, 0.8))
                popup.open()
                break
        return super().on_touch_down(touch)

class LearningPathApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')
        
        toggle_button = Button(text='Toggle View')
        toggle_button.bind(on_press=self.toggle_view)
        main_layout.add_widget(toggle_button)
        
        self.current_view = CourseCreation()
        main_layout.add_widget(self.current_view)
        
        return main_layout
    
    def toggle_view(self, instance):
        if isinstance(self.current_view, CourseCreation):
            new_view = CourseCanvas()
        else:
            new_view = CourseCreation()
        
        self.root.remove_widget(self.current_view)
        self.root.add_widget(new_view)
        self.current_view = new_view

if __name__ == "__main__":
    LearningPathApp().run()
