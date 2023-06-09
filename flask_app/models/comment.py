from flask_app.config.mysqlconnection import connectToMySQL
import mysql.connector
from flask_app.models.user import User

class Comment:
    def __init__(self, data):
        self.id = data.get('id')
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data.get('updated_at', '')
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.user = None

    @classmethod
    def get_all_comments(cls):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='potter123',
            database='whats_the_issue'
        )
        cursor = connection.cursor()

        query = "SELECT comments.content, comments.created_at, comments.user_id, comments.post_id, users.id, users.first_name, users.last_name FROM comments JOIN users ON comments.user_id = users.id"
        cursor.execute(query)

        comments = []
        for row in cursor.fetchall():
            print("Debug: Row:", row)
            comment_data = {
                'id': row[0],
                'content': row[1],
                'created_at': row[2],
                'user_id': row[3],
                'post_id': row[4]
            }
            comment = Comment(comment_data)
            user_data = {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "password": row[4],
                "created_at": row[5],
                "updated_at": row[6]
            }
            comment.user = User(user_data)
            comments.append(comment)

        connection.close()

        return comments

    @classmethod
    def get_comments_by_post_id(cls, post_id):
        query = """
            SELECT comments.*, users.first_name AS comment_user_first_name, users.last_name AS comment_user_last_name
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.post_id = %(post_id)s;
        """

        data = {"post_id": post_id}
        results = connectToMySQL('whats_the_issue').query_db(query, data)
        comments = []

        for result in results:
            comment = cls(result)
            comment.user = User({
                "id": result['user_id'],
                "first_name": result['comment_user_first_name'],
                "last_name": result['comment_user_last_name'],
                "email": "",
                "password": "",
                "created_at": result['created_at'],
                "updated_at": result['updated_at']
            })
            comments.append(comment)

        return comments


