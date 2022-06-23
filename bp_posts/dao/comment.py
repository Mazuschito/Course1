class Comment:
    """Comment abstraction to be used in DAO"""

    def __init__(self,
                 post_id=0,
                 commenter_name="",
                 comment="",
                 pk=0
                 ):
        self.post_id = post_id
        self.commenter_name = commenter_name
        self.comment = comment
        self.pk = pk

    def __repr__(self):
        return f"Comment( " \
               f"{self.post_id}, " \
               f"{self.commenter_name}, " \
               f"{self.comment}, " \
               f"{self.pk}" \
               f")"
