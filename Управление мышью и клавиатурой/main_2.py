from pynput import mouse

# Создаем свой класс обработки исключений
class MyExc (Exception): pass

def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        raise MyExc(f"{button} - error")

# Обрабатываем ошибки слушателя
with mouse.Listener(
        on_click = on_click) as listener:
    try:
        listener.join()
    except MyExc as err:
        print("=" * 50)
        print(err.args[0])
        print("=" * 50)