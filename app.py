from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
from datetime import date
import re
import os
import sys
    
app = Flask(__name__)
   
app.secret_key = 'abcd21234455'  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Priyanka@123'
app.config['MYSQL_DB'] = 'gsms'
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Server-side validation
        if not email or not password:
            message = 'Please enter both email and password!'
        else:
            # Perform database query
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM User WHERE email = %s', (email,))
            user = cursor.fetchone()

            # Check if user exists and password matches
            if user and user['password'] == password:
                # Set session variables upon successful login
                session['loggedin'] = True
                session['userid'] = user['id']
                session['name'] = user['name']
                session['email'] = user['email']
                message = 'Logged in successfully!'
                return redirect(url_for('dashboard'))
            else:
                message = 'Incorrect email or password!'

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    # Clear session variables upon logout
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('login'))

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    # Check if user is logged in
    if 'loggedin' in session:
        return render_template("dashboard.html")
    return redirect(url_for('login'))


########################### Techer section ##################################

# Route for displaying the teachers list
@app.route("/teacher", methods=['GET','POST'])
def teacher():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT teacher_id, first_name, last_name, join_date, dob, gender, phone_no, city, zipcode, district FROM Teacher')
        teachers = cursor.fetchall() 
        return render_template("teacher.html", teachers=teachers)
    return redirect(url_for('login'))

# Route for editing a teacher's information
@app.route("/edit_teacher", methods=['GET'])
def edit_teacher():
    if 'loggedin' in session:
        teacher_id = request.args.get('teacher_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT teacher_id, first_name, last_name, join_date, dob, gender, phone_no, city, zipcode, district FROM Teacher WHERE teacher_id = %s', (teacher_id,))
        teachers = cursor.fetchall() 
        return render_template("edit_teacher.html", teachers=teachers)
    return redirect(url_for('login'))  
    
# Route for saving teacher information
# Route for saving teacher information
@app.route("/save_teacher", methods=['GET', 'POST'])
def save_teacher():
    if 'loggedin' in session:
        if request.method == 'POST':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            teacher_id = request.form.get('teacher_id')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            join_date = request.form.get('join_date')
            dob = request.form.get('dob')
            gender = request.form.get('gender')
            phone_no = request.form.get('phone_no')
            city = request.form.get('city')
            zipcode = request.form.get('zipcode')
            district = request.form.get('district')
            action = request.form.get('action')

            # Check if teacher_id is unique
            cursor.execute('SELECT * FROM Teacher WHERE teacher_id = %s', (teacher_id,))
            if cursor.fetchone():
                return "Error: Teacher ID already exists!"

            if action == 'updateTeacher':
                cursor.execute('UPDATE Teacher SET first_name = %s, last_name = %s, join_date = %s, dob = %s, gender = %s, phone_no = %s, city = %s, zipcode = %s, district = %s WHERE teacher_id = %s',
                               (first_name, last_name, join_date, dob, gender, phone_no, city, zipcode, district, teacher_id))
                mysql.connection.commit()
                return redirect(url_for('teacher'))

            else:
                cursor.execute('INSERT INTO Teacher (teacher_id,first_name, last_name, join_date, dob, gender, phone_no, city, zipcode, district) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (teacher_id,first_name, last_name, join_date, dob, gender, phone_no, city, zipcode, district))
                mysql.connection.commit()
                return redirect(url_for('teacher'))

    return redirect(url_for('login'))

    
# Route for deleting a teacher
@app.route("/delete_teacher", methods=['GET'])
def delete_teacher():
    if 'loggedin' in session:
        teacher_id = request.args.get('teacher_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Delete associated records from the course table
            cursor.execute('DELETE FROM Course WHERE teacher_id = %s', (teacher_id,))
            mysql.connection.commit()   
            
            # Once associated records are deleted, delete the teacher record
            cursor.execute('DELETE FROM Teacher WHERE teacher_id = %s', (teacher_id,))
            mysql.connection.commit()   
            
            return redirect(url_for('teacher'))
        except Exception as e:
            # Handle any exceptions, such as integrity errors
            print("Error:", e)
            return "Error occurred while deleting teacher"
    return redirect(url_for('login'))


########################### STUDENT ##################################

# Route for displaying the students list
@app.route("/student", methods=['GET', 'POST'])
def student():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT student_id, school_id, first_name, last_name, dob, academic_year, city, zip_code, caste FROM Student')
        students = cursor.fetchall()
        return render_template("student.html", students=students)
    return redirect(url_for('login'))

# Route for editing a student's information
@app.route("/edit_student", methods=['GET'])
def edit_student():
    if 'loggedin' in session:
        student_id = request.args.get('student_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT student_id, school_id, first_name, last_name, dob, academic_year, city, zip_code, caste FROM Student WHERE student_id = %s', (student_id,))
        students = cursor.fetchall()
        return render_template("edit_student.html", students=students)
    return redirect(url_for('login'))

# Route for saving student information
@app.route("/save_student", methods=['POST'])
def save_student():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            student_id = request.form.get('student_id')
            school_id = request.form.get('school_id')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            dob = request.form.get('dob')
            academic_year = request.form.get('academic_year')
            city = request.form.get('city')
            zip_code = request.form.get('zip_code')
            caste = request.form.get('caste')
            action = request.form.get('action')

            # Verify if school_id exists
            cursor.execute('SELECT * FROM School WHERE school_id = %s', (school_id,))
            if not cursor.fetchone():
                return "Error: School ID does not exist!"

            # Verify if student_id is unique
            if action != 'updateStudent':
                cursor.execute('SELECT * FROM Student WHERE student_id = %s', (student_id,))
                if cursor.fetchone():
                    return "Error: Student ID already exists!"

            if action == 'updateStudent':
                cursor.execute('UPDATE Student SET school_id = %s, first_name = %s, last_name = %s, dob = %s, academic_year = %s, city = %s, zip_code = %s, caste = %s WHERE student_id = %s',
                               (school_id, first_name, last_name, dob, academic_year, city, zip_code, caste, student_id))
                mysql.connection.commit()
            else:
                cursor.execute('INSERT INTO Student (student_id, school_id, first_name, last_name, dob, academic_year, city, zip_code, caste) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (student_id, school_id, first_name, last_name, dob, academic_year, city, zip_code, caste))
                mysql.connection.commit()
            return redirect(url_for('student'))

    return redirect(url_for('login'))


# Route for deleting a student
@app.route("/delete_student", methods=['GET'])
def delete_student():
    if 'loggedin' in session:
        student_id = request.args.get('student_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute('DELETE FROM Stud_score WHERE student_id = %s', (student_id,))
            mysql.connection.commit()

            cursor.execute('DELETE FROM Parent WHERE student_id = %s', (student_id,))
            mysql.connection.commit()

            cursor.execute('DELETE FROM Student WHERE student_id = %s', (student_id,))
            mysql.connection.commit()
            
            return redirect(url_for('student'))
        except Exception as e:
            print("Error:", e)
            return "Error occurred while deleting student"
    return redirect(url_for('login'))



########################### class ##################################

@app.route("/classes", methods =['GET', 'POST'])
def classes():
    if 'loggedin' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT class_id , name FROM class')
        classes = cursor.fetchall() 
        
        return render_template("class.html", classes = classes)
    return redirect(url_for('login'))

@app.route("/edit_class", methods =['GET'])
def edit_class():
    if 'loggedin' in session:
        class_id = request.args.get('class_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT class_id , name FROM class WHERE class_id = %s', (class_id,))
        classes = cursor.fetchall() 
        
        return render_template("edit_class.html", classes = classes)
    return redirect(url_for('login'))  

# Route for saving class information
@app.route("/save_class", methods=['POST'])
def save_class():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        if request.method == 'POST':
            name = request.form.get('name')
            class_id = request.form.get('class_id')
            action = request.form.get('action')
            
            # Verify if class_id is unique
            if action != 'updateClass':
                cursor.execute('SELECT * FROM class WHERE class_id = %s', (class_id,))
                if cursor.fetchone():
                    return "Error: Class ID already exists!"
                
            if action == 'updateClass':
                cursor.execute('UPDATE class SET name = %s WHERE class_id = %s', (name, class_id))
            else:
                cursor.execute('INSERT INTO class (class_id, name) VALUES (%s, %s)', (class_id, name))
                
            mysql.connection.commit()
            return redirect(url_for('classes'))
    return redirect(url_for('login'))


@app.route("/delete_class", methods =['GET'])
def delete_class():
    if 'loggedin' in session:
        class_id = request.args.get('class_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM class WHERE class_id = % s', (class_id, ))
        mysql.connection.commit()   
        return redirect(url_for('classes'))
    return redirect(url_for('login')) 

########################### parent ##################################

@app.route("/parent", methods=['GET', 'POST'])
def parent():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT first_name, last_name, student_id, phone_no, relationship_with_student,email FROM Parent')
        parents = cursor.fetchall()
        return render_template("parent.html", parents=parents)
    return redirect(url_for('login'))

@app.route("/edit_parent", methods=['GET'])
def edit_parent():
    if 'loggedin' in session:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        student_id = request.args.get('student_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT first_name, last_name, student_id, phone_no, relationship_with_student, email FROM Parent WHERE first_name = %s AND last_name = %s AND student_id = %s', (first_name, last_name, student_id))
        parents = cursor.fetchall()
        return render_template("edit_parent.html", parents=parents)
    return redirect(url_for('login'))
  

# Route for saving parent information
@app.route("/save_parent", methods=['POST'])
def save_parent():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            student_id = request.form['student_id']
            phone_no = request.form['phone_no']
            relationship_with_student = request.form['relationship_with_student']
            email = request.form['email']
            action = request.form['action']
            
            # Check if the parent already exists
            cursor.execute('SELECT * FROM Parent WHERE first_name = %s AND last_name = %s AND student_id = %s', (first_name, last_name, student_id))
            if cursor.fetchone():
                return "Duplicate entry '{}'-'{}'-{} or already parent exists.".format(first_name, last_name, student_id)

            # Verify if student_id exists
            cursor.execute('SELECT * FROM Student WHERE student_id = %s', (student_id,))
            if not cursor.fetchone():
                return "Error: Student ID does not exist!"

            if action == 'updateParent':
                cursor.execute('UPDATE Parent SET phone_no = %s, relationship_with_student = %s, email = %s WHERE first_name = %s AND last_name = %s AND student_id = %s', 
                               (phone_no, relationship_with_student, email, first_name, last_name, student_id))
                mysql.connection.commit()
            else:
                cursor.execute('INSERT INTO Parent (first_name, last_name, student_id, phone_no, relationship_with_student, email) VALUES (%s, %s, %s, %s, %s, %s)', 
                               (first_name, last_name, student_id, phone_no, relationship_with_student, email))
                mysql.connection.commit()
            return redirect(url_for('parent'))
    return redirect(url_for('login'))


@app.route("/delete_parent", methods=['GET'])
def delete_parent():
    if 'loggedin' in session:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        student_id = request.args.get('student_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Parent WHERE first_name = %s AND last_name = %s AND student_id = %s', (first_name, last_name, student_id))
        mysql.connection.commit()
        return redirect(url_for('parent'))
    return redirect(url_for('login'))


########################### course ##################################

# Route for displaying the courses list
@app.route("/course", methods=['GET', 'POST'])
def course():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT course_id, name, teacher_id, class_id FROM Course')
        courses = cursor.fetchall() 
        return render_template("course.html", courses=courses)
    return redirect(url_for('login'))

# Route for editing a course's information
@app.route("/edit_course", methods=['GET'])
def edit_course():
    if 'loggedin' in session:
        course_id = request.args.get('course_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT course_id, name, teacher_id, class_id FROM Course WHERE course_id = %s', (course_id,))
        courses = cursor.fetchall() 
        return render_template("edit_course.html", courses=courses)
    return redirect(url_for('login'))  
    
# Route for saving course information
@app.route("/save_course", methods=['GET', 'POST'])
def save_course():
    if 'loggedin' in session:
        if request.method == 'POST':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            course_id = request.form.get('course_id')
            name = request.form.get('name')
            teacher_id = request.form.get('teacher_id')
            class_id = request.form.get('class_id')
            action = request.form.get('action')

            # Verify if teacher_id exists
            cursor.execute('SELECT * FROM Teacher WHERE teacher_id = %s', (teacher_id,))
            if not cursor.fetchone():
                return "Error: Teacher ID does not exist!"

            # Verify if class_id exists
            cursor.execute('SELECT * FROM Class WHERE class_id = %s', (class_id,))
            if not cursor.fetchone():
                return "Error: Class ID does not exist!"

            # Verify if course_id is unique
            if action != 'updateCourse':
                cursor.execute('SELECT * FROM Course WHERE course_id = %s', (course_id,))
                if cursor.fetchone():
                    return "Error: Course ID already exists!"

            if action == 'updateCourse':
                cursor.execute('UPDATE Course SET name = %s, teacher_id = %s, class_id = %s WHERE course_id = %s',
                               (name, teacher_id, class_id, course_id))
                mysql.connection.commit()
                return redirect(url_for('course'))
            else:
                cursor.execute('INSERT INTO Course (course_id, name, teacher_id, class_id) VALUES (%s, %s, %s, %s)',
                               (course_id, name, teacher_id, class_id))
                mysql.connection.commit()
                return redirect(url_for('course'))

    return redirect(url_for('login'))


# Route for deleting a course
@app.route("/delete_course", methods=['GET'])
def delete_course():
    if 'loggedin' in session:
        course_id = request.args.get('course_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute('DELETE FROM Course WHERE course_id = %s', (course_id,))
            mysql.connection.commit()   
            return redirect(url_for('course'))
        except Exception as e:
            print("Error:", e)  # Print the specific error message
            return "Error occurred while deleting course: " + str(e)  # Return the error message to the user
    return redirect(url_for('login'))

########################### marks ##################################


@app.route("/marks", methods=['GET', 'POST'])
def marks():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT student_id, course_id, marks_scored FROM Stud_score')
        marks = cursor.fetchall()
        return render_template("marks.html", marks=marks)
    return redirect(url_for('login'))

@app.route("/edit_marks", methods=['GET'])
def edit_marks():
    if 'loggedin' in session:
        student_id = request.args.get('student_id')
        course_id = request.args.get('course_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT student_id, course_id, marks_scored FROM Stud_score WHERE student_id = %s AND course_id = %s', (student_id, course_id))
        marks = cursor.fetchall()
        return render_template("edit_marks.html", marks=marks)
    return redirect(url_for('login'))

@app.route("/save_marks", methods=['POST'])
def save_marks():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            student_id = request.form['student_id']
            course_id = request.form['course_id']
            marks_scored = request.form['marks_scored']
            action = request.form['action']

            # Verify if student_id exists
            cursor.execute('SELECT * FROM Student WHERE student_id = %s', (student_id,))
            if not cursor.fetchone():
                return "Error: Student ID does not exist!"

            # Verify if course_id exists
            cursor.execute('SELECT * FROM Course WHERE course_id = %s', (course_id,))
            if not cursor.fetchone():
                return "Error: Course ID does not exist!"

            # Check if marks for the same student and course already exist
            cursor.execute('SELECT * FROM Stud_score WHERE student_id = %s AND course_id = %s', (student_id, course_id))
            existing_marks = cursor.fetchone()
            if existing_marks:
                if action == 'updateMarks':
                    # If updating marks, proceed with the update
                    cursor.execute('UPDATE Stud_score SET marks_scored = %s WHERE student_id = %s AND course_id = %s', 
                                   (marks_scored, student_id, course_id))
                    mysql.connection.commit()
                else:
                    # If adding new marks and they already exist, return an error message
                    return "Error: Marks for the same student and course already exist!"
            else:
                # If marks for the same student and course do not exist, insert the new marks
                cursor.execute('INSERT INTO Stud_score (student_id, course_id, marks_scored) VALUES (%s, %s, %s)', 
                               (student_id, course_id, marks_scored))
                mysql.connection.commit()
                
            return redirect(url_for('marks'))
    return redirect(url_for('login'))



@app.route("/delete_marks", methods=['GET'])
def delete_marks():
    if 'loggedin' in session:
        student_id = request.args.get('student_id')
        course_id = request.args.get('course_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Stud_score WHERE student_id = %s AND course_id = %s', (student_id, course_id))
        mysql.connection.commit()
        return redirect(url_for('marks'))
    return redirect(url_for('login'))


########################### student marks report ##################################


# Flask route for displaying the student marks report
@app.route("/student_marks_report")
def student_marks_report():
    # Fetch list of student IDs from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT DISTINCT student_id FROM Stud_score')
    student_ids = [row['student_id'] for row in cursor.fetchall()]
    return render_template("student_marks_report.html", student_ids=student_ids)

# Flask route for fetching student marks based on student ID
@app.route("/get_student_marks/<int:student_id>")
def get_student_marks(student_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            Student.first_name,
            Student.last_name,
            Course.name AS course,
            Stud_score.marks_scored
        FROM 
            Student
        JOIN 
            Stud_score ON Student.student_id = Stud_score.student_id
        JOIN 
            Course ON Stud_score.course_id = Course.course_id
        WHERE 
            Student.student_id = %s
    ''', (student_id,))
    marks = cursor.fetchall()
    return jsonify(marks)



########################### student details ##################################


# Flask route for displaying the student details and number of students in a class
@app.route("/student_details")
def student_details():
    # Fetch list of class IDs from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT class_id FROM Class')
    class_ids = cursor.fetchall()
    return render_template("student_details.html", class_ids=class_ids)

# Flask route for fetching student details based on class ID
# Flask route for fetching student details based on class ID
@app.route("/get_students_in_class/<int:class_id>")
def get_students_in_class(class_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            distinct(s.student_id), s.first_name, s.last_name
        FROM 
            Student s
        JOIN 
            Stud_score ss ON s.student_id = ss.student_id
        JOIN 
            Course c ON ss.course_id = c.course_id
        JOIN 
            Class cl ON c.class_id = cl.class_id
        WHERE 
            cl.class_id = %s
    ''', (class_id,))
    students = cursor.fetchall()
    return jsonify(students)


# Flask route for fetching the number of students in a class
@app.route("/get_num_students/<int:class_id>")
def get_num_students(class_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT COUNT(Student.student_id) AS num_students
        FROM Student
        JOIN Course ON Student.student_id = Course.student_id
        WHERE Course.class_id = %s
    ''', (class_id,))
    num_students = cursor.fetchone()
    return jsonify(num_students)


if __name__ == "__main__":
    app.run()
    os.execv(__file__, sys.argv)

