# LIBRARY AND MODULE IMPORTATION
from flask import Flask, send_file,  render_template, request
from werkzeug.utils import secure_filename
import openai
import requests
import json
import time
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, InputRequired, length, Email
from flask_bootstrap import Bootstrap5
import sqlite3
import replicate
import os

# SENSITIVE DATA
os.environ["REPLICATE_API_TOKEN"] = "r8_DErOAKQO54r3BYh4aOTbF62JXwKiWyY45Vvtf"

base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": "d833946f10ab40209c8b990593ead9bd"
}

fareed_api_key = "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"

openai.api_key = fareed_api_key

REPLICATE_API_TOKEN = "r8_eBELqZagrXU7Y1o6A5COpQac9XWEsMS3BU8sB"
download_file_path = []
# FLASK APP CREATION
app = Flask(__name__)
app.secret_key = "iamastar"

#DATABASE CREATION
def __init__(self):
    con = sqlite3.connect('user2.db')
    c = con.cursor()
    c.execute("CREATE TABLE user2(email text,password text)")
    con.commit()


# LOG IN CLASS
class Login_form(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), length(min=8, max=12)])
    submit = SubmitField('Log in')


# SIGN UP CLASS
class Register(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), length(min=8, max=12)])
    submit = SubmitField('Sign up')

# DEFAULT ROUTE
@app.route("/home")
def home_page():
    return (render_template("index.html"))

#SIGN UP PAGE ROUTE
@app.route('/', methods=['POST', 'GET'])
def registrationform():
    form = Register()
    con = sqlite3.connect('user1.db')
    c = con.cursor()
    if request.method == 'POST':
        if(request.form["email"]!= "" and request.form["password"]!=""):
            email = request.form["email"]
            password = request.form["password"]
            statement = f"SELECT * from user1 WHERE name= '{email}' and passWord= '{password}';"
            c.execute(statement)
            data = c.fetchone()
            if data:
                return render_template("error.html")
            else:
                if not data:
                    c.execute("INSERT INTO user1 (name, password) VALUES (?, ?)", (email, password))
                    con.commit()
                    con.close()
                    log_in_form = Login_form()
                return render_template("login.html", form=log_in_form)
    elif request.method == "GET":
        return render_template('register.html', form=form)

#LOG IN PAGE ROUTE
@app.route("/login", methods=["GET", "POST"])
def log_in():
    form = Login_form()
    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']
        con = sqlite3.connect('user1.db')
        c = con.cursor()
        statement = f"SELECT * from user1 WHERE name='{email}' AND passWord='{password}';"
        c.execute(statement)
        if not c.fetchone():
            return render_template("login.html", form=form)
        else:
            return render_template("index.html")
    else:
        request.method = "GET"
        return render_template("login.html", form=form)

# TEXT SUMMARIZATION PAGE ROUTE
@app.route("/text-summ", methods=["GET", "POST"])
def text_summ():
    if request.method == 'POST':
        text_data = request.form["textarea_name"]
        selected_length = request.form.get("short")
        selected_type = request.form.get("sumtype")
        if selected_length == "short":
            length_statement = "In less than 150 words"
            summarized_text = summarizer(text_data, selected_type, length_statement)
        elif selected_length == "medium":
            length_statement = "In less than 250 words"
            summarized_text = summarizer(text_data, selected_type, length_statement)
        elif selected_length == "long":
            length_statement = "In more than 300 words"
            summarized_text = summarizer(text_data, selected_type, length_statement)
        text_length = len(text_data.split())
        summary_length = len(summarized_text.split())
        return render_template("result.html", text_data=summarized_text, summary_length=summary_length, text_length=text_length)
    return (render_template("text-summarizer.html"))

# Configure upload folder (adjust the path as needed)
UPLOAD_FOLDER = 'static/'

# AUDIO SUMMARIZATION PAGE ROUTE
@app.route("/audio-summ", methods=["GET", "POST"])
def audio_summ():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        selected_length = request.form.get("short")
        selected_type = request.form.get("sumtype")
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        text_from_audio = audio_retiever(file_path)
        if selected_length == "short":
            length_statement = "In less than 150 words"
            summarized_text = summarizer(text_from_audio, selected_type, length_statement)
        elif selected_length == "medium":
            length_statement = "In less than 250 words"
            summarized_text = summarizer(text_from_audio, selected_type, length_statement)
        elif selected_length == "long":
            length_statement = "In more than 300 words"
            summarized_text = summarizer(text_from_audio, selected_type, length_statement)
        save_file(summarized_text)
        return render_template("result.html", text_data=summarized_text, summary_length=len(summarized_text.split()), text_length=len(text_from_audio.split()))
    return (render_template("audio-summarizer.html"))

# Allowed audio file extensions (adjust as needed)
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file(file):
    if request.method == 'POST':
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            return file_path
    return
    
def save_file(text):
    with open("static/new_file.txt", "w") as file:
        file.write(f"{text}")

@app.route('/download')
def download_file():
    file_path = "static/new_file.txt"
    return send_file(file_path, as_attachment=True)

def summarizer(text, summary_type, length):
    full_response = ""
    for event in replicate.stream("meta/llama-2-70b-chat",
                                  input={"debug": False,"top_p": 1,
                                 "prompt": f"{length}, Generate an {summary_type} summary of the following text: {text}",
                                 "temperature": 0.5,"system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
                                 "max_new_tokens": 500,"min_new_tokens": -1,"prompt_template": "[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]","repetition_penalty": 1.15},):
        full_response += str(event)
    return full_response

# AUDIO RETRIEVER/TRANSCRIPTION FUNCTION

def audio_retiever(filename):
    with open(f"{filename}", "rb") as f:
        response = requests.post(base_url + "/upload", headers=headers, data=f)

    upload_url = response.json()["upload_url"]

    data = {
        "audio_url": upload_url
    }

    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)

    transcript_id = response.json()['id']
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            return transcription_result['text']

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)

# RUN FLASK APP
if __name__ == "__main__":
    app.run(debug=True)