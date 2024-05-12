from datetime import date, datetime, timedelta
dt_fr_iso = datetime.fromisoformat
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as st
from Calendar import Calendar as CLR
from tkcalendar import Calendar, DateEntry
from Backend import Backend as BND
clntr_factor = None


"""
Event_handler в Tkinter календаре на базе рефакторинга tkcalendar
"""

def Eventhandler(event):

    login = BND._curid['login']
    uid = BND._curid['uid']
    if clntr_factor == 2: cln = 0
    else: cln = BND._curid['cln']
    evl = None
    cal = dict()
    CUI = tk.Tk()
    if clntr_factor == 2:
        CUI.title("События всех календарей пользователя")
        emplug = "Список событий всех календарей пользователя"
    else:
        CUI.title(f"{CLR._specs[cln][1]} пользователя")
        emplug = f"События <{CLR._specs[cln][2]}> пользователя"
    CUI.configure(bg="darkblue")
    CUI['padx'] = 2
    CUI['pady'] = 2
    CUI.geometry("+%d+%d" % (70, 15))
    CUI.update()

    def event_label(event):
        evn = ""
        nonlocal evl
        for i in range(1, 13):
            if not cal[i] is event.widget:
                cal[i]._remove_selection()
                if not cal[i]._sel_date is None:
                    cal[i]._sel_date = None
        evd = event.widget.get_date()
        if date.fromisoformat(evd) in event.widget._calevent_dates.keys():
            for j in event.widget._calevent_dates[date.fromisoformat(evd)]:
                if len(event.widget.calevents[j]["tags"]) > 1:
                    calname = event.widget.calevents[j]["tags"][0]
                    descript = event.widget.calevents[j]["tags"][1]
                else: descript = ""
                evn += (f"{calname} >>> {event.widget.calevents[j]["text"]} >>> {descript}\n")
            if len(event.widget._calevent_dates[date.fromisoformat(evd)]) > 4:
                evl.destroy()
                evl = st.ScrolledText(CUI, height=5, wrap="word", font="Arial 12", padx=15,
                                      background="darkblue", foreground="white")
                evl.grid(row=3, column=0, columnspan=3, sticky="nsew")
                evl.insert("insert", evn)
            else:
                if isinstance(evl, st.ScrolledText):
                    evl.frame.destroy()
                    evl.vbar.destroy()
                    evl.destroy()
                    evl_recover()
                    evl.config(text=f"{evn[:-1]}", fg="white")
                else:
                    evl.config(text=f"{evn[:-1]}", fg="white")
        else:
            if isinstance(evl, st.ScrolledText):
                evl.frame.destroy()
                evl.vbar.destroy()
                evl.destroy()
                evl_recover()
                evl.config(text="Выбранная дата: " + evd, fg="white")
            else:
                evl.config(text="Выбранная дата: " + evd, fg="white")

    for i in range(1, 13):
        cal[i] = Calendar(CUI, background="darkblue", foreground="white", selectmode="day", date_pattern="yyyy-mm-dd",
                          month=i, font="Arial 12", locale="ru_RU", showweeknumbers=False, showothermonthdays=False)
        if i == 1:
            cal[i]._header_month.configure(text="Январь")
            cal[i]._month_names[cal[i]._date.month] = "Январь"
        if i == 2:
            cal[i]._header_month.configure(text="Февраль")
            cal[i]._month_names[cal[i]._date.month] = "Февраль"
        if i == 3:
            cal[i]._header_month.configure(text="Март")
            cal[i]._month_names[cal[i]._date.month] = "Март"
        if i == 4:
            cal[i]._header_month.configure(text="Апрель")
            cal[i]._month_names[cal[i]._date.month] = "Апрель"
        if i == 5:
            cal[i]._header_month.configure(text="Май")
            cal[i]._month_names[cal[i]._date.month] = "Май"
        if i == 6:
            cal[i]._header_month.configure(text="Июнь")
            cal[i]._month_names[cal[i]._date.month] = "Июнь"
        if i == 7:
            cal[i]._header_month.configure(text="Июль")
            cal[i]._month_names[cal[i]._date.month] = "Июль"
        if i == 8:
            cal[i]._header_month.configure(text="Август")
            cal[i]._month_names[cal[i]._date.month] = "Август"
        if i == 9:
            cal[i]._header_month.configure(text="Сентябрь")
            cal[i]._month_names[cal[i]._date.month] = "Сентябрь"
        if i == 10:
            cal[i]._header_month.configure(text="Октябрь")
            cal[i]._month_names[cal[i]._date.month] = "Октябрь"
        if i == 11:
            cal[i]._header_month.configure(text="Ноябрь")
            cal[i]._month_names[cal[i]._date.month] = "Ноябрь"
        if i == 12:
            cal[i]._header_month.configure(text="Декабрь")
            cal[i]._month_names[cal[i]._date.month] = "Декабрь"

        cal[i]._l_month.destroy()
        cal[i]._r_month.destroy()
        cal[i]._header_month.pack(side="left", padx=100)
        cal[i]._l_year.destroy()
        cal[i]._r_year.destroy()
        cal[i]._header_year.pack_forget()

        cal[i].tooltip_wrapper.configure(delay=1, alpha=0.8)
        cal[i]._properties["tooltipbackground"] = "darkblue"
        cal[i]._properties["tooltipforeground"] = "white"
        cal[i].style.configure("%s.tooltip.TLabel" % cal[i]._style_prefixe, font="TkDefaultFont 12 bold")

        cal[i].tag_config("own", background="yellow", foreground="black")
        cal[i].tag_config("shared", background="purple", foreground="white")
        cal[i].bind("<<CalendarSelected>>", event_label)
        row = (0 if i in [1, 4, 7, 10]
               else (1 if i in [2, 5, 8, 11]
                     else (2 if i in [3, 6, 9, 12]
                           else 3)))
        col = (0 if i in [1, 2, 3]
               else (1 if i in [4, 5, 6]
                     else (2 if i in [7, 8, 9]
                           else (3 if i in [10, 11, 12]
                                 else 4))))
        cal[i].grid(row=row, column=col)

    # перелистывание всех месяцев/календарей на год назад
    def prev_year():
        for i in range(1, 13):
            cal[i]._prev_year()
            cal[1]._header_year.configure(text=cal[1]._date.year)
            if isinstance(evl, st.ScrolledText):
                evl.frame.destroy()
                evl.vbar.destroy()
                evl.destroy()
            else: evl.destroy()
            evl_recover()

    # перелистывание всех месяцев/календарей на год вперёд
    def next_year():
        for i in range(1, 13):
            cal[i]._next_year()
            cal[1]._header_year.configure(text=cal[1]._date.year)
            if isinstance(evl, st.ScrolledText):
                evl.frame.destroy()
                evl.vbar.destroy()
                evl.destroy()
            else: evl.destroy()
            evl_recover()

    # создание годового скрола в правом нижнем углу
    f_year = ttk.Frame(CUI, style="main.%s.TFrame" % cal[1]._style_prefixe)
    cal[1]._l_year = ttk.Button(f_year, style="L.%s.TButton" % cal[1]._style_prefixe, command=prev_year)
    cal[1]._header_year = ttk.Label(f_year, width=5, anchor="center", text=cal[1]._date.year,
                                    style="main.%s.TLabel" % cal[1]._style_prefixe, font="Arial 15")
    cal[1]._r_year = ttk.Button(f_year, style="R.%s.TButton" % cal[1]._style_prefixe, command=next_year)
    cal[1]._l_year.pack(side="left", fill="y")
    cal[1]._header_year.pack(side="left", padx=4)
    cal[1]._r_year.pack(side="left", fill="y")
    f_year.grid(row=3, column=3)

    def evl_recover():
        nonlocal evl, emplug
        evl = tk.Label(CUI, background="darkblue", foreground="white", justify="left",
                       text=emplug, wraplength=870, font="Arial 12", anchor="w", pady=4, padx=15)
        evl.grid(row=3, column=0, columnspan=3, sticky="nsew")
    evl_recover()
    CUI.update()

    # заполнение собственными событиями выбранного типа календаря пользователя
    if clntr_factor != 2:
        for eid in BND._users[uid]._calendars[cln]._events:
            cal[dt_fr_iso(eid._dates[0]).month].calevent_create(dt_fr_iso(eid._dates[0]).date(), eid._name,
                                                                [CLR._specs[cln][1], eid._descript, "own"])
            # дублирование собственных событий в логике периодичности их уведомлений
            if int(eid._period[0]) == 2:
                tdnt = timedelta(days=1)
                evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                while date(date.today().year + 2, 12, 31) > evnt:
                    cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[cln][1], eid._descript, "own"])
                    evnt += tdnt
            if int(eid._period[0]) == 3:
                tdnt = timedelta(days=7)
                evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                while date(date.today().year + 2, 12, 31) > evnt:
                    cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[cln][1], eid._descript, "own"])
                    evnt += tdnt
            if int(eid._period[0]) == 4:
                tdnt = timedelta(days=30)
                evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                while date(date.today().year + 2, 12, 31) > evnt:
                    cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[cln][1], eid._descript, "own"])
                    evnt += tdnt
            if int(eid._period[0]) == 5:
                tdnt = timedelta(days=90)
                evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                while date(date.today().year + 2, 12, 31) > evnt:
                    cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[cln][1], eid._descript, "own"])
                    evnt += tdnt
            if int(eid._period[0]) == 6:
                tdnt = timedelta(days=181)
                evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                while date(date.today().year + 2, 12, 31) > evnt:
                    cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[cln][1], eid._descript, "own"])
                    evnt += tdnt
            if int(eid._period[0]) == 7:
                tdnt = timedelta(days=365)
                evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                while date(date.today().year + 2, 12, 31) > evnt:
                    cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[cln][1], eid._descript, "own"])
                    evnt += tdnt

        # заполнение календарей событиями других пользователей, в которых отмечен текущий юзер
        for clnt in BND._users[uid]._calendars.keys():
            for j in BND._users[uid]._calendars[clnt]._shared:
                cal[dt_fr_iso(j[0]._dates[0]).month].calevent_create(dt_fr_iso(j[0]._dates[0]).date(), j[0]._name + " 🔀",
                                                                     [CLR._specs[clnt][1], j[0]._descript +
                                                                      f" <<< Событие календаря пользователя"
                                                                      f" {BND._users[j[1]]._login} !!!", "shared"])
                # дублирование событий других пользователей в логике периодичности их уведомлений
                if int(j[0]._period[0]) == 2:
                    tdnt = timedelta(days=1)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 3:
                    tdnt = timedelta(days=7)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 4:
                    tdnt = timedelta(days=30)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 5:
                    tdnt = timedelta(days=90)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 6:
                    tdnt = timedelta(days=181)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 7:
                    tdnt = timedelta(days=365)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt

    # заполнение собственными событиями ВСЕХ типов календарей пользователя
    else:
        for clnt in BND._users[uid]._calendars.keys():
            for eid in BND._users[uid]._calendars[clnt]._events:
                cal[dt_fr_iso(eid._dates[0]).month].calevent_create(dt_fr_iso(eid._dates[0]).date(), eid._name,
                                                                    [CLR._specs[clnt][1], eid._descript, "own"])
                # дублирование собственных событий в логике периодичности их уведомлений
                if int(eid._period[0]) == 2:
                    tdnt = timedelta(days=1)
                    evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[clnt][1], eid._descript, "own"])
                        evnt += tdnt
                if int(eid._period[0]) == 3:
                    tdnt = timedelta(days=7)
                    evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[clnt][1], eid._descript, "own"])
                        evnt += tdnt
                if int(eid._period[0]) == 4:
                    tdnt = timedelta(days=30)
                    evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[clnt][1], eid._descript, "own"])
                        evnt += tdnt
                if int(eid._period[0]) == 5:
                    tdnt = timedelta(days=90)
                    evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[clnt][1], eid._descript, "own"])
                        evnt += tdnt
                if int(eid._period[0]) == 6:
                    tdnt = timedelta(days=181)
                    evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[clnt][1], eid._descript, "own"])
                        evnt += tdnt
                if int(eid._period[0]) == 7:
                    tdnt = timedelta(days=365)
                    evnt = dt_fr_iso(eid._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, eid._name, [CLR._specs[clnt][1], eid._descript, "own"])
                        evnt += tdnt

        # заполнение ВСЕХ календарей событиями других пользователей, в которых отмечен текущий юзер
        for clnt in BND._users[uid]._calendars.keys():
            for j in BND._users[uid]._calendars[clnt]._shared:
                cal[dt_fr_iso(j[0]._dates[0]).month].calevent_create(dt_fr_iso(j[0]._dates[0]).date(), j[0]._name + " 🔀",
                                                                     [CLR._specs[clnt][1], j[0]._descript +
                                                                      f" <<< Событие календаря пользователя"
                                                                      f" {BND._users[j[1]]._login} !!!", "shared"])
                # дублирование событий других пользователей в логике периодичности их уведомлений
                if int(j[0]._period[0]) == 2:
                    tdnt = timedelta(days=1)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 3:
                    tdnt = timedelta(days=7)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 4:
                    tdnt = timedelta(days=30)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 5:
                    tdnt = timedelta(days=90)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 6:
                    tdnt = timedelta(days=181)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt
                if int(j[0]._period[0]) == 7:
                    tdnt = timedelta(days=365)
                    evnt = dt_fr_iso(j[0]._dates[0]).date() + tdnt
                    while date(date.today().year + 2, 12, 31) > evnt:
                        cal[evnt.month].calevent_create(evnt, j[0]._name + " 🔀",
                                                        [CLR._specs[clnt][1], j[0]._descript +
                                                         f" <<< Событие календаря пользователя"
                                                         f" {BND._users[j[1]]._login} !!!", "shared"])
                        evnt += tdnt


"""
Рестилизация pymsgbox.__fillablebox() с добавлением в него tkinter.scrolledtext.ScrolledText
вместо tkinter.Message при выводе найденных по дате событий общей длиной более 1000 символов
"""

rootWindowPosition = "+450+170"
PROPORTIONAL_FONT_SIZE = 10
TEXT_ENTRY_FONT_SIZE = 12
PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]
TIMEOUT_RETURN_VALUE = "Timeout"
TKINTER_IMPORT_SUCCEEDED = True
OK_TEXT = "Погнали!)"
CANCEL_TEXT = "Свалить!)"
dent1, dent2 = None, None
entryWidgetpwd = None
dtntr_factor = None

def __enterboxCancel(event):
    global __enterboxText
    __enterboxText = None
    boxRoot.quit()

def __enterboxGetText(event):
    global __enterboxText
    __enterboxText = entryWidget.get()
    boxRoot.quit()

def _tabRight(event):
    boxRoot.event_generate("<Tab>")

def _tabLeft(event):
    boxRoot.event_generate("<Shift-Tab>")

def _bindArrows(widget, skipArrowKeys=False):
    widget.bind("<Down>", _tabRight)
    widget.bind("<Up>", _tabLeft)
    if not skipArrowKeys:
        widget.bind("<Right>", _tabRight)
        widget.bind("<Left>", _tabLeft)

def timeoutBoxRoot():
    global boxRoot, __replyButtonText, __enterboxText
    boxRoot.destroy()
    __replyButtonText = TIMEOUT_RETURN_VALUE
    __enterboxText = TIMEOUT_RETURN_VALUE

def __fillablebox(msg, title="", default="", mask=None, root=None, timeout=None, dtntr=0, clntr=0):
    """Show a box in which a user can enter some text"""

    global boxRoot, __enterboxText, __enterboxDefaultText, dent1, dent2
    global cancelButton, entryWidget, entryWidgetpwd, okButton, dtntr_factor, clntr_factor
    dtntr_factor = dtntr
    clntr_factor = clntr

    if title == None:
        title == ""
    if default == None:
        default = ""
    __enterboxDefaultText = default
    __enterboxText = __enterboxDefaultText

    if root:
        root.withdraw()
        boxRoot = tk.Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = tk.Tk()
        boxRoot.withdraw()

    boxRoot.title(title)
    boxRoot.iconname("Dialog")
    wh = "415x170" if len(title) in range(35, 50) and len(msg) in range(100) else ""
    boxRoot.geometry(f"{wh}+450+170" if len(msg) < 100 else (f"{wh}+450+150" if len(msg) < 1000 else f"{wh}+450+40"))
    boxRoot.bind("<Escape>", __enterboxCancel)

    # ------------- define the messageFrame -------------------------
    messageFrame = tk.Frame(master=boxRoot)
    messageFrame.pack(side=tk.TOP, fill=tk.BOTH)

    # ------------- define the buttonsFrame -------------------------
    buttonsFrame = tk.Frame(master=boxRoot)
    buttonsFrame.pack(side=tk.TOP, fill=tk.BOTH)

    # ------------- define the entryFrame ---------------------------
    entryFrame = tk.Frame(master=boxRoot)
    entryFrame.pack(side=tk.TOP, fill=tk.BOTH)

    # ------------- define the buttonsFrame -------------------------
    buttonsFrame = tk.Frame(master=boxRoot)
    buttonsFrame.pack(side=tk.TOP, fill=tk.BOTH)

    # -------------------- the msg widget ---------------------------
    if len(msg) > 1000:
        messageWidget = st.ScrolledText(master=messageFrame, width=55, height=33, wrap=tk.WORD,
                                        font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
        messageWidget.grid(column=0, padx="3m", pady="3m")
        messageWidget.insert(tk.INSERT, msg)
    else:
        messageWidget = tk.Message(master=messageFrame, width=("4.4i" if wh == "415x170" else "4.5i"), text=msg)
        messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
        messageWidget.pack(side=tk.TOP, expand=1, fill=tk.BOTH, padx="3m", pady="3m")

    if dtntr == 0:
    # --------- entryWidget -----------------------------------------
        ew = 45 if len(title) in range(35, 50) and len(msg) in range(100, 600) else 40
        entryWidget = tk.Entry(entryFrame, width=ew)
        _bindArrows(entryWidget, skipArrowKeys=True)
        entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
        if mask:
            entryWidget.configure(show=mask)
        entryWidget.pack(side=tk.LEFT, padx="5m")
        entryWidget.bind("<Return>", __enterboxGetText)
        entryWidget.bind("<Escape>", __enterboxCancel)

        # put text into the entryWidget and have it pre-highlighted
        if __enterboxDefaultText != "":
            entryWidget.insert(0, __enterboxDefaultText)
            entryWidget.select_range(0, tk.END)

    elif dtntr == 2:
    # --------- date_entry button -----------------------------------
        entryFrame.configure(padx=60)
        dent1 = DateEntry(entryFrame, width=10, background="darkblue", foreground="white", selectmode="day",
                          locale="ru_RU", date_pattern="yyyy-mm-dd", borderwidth=2, font="Arial 11",
                          showweeknumbers=False, showothermonthdays=False)
        dent1.grid(row=0, column=0, padx=12, sticky="nsew")
        dent2 = DateEntry(entryFrame, width=10, background="darkblue", foreground="white", selectmode="day",
                          locale="ru_RU", date_pattern="yyyy-mm-dd", borderwidth=2, font="Arial 11",
                          showweeknumbers=False, showothermonthdays=False)
        dent2.grid(row=0, column=1, sticky="nsew")

    elif dtntr == 1:
    # --------- entryWidget login-----------------------------------------
        entryWidget = tk.Entry(entryFrame, width=25)
        _bindArrows(entryWidget, skipArrowKeys=True)
        entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
        entryWidget.pack(side=tk.TOP, padx="1m")
        entryWidget.bind("<Escape>", __enterboxCancel)
    # --------- messageWidget password-----------------------------------------
        messageWidgetpwd = tk.Message(entryFrame, width="2.5i", anchor="w", text="Введите пароль >>>")
        messageWidgetpwd.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
        messageWidgetpwd.pack(side=tk.TOP, expand=1, fill=tk.BOTH, padx="7m", pady="1m")
        messageWidget.configure(width="2.5i", padx="6m", pady="1m")
    # --------- entryWidget password-----------------------------------------
        entryWidgetpwd = tk.Entry(entryFrame, width=25)
        _bindArrows(entryWidgetpwd, skipArrowKeys=True)
        entryWidgetpwd.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
        entryWidgetpwd.configure(show="*")
        entryWidgetpwd.pack(side=tk.BOTTOM, padx="3m", pady="1m")
        entryWidgetpwd.bind("<Return>", __enterboxGetText)
        entryWidgetpwd.bind("<Escape>", __enterboxCancel)

    # ------------------ ok button ----------------------------------
    okButton = tk.Button(buttonsFrame, takefocus=1, text=OK_TEXT)
    _bindArrows(okButton)
    okButton.pack(expand=1, side=tk.LEFT, padx="3m", pady="3m", ipadx="2m", ipady="1m")

    # for the commandButton, bind activation events to the activation event handler
    commandButton = okButton
    handler = __enterboxGetText
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ------------------ cancel button ------------------------------
    cancelButton = tk.Button(buttonsFrame, takefocus=1, text=CANCEL_TEXT)
    _bindArrows(cancelButton)
    cancelButton.pack(expand=1, side=tk.RIGHT, padx="3m", pady="3m", ipadx="2m", ipady="1m")

    # for the commandButton, bind activation events to the activation event handler
    commandButton = cancelButton
    handler = __enterboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    if clntr in range(1, 3):
    # ------------------- calendar button ---------------------------
        if clntr == 1: caltxt = "<Выкатить Календарь>"
        if clntr == 2: caltxt = "Выкатить все события в одном Календаре"
        calButton = tk.Button(buttonsFrame, takefocus=1, text=caltxt, wraplength=130, bg="darkblue", fg="white")
        _bindArrows(calButton)
        calButton.pack(expand=1, side=tk.LEFT, padx="3m", pady="3m", ipadx="2m", ipady="1m")

        # for the commandButton, bind activation events to the activation event handler
        commandButton = calButton
        handler = Eventhandler
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)

    # ------------------- time for action! -----------------
    if dtntr in range(2):
        entryWidget.focus_force()
    boxRoot.deiconify()
    if timeout is not None:
        boxRoot.after(timeout, timeoutBoxRoot)
    boxRoot.mainloop()

    # -------- after the run has completed -----------------
    if root:
        root.deiconify()
    try:
        boxRoot.destroy()
    except tk.TclError:
        if __enterboxText != TIMEOUT_RETURN_VALUE:
            return None

    return __enterboxText

def __enterboxGetText(event):
    global __enterboxText, dtntr_factor, entryWidget, entryWidgetpwd, dent1, dent2
    if dtntr_factor == 1:
        __enterboxText = [entryWidget.get(), entryWidgetpwd.get()]
    elif dtntr_factor == 2:
        __enterboxText = [dent1.get(), dent2.get()]
    else:
        __enterboxText = entryWidget.get()
    boxRoot.quit()

def _promptTkinter(text="", title="", default="", root=None, timeout=None, dtntr=0, clntr=0):
    """Displays a message box with text input, and OK & Cancel buttons.
    Returns the text entered, or None if Cancel was clicked."""
    assert TKINTER_IMPORT_SUCCEEDED, "Tkinter is required for pymsgbox"
    text = str(text)
    return __fillablebox(text, title, default=default, mask=None, root=root, timeout=timeout, dtntr=dtntr, clntr=clntr)

