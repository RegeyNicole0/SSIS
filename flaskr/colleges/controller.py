from . import colleges_view
from flask import Flask, redirect, render_template, request, flash
from .models import Colleges
from .forms import AddCollege
import json
from flaskr import mysql


@colleges_view.route('/', methods=['GET'])
def index():
    return redirect('/colleges')


@colleges_view.route('/colleges', methods=['GET'])
def colleges():
    query = request.args.get('query', '')
    if query.strip() == '':
        colleges = Colleges.query_all()
    else:
        colleges = Colleges.query_filter(all=query, search_exact=False)
    
    print(query)
    return render_template('colleges/colleges.html', colleges=colleges, query=query)

@colleges_view.route('/colleges/add', methods=['GET','POST'])
def add_college():  
    form = AddCollege(request.form)
    if request.method == 'POST':
        college_code = form.college_code.data.upper()
        college_name = form.college_name.data.title()
        
        # validate if college already exists
        code_exists = Colleges.query_get(college_code)
        invalid_input = False
        form_validated = form.validate()
        if not form_validated: invalid_input = True
        if code_exists:
            form.college_code.errors = ['This code is already in use.']
            invalid_input = True

        name_exists = Colleges.query_filter(college_name=college_name)

        if len(name_exists) > 0:
            invalid_input = True
            form.college_name.errors = ['This name is already in use.']
        
        if invalid_input == True:
            flash(f'Invalid inputs, please check the fields.', category='error')
            return render_template('colleges/add-colleges.html', form=form)

        
        new_college = Colleges(college_code=college_code, college_name=college_name)

        new_college.add()
        mysql.connection.commit()
        flash(f'Successfully added "{new_college.college_code} - {new_college.college_name}"', category='success')
        return redirect('/colleges')
    return render_template('colleges/add-colleges.html', form=form)


@colleges_view.route('/colleges/delete', methods=['POST'])
def delete_college():
    if request.method == 'POST':
        id = request.form.get('college-code')
        college = Colleges.query_get(id)
        Colleges.delete_college(id)
        mysql.connection.commit()
        flash(f'Successfully Deleted {college["college_code"]} - {college["college_name"]}', category='success')
        return redirect('/colleges')


@colleges_view.route('/colleges/edit/<id>', methods=['GET','POST'])
def edit_college(id):
    college = Colleges.query_get(id)
    form = AddCollege()
    if request.method == 'POST':
        target_college_code = college['college_code']
        target_college_name = college['college_name']
        new_college_code = form.college_code.data.upper()
        new_college_name = form.college_name.data.title()

        # validate if college already exists
        code_exists = Colleges.query_get(new_college_code)
        invalid_input = False
        form_validated = form.validate()
        if not form_validated: invalid_input = True
        if code_exists and code_exists['college_code'] != target_college_code:
            form.college_code.errors = ['This code is already in use by another college.']
            invalid_input = True

        name_exists = Colleges.query_filter(college_name=new_college_name)

        if len(name_exists) > 0 and name_exists[0]['college_name'] != target_college_name:
            invalid_input = True
            form.college_name.errors = ['This name is already in use by another college.']
        
        if invalid_input == True:
            flash(f'Invalid inputs, please check the fields.', category='error')
            return render_template('colleges/edit-colleges.html', form=form, college=college)
        
        Colleges.update(old_code=target_college_code, new_code=new_college_code, new_name=new_college_name)
        mysql.connection.commit()
        flash(f'Successfully edited "{target_college_code} - {target_college_name}" to "{new_college_code} - {new_college_name}"', category='success')
        return redirect('/colleges')
    form.college_code.data = college['college_code']
    form.college_name.data = college['college_name']
    return render_template('colleges/edit-colleges.html', college=college, form=form)
