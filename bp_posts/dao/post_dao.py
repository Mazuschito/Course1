import json
from json import JSONDecodeError

from bp_posts.dao.post import Post
from exceptions.data_exceptions import DataSourceError


class PostDAO:
    """ Manager of posts - loads, searches, get by pk or by poster name"""

    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """Load data from JSON and returns list of dict"""
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                posts_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Fail to get data from {self.path}")

        return posts_data

    def _load_posts(self):
        """Return list of objects Post"""
        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]

        return list_of_posts

    def get_all(self):
        """ Get all posts, return list of object of class Post """
        posts = self._load_posts()

        return posts

    def get_by_pk(self, pk):
        """ Get post by PK """

        if type(pk) != int:
            raise TypeError("pk must be an int")

        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_in_content(self, substring):
        """Returns list of class object where substring is found"""
        substring = str(substring).lower()
        posts = self._load_posts()
        list_of_posts = []
        for post in posts:
            if substring in post.content.lower():
                list_of_posts.append(post)

        return list_of_posts

    def get_by_poster(self, user_name):
        """Returns list of class object instance posted by poster"""

        if type(user_name) != str:
            raise TypeError("Name must be a str")

        user_name = str(user_name).lower()
        posts = self._load_posts()
        matching_posts = [post for post in posts if post.poster_name.lower() == user_name]

        return matching_posts

