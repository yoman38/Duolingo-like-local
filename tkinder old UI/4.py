import tkinter as tk
from tkinter import ttk, colorchooser

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
    if topic and content:
        topics_content[topic] = content
        bubble_colors[topic] = color
        topic_entry.delete(0, tk.END)
        content_entry.delete(0, tk.END)

save_button = ttk.Button(course_frame, text="Save Topic", command=save_topic)
save_button.pack(pady=10, padx=10)

# Mindmap Canvas for displaying courses
canvas = tk.Canvas(root, bg="white", width=600, height=400)
canvas.pack(pady=20, padx=20)

def create_bubble(event):
    x, y = event.x, event.y
    topic = simpledialog.askstring("Input", "Enter the topic name:")
    if topic in topics_content:
        color = bubble_colors.get(topic, "light blue")
        canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, tags=topic)
        bubble_positions[topic] = (x, y)
        canvas.tag_bind(topic, '<Button-1>', lambda e, t=topic: activate_bubble(t))

def activate_bubble(topic):
    content = topics_content.get(topic, "")
    messagebox.showinfo(topic, content)

def link_nearby_bubbles():
    for topic1, pos1 in bubble_positions.items():
        for topic2, pos2 in bubble_positions.items():
            if topic1 != topic2:
                distance = ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
                if distance < 100:  # If bubbles are near enough
                    canvas.create_line(pos1, pos2, fill="gray")

canvas.bind("<Double-Button-1>", create_bubble)
link_button = ttk.Button(root, text="Link Nearby Bubbles", command=link_nearby_bubbles)
link_button.pack(pady=10, padx=10)

# Run the application
root.mainloop()
