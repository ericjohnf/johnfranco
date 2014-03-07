import os, os.path, re
import sqlite3
from werkzeug.serving import run_simple

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
    navNames = getNavNames(names,file)
      
    print names  
    return render_template('single_demo.html',date=date,medium=medium,file=file,names=names,navNames=navNames)

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

def getNavNames(names,file): # lazy helper cause i'm lazy and dumb derp
    
    if file not in names: # if this isn't here, just dump the first four
        return names[1:5] 
        
    length = len(names)
    current_frame = names.index(file)
    if current_frame == 0:
      return names[1:5]
    elif current_frame == 1:
      return [names[0],names[2],names[3],names[4]]
    elif current_frame == 2:
      return [names[0],names[1],names[3],names[4]]
    elif current_frame > 2 and current_frame<length-2: 
      return [names[current_frame-2], names[current_frame-1], names[current_frame+1], names[current_frame+2]]
    elif current_frame<length-1:
      return [names[current_frame-3], names[current_frame-2], names[current_frame-1], names[current_frame+1]]
    else:
      return [names[current_frame-4], names[current_frame-3], names[current_frame-2], names[current_frame-1]]  

if __name__ == '__main__':
    run_simple('localhost', 8000, app, use_reloader=True, use_debugger=True, use_evalex=True) 