import tkinter as tk
from tkinter import ttk, colorchooser, simpledialog, Toplevel

# Initialize main window
root = tk.Tk()
root.title("Course Creation Tool")

# Course Creation Frame
course_frame = ttk.LabelFrame(root, text="Course Creation")
course_frame.pack(pady=20, padx=20, fill="x")

topic_entry = ttk.Entry(course_frame, width=30)
topic_entry.pack(pady=10, padx=10)
content_entry = ttk.Entry(course_frame, width=30)
content_entry.pack(pady=10, padx=10)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    return color_code

color_button = ttk.Button(course_frame, text="Choose Bubble Color", command=choose_color)
color_button.pack(pady=10, padx=10)

topics_content = {}
bubble_positions = {}
bubble_colors = {}

def save_topic():
    topic = topic_entry.get()
    content = content_entry.get()
    color = choose_color()
    x = simpledialog.askinteger("Position", "Enter x-coordinate:")
    y = simpledialog.askinteger("Position", "Enter y-coordinate:")
    if topic and content:
        topics_content[topic] = content
        bubble_colors[topic] = color
        bubble_positions[topic] = (x, y)
        topic_entry.delete(0, tk.END)
        content_entry.delete(0, tk.END)

save_button = ttk.Button(course_frame, text="Save Topic", command=save_topic)
save_button.pack(pady=10, padx=10)

# Mindmap Canvas for displaying courses (Preview)
canvas = tk.Canvas(root, bg="white", width=600, height=400)
canvas.pack(pady=20, padx=20)

def create_bubble(topic, x, y):
    color = bubble_colors.get(topic, "light blue")
    canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags=topic)
    canvas.tag_bind(topic, '<Button-1>', lambda e, t=topic: activate_bubble(t))

def activate_bubble(topic):
    content = topics_content.get(topic, "")
    popup = Toplevel(root)
    popup.title(topic)
    label = ttk.Label(popup, text=content)
    label.pack(pady=20, padx=20)

def display_learning_path():
    learning_window = Toplevel(root)
    learning_window.title("Learning Path")
    learning_canvas = tk.Canvas(learning_window, bg="white", width=600, height=400)
    learning_canvas.pack(pady=20, padx=20)
    for topic, (x, y) in bubble_positions.items():
        create_bubble(topic, x, y)

display_button = ttk.Button(root, text="Display Learning Path", command=display_learning_path)
display_button.pack(pady=10, padx=10)

# Run the application
root.mainloop()
