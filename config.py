import os

DATA_PATH_POSTS = os.path.join("data", "posts.json")
DATA_PATH_COMMENTS = os.path.join("data", "comments.json")
DATA_PATH_BOOKMARKS = os.path.join("data", "bookmarks.json")

LOGGER_API_PATH = os.path.join("logs", "api.log")
LOGGER_FORMAT = f"%(asctime)s - (%(levelname)s) - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
