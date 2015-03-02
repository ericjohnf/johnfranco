import os, os.path 
import sys
import re

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from werkzeug.serving import run_simple

from flask import Flask, url_for, render_template, Response

art = {'2010': {'paint': [{'medium': 'Oil on Linen', 'date_completed': 2008, 'price': 5760, 'height': 36, 'width': 40, 'id': 1}, {'medium': 'Oil on Linen', 'date_completed': 2007, 'price': 4480, 'height': 40, 'width': 28, 'id': 2}, {'medium': 'Oil on Linen', 'date_completed': 2006, 'price': 4080, 'height': 34, 'width': 30, 'id': 3}, {'medium': 'Oil on Linen', 'date_completed': 2010, 'price': 4608, 'height': 32, 'width': 36, 'id': 4}, {'medium': 'Oil on Linen', 'date_completed': 2010, 'price': 4896, 'height': 34, 'width': 36, 'id': 5}, {'medium': 'Oil on Linen', 'date_completed': 2007, 'price': 5440, 'height': 34, 'width': 40, 'id': 6}, {'medium': 'Oil on Linen', 'date_completed': 2008, 'price': 4352, 'height': 32, 'width': 34, 'id': 7}, {'medium': 'Oil on Linen', 'date_completed': 2007, 'price': 7040, 'height': 44, 'width': 40, 'id': 8}, {'medium': 'Oil on Linen', 'date_completed': 2012, 'price': 8448, 'height': 44, 'width': 48, 'id': 9}, {'medium': 'Oil on Linen', 'date_completed': 2008, 'price': 2000, 'height': 40, 'width': 46, 'id': 10}, {'medium': 'Oil on Linen', 'date_completed': 2012, 'price': 3840, 'height': 30, 'width': 32, 'id': 11}, {'medium': 'Oil on Linen', 'date_completed': 2006, 'price': 4352, 'height': 32, 'width': 34, 'id': 12}, {'medium': 'Oil on Linen', 'date_completed': 2011, 'price': 4896, 'height': 34, 'width': 36, 'id': 13}, {'medium': 'Oil on Linen', 'date_completed': 2011, 'price': 4896, 'height': 34, 'width': 36, 'id': 14}, {'medium': 'Oil on Linen', 'date_completed': 2010, 'price': 3120, 'height': 30, 'width': 26, 'id': 15}, {'medium': 'Oil on Linen', 'date_completed': 2010, 'price': 3840, 'height': 30, 'width': 32, 'id': 16}, {'medium': 'Oil on Linen', 'date_completed': 2004, 'price': 4080, 'height': 34, 'width': 30, 'id': 17}, {'medium': 'Oil on Linen', 'date_completed': 2004, 'price': 3808, 'height': 28, 'width': 34, 'id': 18}, {'medium': 'Oil on Linen', 'date_completed': 2002, 'price': 4080, 'height': 30, 'width': 34, 'id': 19}, {'medium': 'Oil on Linen', 'date_completed': 2010, 'price': 6048, 'height': 36, 'width': 42, 'id': 20}], 'draw': [{'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 1}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 2}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 3}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 4}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 5}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 6}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 7}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 8}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2010, 'price': 500, 'height': 18, 'width': 27, 'id': 9}]}, '2013': {'paint': [{'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 24, 'width': 20, 'id': 1}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 26, 'width': 22, 'id': 2}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 26, 'width': 22, 'id': 3}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 26, 'width': 22, 'id': 4}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 26, 'width': 25, 'id': 5}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 24, 'width': 20, 'id': 6}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 32, 'width': 30, 'id': 7}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 26, 'width': 24, 'id': 8}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 32, 'width': 26, 'id': 9}, {'medium': 'Oil on Linen', 'date_completed': 2013, 'price': 2000, 'height': 24, 'width': 27, 'id': 10}], 'draw': [{'medium': 'Graphite on Bond Paper', 'date_completed': 2013, 'price': 500, 'height': 18, 'width': 27, 'id': 1}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2013, 'price': 500, 'height': 18, 'width': 27, 'id': 2}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2012, 'price': 500, 'height': 18, 'width': 27, 'id': 3}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2012, 'price': 500, 'height': 18, 'width': 27, 'id': 4}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2012, 'price': 500, 'height': 18, 'width': 27, 'id': 5}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2012, 'price': 500, 'height': 18, 'width': 27, 'id': 6}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2012, 'price': 500, 'height': 18, 'width': 27, 'id': 7}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2012, 'price': 500, 'height': 18, 'width': 27, 'id': 8}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2012, 'price': 500, 'height': 18, 'width': 27, 'id': 9}, {'medium': 'Graphite on Bond Paper', 'date_completed': 2013, 'price': 500, 'height': 18, 'width': 27, 'id': 10}]}}


app = Flask(__name__)
app.engine = create_engine(os.environ['HEROKU_URI'])
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

@app.route('/art/<id>')
def art(id):
    """ Load cover photo onna store by store tip"""
    query = """SELECT img FROM art WHERE id=:id"""
    result = app.engine.execute(text(query),id=id).first()
    mime_type = 'image/jpeg'
    # Wait does this image even exist?
    if not result:
        img = bytes()
        return Response(img, mimetype=mime_type)    
    # But does it have a cover photo?
    if not result['img']:
        img = bytes()
    else:
        img = result['img']
        # just in case
        if img[:8] == '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
            mime_type = 'image/png'

    return Response(img, mimetype=mime_type)    


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
                      #                                 description='',
                      #                                 medium=piece['medium'],
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