import sqlite3 as sq

def create_DB():        # создаем базу данных
    connection = sq.connect('DB')
    cursor = connection.cursor()

    # Создаем таблицу для объектов класса А
    table_1 = ''' CREATE TABLE IF NOT EXISTS A (id INTEGER PRIMARY KEY AUTOINCREMENT, a_value REAL NOT NULL,
    a_color TEXT NOT NULL)'''
    cursor.execute(table_1)
    connection.commit()

    # Создаем таблицу для объектов класса B
    table_2 = ''' CREATE TABLE IF NOT EXISTS B (id INTEGER PRIMARY KEY AUTOINCREMENT, b_value REAL NOT NULL,
    b_function TEXT NOT NULL)'''
    cursor.execute(table_2)
    connection.commit()

    # Создаем таблицу для результатов
    table_3 = ''' CREATE TABLE IF NOT EXISTS C (id INTEGER PRIMARY KEY AUTOINCREMENT, result TEXT NOT NULL)'''
    cursor.execute(table_3)
    connection.commit()

    cursor.close()
    connection.close()

def function_without_DB(a_value, a_color, b_value, b_function):    # функция, считывающая данные не из базы данных
    dictionary = {'red': 0, 'green': 1, 'blue': 2}

    # доступные функции
    functions = {
        'add': lambda a, b: a + b,
        'subtract': lambda a, b: a - b,
        'multiply': lambda a, b: a * b,
        'divide': lambda a, b: a / b if b != 0 else 'делить на 0 нельзя!',
        'power': lambda a, b: a ** b}

    if b_function not in functions:
        raise ValueError(f"Неподдерживаемая операция: {b_function}")
    
    index = dictionary[a_color]
    result = functions[b_function](a_value, b_value)

    result_list = [0, 0, 0]
    result_list[index] = result

    return result_list

def insert_data():  # Записываем данные в базу данных
    connection = sq.connect('DB')
    cursor = connection.cursor()

    cursor.executemany('INSERT INTO A (a_value, a_color) VALUES (?, ?)',
    [
            (3.0, 'green'),  # id=1
            (2.0, 'red'),  # id=2
            (5.0, 'blue'),  # id=3
            (4.0, 'green'),  # id=4
        ]

    )

    cursor.executemany('INSERT INTO B (b_function, b_value) VALUES (?, ?)',
        [
            ('add', 3.0),  # id=1
            ('power', 2.0),  # id=2
            ('multiply', 2.0),  # id=3
            ('subtract', 1.0), # id=4
            ('divide', 2.0)  #id=5
        ]
    )

    connection.commit()
    connection.close()

def function_with_DB(a_id, b_id):    # функция, считывающая данные из базы даных
    connection = sq.connect('DB')
    cursor = connection.cursor()

    cursor.execute('SELECT a_value, a_color FROM A WHERE id = ?', (a_id,))
    a_value, a_color = cursor.fetchone()

    cursor.execute('SELECT b_function, b_value FROM B WHERE id = ?', (b_id,))
    b_value, b_function= cursor.fetchone()

    result = function_without_DB(a_value, a_color, b_function, b_value)

    cursor.execute('INSERT INTO C (result) VALUES (?)',(str(result), ))  # записываем результат в таблицу С

    connection.commit()
    cursor.close()
    connection.close()
    return result

# Основная программа
create_DB()
insert_data()
print(function_with_DB(2,3))
