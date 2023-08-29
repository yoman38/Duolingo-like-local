# duolingo-like
**using tqinter**

![Zrzut ekranu 2023-08-28 152520](https://github.com/yoman38/Duolingo-like-local/assets/124726056/1af7435f-75cb-4a43-a432-1a17a0d15fc9)
![Zrzut ekranu 2023-08-28 152453](https://github.com/yoman38/Duolingo-like-local/assets/124726056/aa5f7632-322b-451c-b2ad-d8d750f6d15d)

**OLDER VERSION WITH KIVY**
![Zrzut ekranu 2023-08-29 101517](https://github.com/yoman38/Duolingo-like-local/assets/124726056/6f66a2d9-31ab-434d-983b-00684f30e43e)

Why not sticking to kivy, it looks better ! 
> It was difficult to achieve the wanted UI along with the functionalities such as handling pdf and youtube for example


# Learning Path Creation Tool

The Learning Path Creation Tool is a graphical user interface (GUI) application built using the Tkinter library in Python. It allows users to create, visualize, and manage learning paths or course structures in a user-friendly manner. With this tool, users can arrange courses, add content, and create connections between courses and sub-courses.

## Features

- Create and manage courses with titles and content.
- Add images and import PDF content to enrich course content.
- Insert YouTube links with specified start and end times.
- Position courses using X and Y coordinates on a visual canvas.
- Choose bubble colors to visually distinguish courses.
- Link courses to main bubbles and create sub-courses.
- Preview the learning path structure on a canvas with interactive bubbles.
- Delete courses and sub-courses for easy content management.
- View the entire learning path structure in a separate window.
- Display course content by clicking on course bubbles.

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/learning-path-creation-tool.git
   cd learning-path-creation-tool
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Follow the on-screen instructions to create and manage learning paths.

## Usage

- Launch the application and enter the course title and content.
- Add images, import PDF content, and insert YouTube links as needed.
- Choose bubble type and link courses to main bubbles if applicable.
- Specify bubble position and color for each course.
- Save courses using the "Save Topic" button and clear fields with "Cancel."
- Delete courses using the "Delete Course" button.
- View the learning path structure by clicking the "View Path" button.
- Click on bubbles to view course content in separate windows.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-feature`.
3. Make your changes and commit them: `git commit -am 'Add some feature'`.
4. Push the branch: `git push origin feature/my-feature`.
5. Create a pull request detailing your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or suggestions, feel free to contact us at your@email.com.

---

Please make sure to customize the content according to your project's specifics, including repository URLs, contact information, and other relevant details.


## **WIP - to add:**

- "holder" hold a subcanva. For example, clicking on introduction in the ppt display another learning path
- "course" represents a single piece of educational content that can include text, images, videos, and PDFs.
- Quiz is a simple assessment. it can also be added to a learning path and be clicked on it.

**quiz breakdown**
- The user is presented with a question (text or text+multimedia like jpg or gif):
- selecting from multiple-choice options
-- If the user's response is correct, the app provides positive feedback, such as displaying a message like "Correct!" or playing a rewarding sound.
-- If it is wrong, it tells the user and move on to the next question.
- Questions are repeated at specific intervals to reinforce memory retention.
- Difficult questions are shown more frequently, while correctly answered questions are revisited less often. (personnaly i used some loops to randomize, and increment the bad answers)

**App**
adding "videos" or "course" (which can contain videos) is unrelated. 
Quiz from "video" or "written" are unrelated too.
They are like two totally different tab with their own content (but more or less the same quiz functionality, it is easier to code)
 Bubbles are linked if they are near enough, which is a suitable behavior
