import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import PyPDF2
import json
import os

class EnhancedLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Creation")

        # Variables for pagination
        self.current_page = 0
        self.pages = []

        # Check if saved data exists
        self.saved_file = "courses_data.json"
        if os.path.exists(self.saved_file):
            with open(self.saved_file, 'r') as file:
                self.content = json.load(file)
        else:
            self.content = {}

        self.coordinates = {}  # To store coordinates for mindmap-style display
        
        # Course Creation Frame
        self.create_course_frame()

    def create_course_frame(self):
        self.course_creation_frame = ttk.LabelFrame(self.root, text="Course Creation", padding=(10, 5))
        self.course_creation_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ttk.Label(self.course_creation_frame, text="Topic:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.topic_entry = ttk.Entry(self.course_creation_frame, width=30)
        self.topic_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.course_creation_frame, text="Content:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.content_text = tk.Text(self.course_creation_frame, width=40, height=5)
        self.content_text.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.course_creation_frame, text="Position (X, Y):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.pos_x = ttk.Entry(self.course_creation_frame, width=10)
        self.pos_y = ttk.Entry(self.course_creation_frame, width=10)
        self.pos_x.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.pos_y.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        self.pos_x.bind("<KeyRelease>", self.refresh_preview)
        self.pos_y.bind("<KeyRelease>", self.refresh_preview)

        ttk.Label(self.course_creation_frame, text="Color:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.color_button = ttk.Button(self.course_creation_frame, text="Pick Color", command=self.pick_color)
        self.color_button.grid(row=3, column=1, padx=5, pady=5)
        self.selected_color = "lightblue"

        ttk.Button(self.course_creation_frame, text="Delete Course", command=self.delete_course).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.course_creation_frame, text="Save", command=self.save_content).grid(row=4, column=1, padx=5, pady=5)
        
        self.preview_canvas = tk.Canvas(self.course_creation_frame, bg="white", width=800, height=500)
        self.preview_canvas.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(self.course_creation_frame, text="View Learning Paths", command=self.view_learning_paths).grid(row=6, column=1, sticky="e", padx=5, pady=5)

        self.refresh_preview()

        # Pagination buttons
        self.prev_button = ttk.Button(self.course_creation_frame, text="<<", command=self.prev_page)
        self.prev_button.grid(row=7, column=0, padx=5, pady=5)
        self.next_button = ttk.Button(self.course_creation_frame, text=">>", command=self.next_page)
        self.next_button.grid(row=7, column=1, padx=5, pady=5)

        # End of page label
        self.end_label = ttk.Label(self.course_creation_frame, text="End of Page")
        self.end_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)


    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.display_page()

    def display_page(self):
        # Clear the current content and display the content of the current page
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", self.pages[self.current_page])

    def pick_color(self):
        color = askcolor(title="Choose a color")[1]
        if color:
            self.selected_color = color
            self.refresh_preview()


    def delete_course(self):
        topic = self.topic_entry.get()
        if topic and topic in self.content:
            del self.content[topic]
            self.topic_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            self.save_data()
            self.refresh_preview()
        else:
            messagebox.showerror("Error", "Topic not found.")

    def save_content(self):
        topic = self.topic_entry.get()
        content = self.content_text.get("1.0", "end-1c")
        color = self.selected_color
        try:
            x, y = int(self.pos_x.get()), int(self.pos_y.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid x and y positions.")
            return
        
        if not topic or not content:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        self.content[topic] = {'content': content, 'color': color, 'x': x, 'y': y}
        self.save_data()
        self.topic_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.refresh_preview()
        # Split content into pages
        self.split_into_pages()

    def split_into_pages(self):
        content = self.content_text.get("1.0", "end-1c")
        # Split content every 500 characters for simplicity (adjust as needed)
        self.pages = [content[i:i+500] for i in range(0, len(content), 500)]
        self.display_page()

    def save_data(self):
        with open(self.saved_file, 'w') as file:
            json.dump(self.content, file)

    def view_learning_paths(self):
        self.learning_path_window = tk.Toplevel(self.root)
        self.learning_path_window.title("Learning Paths")
        self.learning_path_canvas = tk.Canvas(self.learning_path_window, bg="white", width=800, height=500)
        self.learning_path_canvas.pack(padx=10, pady=10, fill="both", expand=True)
        
        for topic, details in self.content.items():
            x, y = details['x'], details['y']
            color = details['color']
            self.create_bubble(topic, x, y, color, canvas=self.learning_path_canvas)

        self.link_nearby_bubbles(canvas=self.learning_path_canvas)

    def create_bubble(self, text, x, y, color, canvas):
        bubble_id = canvas.create_oval(x, y, x+80, y+80, fill=color, tags=text)
        text_id = canvas.create_text(x+40, y+40, text=text)
        canvas.tag_bind(bubble_id, "<Button-1>", lambda event, t=text: self.show_topic_content(t))
        self.coordinates[text] = (x, y)

    def import_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            with open(filepath, "rb") as file:
                reader = PyPDF2.PdfFileReader(file)
                content = ""
                for page_num in range(reader.numPages):
                    page = reader.getPage(page_num)
                    content += page.extractText()
                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", content)
                self.split_into_pages()

    def insert_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if filepath:
            image = Image.open(filepath)  # Using Pillow's Image module
            photo = ImageTk.PhotoImage(image)
            self.content_text.image_create(tk.END, image=photo)
            # Store reference to avoid garbage collection
            self.content_text.image_ref = photo

    def refresh_preview(self, event=None):
        self.preview_canvas.delete("all")  # Clear the current preview
        
        # Display saved paths first
        for topic, details in self.content.items():
            x, y = details['x'], details['y']
            color = details['color']
            self.create_bubble(topic, x, y, color, canvas=self.preview_canvas)

        # Display the new bubble (if any)
        try:
            x, y = int(self.pos_x.get()), int(self.pos_y.get())
        except ValueError:
            # If user enters non-integer values, just return without drawing the new bubble
            return

        color = self.selected_color
        topic = self.topic_entry.get() or "Preview"
        self.create_bubble(topic, x, y, color, canvas=self.preview_canvas)

    def show_topic_content(self, topic):
        content_details = self.content.get(topic, {})
        content = content_details.get('content', "No content available for this topic.")
        PopupContent(self.root, topic, content)

    def link_nearby_bubbles(self):
        threshold_distance = 150  # Maximum distance to link bubbles
        for topic1, coords1 in self.coordinates.items():
            for topic2, coords2 in self.coordinates.items():
                if topic1 != topic2:
                    distance = ((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2) ** 0.5
                    if distance < threshold_distance:
                        self.learning_path_canvas.create_line(coords1[0]+40, coords1[1]+40, coords2[0]+40, coords2[1]+40)

class PopupContent:
    def __init__(self, parent, title, content):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("300x200")
        ttk.Label(self.window, text=content, wraplength=280).pack(padx=10, pady=10)

# Create main window and launch the app
root = tk.Tk()
root.geometry('1000x700')  # Set window size
app = EnhancedLearningApp(root)
root.mainloop()
