# riskaudit.py
import streamlit as st
import pandas as pd
import sqlite3

# Подключение к базе данных SQLite
def connect_db():
    conn = sqlite3.connect('riskaudit.db')
    cursor = conn.cursor()
    return conn, cursor

# Создание таблицы, если она не существует
def create_table(conn, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            stage TEXT,
            requirements TEXT,
            performed_work TEXT,
            problems TEXT,
            results TEXT
        )
    ''')
    conn.commit()

# Функция для вставки данных в базу данных
def insert_data(cursor, name, position, stage, requirements, performed_work, problems, results):
    cursor.execute('''
        INSERT INTO audit_data (name, position, stage, requirements, performed_work, problems, results)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, position, stage, requirements, performed_work, problems, results))
    cursor.connection.commit()

# Функция для извлечения данных из базы данных
def fetch_data(cursor):
    cursor.execute('SELECT * FROM audit_data')
    data = cursor.fetchall()
    return data

# Тест для выбора варианта аудита
def audit_type_test():
    st.subheader("Тест: Выберите вариант аудита")

    options = ["Легкий аудит для мелких предприятий", "Аудит для средних предприятий", "Аудит для крупных предприятий"]
    chosen_option = st.radio("Выберите вариант аудита:", options)

    if chosen_option == options[0]:
        st.write("Вы выбрали Легкий аудит для мелких предприятий.")
        st.write("Этапы аудита:")
        stages = ["Подготовительный этап", "Сбор информации", "Анализ собранной информации", "Проверка соответствия законодательству и стандартам", "Выявление уязвимостей и возможных угроз безопасности", "Подготовка отчета и рекомендации"]

    elif chosen_option == options[1]:
        st.write("Вы выбрали Аудит для средних предприятий.")
        st.write("Этапы аудита:")
        stages = ["Подготовительный этап", "Сбор информации", "Проверка соответствия законодательству и стандартам", "Выявление уязвимостей и возможных угроз безопасности", "Подготовка отчета и рекомендации"]

    else:
        st.write("Вы выбрали Аудит для крупных предприятий.")
        st.write("Этапы аудита:")
        stages = ["Подготовительный этап", "Сбор информации", "Анализ собранной информации", "Проверка соответствия законодательству и стандартам", "Выявление уязвимостей и возможных угроз безопасности", "Подготовка отчета и рекомендации"]

    return stages

# Описание этапов аудита
def stage_description(stage):
    descriptions = {
        "Подготовительный этап": "На этом этапе определяются цели и задачи аудита, а также формируется команда, которая будет проводить аудит.",
        "Сбор информации": "На этом этапе аудиторы собирают информацию о системе защиты информации, изучают документацию, протоколы и журналы системы, а также проводят интервью с сотрудниками, ответственными за информационную безопасность.",
        "Анализ собранной информации": "На этом этапе аудиторы анализируют собранную информацию и оценивают эффективность системы защиты информации.",
        "Проверка соответствия законодательству и стандартам": "На этом этапе проводится проверка соответствия системы защиты информации законодательству и стандартам безопасности.",
        "Выявление уязвимостей и возможных угроз безопасности": "На этом этапе аудиторы выявляют уязвимости и возможные угрозы безопасности системы защиты информации.",
        "Подготовка отчета и рекомендации": "По результатам аудита составляется отчет, в котором указываются выявленные уязвимости и возможные угрозы безопасности, а также рекомендации по усовершенствованию системы защиты информации."
    }
    return descriptions.get(stage, "")

# Отображение иконок для этапов аудита
def display_stage_icons(stages, cursor):
    selected_stage = st.selectbox("Выберите текущий этап аудита:", stages)
    st.write(f"Выбран этап: {selected_stage}")
    st.subheader(f"Описание этапа '{selected_stage}'")
    st.write(stage_description(selected_stage))

    # Создаем или обновляем значения в переменных
    performed_work_key = f"performed_work_{selected_stage.replace(' ', '_')}"
    problems_key = f"problems_{selected_stage.replace(' ', '_')}"

    performed_work = st.text_area(f"Введите информацию о выполненных работах на этапе '{selected_stage}'", height=100, key=performed_work_key)
    problems = st.text_area(f"Введите информацию о проблемах, возникших на этапе '{selected_stage}'", height=100, key=problems_key)

    return selected_stage, performed_work, problems

# Главная функция приложения
def main():
    # Подключение к базе данных SQLite
    conn, cursor = connect_db()

    # Создание таблицы, если она не существует
    create_table(conn, cursor)

    st.title('RiskAudit - Система управления аудитом')

    # Ввод информации об аудиторе
    auditor_name = st.text_input('Имя аудитора')
    auditor_position = st.text_input('Должность аудитора')

    # Отображение информации об аудиторе
    st.subheader('Информация об аудиторе')
    st.write(f'Имя: {auditor_name}')
    st.write(f'Должность: {auditor_position}')

    # Прохождение теста и получение варианта требований
    stages = audit_type_test()

    # Отображение иконок для выбора этапа
    selected_stage, performed_work, problems = display_stage_icons(stages, cursor)

    # Кнопка "Сохранить"
    if st.button('Сохранить данные'):
        # Сохранение данных в базу данных
        insert_data(cursor, auditor_name, auditor_position, selected_stage, '', performed_work, problems, '')

    # Таблица с данными
    all_data = fetch_data(cursor)
    df = pd.DataFrame(all_data, columns=["ID", "Имя", "Должность", "Этап", "Требования", "Выполненные работы", "Проблемы", "Результаты"])
    st.write(df)


    # Освобождение ресурсов при закрытии приложения
    conn.close()

if __name__ == '__main__':
    main()
