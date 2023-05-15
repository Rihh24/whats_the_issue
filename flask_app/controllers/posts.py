from flask import render_template, request, flash, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment

@app.route('/homepage')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
        
    return render_template('homepage.html', user=user, posts=Post.get_all_posts())

@app.route('/posts/<int:id>')
def user_posts(id):
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_id({"id": id})
    if not user:
        return redirect('/logout')

    posts = Post.get_posts_by_user_id(user.id)

    for post in posts:
        post.comments = Comment.get_comments_by_post_id(post.id)

    return render_template("profile.html", user=user, posts=posts)

@app.route('/profile/<int:id>')
def other_user_posts(id):
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_id({"id": id})
    if not user:
        return redirect('/logout')

    posts = Post.get_posts_by_user_id(user.id)

    for post in posts:
        post.comments = Comment.get_comments_by_post_id(post.id)

    return render_template("other_profiles.html", user=user, posts=posts)


@app.route('/posts/create')
def create_post():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return redirect('/homepage')

@app.route('/post/create/submit', methods =['POST'])
def submit_post():
    if 'user_id' not in session:
        return redirect('/')
    if not Post.validate_new_post(request.form):
        return redirect('/posts/create')

    data = {
        'comic_name': request.form['comic_name'],
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    Post.save_post(data)
    return redirect('/homepage')

@app.route('/posts/update/<int:id>')
def update_post_page(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
    return render_template('update_post.html',user=user, post=Post.get_one_post({'id': id}))


@app.route('/posts/update/submit/<int:id>', methods=['POST'])
def submit_update_post(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Post.validate_new_post(request.form):
        return redirect(f'/posts/update/{id}')
    data={
        'id': id,
        'comic_name': request.form['comic_name'],
        'content': request.form['content']
    }
    Post.update_post(data)
    return redirect('/homepage')



@app.route('/posts/destroy/<int:id>')
def destroy(id):
    data = {
        'post_id': id
    }
    Post.destroy(id)
    return redirect('/homepage')
