from . import courses_view
from flask import Flask, redirect, render_template, request, flash, session
from .models import Courses
from flaskr.colleges.models import Colleges
from .forms import AddCourse
import json
from flaskr import mysql

@courses_view.route('/courses', methods=['GET','POST'])
def view_courses():
    courses = Courses.query_all()
    colleges = Colleges.query_all()
    colleges = [(college['college_code'],college['college_name']) for college in colleges]
    session['college_choices'] = colleges
    query = request.args.get('query','')
    college_filter = request.args.get('college-filter')

    if query.strip() == '':
        courses = Courses.query_all()
    else:
        courses = Courses.query_filter(all=query)

    if college_filter != 'None':
        courses = list(filter(lambda x: x['college_code'] == college_filter, courses))
    print(colleges)
    return render_template('courses/courses.html', courses=courses, query=query, college_choices=colleges, college_filter=college_filter)

@courses_view.route('/courses/add', methods=['GET','POST'])
def add_course():  
    form = AddCourse(request.form)
    colleges = Colleges.query_all()
    colleges = [(college['college_code'],college['college_name']) for college in colleges]
    session['college_choices'] = colleges
    form.college.choices = colleges
    if request.method == 'POST':
        # validate form
        if not form.validate():
            flash(f"Invalid inputs, please check the fields.", category='error')
            return render_template('courses/add-courses.html', form=form)

        course_code = form.course_code.data.upper()
        course_name = form.course_name.data.title()
        college_code = form.college.data
        # validate if course code already exists
        code_exists = Courses.query_get(course_code)
        invalid_input = False
        if code_exists:
            form.course_code.errors = ['This code is already in use.']
            invalid_input = True

        name_exists = Courses.query_filter(course_name=course_name)

        if len(name_exists) > 0:
            invalid_input = True
            form.course_name.errors = ['This name is already in use.']
        
        if invalid_input == True:
            flash(f'Invalid inputs, please check the fields.', category='error')
            return render_template('courses/add-courses.html', form=form)

        
        new_course = Courses(course_name=course_name, course_code=course_code, college_code=college_code)

        new_course.add()
        mysql.connection.commit()
        flash(f'Successfully added "{new_course.course_code} - {new_course.course_name}"', category='success')
        return redirect('/courses')
    return render_template('courses/add-courses.html', form=form)

@courses_view.route('/courses/delete', methods=['POST'])
def delete_course():
    if request.method == 'POST':
        id = request.form.get('course-code')
        course = Courses.query_get(id)
        Courses.delete_course(id)
        mysql.connection.commit()
        flash(f'Successfully Deleted {course["course_code"]} - {course["course_name"]}', category='success')
        return redirect('/courses')
    
@courses_view.route('/courses/edit/<id>', methods=['GET','POST'])
def edit_course(id):
    course = Courses.query_get(id)
    form = AddCourse()
    colleges = Colleges.query_all()
    colleges = [(college['college_code'],college['college_name']) for college in colleges]
    session['college_choices'] = colleges
    form.college.choices = colleges
    college_origin = Colleges.query_get(course['college_code'])

    if request.method == 'POST':
        if not form.validate():
            flash(f"Invalid inputs, please check the fields.", category='error')
            return render_template('courses/edit-courses.html', form=form, course=course, college_origin=college_origin)

        target_course_code = course['course_code']
        target_course_name = course['course_name']
        new_course_code = form.course_code.data.upper()
        new_course_name = form.course_name.data.title()
        new_college_code = form.college.data

        # validate if course already exists
        code_exists = Courses.query_get(new_course_code)
        invalid_input = False
        if code_exists and code_exists['course_code'] != target_course_code:
            form.course_code.errors = ['This code is already in use by another course.']
            invalid_input = True

        name_exists = Courses.query_filter(course_name=new_course_name)

        if len(name_exists) > 0 and name_exists[0]['course_name'] != target_course_name:
            invalid_input = True
            form.course_name.errors = ['This name is already in use by another course.']
        
        if invalid_input == True:
            flash(f'Invalid inputs, please check the fields.', category='error')
            return render_template('courses/edit-courses.html', form=form, course=course,  college_origin=college_origin)
        
        Courses.update(old_code=target_course_code, new_code=new_course_code, new_name=new_course_name, new_college=new_college_code)
        mysql.connection.commit()
        flash(f'Successfully edited "{target_course_code} - {target_course_name}" to "{new_course_code} - {new_course_name}"', category='success')
        return redirect('/courses')
    
    form.course_code.data = course['course_code']
    form.course_name.data = course['course_name']
    form.college.data = course['college_code']
    return render_template('courses/edit-courses.html', course=course, form=form, college_origin=college_origin)