# tracing_ac
Трассировка автономных систем.

Вход: доменное имя или IP адрес. Пример: python tracing_as.py доменное_имя_или_ip

Выход: для каждого IP-адреса – вывести результат трассировки (или кусок результата до появления ***). Для "белых" IP-адресов из него указать номер автономной системы.

Осуществляется трассировка до указанного узла (например, с использованием tracert), т. е. мы узнаем IP адреса маршрутизаторов, через которые проходит пакет. Необходимо определить, к какой автономной системе относится каждый из полученных IP адресов маршрутизаторов. Для определения номеров автономных систем можно обращаться к базам данных региональных интернет регистраторов.
