import os, os.path, re
import sqlite3


from flask import Flask, url_for, render_template

app = Flask(__name__)

# helpers
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]  

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False    


@app.route('/')
def hello(names=None):
    the_path = './static/img/works/'
    names = [str(name) for name in os.listdir(the_path)]
    if '.DS_Store' in names:
      names.remove('.DS_Store')
    
    names.sort(key=alphanum_key)  
    return render_template('index.html',names=names)
    
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
    
@app.route('/single')
@app.route('/single/<date>/<medium>/<file>')
def single(date=None,medium=None,file=None,names=None):
    the_path = './static/img/works/'+date+'/'+medium+'/'
    names = [str(name) for name in os.listdir(the_path)]
    names.sort(key=alphanum_key)
    if file in names:
      names.remove(file)
    return render_template('single.html',date=date,medium=medium,file=file,names=names)

@app.route('/show')
@app.route('/show/<date>/<medium>/')
def show(date=None,medium=None,total=None,names=None):
    the_path = './static/img/works/'+date+'/'+medium+'/'
    names = [str(name) for name in os.listdir(the_path)]
    names.sort(key=alphanum_key)
    total = len([name for name in os.listdir(the_path)])
    
    # if date is not None:
      # split = re.findall(r"[^\W\d_]+|\d+", date)
      
    return render_template('show.html',date=date,medium=medium,total=total,names=names)
