import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from config.config import Config



db_connections_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global db_connections_count
    db_connections_count += 1
    return connection

# Function to get a post using its ID


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY']=Config.secret_key
# Define the main route of the web application


@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('The post ID ' + str(post_id) + ' not found')
      return render_template('404.html'), 404
    else:
      app.logger.info('Article ' + post['title'] + ' retrieved')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('Page About Us retrieved')
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
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info('Article ' + title + ' created.')
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def healthz():
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM posts').fetchall()
        data = {
        'result': "OK - healthy"
        }
        cursor.close()
        connection.close()
        return jsonify(data)  
    except sqlite3.Error as error:
        data = { 
            'result': "ERROR - unhealthy"
        }
        return jsonify(data), 500    

@app.route('/metrics')
def metrics():
    data = {
        "db_connections_count": db_connections_count,
        "post_count": len(get_db_connection().execute('SELECT * FROM posts').fetchall())
    }
    return jsonify(data)
# start the application on port 3111
if __name__ == "__main__":    
    app.run(host=Config.host, port=Config.port)
