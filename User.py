"""
Пользователь - имеет логин и пароль, а так же календарь.
У пользователя есть идентификатор начинающийся с @.
"""

import hashlib
from Backend import Backend as BND
from Calendar import Calendar as CLR
from datetime import datetime

class User:
    _userid = str()
    _login = str()
    _pswrd = str()
    _calendars = dict()
    _lstvs = list()

    def __init__(self, lgn, pwd, uid='@', csv=0, lstvs=datetime.now()):
        self._login = str(lgn)
        if csv == 0:
            self._pswrd = hashlib.md5(pwd.encode()).hexdigest()
            self._userid = uid + str((len(BND._users.keys()) if len(BND._users) > 0 else 0) + 1)
        else:
            self._pswrd = pwd
            self._userid = uid
            self._calendars = dict()
            self._lstvs = lstvs
        BND._lgdct[self._login] = self._userid
        BND._users[self._userid] = self
        BND._notes[self._userid] = []

    def add_calendar(self, cln):
        self._calendars[cln] = CLR._specs[cln][0](cln)
        return self._calendars[cln]

    def del_calendar(self, cln):
        del self._calendars[cln]

