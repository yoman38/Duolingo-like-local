import tkinter as tk
from tkinter import ttk, colorchooser, simpledialog, Toplevel, messagebox, filedialog, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
import json
from PIL import Image, ImageTk, ImageGrab
import fitz
import webbrowser
import os

# Absolute path to courses.json
COURSES_PATH = "C:\\Users\\gbray\\Documents\\webapp_physics\\courses.json"

# Load courses from JSON
def load_courses():
    try:
        with open(COURSES_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(COURSES_PATH, 'w') as file:
            json.dump({}, file)
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the courses: {e}")
        return {}

courses = load_courses()

# Save courses to JSON
def save_courses():
    try:
        with open(COURSES_PATH, 'w') as file:
            json.dump(courses, file)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the courses: {e}")


# Initialize main window
root = TkinterDnD.Tk()
root.title("Course Creation Tool")

# Course Creation Frame
course_frame = ttk.LabelFrame(root, text="Course Creation")
course_frame.pack(pady=20, padx=20, fill="x")

# Course Title
ttk.Label(course_frame, text="Course Title:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
title_entry = ttk.Entry(course_frame, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=5)
title_entry.bind("<KeyRelease>", lambda e: render_preview())

# Course Content
ttk.Label(course_frame, text="Course Content:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
content_text = scrolledtext.ScrolledText(course_frame, width=30, height=5)
content_text.grid(row=1, column=1, padx=5, pady=5)

# Drag and drop images
def drop(event):
    file_path = event.data
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)
    content_text.image_create(tk.END, image=photo)
    content_text.photo = photo

content_text.drop_target_register('DND_Files')
content_text.dnd_bind('<<Drop>>', drop)

# Import PDF
def import_pdf():
    file_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        content_text.insert(tk.END, text + "\n---\n")

pdf_button = ttk.Button(course_frame, text="Import PDF", command=import_pdf)
pdf_button.grid(row=2, column=0, padx=5, pady=5)

chosen_color = tk.StringVar(value="light blue")

# Convert hh:mm:ss to seconds
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

# Insert YouTube link
def insert_youtube_link():
    link = youtube_link_entry.get()
    start_time = time_to_seconds(start_time_entry.get())
    end_time = time_to_seconds(end_time_entry.get())
    formatted_link = f"{link}?start={start_time}&end={end_time}"
    content_text.insert(tk.END, f"\n[YouTube: {formatted_link}]\n")
    webbrowser.open(formatted_link)


# Bubble Type
ttk.Label(course_frame, text="Bubble Type:").grid(row=11, column=0, sticky="w", padx=5, pady=5)
bubble_type = ttk.Combobox(course_frame, values=["Main Bubble", "Course Bubble"], state="readonly")
bubble_type.grid(row=11, column=1, padx=5, pady=5)
bubble_type.set("Course Bubble")  # Default value

# Main Bubble Selection
ttk.Label(course_frame, text="Inside Main Bubble:").grid(row=12, column=0, sticky="w", padx=5, pady=5)
main_bubble_selection = ttk.Combobox(course_frame, values=[main for main, details in courses.items() if details['type'] == 'main'], state="readonly")
main_bubble_selection.grid(row=12, column=1, padx=5, pady=5)


#
ttk.Label(course_frame, text="YouTube Link:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
youtube_link_entry = ttk.Entry(course_frame, width=30)
youtube_link_entry.grid(row=7, column=1, padx=5, pady=5)

ttk.Label(course_frame, text="Start Time (hh:mm:ss):").grid(row=8, column=0, sticky="w", padx=5, pady=5)
start_time_entry = ttk.Entry(course_frame, width=10)
start_time_entry.grid(row=8, column=1, sticky="w", padx=5, pady=5)

ttk.Label(course_frame, text="End Time (hh:mm:ss):").grid(row=9, column=0, sticky="w", padx=5, pady=5)
end_time_entry = ttk.Entry(course_frame, width=10)
end_time_entry.grid(row=9, column=1, sticky="w", padx=5, pady=5)

youtube_button = ttk.Button(course_frame, text="Insert YouTube Link", command=insert_youtube_link)
youtube_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    chosen_color.set(color_code)
    render_preview()

color_button = ttk.Button(course_frame, text="Choose Bubble Color", command=choose_color)
color_button.grid(row=3, column=0, padx=5, pady=5)

# X and Y coordinates
ttk.Label(course_frame, text="X-coordinate:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
x_entry = ttk.Entry(course_frame, width=10)
x_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
x_entry.bind("<KeyRelease>", lambda e: render_preview())

ttk.Label(course_frame, text="Y-coordinate:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
y_entry = ttk.Entry(course_frame, width=10)
y_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
y_entry.bind("<KeyRelease>", lambda e: render_preview())

# Preview Canvas
preview_canvas = tk.Canvas(course_frame, bg="white", width=200, height=200)
preview_canvas.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

# Dropdown to select a bubble for deletion
ttk.Label(course_frame, text="Delete Bubble:").grid(row=13, column=0, sticky="w", padx=5, pady=5)
delete_dropdown = ttk.Combobox(course_frame, values=list(courses.keys()), state="readonly")
delete_dropdown.grid(row=13, column=1, padx=5, pady=5)

def delete_selected_bubble():
    global courses
    selected_bubble = delete_dropdown.get()
    if selected_bubble in courses:
        del courses[selected_bubble]
        save_courses()
        courses = load_courses()  # Reload courses after deleting
        # Refresh the dropdown list
        delete_dropdown['values'] = list(courses.keys())
        delete_dropdown.set('')
        # Refresh the main bubble selection dropdown
        main_bubble_selection['values'] = [main for main, details in courses.items() if details['type'] == 'main']
        main_bubble_selection.set('')
        render_preview()

delete_selected_button = ttk.Button(course_frame, text="Delete Selected Bubble", command=delete_selected_bubble)
delete_selected_button.grid(row=14, column=0, columnspan=2, padx=5, pady=5)

def clear_course_creation():
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)
    bubble_type.set("Course Bubble")
    main_bubble_selection.set('')

# Add a "Cancel" button to clear the course creation fields
cancel_button = ttk.Button(course_frame, text="Cancel", command=clear_course_creation)
cancel_button.grid(row=15, column=0, columnspan=2, padx=5, pady=5)

def calculate_distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5


def render_preview(event=None):
    title = title_entry.get()
    x = int(x_entry.get()) if x_entry.get().isdigit() else 100
    y = int(y_entry.get()) if y_entry.get().isdigit() else 100
    color = chosen_color.get()
    preview_canvas.delete("bubble")  # Clear all bubbles
    
    main_bubble = main_bubble_selection.get()
    if main_bubble:
        # If a main bubble is selected, only show that bubble and its sub-courses
        details = courses[main_bubble]
        cx, cy = details['x'], details['y']
        ccolor = details['color']
        preview_canvas.create_oval(cx-30, cy-30, cx+30, cy+30, fill=ccolor, tags="bubble")
        preview_canvas.create_text(cx, cy, text=main_bubble, tags="bubble")
        
        if 'sub_courses' in details:
            for sub_title, sub_details in details['sub_courses'].items():
                sub_x, sub_y = sub_details['x'], sub_details['y']
                sub_color = sub_details['color']
                preview_canvas.create_oval(sub_x-20, sub_y-20, sub_x+20, sub_y+20, fill=sub_color, tags="bubble")
                preview_canvas.create_text(sub_x, sub_y, text=sub_title, tags="bubble")
    else:
        # If no main bubble is selected, show all main bubbles
        for course_title, details in courses.items():
            if details['type'] == 'main':
                cx, cy = details['x'], details['y']
                ccolor = details['color']
                preview_canvas.create_oval(cx-30, cy-30, cx+30, cy+30, fill=ccolor, tags="bubble")
                preview_canvas.create_text(cx, cy, text=course_title, tags="bubble")
    
    # Link bubbles that are near each other
    threshold_distance = 70  # You can adjust this value as needed
    for course_title, details in courses.items():
        cx, cy = details['x'], details['y']
        if calculate_distance(x, y, cx, cy) <= threshold_distance:
            preview_canvas.create_line(x, y, cx, cy, fill="gray", tags="link")
    
    # Display the current course title and position as a bubble on the preview canvas
    preview_canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags="current_bubble")
    preview_canvas.create_text(x, y, text=title, tags="current_bubble")


title_entry.bind("<KeyRelease>", render_preview)
x_entry.bind("<KeyRelease>", render_preview)
y_entry.bind("<KeyRelease>", render_preview)

def save_topic():
    global courses
    title = title_entry.get()
    content = content_text.get("1.0", tk.END).strip()
    x = int(x_entry.get())
    y = int(y_entry.get())
    color = chosen_color.get()
    bubble_choice = bubble_type.get()
    inside_main_bubble = main_bubble_selection.get()
    
    if title and content:
        course_data = {
            'content': content,
            'x': x,
            'y': y,
            'color': color,
            'type': 'course' if bubble_choice == "Course Bubble" else 'main'
        }
        
        if bubble_choice == "Course Bubble" and inside_main_bubble:
            if 'sub_courses' not in courses[inside_main_bubble]:
                courses[inside_main_bubble]['sub_courses'] = {}
            courses[inside_main_bubble]['sub_courses'][title] = course_data
        else:
            courses[title] = course_data
        
        save_courses()
        courses = load_courses()  # Reload courses after saving
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        render_preview() # Refresh the preview after saving
   
    # Refresh the dropdown list after saving
    delete_dropdown['values'] = list(courses.keys())
    # Refresh the main bubble selection dropdown
    main_bubble_selection['values'] = [main for main, details in courses.items() if details['type'] == 'main']


save_button = ttk.Button(course_frame, text="Save Topic", command=save_topic)
save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

def delete_course():
    global courses  # Declare courses as global at the beginning
    title = title_entry.get()
    if title in courses:
        del courses[title]
        save_courses()
        courses = load_courses()  # Reload courses after deleting
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)

delete_button = ttk.Button(course_frame, text="Delete Course", command=delete_course)
delete_button.grid(row=6, column=2, padx=5, pady=5)

def display_course_content(title, details):
    if details['type'] == 'course':
        # Display course content
        content_window = tk.Toplevel(root)
        content_window.title(f"Content for {title}")
        content_display = scrolledtext.ScrolledText(content_window, width=50, wrap=tk.WORD)
        content_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        content_display.insert(tk.END, details['content'])
        content_display.config(state=tk.DISABLED)
    elif details['type'] == 'main':
        # Display courses under the main bubble
        sub_learning_window = Toplevel(root)
        sub_learning_window.title(f"Sub Learning Path for {title}")
        sub_learning_canvas = tk.Canvas(sub_learning_window, bg="white", width=600, height=400)
        sub_learning_canvas.pack(pady=20, padx=20)
        for course_title, course_details in courses.items():
            if course_details['type'] == 'course':
                x, y = course_details['x'], course_details['y']
                color = course_details['color']
                sub_learning_canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags=course_title)
                sub_learning_canvas.create_text(x, y, text=course_title, tags=course_title)
                sub_learning_canvas.tag_bind(course_title, "<Button-1>", lambda e, title=course_title, details=courses[course_title]: display_course_content(title, details))
        # Add a "Back" button to go back to the main learning path
        back_button = ttk.Button(sub_learning_window, text="Back", command=sub_learning_window.destroy)
        back_button.pack(pady=10)


    # Function to bind each bubble to its content
def display_learning_path():
    learning_window = Toplevel(root)
    learning_window.title("Learning Path")
    learning_canvas = tk.Canvas(learning_window, bg="white", width=600, height=400)
    learning_canvas.pack(pady=20, padx=20)
    
    # Function to bind each bubble to its content
    def bind_bubble(title, details):
        learning_canvas.tag_bind(title, "<Button-1>", lambda e: display_course_content(title, details))
    
    for title, details in courses.items():
        x, y = details['x'], details['y']
        color = details['color']
        
        if details['type'] == 'main':
            learning_canvas.create_oval(x-30, y-30, x+30, y+30, fill=color, tags=title)
            learning_canvas.create_text(x, y, text=title, tags=title)
            
            # Display course bubbles inside the main bubble
            if 'sub_courses' in details:
                for sub_title, sub_details in details['sub_courses'].items():
                    sub_x, sub_y = sub_details['x'], sub_details['y']
                    sub_color = sub_details['color']
                    learning_canvas.create_oval(sub_x-20, sub_y-20, sub_x+20, sub_y+20, fill=sub_color, tags=sub_title)
                    learning_canvas.create_text(sub_x, sub_y, text=sub_title, tags=sub_title)
                    bind_bubble(sub_title, sub_details)
        else:
            # Display course bubbles that are not inside any main bubble
            learning_canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags=title)
            learning_canvas.create_text(x, y, text=title, tags=title)
        
        bind_bubble(title, details)

view_path_button = ttk.Button(root, text="View Path", command=display_learning_path)
view_path_button.pack(pady=10, padx=10)

# Run the application
root.mainloop()
