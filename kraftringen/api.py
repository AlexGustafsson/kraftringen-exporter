import requests


class API:
    def __init__(self, session: requests.Session) -> None:
        self.__session = session
