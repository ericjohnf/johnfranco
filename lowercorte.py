import os, os.path 
import sys
import re

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from werkzeug.serving import run_simple

from flask import Flask, url_for, render_template, Response, send_file, flash, redirect

from forms import ArtForm
from operator import itemgetter

valid_shows = ['2010','2013']
valid_medium = ['paint','draw']

app = Flask(__name__)
app.engine = create_engine(os.environ['HEROKU_URI'])
app.secret_key = 'super secret key'
app.debug = True
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


@app.route('/art/<show>/<medium>/<file>')
def singleArt(show=None,medium=None,file=None):
    # This function will return the image and ascn and desc
    if show not in valid_shows or medium not in valid_medium:
        flash('error', "Can't find that show.")
        return redirect(url_for('hello'))
    # the_path = './static/img/works/'+date+'/'+medium+'/'+file+'.jpg'
    query = "SELECT filename from art where show=:show and medium=:medium"
    result = app.engine.execute(text(query),medium=medium,show=show,file=file)
    artwork = [piece['filename'] for piece in result]

    navNames = getNavNames(artwork,file)
    return render_template('art.html',show=show,medium=medium,file=file,names=artwork,navNames=navNames)

@app.route('/show/<date>/<medium>/', methods=['GET'])
def showdb(date=None,medium=None):
    
    if date not in valid_shows or medium not in valid_medium:
        flash('error', "Can't find that show.")
        return redirect(url_for('hello'))
    
    query = """SELECT title,description,height,width,year,price,filename FROM art WHERE show=:sdate AND medium=:medium ORDER BY filename;"""  
    result = app.engine.execute(text(query),sdate=date,medium=medium)
    artwork = [dict(piece) for piece in result]

    the_path = './static/img/works/'+date+'/'+medium+'/'
    
    artwork = sorted(artwork, key=lambda k: tryint(k['filename']))
    
    return render_template('show.html',date=date,medium=medium,total=len(artwork),the_path=the_path, artwork=artwork)

@app.route('/show_old')
@app.route('/show_old/<date>/<medium>/')
def show(date=None,medium=None,total=None,names=None):
    the_path = './static/img/works/'+date+'/'+medium+'/'
    names = [str(name) for name in os.listdir(the_path)]
    names.sort(key=alphanum_key)
    total = len([name for name in os.listdir(the_path)])
    
    # if date is not None:
      # split = re.findall(r"[^\W\d_]+|\d+", date)
      
    return render_template('show.html',date=date,medium=medium,total=total,names=names)

@app.route('/single/<date>/<medium>/<file>')
def single(date=None,medium=None,file=None,names=None):
    the_path = './static/img/works/'+date+'/'+medium+'/'
    names = [str(name) for name in os.listdir(the_path)]
    names.sort(key=alphanum_key)
    navNames = getNavNames(names,file)
    print navNames
    return render_template('single_demo.html',date=date,medium=medium,file=file,names=names,navNames=navNames)

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

def insertArt():
    
    for date in art:
        for medium, pieces in dict.items(art[date]):
            the_path = './static/img/works/'+date+'/'+medium+'/'
            dirs = os.listdir(the_path)
            # names = [str(name) for name in os.listdir(the_path)]
            for piece in pieces:
                filename = "./static/img/works/{0}/{1}/{2}.jpg".format(date,medium,piece['id'])
                print filename
                with open(filename, "rb") as imageFile:
                  f = imageFile.read()
                  bytes = bytearray(f)
                  # make sure its a jpg
                  if bytes[:3] == '\xFF\xD8\xFF':
                      
                      query = '''INSERT INTO art (title, description, medium, img, show, height, width, year, price, orderid)
                                 VALUES (:title, :description, :medium, :img, :show, :height, :width, :year, :price, :orderid)'''
                        
                      # app.engine.execute(text(query), title='Untitled',
                      #                                 description=piece['medium'],
                      #                                 medium=medium,
                      #                                 img=bytes,
                      #                                 show=date,
                      #                                 height=piece['height'],
                      #                                 width=piece['width'],
                      #                                 year=piece['date_completed'],
                      #                                 price=piece['price'],
                      #                                 orderid=piece['id'])

    return "Nothing"

if __name__ == '__main__':
    run_simple('localhost', 8000, app, use_reloader=True, use_debugger=True, use_evalex=True) 
    
    
    