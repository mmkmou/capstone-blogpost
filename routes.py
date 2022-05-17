from flask import Blueprint
from controllers import posts, post_details, create_post, update_post, delete_post, post_comments, create_comment, update_comment, vote_comment, delete_comment

api = Blueprint('', __name__)

# posts routes
api.route('/posts')(posts)
api.route('/posts/<int:post_id>')(post_details)
api.route('/posts/<int:post_id>/comments')(post_comments)
api.route('/posts', methods=['POST'])(create_post)
api.route('/posts/<int:post_id>', methods=['PATCH'])(update_post)
api.route('/posts/<int:post_id>', methods=['DELETE'])(delete_post)


# Comments routes 
api.route('/comments', methods=['POST'])(create_comment)
api.route('/comments/<int:comment_id>', methods=['PATCH'])(update_comment)
api.route('/comments/<int:comment_id>/vote', methods=['PATCH'])(vote_comment)
api.route('/comments/<int:comment_id>', methods=['DELETE'])(delete_comment)


