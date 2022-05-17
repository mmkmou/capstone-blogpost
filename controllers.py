from xml.etree.ElementTree import Comment
from werkzeug.exceptions import HTTPException
from auth import requires_auth
from models import Comments, Posts
from flask import request, abort, jsonify

PER_PAGE = 10

"""
    Implement paginate method
    
"""
def paginate(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE

    posts = [post.short() for post in selection]

    return posts[start:end]
   

"""
    Get Pos
    
"""
def posts():

    posts = Posts.query.order_by(Posts.id).all()

    current_posts = paginate(request, posts)

    if len(current_posts) == 0:
            abort(404)

    return jsonify(
        {
            "success": True,
            "posts": current_posts,
            "total_posts":  len(posts)
        }
    )

def post_details(post_id):
    try:
        post = Posts.query.filter(Posts.id == post_id).one_or_none()

        if post is None:
            abort(404)
        
        return jsonify(
            {
                "success": True,
                "posts": post.format()
            }
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            abort(422)

def post_comments(post_id):
    try:
        comments = Comments.query.filter(Comments.post_id == post_id).order_by(Comments.vote.desc()).all()
        
        
        if len(comments) == 0:
            abort(404)
        

        return jsonify(
            {
                "success": True,
                "comments": [comment.format() for comment in comments]
            }
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            abort(422)

@requires_auth('create:post')
def create_post():
    try:
        body = request.get_json()
        post = Posts(
                title=body.get("title"),
                image_url=body.get("image_url"),
                body=body.get("body")
            )

        post.insert()

        return jsonify(
            {
                "success": True,
                "posts": post.short()
            }
        )
        
    except Exception:
        abort(422)

@requires_auth('update:post')
def update_post(post_id):
    try:
        body = request.get_json()
        post = Posts.query.filter(Posts.id == post_id).one_or_none()
        
        if post is None:
            abort(404)

        
        if not body.get("title", None) is None:
            post.title = body.get("title")

        if not body.get("body", None) is None:
            post.body = body.get("body")

        if not body.get("image_url", None) is None:
            post.image_url = body.get("image_url")

        
        post.update()

        return jsonify(
            {
                "success": True,
                "updated": post_id
            }
        )
        
    except Exception as e:
        
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            abort(422)

@requires_auth('delete:post')
def delete_post(post_id):

    try:
        post = Posts.query.filter(Posts.id == post_id).one_or_none()
        
        if post is None:
            abort(404)

        post.delete()

        return jsonify(
            {
                "success": True,
                "deleted": post_id
            }
        )
        
    except Exception as e:
        
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            abort(422)

@requires_auth('create:comment')
def create_comment():
    try:
        body = request.get_json()
        comment = Comments(
                title=body.get("title"),
                message=body.get("message"),
                post_id=body.get("post_id")
            )

        comment.insert()

        return jsonify(
            {
                "success": True,
                "comments": comment.format()
            }
        )
        
    except Exception:
        abort(422)

@requires_auth('update:comment')
def update_comment(comment_id):
    try:
        body = request.get_json()
        comment = Comments.query.filter(Comments.id == comment_id).one_or_none()
        
        if comment is None:
            abort(404)

        
        if not body.get("title", None) is None:
            comment.title = body.get("title")

        if not body.get("body", None) is None:
            comment.message = body.get("message")
        
        comment.update()

        return jsonify(
            {
                "success": True,
                "comments": comment.format()
            }
        )
        
    except Exception as e:
        
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            abort(422)

@requires_auth('vote:comment')
def vote_comment(comment_id):

    try:
        comment = Comments.query.filter(Comments.id == comment_id).one_or_none()
        
        if comment is None:
            abort(404)

        comment.vote += 1
        
        comment.update()

        return jsonify(
            {
                "success": True,
                "score":  comment.vote
            }
        )
        
    except Exception as e:
        
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            abort(422)

@requires_auth('delete:comment')
def delete_comment(comment_id):
    try:
        comment = Comments.query.filter(Comments.id == comment_id).one_or_none()
        
        if comment is None:
            abort(404)

        comment.delete()

        return jsonify(
            {
                "success": True,
                "deleted": comment_id
            }
        )
        
    except Exception as e:
        
        if isinstance(e, HTTPException):
            abort(e.code)
        else:
            abort(422)