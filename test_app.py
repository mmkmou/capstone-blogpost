from email import header
import os
from unicodedata import category
import unittest
import json
from wsgiref import headers
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Posts, Comments


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        """
        self.database_name = "trivia_test"
        self.database_path = 'postgres://{}:{}@{}/{}'.format('postgres','Pa553R','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        """

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_post = {
                        "title": "Lorem ipsum dolor sit ame",
                        "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vitae augue vel massa commodo blandit sed non mauris. Phasellus condimentum urna eget porttitor vestibulum. Integer vitae cursus arcu. Aliquam metus eros, consequat quis laoreet in, pharetra vel massa. Praesent finibus augue lacus, sit amet accumsan magna mollis eu. Quisque metus tortor, feugiat eget maximus quis, faucibus ut nibh. In vel elit quis tellus aliquam rutrum a vel leo. Pellentesque a justo at est convallis volutpat vitae eu arcu. Nulla a tellus nulla.",
                        "image_url": "https://ihdemu.com/images/blog/que-es-lorem-ipsum.jpg"
                    }

        self.new_bad_question = {
                        "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam vitae augue vel massa commodo blandit sed non mauris. Phasellus condimentum urna eget porttitor vestibulum. Integer vitae cursus arcu. Aliquam metus eros, consequat quis laoreet in, pharetra vel massa. Praesent finibus augue lacus, sit amet accumsan magna mollis eu. Quisque metus tortor, feugiat eget maximus quis, faucibus ut nibh. In vel elit quis tellus aliquam rutrum a vel leo. Pellentesque a justo at est convallis volutpat vitae eu arcu. Nulla a tellus nulla.",
                        "image_url": "https://ihdemu.com/images/blog/que-es-lorem-ipsum.jpg"
                    }
    
        self.new_comment = {
                        "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
                        "post_id": 1,
                        "title": "a new comment"
                    }
        
        self.new_bad_comment = {
                        "message": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
                        "title": "a new comment"
                    }

        self.reader_header = {
            'Authorization': 'Bearer ' + os.environ['TOKEN_READER']
        }

        self.editor_header = {
            'Authorization': 'Bearer ' + os.environ['TOKEN_EDITOR']
        }
        

    def tearDown(self):
        """Executed after reach test"""
        pass

    
    # Test for Anonymous
    #------------------------------------------------------------#
    
    # Test get all posts
    def test_get_all_posts(self):
        ''' Test anonymous get all posts '''
        res = self.client().get("/api/v1/posts")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["posts"])
        self.assertEqual(data["total_posts"], len(data["posts"]))

    # Test get detailed post
    def test_get_detailed_posts(self):
        ''' Test anonymous get  posts 1 '''
        res = self.client().get("/api/v1/posts/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["posts"])

    # Test get post comments
    def test_get_posts_comments(self):
        ''' Test anonymous get comments posts 1 '''
        res = self.client().get("/api/v1/posts/1/comments")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["comments"])

    # Test create post
    def test_create_post(self):
        ''' Test anonymous create posts 1 '''
        res = self.client().post("/api/v1/posts", json = self.new_post)
        
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test update post
    def test_update_post(self):
        ''' Test anonymous update  posts 1 '''
        res = self.client().patch("/api/v1/posts/1", json = { "title": "updated post title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test create comment
    def test_create_comment(self):
        ''' Test anonymous create comment  posts 1 '''
        res = self.client().post("/api/v1/comments", json = self.new_comment)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test update comment
    def test_update_comment(self):
        ''' Test update comment anonymous '''
        res = self.client().patch("/api/v1/comments/1", json = { "title": "updated comment title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

     # Test update comment
    def test_vote_comment(self):
        ''' Test vote comment anonymous '''
        res = self.client().patch("/api/v1/comments/1/vote")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test for Reader
    #------------------------------------------------------------#
    
    # Test get all posts
    def test_get_all_posts_reader(self):
        ''' Test reader get all posts '''
        res = self.client().get("/api/v1/posts", headers = self.reader_header )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["posts"])
        self.assertEqual(data["total_posts"], len(data["posts"]))

    # Test get detailed post
    def test_get_detailed_posts_reader(self):
        ''' Test reader get  posts 1 '''
        res = self.client().get("/api/v1/posts/1", headers = self.reader_header )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["posts"])

    # Test get post comments
    def test_get_posts_comments_reader(self):
        ''' Test reader get comments posts 1 '''
        res = self.client().get("/api/v1/posts/1/comments", headers = self.reader_header )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["comments"])

    # Test create post
    def test_create_post_reader(self):
        ''' Test reader create posts 1 '''
        res = self.client().post("/api/v1/posts", headers = self.reader_header , json = self.new_post)
        
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    # Test update post
    def test_update_post_reader(self):
        ''' Test reader update posts 1 '''
        res = self.client().patch("/api/v1/posts/1", headers = self.reader_header , json = { "title": "updated post title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    # Test create comment
    def test_create_comment_reader(self):
        ''' Test reader create comment  posts 1 '''
        res = self.client().post("/api/v1/comments", headers = self.reader_header , json = self.new_comment)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["comments"])

    # Test update comment
    def test_update_comment_reader(self):
        ''' Test reader update comment '''
        res = self.client().patch("/api/v1/comments/1", headers = self.reader_header , json = { "title": "updated comment title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    # Test vote comment
    def test_vote_comment_reader(self):
        ''' Test reader vote comment '''
        res = self.client().patch("/api/v1/comments/1/vote", headers = self.reader_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["score"])




    # Test for Editor
    #------------------------------------------------------------#
    
    # Test get all posts
    def test_get_all_posts_editor(self):
        ''' Test editor get all posts '''
        res = self.client().get("/api/v1/posts", headers = self.editor_header )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["posts"])
        self.assertEqual(data["total_posts"], len(data["posts"]))

    # Test get detailed post
    def test_get_detailed_posts_editor(self):
        ''' Test editor get  posts 1 '''
        res = self.client().get("/api/v1/posts/1", headers = self.editor_header )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["posts"])

    # Test get post comments
    def test_get_posts_comments_editor(self):
        ''' Test editor get comments posts 1 '''
        res = self.client().get("/api/v1/posts/1/comments", headers = self.editor_header )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["comments"])

    # Test create post
    def test_create_post_editor(self):
        ''' Test editor create posts 1 '''
        res = self.client().post("/api/v1/posts", headers = self.editor_header , json = self.new_post)
        
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["posts"], True)

    # Test update post
    def test_update_post_editor(self):
        ''' Test editor update posts 1 '''
        post_id = 1
        res = self.client().patch("/api/v1/posts/"+str(post_id), headers = self.editor_header , json = { "title": "updated post title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated"], post_id)

    # Test create comment
    def test_create_comment_editor(self):
        ''' Test editor create comment  posts 1 '''
        res = self.client().post("/api/v1/comments", headers = self.editor_header , json = self.new_comment)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["comments"])

    # Test update comment
    def test_update_comment_editor(self):
        ''' Test editor update comment '''
        comment_id = 1
        res = self.client().patch("/api/v1/comments/"+str(comment_id), headers = self.editor_header , json = { "title": "updated comment title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["comments"])

    # Test vote comment
    def test_vote_comment_editor(self):
        ''' Test editor vote comment '''
        res = self.client().patch("/api/v1/comments/1/vote", headers = self.editor_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["score"])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()