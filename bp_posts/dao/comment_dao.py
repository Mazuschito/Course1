import json
from json import JSONDecodeError

from bp_posts.dao.comment import Comment
from exceptions.data_exceptions import DataSourceError


class CommentDAO():
    """ Manager of comments - loads, returns list of instances and one instance by ID"""

    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """Load data from JSON and returns list of dict"""
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                comments_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Fail to get data from {self.path}")

        return comments_data

    def _load_comments(self):
        """Return list of instance of class Comment"""
        comments_data = self._load_data()
        list_of_comments = [Comment(**comment_data) for comment_data in comments_data]

        return list_of_comments

    def get_by_post_id(self, post_id):
        """Returns list of instances Comment by post ID"""
        comments = self._load_comments()
        matching_comments = []
        for comment in comments:
            if comment.post_id == post_id:
                matching_comments.append(comment)
        return matching_comments
