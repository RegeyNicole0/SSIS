from . import students_view
from flask import Flask, redirect, render_template, request, flash, session, current_app
from flaskr.courses.models import Courses
from flaskr.colleges.models import Colleges
from werkzeug.utils import secure_filename
from .models import Students
from .forms import AddStudent
import json
from flaskr import mysql
from config import CLOUDINARY_API_CLOUD, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_API_CLOUD_FOLDER
import cloudinary
import cloudinary.uploader
import time
import os
          
cloudinary.config( 
  cloud_name = CLOUDINARY_API_CLOUD, 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET,
  secure = True
)

@students_view.route('/students', methods=['GET','POST'])
def view_students():
    courses = Courses.query_all()
    courses = [(course['course_code'],course['course_name'], course['college_code']) for course in courses]

    colleges_query = Colleges.query_all()
    colleges = [(college['college_code'],college['college_name']) for college in colleges_query]
    college_codes = [(college['college_code']) for college in colleges_query]

    session['college_choices'] = colleges
    session['course_choices'] = courses

    query = request.args.get('query') if request.args.get('query') != 'None' else None
    college_filter = request.args.get('college-filter') if request.args.get('college-filter') != 'None' else None
    course_filter = request.args.get('course-filter') if request.args.get('course-filter') != 'None' else None
    gender_filter = request.args.get('gender-filter') if request.args.get('gender-filter') != 'None' else None
    year_filter = request.args.get('year-filter')  if request.args.get('year-filter') != 'None' else None

    students = Students.query_filter(all=query, course=course_filter, gender=gender_filter, year_level=year_filter)
    if (query and query.strip() != '') or query == None:
        students = Students.query_filter(all=query, course=course_filter, gender=gender_filter, year_level=year_filter)

    query = '' if not query else query
    return render_template('students/students.html', students=students, course_choices=courses, college_choices=colleges, college_filter=college_filter, course_filter=course_filter, gender_filter=gender_filter, year_filter=year_filter, query=query, college_codes=college_codes)

@students_view.route('/students/add', methods=['GET','POST'])
def add_student():  
    form = AddStudent(request.form)
    courses = Courses.query_all()
    courses = [(course['course_code'],course['course_name']) for course in courses]
    session['course_choices'] = courses
    form.course.choices = courses
    if request.method == 'POST':
        # validate form

        id_number = form.id.data
        first_name = form.first_name.data.title()
        last_name = form.last_name.data.title()
        profile_pic = request.files['profile_pic']
        year_level = form.year.data
        gender = form.gender.data
        course_code = form.course.data
        timestamp = time.time()
        
        # validate if course code already exists
        id_exists = Students.query_get(id_number)
        invalid_input = False
        form_validated = form.validate()
        if not form_validated: invalid_input = True
        if id_exists:
            form.id.errors = ['This id number is already in use.']
            invalid_input = True

        if invalid_input == True:
            flash(f'Invalid inputs, please check the fields.', category='error')
            return render_template('students/add-students.html', form=form)

        
        new_student = Students(id=id_number,first_name=first_name, last_name=last_name, year=year_level, profile_pic=profile_pic,course_code=course_code, gender=gender)

        new_student.add()
        mysql.connection.commit()

        #uploading profile picture
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))

            profile_pic_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
            img_upload = cloudinary.uploader.upload(profile_pic_path,
                                                    folder= CLOUDINARY_API_CLOUD_FOLDER,
                                                    public_id = f"{id_number}{timestamp}"
                                                    )
            img_url = img_upload['secure_url']
            Students.update_pfp(id=id_number,url=img_url)
            mysql.connection.commit()

        flash(f'Successfully added "{new_student.id} - {new_student.first_name} {new_student.last_name}"', category='success')
        return redirect('/students')
    
    return render_template('students/add-students.html', form=form)

@students_view.route('/students/delete', methods=['POST'])
def delete_student():
    if request.method == 'POST':
        id = request.form.get('student-id')
        student = Students.query_get(id)
        Students.delete_student(id)
        mysql.connection.commit()
        flash(f'Successfully Deleted {student["id"]} - {student["last_name"]}, {student["first_name"]}', category='success')
        return redirect('/students')
    
@students_view.route('/students/edit/<id>', methods=['GET','POST'])
def edit_student(id):  
    form = AddStudent(request.form)
    student =  Students.query_get(id)
    courses = Courses.query_all()
    courses = [(course['course_code'],course['course_name']) for course in courses]
    session['college_choices'] = courses
    form.course.choices = courses
    if request.method == 'POST':
        # validate form
        id_number = form.id.data
        first_name = form.first_name.data.title()
        last_name = form.last_name.data.title()
        profile_pic = request.files['profile_pic']
        year_level = form.year.data
        gender = form.gender.data
        course_code = form.course.data

        # validate if course code already exists
        id_exists = Students.query_get(id_number)
        invalid_input = False

        form_validated = form.validate()
        if not form_validated: invalid_input = True
        if id_exists and id_number != student['id']:
            form.id.errors = ['This id number is already in use.']
            invalid_input = True

        if invalid_input == True:
            flash(f'Invalid inputs, please check the fields.', category='error')
            return render_template('students/edit-students.html', form=form, student=student)
        
        Students.update(
            old_id=student['id'],
            new_fname=first_name,
            new_lname=last_name,
            new_year_level=year_level,
            new_course=course_code,
            new_gender=gender,
            new_id=id_number
            )

        mysql.connection.commit()
        timestamp = time.time()
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))

            profile_pic_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
            img_upload = cloudinary.uploader.upload(profile_pic_path,
                                                    folder= CLOUDINARY_API_CLOUD_FOLDER,
                                                    public_id = f"{id_number}{timestamp}"
                                                    )
            img_url = img_upload['secure_url']
            Students.update_pfp(id=id_number,url=img_url)
            mysql.connection.commit()
        flash(f'Successfully Edited {student["id"]} - {student["first_name"]} {student["last_name"]}"', category='success')
        return redirect('/students')
    
    student=Students.query_get(id)
    form.id.data = student['id']
    form.first_name.data = student['first_name']
    form.last_name.data = student['last_name']
    form.gender.data = student['gender']
    form.year.data = str(student['year_level'])
    form.course.data = student['course_code']
    profile_pic = student['profile_pic']

    return render_template('students/edit-students.html', form=form, student=student, profile_pic=profile_pic)