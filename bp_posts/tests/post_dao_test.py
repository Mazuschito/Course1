import pytest
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO


def check_fields(post):
    """Check if instance has all expected attributes"""
    fields = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]

    for field in fields:
        assert hasattr(post, field), f"No attribute {field}"


class TestPostsDAO:

    @pytest.fixture
    def post_dao(self):
        post_dao_instance = PostDAO("./bp_posts/tests/posts_mock.json")
        return post_dao_instance

    ### Function get_all

    def test_get_all_types(self, post_dao):
        """Test if get_all() returns instance of a class"""
        posts = post_dao.get_all()
        assert type(posts) == list, "Incorrect type for result"

        posts = post_dao.get_all()[0]
        assert type(posts) == Post, "Incorrect type for  of single instance"

    def test_get_all_fields(self, post_dao):
        """Test if instance has all required attributes"""
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_get_all_correct_ids(self, post_dao):
        """Check if pks are matching expected"""
        posts = post_dao.get_all()

        correct_pks = {1, 2, 3}
        pks = set([post.pk for post in posts])
        assert pks == correct_pks, "Received ID are not matching"

    ### Function get_by_pk

    def test_get_by_pk_types(self, post_dao):
        """Test if get_by_pk returns instance of a class"""
        post = post_dao.get_by_pk(1)
        assert type(post) == Post, "Incorrect type for the result for single item"

    def test_get_by_pk_fields(self, post_dao):
        """Test if instance has all required attributes"""
        post = post_dao.get_by_pk(1)
        check_fields(post)

    def test_get_by_pk_none(self, post_dao):
        """Test if instance of non-existent pk is None"""
        post = post_dao.get_by_pk(999)
        assert post is None, "Should be None for non existent pk"

    @pytest.mark.parametrize("pk", [1, 2, 3])
    def test_get_by_correct_id(self, post_dao, pk):
        """Check if pks are matching expected"""
        post = post_dao.get_by_pk(pk)
        assert post.pk == pk, f"Incorrect pk for requested post with pk = {pk}"

    ### Function of searching in content

    def test_search_in_content_types(self, post_dao):
        """Test if search_in_content returns list and first item in the list is instance of a class"""
        posts = post_dao.search_in_content("ага")
        assert type(posts) == list, "Incorrect type for result"
        posts = post_dao.search_in_content("ага")[0]
        assert type(posts) == Post, "Incorrect type for  of single instance"

    def test_search_in_content_fields(self, post_dao):
        """Test if instance has all required attributes"""
        post = post_dao.search_in_content("на")[0]
        check_fields(post)

    def test_search_in_content_not_found(self, post_dao):
        """Test if instance of non-existent pk is empty list"""
        posts = post_dao.search_in_content("12371283721")
        assert posts == [], "Should be empty list [] for substring non found"

    @pytest.mark.parametrize("s, expected_pks", [
        ("Ага", {1}),
        ("Вышел", {2}),
        ("на", {1, 2, 3}),
    ])
    def test_search_in_content_results(self, post_dao, s, expected_pks):
        """Check if pks are matching expected pk when searching for substring"""
        posts = post_dao.search_in_content(s)
        pks = set([post.pk for post in posts])
        assert pks == expected_pks, f"Incorrect results searching for {s}"

    ### Function of searching by poster name

    def test_get_by_poster_types(self, post_dao):
        """Test if search_in_content returns list and first item in the list is instance of a class"""
        posts = post_dao.get_by_poster("leo")
        assert type(posts) == list, "Incorrect type for result"
        post = post_dao.get_by_poster("leo")[0]
        assert type(post) == Post, "Incorrect type for  of single instance"

    def test_get_by_poster_fields(self, post_dao):
        """Test if instance has all required attributes"""
        post = post_dao.get_by_poster("leo")[0]
        check_fields(post)

    def test_get_by_poster_none(self, post_dao):
        """Test if instance of non-existent pk is empty list"""
        post = post_dao.get_by_poster("asd129783")
        assert post == [], "Should be empty list [] for poster not found"

    @pytest.mark.parametrize("poster_name", ["leo", "johnny", "hank"])
    def test_get_by_correct_poster(self, post_dao, poster_name):
        post = post_dao.get_by_poster(poster_name)[0]
        assert post.poster_name == poster_name, f"Incorrect poster name for requested post with poster name = {poster_name}"
