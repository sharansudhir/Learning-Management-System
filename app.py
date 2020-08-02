import requests, json, os
from flask import Flask, request, send_file
from flask.templating import render_template
from werkzeug.utils import secure_filename
import boto3 as b3

app = Flask(__name__)
key_path = "credentials/sdpmodule-a63374297120.json"


@app.route('/')
def login():
    message = ""
    return render_template('login.html', message=message)

@app.route("/chat", methods=['POST', 'GET'])
def chat():
    email = request.form['email']
    return render_template('chat.htm', email = email)

@app.route('/home')
def user_home():
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signupQues')
def signup_ques():
    return render_template('signup_question.html')


@app.route('/loginQues')
def login_ques():
    return render_template('login_question.html')


@app.route('/validSignUp')
def valid_signup():
    return render_template('confirmSignUp.html')


@app.route('/forgotPassword')
def forgot_password():
    return render_template('forgotPassword.html')


@app.route('/validForgotPassword')
def confirm_forgot_password():
    return render_template('confirmForgotPassword.html')


@app.route("/user_login", methods=['POST', 'GET'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    data = {'username': email, 'password': password}
    ques_data = {'email': email}
    response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/login", json=data)
    if (response.json()['status'] == 'success'):
        ques_response = requests.post("https://us-central1-serverless-2-279802.cloudfunctions.net/getQuestions",
                                      json=ques_data)
        if 'success' in ques_response.json().keys():
            message = "Issue with 2nd factor authentication"
            return render_template("login.html", message=message)
        else:
            questions = []
            for key in ques_response.json().keys():
                questions.append(key)
            print(questions[1])
            print(ques_response.json()[questions[1]])
            return render_template("login_question.html", email=email, question=questions[1],
                                   answer=ques_response.json()[questions[1]])
            # return render_template("home.html", email = email)
    else:
        message = "Incorrect password or username"
        return render_template("login.html", message=message)


@app.route("/user_signup", methods=['POST', 'GET'])
def user_signup():
    print("into signup")
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
    university = request.form['university']
    role = request.form['role']
    print(role)
    if password == confirmpassword:
        data = {'email': email, 'password': password, 'name': name, 'university': university, 'username': email,
                'role': role}
        response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/signup", json=data)
        if response.json()['message'] == "Success, Enter OTP":
            return render_template('signup_question.html', username=email, password=password, name=name,
                                   university=university, role=role)
        else:
            message = response.json()['message']
            return render_template("signup.html", message=message)
    else:
        message = "Password are not matching"
        return render_template("signup.html", message=message)


@app.route("/signupValidate", methods=['POST', 'GET'])
def signup_validate():
    # Write logic to check signup otp
    email = request.form['email']
    password = request.form['password']
    otp = request.form['otp']
    name = request.form['name']
    university = request.form['university']
    role = request.form['role']
    data = {'password': password, 'code': otp, 'username': email, 'name': name, 'university': university, 'role': role}
    response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/confirmsignup", json=data)
    if "code" in response.json():
        message = "Successfully Registered"
        return render_template('login.html', message=message)
    else:
        message = response.json()['message']
        return render_template('confirmSignUp.html', role=role, username=email, password=password, name=name,
                               university=university, message=message)


@app.route("/userForgotPassword", methods=['POST', 'GET'])
def password_forgot():
    # Write logic to reset password
    email = request.form['email']
    data = {'username': email}
    response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/forgotpassword", json=data)
    print(response.json())
    if response.json()['success'] == "True":
        return render_template('confirmForgotPassword.html')
    else:
        message = response.json()['message']
        return render_template('forgotPassword.html', message=message)


@app.route("/passwordValidate", methods=['POST', 'GET'])
def password_validate():
    # Write logic to reset password otp

    return render_template('login.html')


@app.route("/signupQues", methods=['POST', 'GET'])
def ques_signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    university = request.form['university']
    role = request.form['role']
    ques1 = request.form['ques1']
    ans1 = request.form['ans1']
    ques2 = request.form['ques2']
    ans2 = request.form['ans2']
    ques3 = request.form['ques3']
    ans3 = request.form['ans3']
    data = {'email': email, 'ques1': ques1, 'ans1': ans1, 'ques2': ques2, 'ans2': ans2, 'ques3': ques3, 'ans3': ans3}
    response = requests.post("https://us-central1-serverless-2-279802.cloudfunctions.net/createQuestions", json=data)
    if response.json()['success'] == "True":
        return render_template('confirmSignup.html', username=email, password=password, name=name,
                               university=university, role=role)
    else:
        message = "Please Submit Again with all answers filled"
        return render_template('signup_question.html', message=message, username=email, password=password, name=name,
                               university=university, role=role)


@app.route("/loginQues", methods=['POST', 'GET'])
def ques_login():
    email = request.form['email']
    answer = request.form['answer']
    givenAnswer = request.form['givenAnswer']
    if answer == givenAnswer:
        return render_template('home.html', email=email)
    else:
        message = "Answer is not valid. Please Try Again"
        return render_template('login.html', message=message)


@app.route("/logout", methods=['POST', 'GET'])
def user_logout():
    email = request.form['email']
    data = {'username': email}
    response = requests.post("https://ril4n9as71.execute-api.us-east-1.amazonaws.com/prod/userlogout", json=data)
    if response.json()['success'] == "True":
        message = "Logged Out Successfully"
        return render_template('login.html', message=message)
    else:
        return render_template('login.html')


@app.route("/resendOTPCode", methods=['POST', 'GET'])
def resend_otp_code():
    email = request.form.get('email')
    password = request.form['password']
    data = {'username': email}
    response = requests.post("https://t30lqnf2cb.execute-api.us-east-1.amazonaws.com/prod/resendcode", json=data)
    if response.json()['success'] == "True":
        message = "Code Sent Again"
        return render_template('confirmSignUp.html', username=email, password=password, message=message)
    else:
        message = "Error Sending Code, Please Try Again"
        return render_template('confirmSignUp.html', username=email, password=password, message=message)


@app.route("/uploadfiles", methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("files")
    non_stopped_words = ''
    for file in uploaded_files:
        for line in file:
            non_stopped_words += line.decode('utf-8').strip()

        print("uploading file: ", file)
        file.save(os.path.join('static', secure_filename(file.filename)))
        with open(os.path.join('static', file.filename), 'rb') as tech_file:
            s3_buckets = b3.resource('s3')
            source_bucket = s3_buckets.Bucket('sdparticles')
            print(source_bucket)
            response = source_bucket.put_object(Key=file.filename, Body=tech_file)
            print("File Uploaded Successfully...")
            print(response)

    response = requests.post('https://dataprocessing-hd4jbagnda-uc.a.run.app/', data={'data': non_stopped_words})
    with open('static/wordcloud.png', 'wb') as wordcloud:
        wordcloud.write(response.content)
    return send_file('static/wordcloud.png')


if __name__ == '__main__':
    app.run()
