from flask import Flask, render_template, url_for, request, redirect, flash
from pymongo import MongoClient
from forms import QuizForm
from bson import ObjectId

app = Flask(__name__)
app.config["SECRET_KEY"] = "N5DgnrRI7fKop4uK4weAjlbGXuMleMJN"
app.config["MONGO_URI"] = "mongodb+srv://poikilothermic40:dsdKbJvJBAmscysO@cluster0.y6hqbeq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(app.config["MONGO_URI"])

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['Quiz']  # Use your actual database name

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/AddQues")
def AddQues():
    form = QuizForm()
    return render_template('AddQues.html', form=form)

@app.route("/add_question", methods=['POST'])
def add_question():
    if request.method == 'POST':
        form = QuizForm(request.form)
        print("Form data received:", request.form) 

        if form.validate():
            question_text = form.questions[0].question_text.data
            options = [
                {
                    "option_text": entry.option_text.data,
                    "is_correct": entry.is_correct.data,
                }
                for entry in form.questions[0].options
            ]

            print(f"Question Text: {question_text}")
            print(f"Options: {options}")

            # Save the question to MongoDB
            questions_collection = db['Questions']  # Use your actual collection name
            questions_collection.insert_one({
                "question_text": question_text,
                "options": options,
            })

            flash("Question added successfully", 'success')
            return redirect(url_for('AddQues'))

        else:
            flash("Form validation failed", 'error')
            print("Form validation failed. Form errors:", form.errors)  # Add this line for debugging

    return redirect(url_for('AddQues'))

@app.route("/quiz")
def quiz():
    # Retrieve quiz questions from MongoDB
    quiz_questions = db['Questions'].find()
    return render_template('ques.html', quiz_questions=quiz_questions)

@app.route("/submit_quiz", methods=['POST'])
def submit_quiz():
    if request.method == 'POST':
        submitted_answers = request.form

        # Retrieve correct options from MongoDB for comparison
        correct_answers = {}
        for question in db['Questions'].find():
            correct_options = [option['option_text'] for option in question['options'] if option['is_correct']]
            correct_answers[str(question['_id'])] = correct_options

        # Compare submitted answers with correct options
        score = 0
        feedback = {}  # Store feedback for each question
        for question_id, submitted_answer in submitted_answers.items():
            question = db['Questions'].find_one({'_id': ObjectId(question_id)})
            correct_option = correct_answers.get(question_id, [])
            feedback[question_id] = {
                'correct_option': correct_option,
                'submitted_answer': submitted_answer,
                'is_correct': submitted_answer in correct_option,
            }
            if submitted_answer in correct_option:
                score += 1

        print("Submitted Quiz Answers:", submitted_answers)
        print("Score:", score)
        print("Feedback:", feedback)

        # Render the result template
        return render_template('quiz_result.html', score=score, feedback=feedback)

    return redirect(url_for('quiz'))

@app.route("/ques")
@app.route("/Quiz")
def ques():
    quiz_questions = list(db['Questions'].find())
    print("Quiz Questions:", quiz_questions)  # Add this line for debugging
    return render_template('ques.html', quiz_questions=quiz_questions)


@app.route("/resources")
def resources():
    return render_template('resources.html', title='Resources')


@app.route("/AddForum", methods=['GET', 'POST'])
def AddForum():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        # MongoDB connection
        client = MongoClient(app.config["MONGO_URI"])
        db = client['Quiz']  # Use your actual database name
        collection = db['questions1']  # Use your actual collection name
        
        # Save the question to the database
        collection.insert_one({'title': title, 'description': description})
        return 'Question submitted successfully!'
    
    return render_template('AddForum.html')

@app.route("/forum")
def forum():
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://poikilothermic40:dsdKbJvJBAmscysO@cluster0.y6hqbeq.mongodb.net/?retryWrites=true&w=majority")
    db = client['Quiz']  # Use your actual database name
    collection = db['questions1']  # Use your actual collection name
    
    # Retrieve all questions from the database collection
    questions = collection.find()
    
    return render_template('forum.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
