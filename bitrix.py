from fast_bitrix24 import Bitrix as FastBitrix24
import time


class Bitrix:
    def __init__(self, token):
        self.token = token

    def get_departments(self) -> dict:
        departments: dict[str] = dict()
        b = FastBitrix24(self.token)
        response = b.get_all("department.get")
        for i, dep in enumerate(response):
            response[i] = {"id": int(dep["ID"]), "name": dep["NAME"]}
        response.sort(key=lambda x: x["id"])
        for dep in response:
            departments[dep["id"]] = dep["name"].strip()
            departments[dep["id"]] = departments.get(dep["id"]).replace("  ", " ")
        return departments

    def get_employees(self, working: bool = True, fired: bool = False):
        users: dict = dict()
        b = FastBitrix24(self.token)
        if working or fired:
            if working and fired:
                response = b.get_all("user.get")
            elif working:
                response = b.get_all("user.get", params={"filter": {"ACTIVE": "true"}})
            else:  # Fired
                response = b.get_all("user.get", params={"filter": {"ACTIVE": True}})

            response.sort(key=lambda x: int(x["ID"]))
            for user in response:
                users[int(user["ID"])] = {
                    "active": user["ACTIVE"],
                    "date_register": user["DATE_REGISTER"],
                    "date_register_unix": int(time.mktime(time.strptime(user["DATE_REGISTER"][:10], "%Y-%m-%d"))) +
                                          int(user["DATE_REGISTER"][12]) * 3600,
                    "name": f'{user["NAME"].capitalize()} {user["LAST_NAME"].capitalize()}'.strip(),
                    "deps": [int(i) for i in user["UF_DEPARTMENT"]]
                }

            # Personal for crm.galtsystems.ru
            if 473 in users:
                users[473]["deps"] = [1033]

            for id in users:
                user = users[id]
                if len(user["deps"]) == 1:
                    user["deps"] = user["deps"][0]
                elif len(user["deps"]) > 1:
                    user["deps"] = min(user["deps"])

        else:
            return "Запрошен пустой список пользователей"

        return users
