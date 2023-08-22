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

# Course Creation Class
class CourseCreation(BoxLayout):
    def __init__(self, preview_window, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.preview_window = preview_window  # Store the reference to the preview window
   
        
        self.title_input = TextInput(hint_text='Enter course title', size_hint_y=0.2)
        self.content_input = TextInput(hint_text='Enter course content', multiline=True, size_hint_y=0.4)
        self.x_input = TextInput(hint_text='Enter x position for the bubble', size_hint_y=0.2)
        self.y_input = TextInput(hint_text='Enter y position for the bubble', size_hint_y=0.2)
        self.color_picker = ColorPicker(size_hint_y=0.6)
        
        self.title_input.bind(text=self.update_preview)
        self.x_input.bind(text=self.update_preview)
        self.y_input.bind(text=self.update_preview)
        
        self.add_widget(self.title_input)
        self.add_widget(self.content_input)
        self.add_widget(self.x_input)
        self.add_widget(self.y_input)
        self.add_widget(self.color_picker)
        
        save_button = Button(text='Save Topic', size_hint_y=0.2)
        save_button.bind(on_press=self.save_course)
        self.add_widget(save_button)

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
        self.draw_courses()

    def draw_courses(self):
        self.canvas.clear()
        courses = self.courses
        
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
        
        return tab_panel

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