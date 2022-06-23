from flask import Flask, render_template, Blueprint, current_app, request
from werkzeug.exceptions import abort
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS
from .dao.comment_dao import CommentDAO
from .dao.post_dao import PostDAO

bp_posts = Blueprint("bp_posts", __name__, template_folder="templates")
post_dao = PostDAO(DATA_PATH_POSTS)
comment_dao = CommentDAO(DATA_PATH_COMMENTS)


@bp_posts.route("/")
def page_posts():
    """ Main page with all posts """
    all_posts = post_dao.get_all()
    return render_template("index.html", posts=all_posts)


@bp_posts.route("/posts/<int:pk>/")
def page_posts_single(pk):
    """ Page of a specific post with comments shown """
    post = post_dao.get_by_pk(pk)
    comments = comment_dao.get_by_post_id(pk)
    comments_count = len(comments)

    if post is None:
        abort(404)

    return render_template("post.html", post=post, comments=comments, comments_count=comments_count)


@bp_posts.route("/users/<poster_name>/")
def page_user(poster_name):
    """ Page of a specific user with all its posts listed """
    posts = post_dao.get_by_poster(poster_name)

    if not posts:
        abort(404, "Such user does not exist")

    return render_template("user-feed.html", posts=posts)


@bp_posts.route("/search/")
def search_by_substring():
    """ Page with result of search listed """
    s = request.values.get("s", None)
    posts = post_dao.search_in_content(s)
    posts_count = len(posts)
    return render_template("search.html", posts=posts, s=s, posts_count=posts_count)
