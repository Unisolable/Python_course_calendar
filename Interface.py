"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта).
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени.
Создать событие или удалить событие.
После создания события можно добавить туда пользователей.
Если нас добавили в событие или удалили мы получаем уведомление.
"""

import asyncio
import re, json, hashlib, pymsgbox
import Outerface
pymsgbox.prompt = Outerface._promptTkinter
import pandas as pd
from Backend import Backend as BND
from User import User as USR
from Calendar import Calendar as CLR
from Calendar import Calendar_specs
from Event import Event as EVN
from datetime import datetime, timedelta
dt_fr_iso = datetime.fromisoformat
uid, cln, evn, login, unotes, notes_breaker = None, None, None, None, None, None

class Interface:
    def __new__(cls, *args, **kwargs): pass  # Заглушка СТАТИЧЕСКОГО класса Interface #

    @staticmethod
    def save_as_csv():
        """Бэкап всей сессии Бэкэнда"""
        BND.save_as_csv()
        BND.save_notes_as_json()

    @staticmethod
    def recover_from_csv(file='users.csv'):
        """Восстановление сессии users.csv через DataFrame Pandas"""
        Calendar_specs()
        try:
            users = pd.read_csv(file, encoding='windows-1251')
            # инициализируем пользователей
            ulpce = pd.DataFrame(users[['userid', 'login', 'pswrd', 'lstvs']].groupby(['userid', 'login', 'pswrd',
                                                                                       'lstvs'])).values
            [USR(i[0][1], i[0][2], i[0][0], csv=1, lstvs=i[0][3]) for i in ulpce]
            # инициализируем календари пользователей
            ulpce = pd.DataFrame(users[['userid', 'calendars']].groupby(['userid', 'calendars'])).values
            [BND._users[i[0][0]].add_calendar(i[0][1]) for i in ulpce]
            # инициализируем события календарей пользователей
            ulpce = pd.DataFrame(users[['userid', 'calendars', 'events']].
                                 groupby(['userid', 'calendars', 'events'])).values
            for i in ulpce:
                j = json.JSONDecoder(strict=False).decode(i[0][2])
                uvn = BND._users[i[0][0]]._calendars[i[0][1]].add_event(j['_name'], j['_descript'],
                                                                        j['_dates'][0], j['_dates'][1], j['_period'])
                uvn._users.extend(j['_users'])
                if uvn._users[0] != '':
                    for lgn in uvn._users:
                        BND._users[BND._lgdct[lgn]]._calendars[i[0][1]]._shared.append([uvn, i[0][0]])
            testcsv = 'consistency'
        except: pass
        try:
            BND.read_notes_from_json()
        except: pass
        return testcsv if testcsv else ''

    @staticmethod
    async def notes_from_json():
        """Основная функция уведомлений пользователя"""
        global uid, login, unotes, notes_breaker
        while True:
            allevn = []
            if notes_breaker != 1:
                try:
                    # собираем все события в один список для проверки периодичности уведомлений
                    for cln in BND._users[uid]._calendars.values():
                        allevn.extend(cln._events)
                        [allevn.append(cln._shared[i][0]) for i in range(len(cln._shared))]
                    for eid in allevn:
                        # Базовая логика проверки наступления фиксированных дат очередных уведомлений
                        # в процессе работы программы в ходе асинхронных ожиданий
                        if eid in BND._eidch.keys():
                            if BND._eidch[eid] < datetime.now() and dt_fr_iso(eid._dates[1]) < datetime.now():
                                BND._notes[uid].append(f'Напоминание: <{eid._name}> '
                                                       f'Дата добавления: '
                                                       f'{datetime.now().strftime('%d.%m.%Y  %H:%M')}\n')
                                next_check = (BND._eidch[eid] +
                                              timedelta(minutes=EVN._specs[eid._period[0]][1] / quantifier))
                                del BND._eidch[eid]
                                BND._eidch[eid] = next_check
                        # Стартовая логика получения уведомлений на момент запуска программы
                        quantifier = int(eid._period[1:]) if eid._period[1:] != '' else 1
                        if ((notes_breaker is None and ((dt_fr_iso(eid._dates[0]) +
                            timedelta(minutes = EVN._specs[eid._period[0]][1] / quantifier)) < datetime.now())) and
                            (dt_fr_iso(eid._dates[1]) < datetime.now() or ((dt_fr_iso(BND._users[uid]._lstvs) +
                            timedelta(minutes = EVN._specs[eid._period[0]][1] / quantifier)) < datetime.now()))):
                            BND._notes[uid].append(f'Напоминание: <{eid._name}> Дата окончания: '
                                                   f'{dt_fr_iso(eid._dates[1]).strftime('%d.%m.%Y  %H:%M')}\n')
                        # Фиксация даты очередного уведомления
                        if EVN._specs[eid._period[0]][1] != 0:
                            next_check = (dt_fr_iso(eid._dates[0]) +
                                  timedelta(minutes = int((datetime.now() - dt_fr_iso(eid._dates[0])) /
                                                          timedelta(minutes = (EVN._specs[eid._period[0]][1] /
                                                                               quantifier))) *
                                                      (EVN._specs[eid._period[0]][1] / quantifier) +
                                                      (EVN._specs[eid._period[0]][1] / quantifier)))
                            BND._eidch[eid] = next_check
                    # Вывод пользователю всех текущих уведомлений
                    if len(BND._notes[uid]) > 1:
                        pymsgbox.rootWindowPosition = '+450+90'
                        if notes_breaker is None:
                            unotes = pymsgbox.confirm(f'{''.join([BND._notes[uid][i]
                                                                  for i in range(1, len(BND._notes[uid]))])}',
                                                      f'Список завершённых событий и просроченных уведомлений {login}:',
                                                      ['Окей на!', 'Потом на!'])
                            notes_breaker = 0
                        else:
                            unotes = pymsgbox.confirm(f'{''.join([BND._notes[uid][i]
                                                                  for i in range(1, len(BND._notes[uid]))])}',
                                                      f'Список непрочитанных уведомлений пользователя {login}:',
                                                      ['Окей на!', 'Потом на!'])
                    elif len(BND._notes[uid]) == 1:
                        if notes_breaker is None:
                            unotes = pymsgbox.confirm(f'{''.join([BND._notes[uid][0]])}',
                                                      f'Список непрочитанных уведомлений пользователя {login}:',
                                                      ['Окей на!', 'Потом на!'])
                            notes_breaker = 0

                    if unotes == 'Потом на!' or unotes is None: pass
                    else:
                        del BND._notes[uid]
                        BND._notes[uid] = ['Нет непрочитанных уведомлений\n']

                    await asyncio.sleep(0.1)
                except:
                    await asyncio.sleep(0.1)
            else: break

    @staticmethod
    def add_user(lgn, pwd):
        """Добавление пользователя"""
        global uid
        USR(lgn, pwd)
        BND._notes[uid] = ['Нет непрочитанных уведомлений\n']

    @staticmethod
    def del_user(uid):
        """Удаление пользователя"""
        global login
        del BND._lgdct[login]
        del BND._users[uid]
        del BND._notes[uid]

    @staticmethod
    def add_calendar(uid, cln):
        """Добавление календаря пользователю"""
        global login
        pymsgbox.rootWindowPosition = '420x110+450+150'
        if cln not in BND._users[uid]._calendars.keys():
            BND._users[uid].add_calendar(cln)
            add_conf = pymsgbox.confirm(f'{CLR._specs[cln][1]} добавлен пользователю {login}\n',
                                        f'Свидетельство о рождении календаря 💘💘💘', ['Ура-Ура!'])
        else:
            cln_error = pymsgbox.confirm(f'Выбранный тип календаря уже используется >>>\n{cln} - {CLR._specs[cln][1]}',
                                         f'Ошибка выбора календаря ☢☢☢', ['Сорян!'])

    @staticmethod
    def del_calendar(uid, cln):
        """Удаление календаря у пользователя"""
        global login
        pymsgbox.rootWindowPosition = '410x110+450+150'
        if cln in BND._users[uid]._calendars.keys():
            BND._users[uid].del_calendar(cln)
            def_conf = pymsgbox.confirm(f'{CLR._specs[cln][1]} {login} удалён ✞✞✞\n',
                                        f'Свидетельство о смерти календаря ☠☠☠', ['Помянем на!'])

    @staticmethod
    def add_event(uid, cln, name, descript, start, end, per='0'):
        """Добавление события в календарь пользователя"""
        BND._users[uid]._calendars[cln].add_event(name, descript, start, end, per)

    @staticmethod
    def del_event(uid, cln, eid):
        """Удаление события в календаре пользователя"""
        delevn = BND._users[uid]._calendars[cln]._events[eid]._name
        BND._users[uid]._calendars[cln].del_event(eid)
        pymsgbox.rootWindowPosition = '430x120+450+150'
        def_conf = pymsgbox.confirm(f'Событие <{delevn}> удалёно из '
                                    f'Вашего {CLR._specs[cln][2]}\n',
                                    f'Свидетельство о смерти события ☠☠☠', ['Помянем на!'])

    @staticmethod
    def find_event(uid, start, end):
        """Поиск событий во всех календарях пользователей по интервалу дат"""
        return CLR.find_by_date(uid, start, end)

    @staticmethod
    def add_event_users(uid, cln, eid, uvn):
        """Добавление нового пользователя к событию календаря"""
        BND._users[uid]._calendars[cln]._events[eid].add_user(uid, cln, uvn)
        pymsgbox.rootWindowPosition = '440x115+450+150'
        add_conf = pymsgbox.confirm(f'Пользователь {uvn} добавлен к событию '
                                    f'<{BND._users[uid]._calendars[cln]._events[eid]._name}> '
                                    f'Вашего {CLR._specs[cln][2]}\n',
                                    f'Свидетельство о добавлении нового пользователя 💘💘💘', ['Ура-Ура!'])

    @staticmethod
    def del_event_users(uid, cln, eid, uvn):
        """Удаление пользователя из события календаря"""
        BND._users[uid]._calendars[cln]._events[eid].del_user(uid, cln, uvn)
        pymsgbox.rootWindowPosition = '430x120+450+150'
        add_conf = pymsgbox.confirm(f'Пользователь {uvn} удалён из события '
                                    f'<{BND._users[uid]._calendars[cln]._events[eid]._name}> '
                                    f'Вашего {CLR._specs[cln][2]}\n',
                                    f'Свидетельство об удалении пользователя ☠☠☠', ['Помянем на!'])

    @staticmethod
    def del_self_from_event_users(uid, cln, eid):
        """Удаление себя из пользователей события календаря"""
        global login
        devn = BND._users[uid]._calendars[cln]._shared[eid][0]._name
        devl = BND._users[uid]._calendars[cln]._shared[eid][1]
        BND._users[uid]._calendars[cln]._shared[eid][0]._users.remove(login)
        del BND._users[uid]._calendars[cln]._shared[eid]
        pymsgbox.rootWindowPosition = '460x120+450+150'
        def_conf = pymsgbox.confirm(f'Вы покинули событие <{devn}> {CLR._specs[cln][2]} пользователя '
                                    f'{BND._users[devl]._login}?\n',
                                    f'Свидетельство об удалении себя из события ☠☠☠', ['Помянем на!'])

    @staticmethod
    async def intface_mode():
        """Основная функция вызова пользовательского интерфейса"""
        global uid, login, cln, evn, unotes, notes_breaker
        login, newuser = None, False

        while True:
            # Идентифицируем пользователя
            try:
                if not newuser or newuser == 'Дану на!':
                    login, pswrd = pymsgbox.prompt('При отсутствии логина пользователю автоматически'
                                                   ' будет предложена регистрация\n\n'
                                                   'Введите логин пользователя >>>', 'Вход в систему :))', dtntr=1)
                else: pass
            except: pass

            if login is None:
                notes_breaker = 1
                break
            elif login == '': login = None
            elif login in BND._lgdct.keys():

                # Верифицируем пароль
                if hashlib.md5(pswrd.encode()).hexdigest() == BND._users[BND._lgdct[login]]._pswrd:
                    uid = BND._lgdct[login]
                    BND._curid['login'] = login
                    BND._curid['uid'] = uid

                    while True:
                        # Проверяем набор уведомлений пользователя
                        await asyncio.sleep(0.1)
                        notes_breaker = 0
                        BND._users[uid]._lstvs = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                        # Выводим меню базовых действий
                        interface = pymsgbox.prompt('⮚ Введите 1 для выбора календаря >>>\n'
                                                    '⮚ Введите 2 для добавления нового календаря >>>\n'
                                                    '⮚ Введите 3 для поиска событий по датам >>>\n'
                                                    '⮚ Введите 4 для удаления календаря >>>\n'
                                                    '⮚ Введите 5 для удаления пользователя >>>\n\n'
                                                    '<Свалить!> для завершения работы >>>\n',
                                                    'Выберите действие :))', clntr=2)

                        # Введите 1 для выбора календаря >>>
                        if interface is None:
                            login, uid, newuser, notes_breaker = None, None, False, None
                            break
                        elif interface == '': continue
                        elif interface == '1':
                            await asyncio.sleep(0.1)
                            while True:
                                cln = pymsgbox.prompt(f'{''.join([str(i[0]) + ' - ' + CLR._specs[i[0]][1] + '\n' 
                                                                  for i in BND._users[uid]._calendars.items()])}\n'
                                                      '<Свалить!> для возвращения в предыдущий раздел\n'
                                                      '⮚ Выберите календарь для просмотра его событий',
                                                      'Просмотр событий календарей :))')
                                try:
                                    if cln is None: break
                                    elif cln == '': continue
                                    elif int(cln) in range(1, 6) and int(cln) in BND._users[uid]._calendars.keys():
                                        cln = int(cln)
                                        BND._curid['login'] = login
                                        BND._curid['uid'] = uid
                                        BND._curid['cln'] = cln
                                        await Interface.event_checker()
                                except: pass

                        # Введите 2 для добавления нового календаря >>>
                        elif interface == '2':
                            await asyncio.sleep(0.1)
                            while True:
                                cln = pymsgbox.prompt(f'{''.join([str(i[0]) + ' - ' + i[1][1] + '\n' 
                                                                  for i in CLR._specs.items()])}\n'
                                                      '<Свалить!> для возвращения в предыдущий раздел\n'
                                                      '⮚ Выберите индекс календаря для добавления',
                                                      'Добавление нового календаря :))')
                                try:
                                    if cln is None: break
                                    elif cln == '': continue
                                    elif int(cln) in range(1, 5): Interface.add_calendar(uid, int(cln))
                                except: pass

                        # Введите 3 для поиска событий по датам >>>
                        elif interface == '3':
                            await asyncio.sleep(0.1)
                            while True:
                                prd = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                                      '⮚ Введите диапазон для дат начала событий '
                                                      'в формате \nГГГГ-ММ-ДД ГГГГ-ММ-ДД',
                                                      'Поиск событий по датам :))', dtntr=2)
                                if prd is None: break
                                elif prd == '': continue
                                else:
                                    efn = Interface.find_event(uid, prd[0], prd[1])
                                    # Отображаем найденные по датам события
                                    epn = pymsgbox.prompt(
        f'{''.join([''.join([str(str(efn.index(j) + 1) + '. '), str(j[2]._name + ': '), j[2]._descript, ' ===\n',
                             str('начало: ' + dt_fr_iso(j[2]._dates[0]).strftime('%d.%m.%Y  %H:%M')), ' >>> ',
                             str('конец: ' + dt_fr_iso(j[2]._dates[1]).strftime('%d.%m.%Y  %H:%M')), '\n',
                             'напоминание - ', EVN._specs[j[2]._period[0]][0], '\n']) for j in efn if j[3] == 'own'])}\n'
        f'\nСобытия из чужих календарей, участником которых Вы являетесь:\n'
        f'{''.join([''.join([str(str(efn.index(j) + 1) + '. '), str(j[2]._name + ': '), j[2]._descript, ' ===\n',
                             str('начало: ' + dt_fr_iso(j[2]._dates[0]).strftime('%d.%m.%Y  %H:%M')), ' >>> ',
                             str('конец: ' + dt_fr_iso(j[2]._dates[1]).strftime('%d.%m.%Y  %H:%M')), '\n',
                             'напоминание - ', EVN._specs[j[2]._period[0]][0], '\n']) for j in efn if j[3] == 'shr'])}\n'
        '<Свалить!> для возвращения в предыдущий раздел\n'
        '⮚ Выберите НОМЕР события из списка, автором которого Вы являетесь, для его редактирования',
        'Список всех найденных событий для заданного промежутка времени :))')
                                    if epn is None or epn == '': continue
                                    else:
                                        try:
                                            epn = int(epn) - 1
                                            if efn[epn][3] == 'own':
                                                cln = efn[epn][1]
                                                evn = efn[epn][2]
                                                Interface.edit_event(0)
                                        except: pass

                        # Введите 4 для удаления календаря >>>
                        elif interface == '4':
                            await asyncio.sleep(0.1)
                            while True:
                                cln = pymsgbox.prompt(f'{''.join([str(i[0]) + ' - ' + CLR._specs[i[0]][1] + '\n' 
                                                                  for i in BND._users[uid]._calendars.items()])}\n'
                                                      '<Свалить!> для возвращения в предыдущий раздел\n'
                                                      '⮚ Выберите индекс календаря для удаления',
                                                      'Удаление календаря пользователя :))')
                                try:
                                    if cln is None: break
                                    elif cln == '': continue
                                    elif int(cln) in range(1, 5): Interface.del_calendar(uid, int(cln))
                                except: pass

                        # Введите 5 для удаления пользователя >>>
                        elif interface == '5':
                            await asyncio.sleep(0.1)
                            while True:
                                ucl = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                                      'Подтвердите удаление пользователя ' +
                                                      BND._users[uid]._login + '\n\n'
                                                      '⮚ Введите DEL для подтверждения удаления\n'
                                                      '!!! Операция удаления пользователя необратима !!!',
                                                      'Удаление аккаунта пользователя :((')
                                if ucl is None: break
                                elif ucl == '': continue
                                elif ucl == 'DEL':
                                    Interface.del_user(uid)
                                    login, newuser = None, False
                                    break

            # Предлагаем зарегистрировать нового пользователя в случае отсутствия логина в системе
            else:
                pymsgbox.rootWindowPosition = '480x130+450+150'
                newuser = pymsgbox.confirm(f'Желаете зарегистрировать пользователя {login} в системе?\n'
                                           f'Ответ <Дану на!> - новая попытка ввода\n'
                                           f'<Я хз!> - завершения работы',
                                           f'Пользователь с логином {login} отсутствует в системе!',
                                           ['Не вопрос!', 'Дану на!', 'Я хз!'])
                if newuser == 'Дану на!': continue
                elif newuser == 'Не вопрос!': Interface.add_user(login, pswrd)
                else:
                    notes_breaker = 1
                    break
            await asyncio.sleep(0.1)

    @staticmethod
    async def event_checker():
        """Вывод текущего набора событий выбранного календаря пользователя"""
        global uid, login, cln, evn
        while True:
            shared = ''
            i = len(BND._users[uid]._calendars[cln]._events)
            for j in BND._users[uid]._calendars[cln]._shared:
                shared += str(str(i := i + 1) + '. ' + j[0]._name + ': ' + j[0]._descript + ' ===\n' +
                              'начало: ' + dt_fr_iso(j[0]._dates[0]).strftime('%d.%m.%Y  %H:%M') + ' >>> ' +
                              'конец: ' + dt_fr_iso(j[0]._dates[1]).strftime('%d.%m.%Y  %H:%M') + '\n' +
                              'напоминание - ' + EVN._specs[j[0]._period[0]][0] + '\n')
            if shared == '': shared = '<< oбщие события данного календаря с другими участниками отсутствуют >>\n'
            evn = pymsgbox.prompt(
            f'{''.join([''.join([str(str(BND._users[uid]._calendars[cln]._events.index(j) + 1) + '. '),
                                 str(j._name + ': '), j._descript, ' ===\n',
                                 str('начало: ' + dt_fr_iso(j._dates[0]).strftime('%d.%m.%Y  %H:%M')), ' >>> ',
                                 str('конец: ' + dt_fr_iso(j._dates[1]).strftime('%d.%m.%Y  %H:%M')), '\n',
                                 'напоминание - ', EVN._specs[j._period[0]][0], '\n'])
                        for j in BND._users[uid]._calendars[cln]._events])}\n'
            f'События из чужих календарей, участником которых Вы являетесь: \n\n{shared}\n'
            '<Свалить!> для возвращения в предыдущий раздел\n'
            '⮚ Выберите НОМЕР события, автором которого Вы являетесь, из верхнего списка для его редактирования.\n'
            '⮚ Или введите НАЗВАНИЕ нового события для его добавления в календарь.',
            f'Список событий {CLR._specs[cln][2]} пользователя :))', clntr=1)
            if evn is None: break
            elif evn == '': continue
            else:
                try:
                    users = ''
                    evn = int(evn) - 1
                    for i in BND._users[uid]._calendars[cln]._events[evn]._users:
                        users += i + ', ' if i != '' else users
                    users = users[:-2] if users[:-2] != '' else 'только Вы 💘💘💘'
                    if evn in range(len(BND._users[uid]._calendars[cln]._events)):
                        editevent = pymsgbox.prompt('⮚ Введите 1 для редактирования события >>>\n'
                                                    '⮚ Введите 2 для добавления к событию нового пользователя >>>\n'
                                                    '⮚ Введите 3 для удаления из события пользователя >>>\n'
                                                    '⮚ Введите 4 для удаления события >>>\n\n'
                                                    'Список участников события:\n'
                                                    f'<<{BND._users[uid]._calendars[cln]._events[evn]._name}>>:\n'
                                                    f'{users}\n\n<Свалить!> для завершения работы >>>\n',
                                                    f'Выберите действие для события :))',
                                                    default='участники: ' + users)
                        if editevent == '1':
                            evn = BND._users[uid]._calendars[cln]._events[evn]
                            Interface.edit_event(0)

                        elif editevent == '2':
                            uvn = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                                  f'⮚ Введите имя пользователя для добавления его к событию\n'
                                                  f'<{BND._users[uid]._calendars[cln]._events[evn]._name}> '
                                                  f'Вашего {CLR._specs[cln][2]}',
                                                  'Добавление к событию нового пользователя :))')
                            if uvn in BND._lgdct.keys() and uvn != login: Interface.add_event_users(uid, cln, evn, uvn)

                        elif editevent == '3':
                            uvn = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                                  f'⮚ Введите имя пользователя для удаления его из события\n'
                                                  f'<{BND._users[uid]._calendars[cln]._events[evn]._name}> '
                                                  f'Вашего {CLR._specs[cln][2]}',
                                                  'Удаление из события пользователя :))')
                            if uvn in BND._lgdct.keys() and uvn != login: Interface.del_event_users(uid, cln, evn, uvn)

                        elif editevent == '4':
                            pymsgbox.rootWindowPosition = '420x120+450+150'
                            del_conf = pymsgbox.confirm(f'Событие <{BND._users[uid]._calendars[cln]._events[evn]._name}> '
                                                        f'будет удалено из {CLR._specs[cln][2]} '
                                                        f'пользователя {login}\n',
                                                        f'Подтверждение удаления события ☠☠☠',
                                                        ['Окей на!', 'Да ну на!'])
                            if del_conf == 'Окей на!': Interface.del_event(uid, cln, evn)
                            else: pass
                except:
                    try:
                        evn = evn - len(BND._users[uid]._calendars[cln]._events)
                        pymsgbox.rootWindowPosition = '450x120+450+150'
                        del_conf = pymsgbox.confirm(f'Желаете покинуть событие '
                                            f'<{BND._users[uid]._calendars[cln]._shared[evn][0]._name}> '
                                            f'{CLR._specs[cln][2]} пользователя '
                                            f'{BND._users[BND._users[uid]._calendars[cln]._shared[evn][1]]._login}?\n',
                                            f'Подтверждение удаления себя из события ☠☠☠',
                                            ['Окей на!', 'Да ну на!'])
                        if del_conf == 'Окей на!': Interface.del_self_from_event_users(uid, cln, evn)
                    except: Interface.edit_event(1)
        await asyncio.sleep(0.1)

    @staticmethod
    def edit_event(new):
        """Редактирование / Ввод нового события в выбранный календарь пользователя"""
        global uid, login, cln, evn
        date_error, time_error = 0, 0
        while True:
            if new == 1:
                descript = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                           f'⮚ Введите описание события <{evn}>',
                                           'Ввод описания нового события :))')
                if descript is None: break
                startup = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                          f'⮚ Введите дату начала события <{evn}> в формате\n'
                                          f'ГГГГ-ММ-ДД ЧЧ:ММ', 'Ввод даты начала нового события :))',
                                          default=datetime.now().strftime('%Y-%m-%d %H:%M'))
            elif new == 0:
                name = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                       f'⮚ Введите описание события <{evn._name}>',
                                       'Редактирование названия события :))', default=evn._name)
                if name is None: break
                descript = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                           f'⮚ Введите описание события <{evn._name}>',
                                           'Редактирование описания события :))', default=evn._descript)
                if descript is None: break
                startup = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                          f'⮚ Введите дату начала события <{evn._name}> в формате\n'
                                          f'ГГГГ-ММ-ДД ЧЧ:ММ', 'Редактирование даты начала события :))',
                                          default=evn._dates[0].split('T')[0] + ' ' + evn._dates[0].split('T')[1][:-3])
            if not startup is None:
                startup = startup.split(' ')
                if not re.search('^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])'
                                 '(\\|.|-|_|/)([1-9]|0[1-9]|1[0-2])'
                                 '(\\|.|-|_|/)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$', startup[0]) is None:
                    startup[0] = startup[0].replace('.', '-').replace('\\', '-').replace('/', '-').replace('_', '-')
                else:
                    pymsgbox.rootWindowPosition = '420x110+450+150'
                    date_error = pymsgbox.confirm(f'Некорректный формат даты начала события ГГГГ-ММ-ДД >>> '
                                                  f'{startup[0]}\n', 'Ошибка ввода даты начала события ☢☢☢',
                                                  ['Сорян!'])
                if re.search('^((([0-1][0-9])|2[0-3]):[0-5][0-9])$', startup[1]) is None:
                    pymsgbox.rootWindowPosition = '420x110+450+150'
                    time_error = pymsgbox.confirm(f'Некорректный формат времени начала события ЧЧ:ММ >>> '
                                                  f'{startup[1]}\n', 'Ошибка ввода времени начала события ☢☢☢',
                                                  ['Сорян!'])
                if date_error != 'Сорян!' and time_error != 'Сорян!':
                    start = startup[0] + 'T' + startup[1] + ':00'
            else:
                break

            while True:
                if new == 1:
                    end = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                          f'⮚ Введите дату окончания события <{evn}> в формате\n'
                                          f'ГГГГ-ММ-ДД ЧЧ:ММ', 'Редактирование даты окончания нового события :))',
                                          default=startup[0] + ' ' + startup[1])
                elif new == 0:
                    end = pymsgbox.prompt('<Свалить!> для возвращения в предыдущий раздел\n'
                                          f'⮚ Введите дату окончания события <{evn._name}> в формате\n'
                                          f'ГГГГ-ММ-ДД ЧЧ:ММ', 'Редактирование даты окончания события :))',
                                          default=evn._dates[1].split('T')[0] + ' ' + evn._dates[1].split('T')[1][:-3])
                if not end is None:
                    end = end.split(' ')
                    if not re.search('^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])'
                                     '(\\|.|-|_|/)([1-9]|0[1-9]|1[0-2])'
                                     '(\\|.|-|_|/)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$', end[0]) is None:
                        end[0] = end[0].replace('.', '-').replace('\\', '-').replace('/', '-').replace('_', '-')
                    else:
                        pymsgbox.rootWindowPosition = '420x110+450+150'
                        date_error = pymsgbox.confirm(f'Некорректный формат даты окончания события ГГГГ-ММ-ДД >>> '
                                                      f'{end[0]}\n', 'Ошибка ввода даты начала события ☢☢☢',
                                                      ['Сорян!'])
                    if re.search('^((([0-1][0-9])|2[0-3]):[0-5][0-9])$', end[1]) is None:
                        pymsgbox.rootWindowPosition = '420x110+450+150'
                        time_error = pymsgbox.confirm(f'Некорректный формат времени окончания события ЧЧ:ММ >>> '
                                                      f'{end[1]}\n', 'Ошибка ввода времени начала события ☢☢☢',
                                                      ['Сорян!'])
                    if date_error != 'Сорян!' and time_error != 'Сорян!':
                        end = end[0] + 'T' + end[1] + ':00'
                else:
                    break

                while True:
                    if new == 1:
                        per = pymsgbox.prompt(f'{''.join([''.join([i[0], ' - ', i[1][0], '\n'])
                                                          for i in EVN._specs.items()])}\n'
                                      '<Свалить!> для возвращения в предыдущий раздел\n\n'
                                      f'⮚ Введите значение фактора периодичности напоминаний для события <{evn}> '
                                      'и количество напоминаний для данного периода в формате числа без пробелов, '
                                      '(где ПЕРВАЯ цифра указывает на периодичность события, '
                                      'а СЛЕДУЮЩИЕ за ней цифры указывают количество напоминаний в данном периоде, '
                                      'не чаще одного раза в минуту)\n'
                                      '⮚ Введите 0 для игнорирования фактора периодичности',
                                      'Ввод фактора периодичности нового события :))')
                    elif new == 0:
                        per = pymsgbox.prompt(f'{''.join([''.join([i[0], ' - ', i[1][0], '\n'])
                                                          for i in EVN._specs.items()])}\n'
                                      '<Свалить!> для возвращения в предыдущий раздел\n\n'
                                      f'⮚ Введите значение фактора периодичности напоминаний для события <{evn._name}> '
                                      'и количество напоминаний для данного периода в формате числа без пробелов, '
                                      '(где ПЕРВАЯ цифра указывает на периодичность события, '
                                      'а СЛЕДУЮЩИЕ за ней цифры указывают количество напоминаний в данном периоде, '
                                      'не чаще одного раза в минуту)\n'
                                      '⮚ Введите 0 для игнорирования фактора периодичности :))',
                                      'Редактирование фактора периодичности события :))', default=evn._period)

                    try:
                        pymsgbox.rootWindowPosition = '420x115+450+150'
                        if per is None: break
                        elif int(per[1:]) not in range(EVN._specs[per[0]][1] + 1):
                            per_error = pymsgbox.confirm(f'Число напоминаний превышает 1 раз в минуту >>> {per[1:]}\n',
                                                         f'Ошибка ввода фактора периодичности напоминаний ☢☢☢',
                                                         ['Сорян!'])
                        else:
                            if new == 1:
                                Interface.add_event(uid, cln, evn, descript, start, end, per)
                                add_conf = pymsgbox.confirm(f'Событие <{evn}> внесено в {CLR._specs[cln][1]} '
                                                            f'пользователя {login}\n',
                                                            f'Свидетельство о рождении события 💘💘💘',
                                                            ['Ура-Ура!'])
                                break
                            elif new == 0:
                                evn._name = name
                                evn._descript = descript
                                evn._start = start
                                evn._end = end
                                evn._period = per
                                ref_conf = pymsgbox.confirm(f'Событие <{evn._name}> {CLR._specs[cln][2]} '
                                                            f'пользователя {login} обновлено\n',
                                                            f'Непоправимые улучшения {CLR._specs[cln][2]}',
                                                            ['Окей на!'])
                                break
                    except:
                        per_error = pymsgbox.confirm(f'Некорректный формат периодичности напоминаний >>> {per}\n',
                                                     f'Ошибка ввода фактора периодичности напоминаний ☢☢☢',
                                                     ['Сорян!'])
                break
            break

