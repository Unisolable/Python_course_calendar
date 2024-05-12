"""
Класс календаря - хранит события.
Он умеет искать все события из промежутка (в том числе повторяющиеся).
Он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.
У каждого пользователя несколько типов календарей (рабочий, личный, тренировочный, медицинский)
"""

from Event import Event as EVN
from Backend import Backend as BND
from datetime import datetime
dt_fr_iso = datetime.fromisoformat

class Calendar():
    _cln = int()
    _events = list()
    _shared = list()
    _specs = dict()

    def __init__(self, cln):
        self._cln = cln
        self._events = list()
        self._shared = list()

    def add_event(self, name, descript, start, end, per):
        new = EVN(name, descript, start, end, per)
        self._events.append(new)
        return new

    def del_event(self, eid):
        del self._events[eid]

    @staticmethod
    def find_by_date(uid, start, end):
        events_list = []
        for cln in BND._users[uid]._calendars.values():
            for eid in cln._events:
                if (dt_fr_iso(eid._dates[0]).date() >= dt_fr_iso(start).date()
                        and dt_fr_iso(eid._dates[1]).date() <= dt_fr_iso(end).date()):
                    events_list.append([uid, cln._cln, eid, 'own'])
        for cln in BND._users[uid]._calendars.values():
            for eid in cln._shared:
                if (dt_fr_iso(eid[0]._dates[0]).date() >= dt_fr_iso(start).date()
                        and dt_fr_iso(eid[0]._dates[1]).date() <= dt_fr_iso(end).date()):
                    events_list.append([uid, cln._cln, eid[0], 'shr'])
        return events_list

class Calendar_workn(Calendar):
    pass

class Calendar_persn(Calendar):
    pass

class Calendar_train(Calendar):
    pass

class Calendar_medcn(Calendar):
    pass

def Calendar_specs():
    Calendar._specs[1] = [Calendar_workn, 'Рабочий календарь', 'Рабочего календаря']
    Calendar._specs[2] = [Calendar_persn, 'Личный календарь', 'Личного календаря']
    Calendar._specs[3] = [Calendar_train, 'Тренировочный календарь', 'Тренировочного календаря']
    Calendar._specs[4] = [Calendar_medcn, 'Медицинский календарь', 'Медицинского календаря']

