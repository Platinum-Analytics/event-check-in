from .models import User
from .extensions import lm


def checkInt(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def checkString(value: str) -> str | None:
    if value in ("", " "):
        return None
    else:
        return value


def checkBool(value: str) -> bool | None:
    if value in ('Y', 'y'):
        return True
    else:
        return False


def checkCash(value: str) -> tuple | None:
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
    return User.query.get(int(user_id))
