import requests
import re


class Efficiency:

    def __init__(self, login, password):
        self.session = requests.Session()

        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 YaBrowser/22.1.0.2517 Yowser/2.5 Safari/537.36"
        }

        login_data = {
            "AUTH_FORM": "Y",
            "TYPE": "AUTH",
            "backurl": "/",
            "USER_LOGIN": login,
            "USER_PASSWORD": password
        }
        # Авторизация на сайте для сессии. Получение куки
        response = self.session.post("https://crm.galtsystems.ru/?login=yes", headers=self.headers, data=login_data)
        if response.ok:
            if "Неверный логин или пароль." in response.text:
                print("Неверный логин или пароль.")
                self.session = None
            else:
                print("Успешный логин")

    def by_month(self, month, year, userid):
        # Переход на страницу эффективности сотрудника
        r = self.session.get(f"https://crm.galtsystems.ru/company/personal/user/{userid}/tasks/effective/",
                             headers=self.headers)
        if r.text.count("Доступ запрещен") == 2:
            return "Нет доступа"
        # Получение токенов
        sessid = re.search(r"'bitrix_sessid':'(.+)'}", r.text)[1]
        emmiter = re.search(r'"TasksReportEffectiveComponent","componentId":"(.+?)"', r.text)

        # TODO Применение фильтра формы
        set_filter_url = "https://crm.galtsystems.ru/bitrix/services/main/ajax.php?analyticsLabel[FILTER_ID]=TASKS_REPORT_EFFECTIVE_GRID&analyticsLabel[GRID_ID]=&analyticsLabel[PRESET_ID]=tmp_filter&analyticsLabel[FIND]=N&analyticsLabel[ROWS]=N&mode=ajax&c=bitrix%3Amain.ui.filter&action=setFilter"
        headers_filter = {
                             "bx-ajax": "true",
                             "content-type": "application/x-www-form-urlencoded",
                             "origin": "https://crm.galtsystems.ru",
                             "referer": f"https://crm.galtsystems.ru/company/personal/user/{userid}/tasks/effective/",
                             "x-bitrix-csrf-token": sessid,
                             "x-bitrix-site-id": "s1"
                         } | self.headers

        params_filter = {
            'analyticsLabel[FILTER_ID]': ['TASKS_REPORT_EFFECTIVE_GRID'],
            'analyticsLabel[PRESET_ID]': ['tmp_filter'],
            'analyticsLabel[FIND]': ['N'],
            'analyticsLabel[ROWS]': ['N'],
            'mode': ['ajax'],
            'c': ['bitrix:main.ui.filter'],
            'action': ['setFilter']
        }
        form_filter = {
            'params[FILTER_ID]': ['TASKS_REPORT_EFFECTIVE_GRID'],
            'params[action]': ['setFilter'],
            'params[forAll]': ['false'],
            'params[apply_filter]': ['Y'],
            'params[clear_filter]': ['N'],
            'params[with_preset]': ['N'],
            'params[save]': ['Y'],
            'data[fields][DATETIME_datesel]': ['MONTH'],
            'data[fields][DATETIME_month]': [month],
            'data[fields][DATETIME_year]': [year],
            'data[rows]': ['GROUP_ID,DATETIME'],
            'data[preset_id]': ['tmp_filter'],
            'data[name]': ['Текущий день']
        }
        response = self.session.post(set_filter_url, headers=headers_filter, params=params_filter, data=form_filter)
        if response.json()["status"] != "success":
            print("Установка фильтра прошла с ошибкой. Данные могут быть неверны!")

        # Запрос на получение данных эффективности по фильтру
        efficiency_form = {
            'sessid': [sessid],
            'SITE_ID': ['s1'],
            'EMMITER': [emmiter],
            'ACTION[0][OPERATION]': ['tasksreporteffectivecomponent.getEfficiencyData'],
            'ACTION[0][ARGUMENTS][DATETIME_datesel]': ['MONTH'],
            'ACTION[0][ARGUMENTS][DATETIME_month]': [month],
            'ACTION[0][ARGUMENTS][DATETIME_year]': [year],
            'ACTION[0][ARGUMENTS][userId]': [userid],
            'ACTION[0][PARAMETERS][code]': ['op_0']}

        response = self.session.post(
            "https://crm.galtsystems.ru/bitrix/components/bitrix/tasks.report.effective/ajax.php",
            headers=self.headers, data=efficiency_form)

        return response

    def by_weeks(self, start, end, userid):
        # Переход на страницу эффективности сотрудника
        r = self.session.get(f"https://crm.galtsystems.ru/company/personal/user/{userid}/tasks/effective/",
                             headers=self.headers)
        if r.text.count("Доступ запрещен") == 2:
            return "Нет доступа"
        # Получение токенов
        sessid = re.search(r"'bitrix_sessid':'(.+)'}", r.text)[1]
        emmiter = re.search(r'"TasksReportEffectiveComponent","componentId":"(.+?)"', r.text)

        # TODO Применение фильтра формы
        set_filter_url = "https://crm.galtsystems.ru/bitrix/services/main/ajax.php?analyticsLabel[FILTER_ID]=TASKS_REPORT_EFFECTIVE_GRID&analyticsLabel[GRID_ID]=&analyticsLabel[PRESET_ID]=tmp_filter&analyticsLabel[FIND]=N&analyticsLabel[ROWS]=N&mode=ajax&c=bitrix%3Amain.ui.filter&action=setFilter"
        headers_filter = {
                             "bx-ajax": "true",
                             "content-type": "application/x-www-form-urlencoded",
                             "origin": "https://crm.galtsystems.ru",
                             "referer": f"https://crm.galtsystems.ru/company/personal/user/{userid}/tasks/effective/?IFRAME=Y&IFRAME_TYPE=SIDE_SLIDER",
                             "x-bitrix-csrf-token": sessid,
                             "x-bitrix-site-id": "s1"
                         } | self.headers

        params_filter = {
            'analyticsLabel[FILTER_ID]': ['TASKS_REPORT_EFFECTIVE_GRID'],
            'analyticsLabel[PRESET_ID]': ['tmp_filter'],
            'analyticsLabel[FIND]': ['N'],
            'analyticsLabel[ROWS]': ['N'],
            'mode': ['ajax'],
            'c': ['bitrix:main.ui.filter'],
            'action': ['setFilter']
        }
        form_filter = {
            'params[FILTER_ID]': ['TASKS_REPORT_EFFECTIVE_GRID'],
            'params[action]': ['setFilter'],
            'params[forAll]': ['false'],
            'params[apply_filter]': ['Y'],
            'params[clear_filter]': ['N'],
            'params[with_preset]': ['N'],
            'params[save]': ['Y'],
            'data[fields][DATETIME_datesel]': ['RANGE'],
            'data[fields][DATETIME_from]': [start],
            'data[fields][DATETIME_to]': [end],
            'data[rows]': ['GROUP_ID,DATETIME'],
            'data[preset_id]': ['tmp_filter'],
            'data[name]': ['Текущий день']
        }
        response = self.session.post(set_filter_url, headers=headers_filter, params=params_filter, data=form_filter)
        if response.json()["status"] != "success":
            print("Установка фильтра прошла с ошибкой. Данные могут быть неверны!")

        # Запрос на получение данных эффективности по фильтру
        efficiency_form = {
            'sessid': [sessid],
            'SITE_ID': ['s1'],
            'EMMITER': [emmiter],
            'ACTION[0][OPERATION]': ['tasksreporteffectivecomponent.getEfficiencyData'],
            'ACTION[0][ARGUMENTS][DATETIME_datesel]': ['RANGE'],
            'ACTION[0][ARGUMENTS][DATETIME_from]': [start],
            'ACTION[0][ARGUMENTS][DATETIME_to]': [end],
            'ACTION[0][ARGUMENTS][userId]': [userid],
            'ACTION[0][PARAMETERS][code]': ['op_0']}

        response = self.session.post(
            "https://crm.galtsystems.ru/bitrix/components/bitrix/tasks.report.effective/ajax.php",
            headers=self.headers, data=efficiency_form)

        return response
