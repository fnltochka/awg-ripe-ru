# awg-ripe-ru: Генератор Российских IP-адресов для [Amnezia VPN](https://github.com/amnezia-vpn)

## Описание
awg-ripe-ru - это Python-скрипт, который генерирует список Российских IP-адресов для использования в [Amnezia VPN](https://github.com/amnezia-vpn). Он использует данные от [RIPE NCC](https://stat.ripe.net) для получения списка IPv4-адресов, связанных с Россией.

## Установка
Для работы скрипта требуется Python 3.6 или выше. Также требуются следующие библиотеки:
- requests
- requests_cache
- netaddr
- rich

Вы можете установить их с помощью pip:
```bash
pip install -r requirements.txt
```

## Использование
Для запуска скрипта просто выполните команду:
```bash
python main.py
```
Скрипт сгенерирует файлы со списками IP-адресов с различными уровнями маски подсети.

## Файлы
- `runet.json`: Список всех IP-адресов.
- `runet_reduced.json`: Список IP-адресов с уменьшенной маской подсети.
- `runet_reduced_16.json`: Список IP-адресов с маской подсети /16.
- `runet_reduced_8.json`: Список IP-адресов с маской подсети /8.

## Примечание
Этот скрипт предназначен только для образовательных целей. Используйте его на свой страх и риск.
