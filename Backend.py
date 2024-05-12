"""
Сущность, отвечающая за хранение и предоставление данных.
Она хранит пользователей, календари и события.
Хранение, в том числе, означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash).

Должен быть статическим или Синглтоном.

Нужно хранить для каждого пользователя все события которые с ним произошли, но ещё не были обработаны.
"""

import json

class Backend:
    _lgdct = dict()
    _users = dict()
    _notes = dict()
    _eidch = dict()
    _curid = dict()
    def __new__(cls, *args, **kwargs): pass  # Заглушка СТАТИЧЕСКОГО класса Backend #

    @staticmethod
    def save_as_csv(file='users.csv'):
        with open(file, 'w') as f:
            f.write(f'userid,login,pswrd,calendars,events,lstvs\n')
            for uid in Backend._users.keys():
                for cln in Backend._users[uid]._calendars.values():
                    for eid in cln._events:
                        users = (f'{uid},{Backend._users[uid]._login},'
                                 f'{Backend._users[uid]._pswrd},{cln._cln},'
                                 f'"{str(eid.__dict__).replace("'", "\"\"")}",{Backend._users[uid]._lstvs}\n')
                        f.write(users)
        return 'consistency'

    @staticmethod
    def save_notes_as_json(file='notes.json'):
        with open(file, 'w') as f:
            f.write(json.dumps(Backend._notes, ensure_ascii=False))
        return 'consistency'

    @staticmethod
    def read_notes_from_json(file='notes.json'):
        with open(file, 'r') as f:
            Backend._notes = json.JSONDecoder(strict=False).decode(f.read())
        return 'consistency'

