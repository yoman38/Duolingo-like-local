import tkinter as tk
from tkinter import ttk, simpledialog

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

topics_content = {}

def save_topic():
    topic = topic_entry.get()
    content = content_entry.get()
    if topic and content:
        topics_content[topic] = content
        create_bubble(learning_frame, topic)
        topic_entry.delete(0, tk.END)
        content_entry.delete(0, tk.END)

save_button = ttk.Button(course_frame, text="Save Topic", command=save_topic)
save_button.pack(pady=10, padx=10)

# Course Display Frame
display_frame = ttk.LabelFrame(root, text="Course Display")
display_frame.pack(pady=20, padx=20, fill="x")

content_label = ttk.Label(display_frame, text="")
content_label.pack(pady=10, padx=10)

# Learning Paths Frame
learning_frame = ttk.LabelFrame(root, text="Learning Paths")
learning_frame.pack(pady=20, padx=20, fill="x")

bubble_style = ttk.Style()
bubble_style.configure("TButton", background="light blue")
bubble_style.configure("Activated.TButton", background="light green")

def activate_bubble(topic):
    content_label.config(text=topics_content.get(topic, ""))

def create_bubble(frame, topic):
    bubble = ttk.Button(frame, text=topic, style="TButton", command=lambda: activate_bubble(topic))
    bubble.pack(side="left", padx=5)
    return bubble

# Run the application
root.mainloop()
