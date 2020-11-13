from sqlalchemy import Column, String
from bot.modules.sql import BASE, SESSION

class Credentials(BASE):
    __tablename__ = "Credentials"
    user = Column(String, primary_key=True, nullable=False)
    secret = Column(String, nullable=False)

    def __init__(self, user, secret):
        self.user = str(user)
        self.secret = secret


Credentials.__table__.create(checkfirst=True)


def save_cred(user_id, secret):
    adder = Credentials(str(user_id), secret)
    SESSION.merge(adder)
    SESSION.commit()
    return True


def get_cred(user_id):
    data = SESSION.query(Credentials).get(str(user_id))
    SESSION.close()
    if data:
        return data.secret
    else:
        return None
    
def del_cred(user_id):
    data = SESSION.query(Credentials).get(str(user_id))
    if data:
        SESSION.delete(data)
        SESSION.commit()
        return True
    else:
        return False