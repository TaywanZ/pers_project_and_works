import configparser
from pathlib import Path
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Admin:
    admin_id: list
    admin_name: list
    active_admin: int


@dataclass
class Booking:
    username: str
    password: str


def load_config(flag):
    """
    This function read config file 'config.ini'
    and returns parameters.
    :param flag: 0-2, determines which parameters to return/
    :return: parameters
    """
    config = configparser.ConfigParser()
    path = Path(Path.cwd(), 'config.ini')
    config.read(path)

    if flag == 0:
        tg_bot = config['t_bot']
        return (TgBot(
            token=tg_bot['token']))
    elif flag == 1:
        tg_bot = config['admin']
        return (Admin(
                admin_name=tg_bot['admin_name'].split(','),
                admin_id=tg_bot['admin_id'].split(','),
                active_admin=int(tg_bot['active_admin'])))
    elif flag == 2:
        tg_bot = config['booking']
        return (Booking(
                username=tg_bot['username'],
                password=tg_bot['password']))




def write_config(value):
    """
    Функция правки конфига, применяется для изменения "active_admin"
    :param value: позиция id админа, которого надо сделать активным
    :return: bool
    """
    config = configparser.ConfigParser()
    path = Path(Path.cwd(), 'config.ini')
    print(path)
    config.read(path)
    try:
        config.set('admin', 'active_admin', str(value))
        print(config)
        with open(path, "w") as config_file:
            config.write(config_file)
        return True
    except Exception as exp:
        print(exp)
        return False



