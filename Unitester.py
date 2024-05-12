try: import pathlib
except: import os
import filecmp
import unittest
from Event import Event
from Backend import Backend
from Interface import Interface

fu = 'test_data/users_test.csv'
fur = Interface.recover_from_csv(file=fu)
fut = 'test_data/users_test_temp.csv'
futr = Backend.save_as_csv(file=fut)
fn = 'test_data/notes_test.json'
fnr = Backend.read_notes_from_json(file=fn)
fnt = 'test_data/notes_test_temp.json'
fntr = Backend.save_notes_as_json(file=fnt)
[[cln._events.clear() for cln in Backend._users[uid]._calendars.values()] for uid in Backend._users.keys()]
fe = 'test_data/events_test.json'
fer = Event.read_events_from_json(file=fe)
fet = 'test_data/events_test_temp.json'
fetr = Event.save_events_as_json(file=fet)
[[cln._events.clear() for cln in Backend._users[uid]._calendars.values()] for uid in Backend._users.keys()]
feu = 'test_data/events_u_test.json'
feur = Event.read_events_from_json(file=feu)
feut = 'test_data/events_u_test_temp.json'
feutr = Event.save_events_as_json(uid='@3', file=feut)
[[cln._events.clear() for cln in Backend._users[uid]._calendars.values()] for uid in Backend._users.keys()]
feuc = 'test_data/events_uc_test.json'
feucr = Event.read_events_from_json(file=feuc)
feuct = 'test_data/events_uc_test_temp.json'
feuctr = Event.save_events_as_json(uid='@3', cln=3, file=feuct)

class TestInterface(unittest.TestCase):

    def test_Interface_static(self):
        """Проверка того, что Interface статический"""
        self.assertTrue(Interface() is None, 'Interface НЕ является статическим!')
    def test_recover_from_csv_json(self):
        """Проверка консистентности импорта из CSV файлов"""
        self.assertEqual(fur, 'consistency',
                         'Interface.recover_from_csv НЕ отрабатывает импорт из CSV!')

class TestBackend(unittest.TestCase):

    def test_Backend_static(self):
        """Проверка того, что Backend - статический"""
        self.assertTrue(Backend() is None, 'Backend НЕ является статическим!')
    def test_read_notes_from_json(self):
        """Проверка консистентности импорта уведомлений из JSON файлов"""
        Backend._notes.clear()
        self.assertEqual(fnr, 'consistency',
                         'Backend.read_notes_from_json НЕ отрабатывает импорт из JSON!')
    def test_save_as_csv(self):
        """Проверка сохранения users в CSV"""
        self.assertEqual(futr, 'consistency',
                         'Backend.save_as_csv НЕ отрабатывает экспорт в CSV!')
    def test_save_notes_as_json(self):
        """Проверка сохранения notes в JSON"""
        self.assertEqual(fntr, 'consistency',
                         'Backend.save_notes_as_json НЕ отрабатывает экспорт в JSON!')
    def test_users_comp(self):
        """Проверка содержимого импорта/экспорта users_test/users_test_temp CSV"""
        self.assertTrue(filecmp.cmp(fu, fut, shallow=False),
                        f'Содержимое файла импорта {fu} НЕ соответствует содержимому файла экспорта {fut}')
    def test_notes_comp(self):
        """Проверка содержимого импорта/экспорта notes_test/notes_test_temp notes JSON"""
        self.assertTrue(filecmp.cmp(fn, fnt, shallow=False),
                        f'Содержимое файла импорта {fn} НЕ соответствует содержимому файла экспорта {fnt}')
    @classmethod
    def tearDownClass(cls):
        try: pathlib.Path(fut).unlink()
        except: os.remove(fut) if os.path.isfile(fut) else fut
        try: pathlib.Path(fnt).unlink()
        except: os.remove(fnt) if os.path.isfile(fnt) else fnt

class TestEvent(unittest.TestCase):
    
    def test_read_events_from_json(self):
        """Проверка чтения событий всех календарей всех пользователей Backend из JSON"""
        self.assertEqual(fer, 'consistency',
                         'Event.read_events_from_json НЕ отрабатывает импорт из JSON!')
    def test_save_events_as_json(self):
        """Проверка сохранения всех событий всех календарей всех пользователей Backend в JSON"""
        self.assertEqual(fetr, 'consistency',
                         'Event.save_events_as_json НЕ отрабатывает экспорт в JSON!')
    def test_events_comp(self):
        """Сравнение содержимого импорта/экспорта events_test/events_test_temp
        всех событий всех календарей всех пользователей Backend"""
        self.assertTrue(filecmp.cmp(fe, fet, shallow=False),
                        f'Содержимое файла импорта {fe} НЕ соответствует содержимому файла экспорта {fet}')
    @classmethod
    def tearDownClass(cls):
        try: pathlib.Path(fet).unlink()
        except: os.remove(fet) if os.path.isfile(fet) else fet

class TestEvent_user(unittest.TestCase):
    def test_read_events_u_from_json(self):
        """Проверка чтения событий всех календарей отдельного пользователя Backend из JSON"""
        self.assertEqual(feur, 'consistency',
                         'Event.read_events_from_json НЕ отрабатывает импорт из JSON!')
    def test_save_events_u_as_json(self):
        """Проверка сохранения событий всех календарей отдельного пользователя Backend в JSON"""
        self.assertEqual(feutr, 'consistency',
                         'Event.save_events_as_json НЕ отрабатывает экспорт в JSON!')
    def test_events_u_comp(self):
        """Сравнение содержимого импорта/экспорта events_u_test/events_u_test_temp
        событий всех календарей отдельного пользователя Backend"""
        self.assertTrue(filecmp.cmp(feu, feut, shallow=False),
                        f'Содержимое файла импорта {feu} НЕ соответствует содержимому файла экспорта {feut}')
    @classmethod
    def tearDownClass(cls):
        try: pathlib.Path(feut).unlink()
        except: os.remove(feut) if os.path.isfile(feut) else feut

class TestEvent_user_cal(unittest.TestCase):
    def test_read_events_uc_from_json(self):
        """Проверка чтения событий одного календаря отдельного пользователя Backend из JSON"""
        self.assertEqual(feucr, 'consistency',
                         'Event.read_events_from_json НЕ отрабатывает импорт из JSON!')
    def test_save_events_uc_as_json(self):
        """Проверка сохранения всех событий одного календаря отдельного пользователя Backend в JSON"""
        self.assertEqual(feuctr, 'consistency',
                         'Event.save_events_as_json НЕ отрабатывает экспорт в JSON!')
    def test_events_uc_comp(self):
        """Сравнение содержимого импорта/экспорта events_uc_test/events_uc_test_temp
        всех событий одного календаря отдельного пользователя Backend"""
        self.assertTrue(filecmp.cmp(feuc, feuct, shallow=False),
                        f'Содержимое файла импорта {feuc} НЕ соответствует содержимому файла экспорта {feuct}')
    @classmethod
    def tearDownClass(cls):
        try: pathlib.Path(feuct).unlink()
        except: os.remove(feuct) if os.path.isfile(feuct) else feuct


if __name__ == '__main__':
    unittest.main()

