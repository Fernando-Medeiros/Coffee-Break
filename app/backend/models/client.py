from flask_login import UserMixin


class Client(UserMixin):
    def __init__(self):
        super().__init__()

        self.__refresh_token: str

    @property
    def refresh(self):
        return self.__refresh_token

    @refresh.setter
    def refresh(self, value: str):
        self.__refresh_token = value

    def get_id(self):
        return self.refresh or None

    def load_attr(self, data: dict) -> None:
        for attr, value in data.items():
            self.__setattr__(attr, value)
