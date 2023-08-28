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
from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image

import json
import os
import math
import re


class TextSegment:
    def __init__(self, word, styles=None):
        self.word = word
        self.styles = styles or {}

    def apply_style(self, key, value):
        self.styles[key] = value

    def to_dict(self):
        return {"word": self.word, "styles": self.styles}

    @classmethod
    def from_dict(cls, data):
        return cls(data["word"], data.get("styles", {}))


# File path
FILE_PATH = r'C:\Users\gbray\Documents\webapp_physics\courses.json'

# File Operations
def load_courses_from_file():
    if not os.path.exists(FILE_PATH):
        save_courses_to_file([])
    
    with open(FILE_PATH, 'r') as file:
        courses = json.load(file)
        return [course for course in courses if isinstance(course, dict)]


def parse_kivy_markup(text):
    """
    Parse Kivy markup to extract styles and content.
    
    Args:
    - text (str): The text containing Kivy markup.
    
    Returns:
    - List[Dict]: A list of dictionaries where each dictionary represents a segment of text and its associated styles.
    """
    # Regular expressions for different styles
    font_pattern = re.compile(r'\[font=(.*?)\](.*?)\[/font\]')
    color_pattern = re.compile(r'\[color=(.*?)\](.*?)\[/color\]')
    size_pattern = re.compile(r'\[size=(.*?)\](.*?)\[/size\]')
    bg_pattern = re.compile(r'\[bg=(.*?)\](.*?)\[/bg\]')
    bold_pattern = re.compile(r'\[b\](.*?)\[/b\]')
    
    segments = []
    
    # Split text by spaces to analyze each word
    for word in text.split():
        styles = {}
        
        # Check and extract font
        font_match = font_pattern.search(word)
        if font_match:
            styles['font'] = font_match.group(1)
            word = font_match.group(2)
        
        # Check and extract color
        color_match = color_pattern.search(word)
        if color_match:
            styles['color'] = color_match.group(1)
            word = color_match.group(2)
        
        # Check and extract size
        size_match = size_pattern.search(word)
        if size_match:
            styles['size'] = size_match.group(1)
            word = size_match.group(2)
        
        # Check and extract background color (highlight)
        bg_match = bg_pattern.search(word)
        if bg_match:
            styles['bg'] = bg_match.group(1)
            word = bg_match.group(2)
        
        # Check for bold
        bold_match = bold_pattern.search(word)
        if bold_match:
            styles['bold'] = True
            word = bold_match.group(1)
        
        segments.append({'word': word, 'styles': styles})
    
    return segments


def save_courses_to_file(courses):
    with open(FILE_PATH, 'w') as file:
        
        for course in courses:
            if "content" in course:
                course["content"] = parse_kivy_markup(course["content"])
        json.dump(courses, file)
    

# Draggable Image class
class DraggableImage(DragBehavior, Image):
    def __init__(self, **kwargs):
        super(DraggableImage, self).__init__(**kwargs)
        self.drag_distance = 0  # Set drag_distance to 0 to make it draggable from any position

# Custom TextInput class to handle dropped images
class CustomTextInput(TextInput):
    def on_drop(self, drop_widget):
        if isinstance(drop_widget, DraggableImage):
            self.text += "[Image Here]"    

class TextCustomizationToolbar(BoxLayout):
    def show_color_picker(self, instance):
        color_popup = Popup(title="Select Color", content=self.color_picker, size_hint=(0.6, 0.6))
        self.color_picker.bind(color=color_popup.dismiss)  # Close the popup once a color is selected
        color_popup.open()

    def __init__(self, text_input, **kwargs):
        super().__init__(**kwargs)
        self.text_input = text_input
        self.size_hint_y = 0.1
        self.spacing = 10

        # Placeholder for font icon
        font_icon = Button(text="F", size_hint_x=None, width=40)
        font_icon.bind(on_press=self.show_font_options)
        self.add_widget(font_icon)

        # Placeholder for color icon
        color_icon = Button(text="C", size_hint_x=None, width=40)
        color_icon.bind(on_press=self.show_color_picker)
        self.add_widget(color_icon)

        # Placeholder for font size selection
        font_size_icon = Spinner(text='12', values=('10', '12', '14', '16', '18', '20'), size_hint_x=None, width=60)
        font_size_icon.bind(text=self.set_font_size)
        self.add_widget(font_size_icon)

        # Placeholder for highlight text
        bold_icon = Button(text="B", size_hint_x=None, width=40)
        bold_icon.bind(on_press=self.bold_text)
        self.add_widget(bold_icon)

        # Initialize the color picker attribute
        self.color_picker = ColorPicker()

    def show_font_options(self, instance):
        font_spinner = Spinner(text=self.text_input.font_name, values=('Roboto', 'Arial', 'Times New Roman'))
        font_popup = Popup(title="Select Font", content=font_spinner, size_hint=(0.4, 0.4))
        font_spinner.bind(text=self.set_font)
        font_popup.open()

    
    def set_font(self, spinner, font_name):
        # Splitting the text into segments
        segments = [TextSegment(word) for word in self.text_input.text.split()]
        
        # Applying the font style to the selected segment
        selected_segment_index = self.text_input.cursor[0]  # Assuming cursor position determines the selected word
        segments[selected_segment_index].apply_style('font', font_name)
        
        # Recombining the segments back into the text
        self.text_input.text = ' '.join(segment.word for segment in segments)
        self.text_input.markup = True  # This line might need adjustments when other styles are applied

        selected_text = self.text_input.selection_text
        if selected_text:
            self.text_input.delete_selection()
            self.text_input.insert_text(f'[font={font_name}]{selected_text}[/font]')
        self.text_input.markup = True

    
    def set_text_color(self, picker, color):
        # Splitting the text into segments
        segments = [TextSegment.from_dict(data) for data in json.loads(self.text_input.text)]
        
        # Determining which segments are selected based on text selection
        start, end = self.text_input.selection_from, self.text_input.selection_to
        for i in range(len(segments)):
            segment_start = sum(len(segment.word) for segment in segments[:i]) + i  # +i for spaces
            segment_end = segment_start + len(segments[i].word)
            if start <= segment_start < end or start < segment_end <= end:
                hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]*255), int(color[1]*255), int(color[2]*255))
                segments[i].apply_style('color', hex_color)
        
        # Recombining the segments back into the text
        self.text_input.text = json.dumps([segment.to_dict() for segment in segments])

        selected_text = self.text_input.selection_text
        if selected_text:
            hex_color = "#{:02x}{:02x}{:02x}".format(int(color[0]*255), int(color[1]*255), int(color[2]*255))
            self.text_input.delete_selection()
            self.text_input.insert_text(f'[color={hex_color}]{selected_text}[/color]')
        self.text_input.markup = True

    
    def set_font_size(self, spinner, font_size):
        # Splitting the text into segments
        segments = [TextSegment.from_dict(data) for data in json.loads(self.text_input.text)]
        
        # Determining which segments are selected based on text selection
        start, end = self.text_input.selection_from, self.text_input.selection_to
        for i in range(len(segments)):
            segment_start = sum(len(segment.word) for segment in segments[:i]) + i  # +i for spaces
            segment_end = segment_start + len(segments[i].word)
            if start <= segment_start < end or start < segment_end <= end:
                segments[i].apply_style('font_size', font_size)
        
        # Recombining the segments back into the text
        self.text_input.text = json.dumps([segment.to_dict() for segment in segments])

        selected_text = self.text_input.selection_text
        if selected_text:
            self.text_input.delete_selection()
            self.text_input.insert_text(f'[size={font_size}]{selected_text}[/size]')
        self.text_input.markup = True

    
    def bold_text(self, instance):
        # Splitting the text into segments
        segments = [TextSegment.from_dict(data) for data in json.loads(self.text_input.text)]
        
        # Determining which segments are selected based on text selection
        start, end = self.text_input.selection_from, self.text_input.selection_to
        for i in range(len(segments)):
            segment_start = sum(len(segment.word) for segment in segments[:i]) + i  # +i for spaces
            segment_end = segment_start + len(segments[i].word)
            if start <= segment_start < end or start < segment_end <= end:
                segments[i].apply_style('bold', True)
        
        # Recombining the segments back into the text
        self.text_input.text = json.dumps([segment.to_dict() for segment in segments])

        selected_text = self.text_input.selection_text
        if selected_text:
            self.text_input.delete_selection()
            self.text_input.insert_text(f'[b]{selected_text}[/b]')
        self.text_input.markup = True




# Course Creation Class
class CourseCreation(BoxLayout):
    def __init__(self, preview_window, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.preview_window = preview_window

        # Spinner for bubble type
        self.bubble_type = Spinner(text='Main', values=('Main', 'Course'), size_hint_y=0.2)
        self.main_bubble_dropdown = Spinner(text='None', values=self.get_main_bubbles(), size_hint_y=0.2)
   

        self.title_input = TextInput(hint_text='Enter course title', size_hint_y=0.2)
        self.content_input = TextInput(hint_text='Enter course content', multiline=True, size_hint_y=0.4)
        self.content_input.markup = True
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

        # Set markup property after object creation
        self.title_input.markup = True
        self.content_input.markup = True

        # Now create the TextCustomizationToolbar instance
        self.text_customization_toolbar = TextCustomizationToolbar(text_input=self.content_input)
        self.add_widget(self.text_customization_toolbar)

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
        
        try:
            x = int(self.x_input.text)
            y = int(self.y_input.text)
        except ValueError:
            # Show an error popup to the user
            error_popup = Popup(title="Error", content=Label(text="Please enter valid x and y coordinates."), size_hint=(0.6, 0.3))
            error_popup.open()
            return
        color = self.color_picker.color[:3]
        bubble_type = self.bubble_type.text
        main_bubble = self.main_bubble_dropdown.text if self.main_bubble_dropdown.text != 'None' else None

        # Extract font, color, size, etc. from the content text
        content_style = {
            'font': self.content_input.font_name,
            'font_size': self.content_input.font_size,
            'color': self.content_input.foreground_color
        }

        courses = load_courses_from_file()
        courses.append({
            'title': course_title, 'content': course_content, 'x': x, 'y': y, 
            'color': color, 'type': bubble_type, 'main_bubble': main_bubble,
            'content_style': content_style
        })
        save_courses_to_file(courses)

        # Update the main bubble dropdown options
        self.main_bubble_dropdown.values = self.get_main_bubbles()
        
        self.title_input.text = ''
        self.content_input.text = ''
        self.x_input.text = ''
        self.y_input.text = ''
        
        # Refresh the preview after saving
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


    def delete_selected_bubble(self, instance):
        # Get the currently selected bubble title from the list
        selected_bubble_title = self.bubble_list.text
        
        # Remove this bubble from the courses list
        self.courses = [course for course in self.courses if course['title'] != selected_bubble_title]
        
        # Save the updated list to the JSON file
        save_courses_to_file(self.courses)
        
        # Redraw the interface
        self.draw_courses()
        # Bubble Deletion
        self.bubble_list = Spinner(text='Select a bubble', values=self.get_all_bubbles(), size_hint_y=0.2)
        self.add_widget(self.bubble_list)
        
        delete_button = Button(text='Delete Selected Bubble', size_hint_y=0.2)
        delete_button.bind(on_press=self.delete_selected_bubble)
        self.add_widget(delete_button)

    def get_all_bubbles(self):
        return [course['title'] for course in load_courses_from_file()]
    
    def draw_courses(self):
        self.canvas.clear()
        courses = load_courses_from_file()  # Only draw courses from the JSON
        
        # If there are no courses, return immediately
        if not courses:
            return
        
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
                    content = course.get('content', 'No content available')
                    popup = Popup(title=course['title'], content=Label(text=content, text_size=(300, None)), size_hint=(0.8, 0.8))
                    popup.open()
                break
        return super().on_touch_down(touch)
    
    def get_all_bubbles(self):
        return [course['title'] for course in load_courses_from_file()]

    def delete_selected_bubble(self, instance):
        selected_bubble = self.bubble_list.text
        courses = load_courses_from_file()
        courses = [course for course in courses if course['title'] != selected_bubble]
        save_courses_to_file(courses)
        self.bubble_list.values = self.get_all_bubbles()
        self.preview_window.draw_courses()


class LearningPathApp(App):
    def build(self):
        # Main layout with tabs
        tab_panel = TabbedPanel(do_default_tab=False)
        
        # Create an instance of CourseCanvas first without the preview_window attribute
        self.preview_window = CourseCanvas(size_hint_y=0.7)
        
        # Now, set the preview_window attribute
        self.preview_window.preview_window = self.preview_window

        # Course Creation Tab
        course_creation_tab = TabbedPanelItem(text="Course Creation")
        course_creation_layout = BoxLayout(orientation='vertical')
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