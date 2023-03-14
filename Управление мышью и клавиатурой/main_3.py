from pynput.keyboard import Key, Controller

keyboard = Controller()

# Нажимаем и отпускаем пробел
keyboard.press(Key.space)
keyboard.release(Key.space)

# Нажимаем и отпускаем А
keyboard.press("A")
keyboard.release("A")

# Нажимаем и отпускаем a
keyboard.press('a')
keyboard.release('a')

# Удерживаем shift и вводим 'a', затем отпускаем его
with keyboard.pressed(Key.shift):
    keyboard.press('a')
    keyboard.release('a')

#Вводим текст
keyboard.type('Hello world!')

