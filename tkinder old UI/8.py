import tkinter as tk
from tkinter import ttk, colorchooser, simpledialog, Toplevel, messagebox
import json

# Load courses from JSON
def load_courses():
    try:
        with open('courses.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

courses = load_courses()

# Save courses to JSON
def save_courses():
    with open('courses.json', 'w') as file:
        json.dump(courses, file)

# Initialize main window
root = tk.Tk()
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
content_text = tk.Text(course_frame, width=30, height=5)
content_text.grid(row=1, column=1, padx=5, pady=5)

chosen_color = tk.StringVar(value="light blue")

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    chosen_color.set(color_code)
    render_preview()

color_button = ttk.Button(course_frame, text="Choose Bubble Color", command=choose_color)
color_button.grid(row=2, column=0, padx=5, pady=5)

# X and Y coordinates
ttk.Label(course_frame, text="X-coordinate:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
x_entry = ttk.Entry(course_frame, width=10)
x_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
x_entry.bind("<KeyRelease>", lambda e: render_preview())

ttk.Label(course_frame, text="Y-coordinate:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
y_entry = ttk.Entry(course_frame, width=10)
y_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
y_entry.bind("<KeyRelease>", lambda e: render_preview())

# Preview Canvas
preview_canvas = tk.Canvas(course_frame, bg="white", width=200, height=200)
preview_canvas.grid(row=0, column=2, rowspan=5, padx=10, pady=10)

def render_preview(event=None):
    title = title_entry.get()
    x = int(x_entry.get()) if x_entry.get().isdigit() else 100
    y = int(y_entry.get()) if y_entry.get().isdigit() else 100
    color = chosen_color.get()
    preview_canvas.delete("bubble")
    for course_title, details in courses.items():
        cx, cy = details['x'], details['y']
        ccolor = details['color']
        preview_canvas.create_oval(cx-20, cy-20, cx+20, cy+20, fill=ccolor, tags="bubble")
        preview_canvas.create_text(cx, cy, text=course_title, tags="bubble")
    preview_canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags="bubble")
    preview_canvas.create_text(x, y, text=title, tags="bubble")

def save_topic():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END).strip()
    x = int(x_entry.get())
    y = int(y_entry.get())
    color = chosen_color.get()
    if title and content:
        courses[title] = {'content': content, 'x': x, 'y': y, 'color': color}
        save_courses()
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)

save_button = ttk.Button(course_frame, text="Save Topic", command=save_topic)
save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

def delete_course():
    title = title_entry.get()
    if title in courses:
        del courses[title]
        save_courses()
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)

delete_button = ttk.Button(course_frame, text="Delete Course", command=delete_course)
delete_button.grid(row=5, column=2, padx=5, pady=5)

def display_learning_path():
    learning_window = Toplevel(root)
    learning_window.title("Learning Path")
    learning_canvas = tk.Canvas(learning_window, bg="white", width=600, height=400)
    learning_canvas.pack(pady=20, padx=20)
    for title, details in courses.items():
        x, y = details['x'], details['y']
        color = details['color']
        learning_canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags=title)
        learning_canvas.create_text(x, y, text=title, tags=title)

view_path_button = ttk.Button(root, text="View Path", command=display_learning_path)
view_path_button.pack(pady=10, padx=10)

# Run the application
root.mainloop()
