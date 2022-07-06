import os
import sys
import time
import config
from openpyxl import Workbook
from bitrix import Bitrix
from efficiency import Efficiency
from gui import *
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)


def disable_ui():
    ui.login.setEnabled(False)
    ui.password.setEnabled(False)
    ui.webhook.setEnabled(False)
    ui.month.setEnabled(False)
    ui.year.setEnabled(False)
    ui.working_emp.setEnabled(False)
    ui.fired_emp.setEnabled(False)
    ui.create_report_button.setEnabled(False)
    app.processEvents()


def enable_ui():
    ui.login.setEnabled(True)
    ui.password.setEnabled(True)
    ui.webhook.setEnabled(True)
    ui.month.setEnabled(True)
    ui.year.setEnabled(True)
    ui.working_emp.setEnabled(True)
    ui.fired_emp.setEnabled(True)
    ui.create_report_button.setEnabled(True)
    app.processEvents()


def make_report():
    disable_ui()
    # Получение параметров с UI
    login = ui.login.text()
    password = ui.password.text()
    token = ui.webhook.text()
    month = int(ui.month.text())
    month_rus = ('январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль',
                 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь')[month - 1].capitalize()
    year = int(ui.year.text())
    working = ui.working_emp.isChecked()
    fired = ui.fired_emp.isChecked()
    if not all((login, password, token, month, year)):
        ui.status.setText("Ошибка! Заполнены не все поля")
        ui.status.adjustSize()
        return 1

    # Авторизация и получение сессии
    try:
        ui.status.setText("Авторизация..")
        ui.status.adjustSize()
        efficiency = Efficiency(login, password)
        if efficiency.session is None:
            raise Exception

        ui.status_bar.setProperty("value", 1)
        ui.status.setText("Авторизация....Успех")
        ui.status.adjustSize()
    except Exception as e:
        QtWidgets.QMessageBox.information(Form, "Неверный логин или пароль", f"Ошибка с авторизацией.\n"
                                                                  f"Неверный логин или пароль.\n")
        enable_ui()
        return 1

    # Получение списка департаментов и сотрудников
    try:
        crm = Bitrix(token)

        ui.status.setText("Получение департаментов..")
        ui.status.adjustSize()

        deps = crm.get_departments()

        ui.status_bar.setProperty("value", 6)
        ui.status.setText("Получение департаментов....Успех")
        ui.status.adjustSize()

        ui.status.setText("Получение сотрудников..")
        ui.status.adjustSize()

        users = crm.get_employees(working=working, fired=fired)

        ui.status_bar.setProperty("value", 10)
        ui.status.setText("Получение сотрудников....Успех")
        ui.status.setText("Подбор департаментов по словарю..")
        ui.status.adjustSize()
    except Exception as e:
        QtWidgets.QMessageBox.information(Form, "Неверный токен", f"Ошибка с токеном.\n"
                                                                  f"Не удалось получить список сотрудников и отделов.\n"
                                                                  f"Ошибка: {str(e)}")
        config.set(login, password, "")
        enable_ui()
        return 1
    try:
        for user_id in users.values():
            if user_id["deps"] in deps.keys():
                user_id["deps"] = deps[user_id["deps"]]
            else:
                print("Неизвестный департамент:", str(user_id["deps"]), "у сотрудника:", user_id["name"])
                user_id["deps"] = "Без привязки к отделу"
    except Exception as e:
        ui.status.setText("Ошибка!" + str(e))
        ui.status.adjustSize()
        return 1

    ui.status.setText("Подбор департаментов по словарю..Успех")
    ui.status.adjustSize()

    sorted_users_id = sorted(users.keys(), key=lambda x: (users[x]["deps"], users[x]["name"]))
    sorted_users = {k: users[k] for k in sorted_users_id}
    pbar_step = int(90 / len(sorted_users))

    # Сохраняем конфиг, т.к. всё ок
    config.set(login, password, token)

    # Начало получения и записи данных
    wb = Workbook()
    data_sheet = wb.active
    data_sheet.title = f"{month_rus} - {year}"

    data_sheet.append(["Все сотрудники", month_rus])

    current_month = time.localtime().tm_mon
    current_year = time.localtime().tm_year
    current_dep = ""
    # k = 0
    for user_id in sorted_users:
        # k += 1
        # if k < 5 or k > 10: continue
        try:
            name = users[user_id]['name']
            ui.status.setText(f"Получение: {name}")
            ui.status.adjustSize()
            app.processEvents()

            efficiency_list = list()

            is_new_dep = False
            if users[user_id]["deps"] != current_dep:
                current_dep = users[user_id]["deps"]
                dep_line = [current_dep]
                is_new_dep = True

            year_of_reg = int(users[user_id]["date_register"][:4])
            month_of_reg = int(users[user_id]["date_register"][5:7])

            if year > current_year or year < year_of_reg:
                efficiency_list.append(["", "", "", ""])
            elif (year == current_year and month > current_month) or (year == year_of_reg and month < month_of_reg):
                efficiency_list.append(["", "", "", ""])
            else:
                result = efficiency.by_month(month, year, user_id)
                if result != "Нет доступа":
                    result = result.json()["data"]
                    result = dict(
                        zip(["Эффективность", "Завершено задач", "Замечаний", "Всего в работе", "График", "DEL"],
                            result.values()))
                    result["Эффективность"] = str(result["Эффективность"]) + "%"
                    del result["DEL"]
                    ef_month = [result["Эффективность"], result["Всего в работе"], result["Завершено задач"],
                                result["Замечаний"]]
                    efficiency_list.append(ef_month)
                    time.sleep(0.05)
                else:
                    efficiency_list.append(["403", "403", "403", "403"])
                    break

            efficiency_list = [list(x) for x in zip(*efficiency_list)]

            efficiency_list[0].insert(0, name)
            efficiency_list[1].insert(0, "Всего в работе")
            efficiency_list[2].insert(0, "Завершено задач")
            efficiency_list[3].insert(0, "Замечаний")
            if is_new_dep:
                efficiency_list.insert(0, dep_line)

            efficiency_list.append([""])
            for row in efficiency_list:
                data_sheet.append(row)
            ui.status_bar.setProperty("value", ui.status_bar.value() + pbar_step)
        except Exception as e:
            ui.status.setText(f"Ошибка! {str(e)}")
            ui.status.adjustSize()
            app.processEvents()
            time.sleep(5)

    ui.status_bar.setProperty("value", 99)
    if not os.path.exists("./Отчёты"):
        os.mkdir("./Отчёты")

    # Автонастройка ширины ячеек
    dims = {}
    for row in data_sheet.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
    for col, value in dims.items():
        data_sheet.column_dimensions[col].width = value + 5
    try:
        wb.save("./Отчёты/" + f"Отчёт эффективности за {month_rus} {year}.xlsx")
        ui.status.setText("Запись данных в таблицу эксель....Успех")
        ui.status_bar.setProperty("value", 100)
        QtWidgets.QMessageBox.information(Form, "Успех!", "Отчёт создан в папке \"Отчёты\".")
    except Exception as e:
        ui.status.setText(f"Ошибка при сохранении файла! {str(e)}")
        ui.status.adjustSize()
        app.processEvents()
        wb.save(f"backup {time.time()}.xlsx")
        time.sleep(5)
        ui.status.setText(f"Ошибка при сохранении. Файл сохранён как backup.")
        ui.status.adjustSize()
        app.processEvents()
        QtWidgets.QMessageBox.information(Form, "Что-то пошло не так...", "Ошибка! Отчёт сохранён как backup.xlsx")
    finally:
        enable_ui()


def start():
    # Запись данных из конфига в UI
    cfg = config.get()
    ui.login.setText(cfg[0])
    ui.password.setText(cfg[1])
    ui.webhook.setText(cfg[2])

    # Подключение функций к кнопкам
    ui.create_report_button.clicked.connect(make_report)

    # Rock and Roll
    Form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
