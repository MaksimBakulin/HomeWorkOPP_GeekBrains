from pynput import keyboard

def on_activate_q():
    print("Обнаружена комбинация клавиш 'Ctrl+Alt+q'")

def on_activate_w():
    print("Обнаружена комбинация клавиш 'Ctrl+Alt+w'")

with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+q' : on_activate_q,
        '<ctrl>+<alt>+w' : on_activate_w}) as h:
    h.join()
