# Python Console Chat

Мой первый сетевой проект на чистом Python! Простой консольный чат для общения по локалке или через Radmin VP Написан без тяжелых фреймворков и асинхронщины — только ванильный `socket` для сети и низкоуровневый `msvcrt` для нормального ввода текста без зависаний.

## Что внутри
В репозитории есть две версии:
- **Plain Chat** — базовая версия, где сообщения летают в открытом виде.
- **Encrypted Chat** — версия с симметричным шифрованием (**Fernet / AES**), чтобы трафик нельзя было просто так прочитать.

## Как запустить (версия с шифрованием)

1. Устанавливаем библиотеку для криптографии:
   ```bash
   pip install cryptography

2 Запуск сервера на одном ПК
python HostServerEncrypted.py

3. Запуск клиента(если тест на одном ПК — оставляем 127.0.0.1, если через Radmin — меняем на IP хоста)
python ClientEncrypted.py


СДЕЛАНО СВОИМИ РУЧКМИ <3




My first network project in pure Python! A simple console chat for communication over a local network or via Radmin VPN. Written without heavy frameworks or async libraries — just vanilla socket for networking and low-level msvcrt for normal text input without freezing.
What's Inside

The repository contains two versions:

    Plain Chat — a basic version where messages are sent in plaintext.

    Encrypted Chat — a version with symmetric encryption (Fernet / AES) so that traffic cannot be easily read.

How to Run (Encrypted Version)

    Install the cryptography library:
    pip install cryptography

    Run the server on one PC:
    python HostServerEncrypted.py

    Run the client (if testing on one PC, keep 127.0.0.1; if via Radmin, change it to the host IP):
    python ClientEncrypted.py

MADE BY MYSELF <3