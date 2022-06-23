import logging

from flask import Flask, render_template, Blueprint, current_app, request, jsonify
from werkzeug.exceptions import abort
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS
from bp_posts.dao.post import Post
from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post_dao import PostDAO

bp_api = Blueprint("bp_api", __name__)

post_dao = PostDAO(DATA_PATH_POSTS)
comment_dao = CommentDAO(DATA_PATH_COMMENTS)

api_logger = logging.getLogger("api_logger")


@bp_api.route("/posts/")
def api_posts_all():
    """ Returns JSON with all posts"""
    all_posts: list[Post] = post_dao.get_all()
    all_posts_as_dict: list[dict] = [post.as_dict() for post in all_posts]

    api_logger.debug("All posts are requested")

    return jsonify(all_posts_as_dict), 200


@bp_api.route("/posts/<int:pk>")
def api_posts_single(pk: int):
    """ Returns JSON with post for requested pk"""
    post: Post | None = post_dao.get_by_pk(pk)
    if post is None:
        api_logger.debug(f"Post {pk} was requested, but not exist")
        abort(404)
    else:
        api_logger.debug(f"Post {pk} was requested")

    return jsonify(post.as_dict()), 200

@bp_api.errorhandler(404)
def api_error_404(error):
    api_logger.error(f"Error: {error}")
    return jsonify({"error": str(error)}), 404


@bp_api.route("/")
def api_index():
    """ Returns basic instruction for a frontend """
    return f"See README on GitHub. Avaliable endpoints /api/posts and /api/posts/pk "
