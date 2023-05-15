from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import bcrypt
from flask import flash

class User:
    db ="whats_the_issue"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data.get('password', '')
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []
        self.comments = []


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL('whats_the_issue').query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('whats_the_issue').query_db(query)
        users=[]
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('whats_the_issue').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('whats_the_issue').query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return None


    @classmethod
    def get_one_with_posts(cls, data):
        from flask_app.models.post import Post
        from flask_app.models.comment import Comment
        from flask_app.config.mysqlconnection import connectToMySQL

        query = "SELECT users.id, users.first_name, users.last_name, users.email, users.created_at, users.updated_at, posts.id AS post_id, posts.comic_name, posts.content AS post_content, posts.created_at AS post_created_at, comments.content AS comment_content, comments.created_at AS comment_created_at FROM users LEFT JOIN posts ON users.id = posts.user_id LEFT JOIN comments ON posts.id = comments.post_id WHERE users.id = %(id)s"
        results = connectToMySQL('whats_the_issue').query_db(query, data)

        user = None
        posts = []
        current_post = None

        for row in results:
            if user is None:
                user_data = {
                    'id': row['id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                user = cls(user_data)

            if current_post is None or current_post.id != row['post_id']:
                post_data = {
                    'id': row['post_id'],
                    'comic_name': row['comic_name'],
                    'content': row['post_content'],
                    'created_at': row['post_created_at']
                }
                current_post = Post(post_data)
                posts.append(current_post)

            if row['comment_content'] is not None:
                comment_data = {
                    'id': row['id'],
                    'content': row['comment_content'],
                    'created_at': row['comment_created_at'],
                    'user_id': row['id'],
                    'post_id': row['post_id']
                }
                comment = Comment(comment_data)
                current_post.comments.append(comment)

        user.posts = posts
        for post in posts:
            print(post.creator)
            print(post.comic_name)
            print(post.content)
        return user



    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('whats_the_issue').query_db(query,user)
        if len(results) >= 1:
            flash("This email is already in use", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is invalid, try again", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("Your name must be 2 characters or more", "register")
            is_valid=False
        if len(user["last_name"]) < 2:
            flash("Last name must be 2 characters or more", "register")
            is_valid=False
        if len(user["password"]) < 6:
            flash("Your password must be 6 characters or more", "register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Your passwords do not match try again", "register")
            is_valid= False
        return is_valid
    
    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email/password.","login")
            return False

        user = User.get_by_email(form_data)
        if not user:
            flash("Invalid email/password.","login")
            return False
        
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Invalid email/password.","login")
            return False
        
        return user