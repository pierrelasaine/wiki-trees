# Solution: Required to user login manager
class User:

    def __init__(self, name):
        self.name = name

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

    def to_json(self):
        return {"name": self.name}
