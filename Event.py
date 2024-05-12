"""
Описывает некоторое "событие" - промежуток времени с присвоенными характеристиками.
У события должно быть описание, название и список участников.
Событие может быть единожды созданным,
Или периодическим (каждый день/месяц/год/неделю).

Каждый пользователь ивента имеет свою "роль".
Организатор умеет изменять названия, список участников, описание, а так же может удалить событие.
Участник может покинуть событие.

Запрос на хранение в json.
Уметь создавать из json и записывать в него.

Иметь покрытие тестами.
Комментарии на нетривиальных методах и в целом документация.
"""

import json
from Backend import Backend as BND
from datetime import datetime

class Event:
    _name = str()
    _descript = str()
    _dates = list()
    _period = str()
    _users = list()
    _specs = dict()
    # периоды с усредненным количеством минут
    _specs['0'] = ['отсутствует', 0]
    _specs['1'] = ['ежечасно', 60]
    _specs['2'] = ['ежедневно', 1440]
    _specs['3'] = ['еженедельно', 10080]
    _specs['4'] = ['ежемесячно', 43200]
    _specs['5'] = ['ежеквартально', 129600]
    _specs['6'] = ['каждое полугодие', 263520]
    _specs['7'] = ['ежегодно', 525600]

    def __init__(self, name, descript, start, end, per):
        self._name = name
        self._descript = descript
        self._dates = [start, end]
        self._period = per
        self._users = list()

    def add_user(self, uid, cln, uvn):
        self._users.append(uvn)
        BND._users[BND._lgdct[uvn]]._calendars[cln]._shared.append(self)
        BND._notes[BND._lgdct[uvn]].append(f'Вы являетесь участником события <{self._name}> '
                                           f'Дата добавления: {datetime.now().strftime('%d.%m.%Y  %H:%M')}\n')

    def del_user(self, uid, cln, uvn):
        self._users.remove(uvn)
        BND._users[BND._lgdct[uvn]]._calendars[cln]._shared.remove(self)
        BND._notes[BND._lgdct[uvn]].append(f'Вы удалены их списка участников события <{self._name}> '
                                           f'Дата добавления: {datetime.now().strftime('%d.%m.%Y  %H:%M')}\n')

    @staticmethod
    def save_events_as_json(uid=None, cln=None, file='events.json'):
        """Техническая отгрузка в json событий для любой комбинации отдельного пользователя/всех пользователей
        и их календарей. Выбор нескольких пользователей и нескольких календарей в данном методе НЕ реализован!"""
        with open(file, 'w') as f:
            events_dict = {}
            events_list = []
            # Сохранение всех событий всех календарей всех пользователей
            if uid is None and cln is None:
                for uid in BND._users.keys():
                    for cln in BND._users[uid]._calendars.values():
                        for eid in cln._events:
                            events_list.append(eid.__dict__)
                        events_dict[f'{uid}, {cln._cln}'] = list(*[events_list])
                        events_list.clear()
                f.write(json.dumps(events_dict, ensure_ascii=False))
                events_dict.clear()
            # Сохранение всех событий указанного типа календаря всех пользователей
            elif uid is None:
                for uid in BND._users.keys():
                    for eid in BND._users[uid]._calendars[cln]._events:
                        events_list.append(eid.__dict__)
                    events_dict[f'{uid}, {cln._cln}'] = list(*[events_list])
                    events_list.clear()
                f.write(json.dumps(events_dict, ensure_ascii=False))
                events_dict.clear()
            # Сохранение всех событий всех календарей указанного пользователя
            elif cln is None:
                for cln in BND._users[uid]._calendars.values():
                    for eid in cln._events:
                        events_list.append(eid.__dict__)
                    events_dict[f'{uid}, {cln._cln}'] = list(*[events_list])
                    events_list.clear()
                f.write(json.dumps(events_dict, ensure_ascii=False))
                events_dict.clear()
            # Сохранение всех событий указанного типа календаря указанного пользователя
            else:
                for eid in BND._users[uid]._calendars[cln]._events:
                    events_list.append(eid.__dict__)
                events_dict[f'{uid}, {cln}'] = list(*[events_list])
                events_list.clear()
                f.write(json.dumps(events_dict, ensure_ascii=False))
                events_dict.clear()
        return 'consistency'

    @staticmethod
    def read_events_from_json(file='events.json'):
        """!!!Технический метод импорта событий в Бэкэнд для разработчиков!!!"""
        with open(file, 'r') as f:
            json_events = json.JSONDecoder(strict=False).decode(f.read())
            for k in json_events.keys():
                i = (k.split(', ')[0], int(k.split(', ')[1]))
                for j in json_events[k]:
                    uvn = BND._users[i[0]]._calendars[i[1]].add_event(j['_name'], j['_descript'],
                                                                      j['_dates'][0], j['_dates'][1], j['_period'])
                    uvn._users.extend(j['_users'])
        return 'consistency'

