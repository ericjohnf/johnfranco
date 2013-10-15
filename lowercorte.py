import os
import sqlite3

from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')
    
@app.route('/statement')
def state():
    return render_template('statement.html')    
    
@app.route('/bio')
def bio():
    return render_template('bio.html')    

@app.route('/contact')
def contact():
    return render_template('contact.html')    

@app.route('/drawing')
def drawing():
    return render_template('drawing.html')   

@app.route('/painting')
def painting():
    return render_template('painting.html')       
    
