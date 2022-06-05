import re
import subprocess
from json import loads
from urllib import request
import argparse

ip_regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

answers = {
    'ii': 'Не удается разрешить системное имя узла.\n',
    'tr': 'Трассировка маршрута',
    'hu': 'Заданный узел недоступен.\n',
    'tc': 'Трассировка finished.\n',
    'mh': 'с максимальным числом прыжков'
}


class ASResponse:
    """
    Translate: отклик от автономной системы. Класс необходим
    для грамотной выдачи необходимой по заданию полей.
    """

    def __init__(self, json: dict):
        self._json = json
        self._parse()

    def _parse(self):
        """
        Парсер json-файла
        """
        self.ip = self._json.get('ip') or '--'
        self.city = self._json.get('city') or '--'
        self.hostname = self._json.get('hostname') or '--'
        self.country = self._json.get('country') or '--'
        org = self._json.get('org')
        self.AS = '--' if org is None else org.split()[0]
        self.provider = '--' if org is None else ' '.join(org.split()[1:])


class Output:
    """
    Красивая табличка результатов трассировки
    """
    _IP_LEN = 15
    _AS_LEN = 6
    _COUNTRY_CITY_LEN = 20

    def __init__(self):
        self._number = 1

    def print(self, ip: str, a_s: str, country: str, city: str, provider: str):
        if self._number == 1:
            self._print_header()
        string = f'{self._number}' + ' ' * (3 - len(str(self._number)))
        string += ip + self._spaces(self._IP_LEN, len(ip))
        string += a_s + self._spaces(self._AS_LEN, len(a_s))
        country_city = f'{country}/{city}'
        string += country_city + self._spaces(self._COUNTRY_CITY_LEN, len(country_city))
        string += provider
        self._number += 1
        print(string)

    @staticmethod
    def _print_header():
        """
        Заголовки таблицы.
        """
        print('№  IP' + ' ' * 16 + 'AS' + ' ' * 7 + 'Country/City' + ' ' * 11 + 'Provider')

    @staticmethod
    def _spaces(expected: int, actual: int) -> str:
        return ' ' * (3 + (expected - actual))


def get_as_number_by_ip(ip) -> ASResponse:
    """
    По полученному ip-адресу вернуть объект отклика.
    """
    return ASResponse(loads(request.urlopen('https://ipinfo.io/' + ip + '/json').read()))


def get_route(address: str):
    """
    функция получения пути следования пакета от нас до цели.
    """
    traceroute = subprocess.Popen(['tracert', address], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    get_as = False
    output = Output()
    for line in iter(traceroute.stdout.readline, ""):
        line = line.decode(encoding='cp866')
        if line.find(answers['ii']) != -1:
            print(line)
            break
        elif line.find(answers['tr']) != -1:
            print(line, end='')
            ending = ip_regex.findall(line)[0]
        elif line.find(answers['mh']) != -1:
            get_as = True
        elif line.find(answers['hu']) != -1:
            print(line.removeprefix(' '))
            break
        elif line.find(answers['tc']) != -1:
            print(line)
            break

        try:
            ip = ip_regex.findall(line)[0]
        except IndexError:
            continue

        if get_as:
            response = get_as_number_by_ip(ip)
            output.print(response.ip, response.AS, response.country, response.city, response.provider)
            if ip == ending:
                print(answers['tc'])
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('address', type=str)
    get_route(parser.parse_args().address)