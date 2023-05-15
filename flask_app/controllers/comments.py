from flask import render_template, request, flash, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment
from datetime import datetime
import mysql.connector


@app.route('/comment/create/submit/<post_id>', methods=['POST'])
def submit_comment(post_id):
    if 'user_id' not in session:
        return redirect('/')

    content = request.form['content']
    user_id = session['user_id']

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='potter123',
        database='whats_the_issue'
    )
    cursor = connection.cursor()

    insert_query = "INSERT INTO comments (content, created_at, updated_at, user_id, post_id) VALUES (%s, %s, %s, %s, %s)"
    values = (content, datetime.now(), datetime.now(), user_id, post_id)
    cursor.execute(insert_query, values)

    connection.commit()
    connection.close()

    return redirect('/homepage')

@app.route('/post/<int:post_id>/comments')
def show_comments(post_id):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='potter123',
        database='whats_the_issue'
    )
    cursor = connection.cursor()

    query = "SELECT content, created_at, user_id FROM comments WHERE post_id = %s"
    values = (post_id,)
    cursor.execute(query, values)

    comments = cursor.fetchall()

    connection.close()

    return render_template('homepage.html', comments=Comment.get_all_comments)
