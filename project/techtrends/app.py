import sqlite3
import logging
import datetime

from flask import Flask, jsonify, json, render_template, request, sessions, url_for, redirect, flash
from flask.helpers import make_response
from werkzeug.exceptions import abort

#Count visit to database
counter = 0
def db_counter():
    global counter
    counter += 1
    return counter

#Define date
recent = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S,")


# Function to get a database connection.
# This function connects to database with the name `database.db`

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    db_counter()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'




  


# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    db_counter()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    # print(posts)
    connection.close()
    return render_template('index.html', posts=posts)





#Count Posts
def countPosts():
    connection = sqlite3.connect('database.db')
    connect = connection.cursor()
    # posts = connection.execute('SELECT COUNT (*) FROM posts').fetchall()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    db_counter()
    connect.close()
    # print(posts)
    return posts


    #Define health check
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )

    app.logger.info(str(recent)  + '  health check successful')
    return response

#Define Metrics
@app.route('/metrics')
def metrics():

    postCount = len(countPosts())
    # dbcount = counter
    


    response = make_response(
            jsonify({
                "db_connection_count": counter ,
                "post_count": postCount}),
            200,
    )

    app.logger.info(str(recent)  + '  Metrics request successful')
    return response



# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info(str(recent)  +'  A non-existing article is accessed')
      return render_template('404.html'), 404
      
    else:
    #  connection = get_db_connection()
    #  title = connection.execute('SELECT title FROM posts WHERE id = ?',
    #                     (post_id,))
    
     app.logger.info( str(recent)  + '  Article "{}" is retrieved'.format(post['title']))
     return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
  
    app.logger.info(str(recent)  + '  The "About Us" page is retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            db_counter()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            app.logger.info(str(recent) + 'A new article "{}" is created'.format(title))
            
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
        ## stream logs to a file
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port='3111')
    # app.debug = True
    ##app.run(debug=True,host='0.0.0.0')


