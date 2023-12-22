from . import colleges_view
from flask import Flask, redirect

@colleges_view.route('/', methods=['GET','POST'])
def index():
    return redirect('/colleges')


@colleges_view.route('/colleges', methods=['GET','POST'])
def colleges():
    return "<h1>Hello colleges! </h1>"