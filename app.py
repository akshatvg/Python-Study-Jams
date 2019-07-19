from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
import re

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'student_db'
app.config['MONGO_URI'] = 'mongodb+srv://naynika:wason@cluster0-wunee.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
#def show():
#    return jsonify({'routes active':"/new and /show"})
def index():
    return render_template('index.html')

@app.route('/show', methods = ['GET'])
def get_student_records():
    student_details = mongo.db.student_details

    output = []

    for q in student_details.find():
        output.append({'first_name' : q['first_name'], 'last_name' : q['last_name'], 'reg_no' : q['reg_no'], 'mob_no' : q['mob_no'], 'email' : q['email'], 'gender' : q['gender']})


    return jsonify({'students' : output})

@app.route('/show/<reg_no>', methods = ['GET'])
def get_one_student(reg_no):
    student_details = mongo.db.student_details

    q = student_details.find_one({'reg_no' : reg_no })

    if q:
        output = {'first_name' : q['first_name'], 'last_name' : q['last_name'], 'reg_no' : q['reg_no'], 'mob_no' : q['mob_no'], 'email' : q['email'], 'gender' : q['gender']}
    else:
        output = 'No student found'

    return jsonify({'student' : output})



@app.route('/new', methods = ['POST'])
def add_student():
    if request.method == 'POST':
        first_name=json['first-name']
        last_name = json['last-name']
        email = json['email']
        mob_no = json['phone']
        reg_no=json['reg-no']
        gender=json['gender']
        email_pat = re.compile('^[a-zA-Z0-9_]*[@][a-zA-Z.]*[a-zA-Z.]{3}$')
        phone_pattern = re.compile("(0/91)?[6-9][0-9]{9}")
        regno_pat = re.compile('^[1][7-9][a-zA-Z]{3}[0-9]{4}$')

        student_details = mongo.db.student_details

        if regno_pat.match(reg_no):
            reg_no = reg_no
        else:
            output = "Invalid Registration Number"
            return jsonify({'students' : output})
        #mob_no = request.json['mob_no']
        if phone_pattern.match(mob_no):
            mob_no = mob_no
        else:
            output = "Invalid Mobile Number"
            return jsonify({'students' : output})
        #email = request.json['email']
        if email_pat.match(email):
            email = email
        else:
            output = "Invalid Email"
            return jsonify({'students' : output})
        #gender = request.json['gender']

        student_details_id = student_details.insert({'first_name' : first_name, 'last_name' : last_name, 'reg_no' : reg_no, 'mob_no' : mob_no, 'email' : email, 'gender' : gender})
        new_student = student_details.find_one({'_id' : student_details_id})
        
        output = {'first_name' : new_student['first_name'], 'last_name' : new_student['last_name'], 'reg_no' : new_student['reg_no'], 'mob_no' : new_student['mob_no'], 'email' : new_student['email'], 'gender' : new_student['gender']}
        print(output)
        return jsonify({'students' : output})

    else:
        output = "GET method is not applicable on this route"
        return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug = True)
