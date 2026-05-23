from pip._internal.cli.cmdoptions import python

python

import tkinter as tk
import pygame
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import random
from datetime import datetime

# ==========================================
# ЗВУК
# ==========================================

pygame.mixer.init()

# ==========================================
# БАЗА ДАННЫХ
# ==========================================

conn = sqlite3.connect("characters.db")
cursor = conn.cursor()

# Таблица рас
cursor.execute("""
CREATE TABLE IF NOT EXISTS races (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    race_name TEXT UNIQUE,
    description TEXT
)
""")

# Таблица классов
cursor.execute("""
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT UNIQUE,
    role TEXT
)
""")

# Главная таблица персонажей
cursor.execute("""
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    race_id INTEGER,
    class_id INTEGER,
    weapon TEXT,
    level INTEGER,
    strength INTEGER,
    agility INTEGER,
    intelligence INTEGER,
    bio TEXT,
    created_at TEXT,

    FOREIGN KEY (race_id) REFERENCES races(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
)
""")

conn.commit()

# ==========================================
# ДАННЫЕ
# ==========================================

names = [
    "Артас", "Луна", "Дориан", "Селена",
    "Вариан", "Моргана", "Каэль", "Ривен",
    "Сайлас", "Эйлин", "Дрейк", "Люциан",
    "Тирион", "Фенрис", "Леона", "Малек"
]

races = [
    "Человек",
    "Эльф",
    "Орк",
    "Гном",
    "Тифлинг",
    "Нежить",
    "Драконорождённый"
]

classes = [
    "Воин",
    "Маг",
    "Паладин",
    "Разбойник",
    "Некромант",
    "Следопыт",
    "Берсерк"
]
# ==========================================
# ЗАПОЛНЕНИЕ ТАБЛИЦ
# ==========================================

for race in races:

    cursor.execute(
        """
        INSERT OR IGNORE INTO races (
            race_name,
            description
        )
        VALUES (?, ?)
        """,
        (
            race,
            f"Описание расы {race}"
        )
    )

conn.commit()

for cls in classes:

    cursor.execute(
        """
        INSERT OR IGNORE INTO classes (
            class_name,
            role
        )
        VALUES (?, ?)
        """,
        (
            cls,
            f"Роль класса {cls}"
        )
    )

conn.commit()

weapons = [
    "Меч",
    "Лук",
    "Топор",
    "Кинжал",
    "Посох",
    "Молот",
    "Арбалет"
]

biographies = [
    "Вырос в северных землях и с детства обучался владению оружием.",
    "Поклялся защищать королевство от сил тьмы после гибели своей семьи.",
    "Был изгнан из своего клана за использование запретной магии.",
    "Изучает древние руины в поисках утерянных артефактов.",
    "Много лет служил наёмником в приграничных землях.",
    "Служит тайному ордену магов и скрывает своё прошлое.",
    "Охотится на чудовищ, чтобы отомстить за разрушенную деревню.",
    "Бывший рыцарь, потерявший титул после предательства короля."
]

origins = [
    "родился в бедной семье ремесленников",
    "вырос среди воинов северного клана",
    "был воспитан магами древнего ордена",
    "провёл детство в лесах эльфийского королевства",
    "долгое время жил среди наёмников и авантюристов",
    "вырос в подземных шахтах гномов"
]

traits = [
    "отличается храбростью",
    "обладает вспыльчивым характером",
    "умеет сохранять хладнокровие в бою",
    "ненавидит несправедливость",
    "всегда стремится к знаниям",
    "готов пожертвовать собой ради союзников"
]

missions = [
    "ищет древний артефакт великой силы",
    "пытается остановить вторжение демонов",
    "охотится за предателем своего ордена",
    "мечтает стать легендой среди героев",
    "пытается раскрыть тайну своего происхождения",
    "разыскивает утраченное сокровище королевства"
]



conn.commit()



current_character = None

# ==========================================
# ЦВЕТА И СТИЛЬ
# ==========================================

BG_COLOR = "#121212"
CARD_COLOR = "#1f1f1f"
TEXT_COLOR = "#f5f5dc"
BUTTON_COLOR = "#7b1113"
BUTTON_HOVER = "#9c1c1f"
ACCENT = "#d4af37"
SUCCESS = "#4CAF50"

# ==========================================
# ФУНКЦИИ
# ==========================================



def clear_text():
    text.delete("1.0", tk.END)


# ==========================================
# ГЕНЕРАЦИЯ РЕДКОСТИ
# ==========================================


def get_rarity(level):
    if level <= 5:
        return "Обычный"
    elif level <= 10:
        return "Редкий"
    elif level <= 15:
        return "Эпический"
    else:
        return "Легендарный"


# ==========================================
# ГЕНЕРАЦИЯ ПЕРСОНАЖА
# ==========================================


def generate_character():

    global current_character

    level = random.randint(1, 20)

    name = random.choice(names)

    bio = f"""
{name} {random.choice(origins)}.

Персонаж {random.choice(traits)} и обладает большим боевым опытом.

В настоящее время герой {random.choice(missions)}.

Дополнительная информация:
{random.choice(biographies)}
"""

    current_character = {
        "name": name,
        "race": random.choice(races),
        "class_name": random.choice(classes),
        "weapon": random.choice(weapons),
        "level": level,
        "strength": random.randint(1, 20),
        "agility": random.randint(1, 20),
        "intelligence": random.randint(1, 20),
        "rarity": get_rarity(level),
        "bio": bio
    }

    clear_text()

    text.insert(tk.END, f"""
══════════════════════════════
      НОВЫЙ ПЕРСОНАЖ
══════════════════════════════

Имя: {current_character['name']}

Раса: {current_character['race']}

Класс: {current_character['class_name']}

Оружие: {current_character['weapon']}

Редкость: {current_character['rarity']}

══════════════════════════════

Уровень: {current_character['level']}

Сила:        {current_character['strength']}
Ловкость:    {current_character['agility']}
Интеллект:   {current_character['intelligence']}

══════════════════════════════

Биография:
{current_character['bio']}

══════════════════════════════
""")

def generate_filtered():

    global current_character

    level = random.randint(1, 20)

    bio = f"""
{random.choice(names)} {random.choice(origins)}.

Персонаж {random.choice(traits)} и обладает большим боевым опытом.

В настоящее время герой {random.choice(missions)}.

Дополнительная информация:
{random.choice(biographies)}
"""

    current_character = {
        "name": random.choice(names),
        "race": random.choice(races),
        "class_name": random.choice(classes),
        "weapon": random.choice(weapons),
        "level": level,
        "strength": random.randint(1, 20),
        "agility": random.randint(1, 20),
        "intelligence": random.randint(1, 20),
        "rarity": get_rarity(level),
        "bio": bio
    }

    clear_text()

    text.insert(tk.END, f"""
    
══════════════════════════════
      НОВЫЙ ПЕРСОНАЖ
══════════════════════════════

Имя: {current_character['name']}

Раса: {current_character['race']}

Класс: {current_character['class_name']}

Оружие: {current_character['weapon']}

Редкость: {current_character['rarity']}

══════════════════════════════

Уровень: {current_character['level']}

Сила:        {current_character['strength']}
Ловкость:    {current_character['agility']}
Интеллект:   {current_character['intelligence']}

══════════════════════════════

Биография:
{current_character['bio']}

══════════════════════════════
""")
def custom_generate():

    filter_window = tk.Toplevel(window)

    filter_window.title("Настройка генерации")

    filter_window.geometry("450x400")

    filter_window.configure(bg="#1f1f1f")

    filter_window.resizable(False, False)

    # =========================
    # TITLE
    # =========================

    title = tk.Label(
        filter_window,
        text="⚔ НАСТРОЙКА ГЕРОЯ ⚔",
        font=("Times New Roman", 18, "bold"),
        bg="#1f1f1f",
        fg="#d4af37"
    )

    title.pack(pady=15)

    # =========================
    # CLASS
    # =========================

    class_label = tk.Label(
        filter_window,
        text="Исключить класс:",
        font=("Arial", 11),
        bg="#1f1f1f",
        fg="white"
    )

    class_label.pack()

    class_entry = tk.Entry(
        filter_window,
        width=30,
        font=("Arial", 11),
        bg="#2b2b2b",
        fg="white",
        insertbackground="white"
    )

    class_entry.pack(pady=5)

    # =========================
    # RACE
    # =========================

    race_label = tk.Label(
        filter_window,
        text="Исключить расу:",
        font=("Arial", 11),
        bg="#1f1f1f",
        fg="white"
    )

    race_label.pack()

    race_entry = tk.Entry(
        filter_window,
        width=30,
        font=("Arial", 11),
        bg="#2b2b2b",
        fg="white",
        insertbackground="white"
    )

    race_entry.pack(pady=5)

    # =========================
    # WEAPON
    # =========================

    weapon_label = tk.Label(
        filter_window,
        text="Исключить оружие:",
        font=("Arial", 11),
        bg="#1f1f1f",
        fg="white"
    )

    weapon_label.pack()

    weapon_entry = tk.Entry(
        filter_window,
        width=30,
        font=("Arial", 11),
        bg="#2b2b2b",
        fg="white",
        insertbackground="white"
    )

    weapon_entry.pack(pady=5)

    # =========================
    # GENERATE
    # =========================

    def generate_filtered():

        excluded_class = class_entry.get()
        excluded_race = race_entry.get()
        excluded_weapon = weapon_entry.get()

        filtered_classes = [
            c for c in classes
            if c != excluded_class
        ]

        filtered_races = [
            r for r in races
            if r != excluded_race
        ]

        filtered_weapons = [
            w for w in weapons
            if w != excluded_weapon
        ]

        if not filtered_classes:
            messagebox.showerror(
                "Ошибка",
                "Нет доступных классов!"
            )
            return

        if not filtered_races:
            messagebox.showerror(
                "Ошибка",
                "Нет доступных рас!"
            )
            return

        if not filtered_weapons:
            messagebox.showerror(
                "Ошибка",
                "Нет доступного оружия!"
            )
            return

        global current_character

        level = random.randint(1, 20)

        current_character = {
            "name": random.choice(names),
            "race": random.choice(filtered_races),
            "class_name": random.choice(filtered_classes),
            "weapon": random.choice(filtered_weapons),
            "level": level,
            "strength": random.randint(1, 20),
            "agility": random.randint(1, 20),
            "intelligence": random.randint(1, 20),
            "bio": "Герой был создан с пользовательскими настройками."
        }

        clear_text()

        text.insert(tk.END, f"""
══════════════════════════════
     ГЕРОЙ ПО ФИЛЬТРУ
══════════════════════════════

Имя: {current_character['name']}

Раса: {current_character['race']}

Класс: {current_character['class_name']}

Оружие: {current_character['weapon']}

══════════════════════════════

Уровень: {current_character['level']}

Сила: {current_character['strength']}
Ловкость: {current_character['agility']}
Интеллект: {current_character['intelligence']}

══════════════════════════════
""")

        filter_window.destroy()

    # =========================
    # BUTTON
    # =========================

    generate_btn = tk.Button(
        filter_window,
        text="СГЕНЕРИРОВАТЬ",
        command=generate_filtered,
        font=("Arial", 11, "bold"),
        bg="#7b1113",
        fg="white",
        activebackground="#a61b1f",
        width=20,
        height=2,
        bd=0,
        cursor="hand2"
    )

    generate_btn.pack(pady=25)
# ==========================================
# СОХРАНЕНИЕ ПЕРСОНАЖА
# ==========================================


def save_character():

    global current_character

    if not current_character:
        messagebox.showwarning(
            "Ошибка",
            "Сначала сгенерируйте персонажа"
        )
        return

    # Получаем ID расы
    cursor.execute(
        "SELECT id FROM races WHERE race_name = ?",
        (current_character['race'],)
    )

    race_row = cursor.fetchone()

    if not race_row:
        messagebox.showerror(
            "Ошибка",
            "Раса не найдена в базе"
        )
        return

    race_id = race_row[0]

    # Получаем ID класса
    cursor.execute(
        "SELECT id FROM classes WHERE class_name = ?",
        (current_character['class_name'],)
    )

    class_row = cursor.fetchone()

    if not class_row:
        messagebox.showerror(
            "Ошибка",
            "Класс не найден в базе"
        )
        return

    class_id = class_row[0]

    # Сохраняем персонажа
    cursor.execute(
        """
        INSERT INTO characters (
            name,
            race_id,
            class_id,
            weapon,
            level,
            strength,
            agility,
            intelligence,
            bio,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            current_character['name'],
            race_id,
            class_id,
            current_character['weapon'],
            current_character['level'],
            current_character['strength'],
            current_character['agility'],
            current_character['intelligence'],
            current_character['bio'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()

    messagebox.showinfo(
        "Сохранено",
        "Персонаж успешно сохранён!"
    )

# ==========================================
# ПОКАЗАТЬ ПЕРСОНАЖЕЙ
# ==========================================


def show_characters():

    clear_text()

    cursor.execute("""
    SELECT
        characters.id,
        characters.name,
        races.race_name,
        classes.class_name,
        characters.weapon,
        characters.level

    FROM characters

    JOIN races
    ON characters.race_id = races.id

    JOIN classes
    ON characters.class_id = classes.id
    """)

    rows = cursor.fetchall()

    text.insert(tk.END, """
══════════════════════════════
        ПЕРСОНАЖИ
══════════════════════════════
""")

    if not rows:
        text.insert(tk.END, "\nНет сохранённых персонажей")
        return

    for row in rows:

        text.insert(tk.END, f"""
ID: {row[0]}
Имя: {row[1]}
Раса: {row[2]}
Класс: {row[3]}
Оружие: {row[4]}
Уровень: {row[5]}

──────────────────────────────
""")


# ==========================================
# УДАЛЕНИЕ ПЕРСОНАЖА
# ==========================================


def delete_character():


    char_id = simpledialog.askinteger(
        "Удаление",
        "Введите ID персонажа:"
    )

    if char_id is None:
        return

    cursor.execute("""
    DELETE FROM characters
    WHERE id = ?
    """, (char_id,))

    conn.commit()

    messagebox.showinfo(
        "Удалено",
        "Персонаж удалён!"
    )


# ==========================================
# ПОИСК
# ==========================================


def search_character():

    class_name = simpledialog.askstring(
        "Поиск",
        "Введите класс персонажа"
    )

    if not class_name:
        return

    cursor.execute("""
        SELECT
            characters.name,
            races.race_name,
            classes.class_name,
            characters.level

        FROM characters

        JOIN races
        ON characters.race_id = races.id

        JOIN classes
        ON characters.class_id = classes.id

        WHERE classes.class_name = ?
    """, (class_name,))

    rows = cursor.fetchall()

    clear_text()

    if not rows:
        text.insert(tk.END, "Персонажи не найдены")
        return

    for row in rows:

        text.insert(tk.END, f"""
Имя: {row[0]}
Раса: {row[1]}
Класс: {row[2]}
Уровень: {row[3]}

────────────────────
""")


# ==========================================
# СТАТИСТИКА
# ==========================================


def statistics():

    clear_text()

    # Всего персонажей
    cursor.execute("SELECT COUNT(*) FROM characters")
    total = cursor.fetchone()[0]

    # Средний уровень
    cursor.execute("SELECT AVG(level) FROM characters")
    avg_level = cursor.fetchone()[0]

    # Самый популярный класс
    cursor.execute("""
    SELECT classes.class_name, COUNT(*)

    FROM characters

    JOIN classes
    ON characters.class_id = classes.id

    GROUP BY classes.class_name

    ORDER BY COUNT(*) DESC

    LIMIT 1
    """)

    popular = cursor.fetchone()

    text.insert(tk.END, f"""
══════════════════════════════
         СТАТИСТИКА
══════════════════════════════

Всего персонажей: {total}

Средний уровень: {round(avg_level, 2) if avg_level else 0}

Самый популярный класс:
{popular[0] if popular else 'Нет данных'}

══════════════════════════════
""")


# ==========================================
# ОЧИСТКА БАЗЫ
# ==========================================


def clear_database():

    result = messagebox.askyesno(
        "Подтверждение",
        "Удалить ВСЕХ персонажей?"
    )

    if result:
        cursor.execute("DELETE FROM characters")
        conn.commit()

        messagebox.showinfo(
            "Готово",
            "База данных очищена!"
        )


# ==========================================
# ВЫХОД
# ==========================================


def exit_program():
    conn.close()
    window.destroy()


# ==========================================
# ОКНО
# ==========================================

# ==========================================
# ФОНОВАЯ МУЗЫКА
# ==========================================

try:
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except:
    pass

window = tk.Tk()

window.title("Генератор RPG-персонажей")

window.geometry("1050x750")

window.configure(bg=BG_COLOR)

window.resizable(False, False)

# ==========================================
# ЗАГОЛОВОК
# ==========================================

title = tk.Label(
    window,
    text="⚔ ГЕНЕРАТОР RPG-ПЕРСОНАЖЕЙ ⚔",
    font=("Times New Roman", 26, "bold"),
    bg=BG_COLOR,
    fg=ACCENT
)

title.pack(pady=15)

# ==========================================
# ПОДЗАГОЛОВОК
# ==========================================

subtitle = tk.Label(
    window,
    text="Курсовой проект на Python + SQLite",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg="gray"
)

subtitle.pack()

# ==========================================
# БЛОК КНОПОК
# ==========================================

button_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

button_frame.pack(pady=15)

# ==========================================
# СТИЛЬ КНОПОК
# ==========================================

button_style = {
    "font": ("Arial", 11, "bold"),
    "bg": BUTTON_COLOR,
    "fg": "white",
    "activebackground": BUTTON_HOVER,
    "activeforeground": "white",
    "width": 18,
    "height": 2,
    "bd": 0,
    "cursor": "hand2"
}

# ==========================================
# КНОПКИ
# ==========================================

buttons = [
    ("Сгенерировать", generate_character),
    ("Сохранить", save_character),
    ("Показать всех", show_characters),
    ("Поиск", search_character),
    ("Удалить", delete_character),
    ("Статистика", statistics),
    ("Очистить БД", clear_database),
    ("Выход", exit_program),
    ("Генерация с фильтром", custom_generate),
]

row = 0
col = 0

for text_btn, command in buttons:

    btn = tk.Button(
        button_frame,
        text=text_btn,
        command=command,
        **button_style
    )

    btn.grid(row=row, column=col, padx=8, pady=8)

    col += 1

    if col > 3:
        col = 0
        row += 1

# ==========================================
# ТЕКСТОВОЕ ПОЛЕ
# ==========================================

text_frame = tk.Frame(window, bg=BG_COLOR)
text_frame.pack(pady=10)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text = tk.Text(
    text_frame,
    width=105,
    height=28,
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    font=("Consolas", 11),
    insertbackground="white",
    bd=2,
    relief="solid",
    yscrollcommand=scrollbar.set
)

text.pack(side=tk.LEFT)

scrollbar.config(command=text.yview)

# ==========================================
# СТАРТОВОЕ СООБЩЕНИЕ
# ==========================================

text.insert(tk.END, """
══════════════════════════════
   ДОБРО ПОЖАЛОВАТЬ В RPG МИР
══════════════════════════════

Нажмите кнопку:

• Сгенерировать

чтобы создать нового персонажа.

══════════════════════════════
""")

# ==========================================
# НИЖНЯЯ ПАНЕЛЬ
# ==========================================

footer = tk.Label(
    window,
    text="2026 • Python • Tkinter • SQLite",
    font=("Arial", 10),
    bg=BG_COLOR,
    fg="gray"
)

footer.pack(pady=10)

# ==========================================
# ЗАПУСК
# ==========================================

window.mainloop()


