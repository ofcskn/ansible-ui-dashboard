class LoginDTO:
    def __init__(self, handle: str, password: str):
        self.handle = handle
        self.password = password

    def to_dict(self):
        return {
            "handle": self.handle,
            "password": self.password
        }

