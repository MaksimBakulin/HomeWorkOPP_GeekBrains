from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js

import asyncio

chat_msgs = [] #глобальный список сообщений в чате
online_users = set() #сет, состоящий из онлайн-пользователей в чате

MAX_MESSAGES_COUNT = 100 #максимальное количество сохраняемых сообщений

async def main():
    global chat_msgs

    put_markdown("Добро пожаловать в чат!")

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя", validate=lambda n: "Такое имя уже используется!"
    if n in online_users or n == "AdminBot" else None)

    chat_msgs.append(("AdminBot", f"'{nickname}' присоединился к чату!"))
    msg_box.append(put_markdown(f"'{nickname}' присоединился к чату!"))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("Новое сообщение", [
            input(placeholder="Текст сообщения", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label':"Выйти из чата", 'type':'cancel'}])
        ], validate=lambda m:('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m["cmd"] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"'{nickname}': {data['msg']}"))
        chat_msgs.append((nickname, data['msg']))

    # exit chat
    refresh_task.close()

    online_users.remove(nickname)
    toast("Вы вышли из чата!")
    msg_box.append(put_markdown(f"AdminBot Пользователь '{nickname}' покинул чат!"))
    chat_msgs.append(('AdminBot', f"Пользователь '{nickname}' покинул чат!"))

    put_buttons(["Перезайти"], onclick=lambda btn: run_js('window.location.reload('))

async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:
                msg_box.append(put_markdown(f"'{m[0]}': {m[1]}"))

        # remove expired
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)

if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False) #запуск сервера
