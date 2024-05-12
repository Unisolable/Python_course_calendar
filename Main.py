"""
В main можно использовать ТОЛЬКО Interface
"""

import asyncio
from Interface import Interface

Interface.recover_from_csv()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(True)
    loop.run_until_complete(asyncio.wait([loop.create_task(Interface.intface_mode()),
                                          loop.create_task(Interface.notes_from_json())]))
    loop.close()

Interface.save_as_csv()

# Блок технических методов отгрузки в json событий для любой комбинации отдельного пользователя/всех пользователей
# и их календарей. Методы реализованы в рамках ТЗ для разработчиков. Для рядовых юзеров ценности не представляют.
# from Event import Event as EVN
# EVN.save_events_as_json()
# # EVN.save_events_as_json(uid='@5')
# # EVN.save_events_as_json(uid='@5', cln=3)
# EVN.read_events_from_json()

