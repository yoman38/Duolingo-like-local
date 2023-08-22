import tkinter as tk
from tkinter import ttk, colorchooser, simpledialog, Toplevel, messagebox, filedialog, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
import json
from PIL import Image, ImageTk, ImageGrab
import fitz
import webbrowser

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

# Bubble Type (Main or Course)
ttk.Label(course_frame, text="Bubble Type:").grid(row=11, column=0, sticky="w", padx=5, pady=5)
bubble_type = ttk.Combobox(course_frame, values=["Main", "Course"], state="readonly")
bubble_type.grid(row=11, column=1, padx=5, pady=5)
bubble_type.set("Course")  # Default value

ttk.Label(course_frame, text="Y-coordinate:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
y_entry = ttk.Entry(course_frame, width=10)
y_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
y_entry.bind("<KeyRelease>", lambda e: render_preview())

# Preview Canvas
preview_canvas = tk.Canvas(course_frame, bg="white", width=200, height=200)
preview_canvas.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

def render_preview(event=None):
    title = title_entry.get()
    x = int(x_entry.get()) if x_entry.get().isdigit() else 100
    y = int(y_entry.get()) if y_entry.get().isdigit() else 100
    color = chosen_color.get()
    preview_canvas.delete("bubble")
    for course_title, details in courses.items():
        cx, cy = details['x'], details['y']
        ccolor = details['color']
        if details['type'] == 'main':
            preview_canvas.create_oval(cx-30, cy-30, cx+30, cy+30, fill=ccolor, tags="bubble")
        else:
            preview_canvas.create_oval(cx-20, cy-20, cx+20, cy+20, fill=ccolor, tags="bubble")
        preview_canvas.create_text(cx, cy, text=course_title, tags="bubble")

def save_topic():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END).strip()
    x = int(x_entry.get())
    y = int(y_entry.get())
    color = chosen_color.get()
    type_ = bubble_type.get().lower()  # Get the selected bubble type
    if title and content:
        courses[title] = {'content': content, 'x': x, 'y': y, 'color': color, 'type': type_}
        save_courses()
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)


def delete_course():
    title = title_entry.get()
    if title in courses:
        del courses[title]
        save_courses()
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)

delete_button = ttk.Button(course_frame, text="Delete Course", command=delete_course)
delete_button.grid(row=6, column=2, padx=5, pady=5)

def display_course_content(title, details):
    # Create a new top-level window
    popup = Toplevel(root)
    popup.title(title)

    # Create a scrollable text widget to display the course content
    content_display = scrolledtext.ScrolledText(popup, width=50, height=20)  # Adjust width and height as needed
    content_display.pack(pady=10, padx=10)
    content_display.insert(tk.END, details['content'])
    content_display.config(state=tk.DISABLED)  # Make the text widget read-only

    # Close button
    close_button = ttk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)


def display_learning_path():
    learning_window = Toplevel(root)
    learning_window.title("Learning Path")
    learning_canvas = tk.Canvas(learning_window, bg="white", width=600, height=400)
    learning_canvas.pack(pady=20, padx=20)
    for title, details in courses.items():
        x, y = details['x'], details['y']
        color = details['color']
        if details['type'] == 'main':
            learning_canvas.create_oval(x-30, y-30, x+30, y+30, fill=color, tags=title)
        else:
            learning_canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags=title)
        learning_canvas.create_text(x, y, text=title, tags=title)

view_path_button = ttk.Button(root, text="View Path", command=display_learning_path)
view_path_button.pack(pady=10, padx=10)

# Run the application
root.mainloop()