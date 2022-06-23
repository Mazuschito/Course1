import pytest
from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO


def check_fields_comment(comment):
    """Check if instance has all expected attributes"""
    fields = ["post_id", "commenter_name", "comment", "pk"]

    for field in fields:
        assert hasattr(comment, field), f"No attribute {field}"


class TestCommentDAO:

    @pytest.fixture
    def comment_dao(self):
        comment_dao_instance = CommentDAO("./bp_posts/tests/comments_mock.json")
        return comment_dao_instance

    ### Function _load_comments

    def test_load_comments_types(self, comment_dao):
        """Test if _load_comments returns list and first item in the list is instance of a class"""
        comments = comment_dao._load_comments()
        assert type(comments) == list, "Incorrect type for result"

        comment = comment_dao._load_comments()[0]
        assert type(comment) == Comment, "Incorrect type for  of single instance"

    def test_load_comments_fields(self, comment_dao):
        """Test if instance has all required attributes"""
        comment = comment_dao._load_comments()[0]
        check_fields_comment(comment)

    def test_load_comments_correct_ids(self, comment_dao):
        """Check if pks are matching expected"""
        comments = comment_dao._load_comments()

        correct_pks = {1, 2, 5, 6, 9, 10}
        pks = set([comment.pk for comment in comments])
        assert pks == correct_pks, "Received ID are not matching"

    ### Function get_by_post_id

    def test_get_by_post_id_types(self, comment_dao):
        """Test if get_by_post_id returns first item in the list is instance of a class"""
        comment = comment_dao.get_by_post_id(1)[0]
        assert type(comment) == Comment, "Incorrect type for the result for single item"

    def test_get_by_post_id_fields(self, comment_dao):
        """Test if instance has all required attributes"""
        comment = comment_dao.get_by_post_id(1)[0]
        check_fields_comment(comment)

    def test_get_by_post_id_none(self, comment_dao):
        """Test if instance of non-existent pk is empty list"""
        comment = comment_dao.get_by_post_id(999)
        assert comment == [], "Should be [] for non existent post_id"

    @pytest.mark.parametrize("post_id", [1, 1, 2, 2, 3, 3])
    def test_get_by_correct_post_id(self, comment_dao, post_id):
        """Check if pks are matching expected"""
        comment = comment_dao.get_by_post_id(post_id)[0]
        assert comment.post_id == post_id, f"Incorrect pk for requested post with pk = {post_id}"
