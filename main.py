# 1. Setup
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///physics_app.db'
db = SQLAlchemy(app)

# 2. User Authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('lessons'))
    return render_template('login.html')

# 3. Lessons
lessons = [
    {"title": "Newton's Laws", "content": "Description about Newton's Laws..."},
    # Add more lessons...
]

@app.route('/lessons')
def lessons():
    return render_template('lessons.html', lessons=lessons)

# 4. Quizzes
@app.route('/quiz/<int:lesson_id>', methods=['GET', 'POST'])
def quiz(lesson_id):
    # Sample questions for the first lesson
    if lesson_id == 1:
        questions = [
            {"question": "What is Newton's first law?", "options": ["A", "B", "C", "D"], "answer": "A"},
            # Add more questions...
        ]
    # Implement for other lessons...
    
    if request.method == 'POST':
        # Check answers and provide feedback...
        pass
    return render_template('quiz.html', questions=questions)

# 5. User Progress (to be implemented)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

# Existing User model...

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    lessons = db.relationship('Lesson', backref='course', lazy=True)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(500), nullable=True)  # YouTube video URL
    pdf_file = db.Column(db.String(300), nullable=True)  # Path to the PDF file
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='lesson', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    options = db.Column(db.PickleType, nullable=False)  # List of options
    answer = db.Column(db.String(50), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        course = Course(title=title, description=description)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_course.html')

@app.route('/create_lesson/<int:course_id>', methods=['GET', 'POST'])
def create_lesson(course_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        video_url = request.form['video_url']
        pdf_file = request.form['pdf_file']  # This should be handled with a file upload in a real scenario
        lesson = Lesson(title=title, content=content, video_url=video_url, pdf_file=pdf_file, course_id=course_id)
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_lesson.html')

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>


@app.route('/create_quiz/<int:lesson_id>', methods=['GET', 'POST'])
def create_quiz(lesson_id):
    if request.method == 'POST':
        question = request.form['question']
        options = request.form.getlist('options')  # Get list of options
        answer = request.form['answer']
        quiz = Quiz(question=question, options=options, answer=answer, lesson_id=lesson_id)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_quiz.html')


import os
from flask import send_from_directory

UPLOAD_FOLDER = 'uploads'

@app.route('/pdfs/<filename>')
def serve_pdf(filename):
    return send_from_directory(os.path.join(UPLOAD_FOLDER, 'pdfs'), filename)

# Existing models...

class LearningPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    courses = db.relationship('Course', backref='learning_path', lazy=True)

@app.route('/learning_paths')
def learning_paths():
    paths = LearningPath.query.all()
    return render_template('learning_paths.html', paths=paths)

@app.route('/choose_path/<int:path_id>')
def choose_path(path_id):
    path = LearningPath.query.get_or_404(path_id)
    courses = Course.query.filter_by(learning_path_id=path.id).all()
    return render_template('path_courses.html', path=path, courses=courses)

# Existing models...

class UserXP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    xp = db.Column(db.Integer, default=0)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    users = db.relationship('User', secondary='user_badges')

class UserBadges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    users = db.relationship('User', secondary='user_rewards')

class UserRewards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id'), nullable=False)

class Citadel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    strength = db.Column(db.Integer, default=100)  # Example attribute

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    xp = UserXP.query.filter_by(user_id=user.id).first()
    badges = UserBadges.query.filter_by(user_id=user.id).all()
    rewards = UserRewards.query.filter_by(user_id=user.id).all()
    citadel = Citadel.query.filter_by(user_id=user.id).first()
    return render_template('profile.html', user=user, xp=xp, badges=badges, rewards=rewards, citadel=citadel)

@app.route('/leaderboard')
def leaderboard():
    users = User.query.join(UserXP).order_by(UserXP.xp.desc()).all()
    return render_template('leaderboard.html', users=users)
