import configparser
import os

config_path = r"./config/config.ini"
service_url = "crm.galtsystems.ru"


def get():
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        if service_url in config:
            user = config[service_url]
            login = user["login"] if "login" in user else ""
            password = user["password"] if "password" in user else ""
            webhook = user["webhook"] if "webhook" in user else ""
            return login, password, webhook

    return "", "", ""


def set(login="", password="", webhook=""):
    if not os.path.exists("./Config"):
        os.mkdir("./Config")

    config = configparser.ConfigParser()
    config[service_url] = {
        "login": login,
        "password": password,
        "webhook": webhook
    }

    with open(config_path, 'w') as configfile:
        config.write(configfile)
    return "Конфигурации успешно сохранены!"
