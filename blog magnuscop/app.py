from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blog_db'

mysql = MySQL(app)

# Home route - display blog posts
@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM posts ORDER BY publish_date DESC')
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

# Filter posts by custom date range
@app.route('/filter', methods=['POST'])
def filter_posts():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Filter posts between start_date and end_date
    if start_date and end_date:
        cursor.execute('SELECT * FROM posts WHERE publish_date BETWEEN %s AND %s ORDER BY publish_date DESC', (start_date, end_date))
    else:
        cursor.execute('SELECT * FROM posts ORDER BY publish_date DESC')
        
    posts = cursor.fetchall()
    
    return render_template('index.html', posts=posts, start_date=start_date, end_date=end_date)

# Display single post with comments
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:  # Ensure comment is not empty
            cursor.execute('INSERT INTO comments (post_id, comment) VALUES (%s, %s)', (id, comment))
            mysql.connection.commit()
    
    cursor.execute('SELECT * FROM posts WHERE id = %s', (id,))
    post = cursor.fetchone()
    
    cursor.execute('SELECT * FROM comments WHERE post_id = %s', (id,))
    comments = cursor.fetchall()
    
    return render_template('post.html', post=post, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
