import threading

from sqlalchemy import Column, String
from bot.modules.sql import BASE, SESSION

class Credentials(BASE):
    __tablename__ = "Credentials"
    user = Column(String, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    secret = Column(String, nullable=False)

    def __init__(self, user, username, secret):
        self.user = str(user)
        self.username = username
        self.secret = secret


Credentials.__table__.create(checkfirst=True)


def save_cred(user_id, username, password):
    adder = Credentials(str(user_id), username, password)
    SESSION.merge(adder)
    SESSION.commit()
    return True


def get_cred(user_id):
    data = SESSION.query(Credentials).get(str(user_id))
    SESSION.close()
    if data:
        return (
            data.username,
            data.secret,
        )
    else:
        return None, None
