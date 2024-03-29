from .models import User_
from .extensions import lm


def checkInt(value: str):
    try:
        return int(value)
    except ValueError:
        return None


def checkString(value: str):
    if value in ("", " "):
        return None
    else:
        return value.title()


def checkBool(value: str):
    if value in ('Y', 'y'):
        return True
    else:
        return False


def checkCash(value: str):
    if value == "cash":
        is_cash = True
        check_num = None
    else:
        is_cash = False
        try:
            check_num = int(value)
        except ValueError:
            check_num = None

    return is_cash, check_num


@lm.user_loader
def load_user(user_id):
    return User_.query.filter_by(session_token=user_id).first()
