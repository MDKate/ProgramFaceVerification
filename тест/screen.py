import time
import pyautogui

def screen():
    pyautogui.FAILSAFE = False

    pyautogui.hotkey('win', 's')
    pyautogui.typewrite('Internet Explorer')
    pyautogui.press('enter')
    # time.sleep(2)
    # Подождать 2 секунды для плавного открытия окна
    # Активация окна Internet Explorer
    window_title = "Орландо Блум (Orlando Bloom): фильмы, биография, семья, фильмография — Кинопоиск"
    pyautogui.getWindowsWithTitle(window_title)[0].activate()

    # time.sleep(2)  # Подождать 1 секунду для плавного переключения окна

    # Определение координат и размеров области для обрезки
    left = 0
    top = 0
    width = 910
    height = 950

    # Создание скриншота экрана и обрезка по указанным размерам
    screenshot = pyautogui.screenshot()
    cropped_screenshot = screenshot.crop((left, top, width, height))

    # Сохранение обрезанного скриншота в файл
    cropped_screenshot.save("C:/Users/50AdmNsk/PycharmProjects/detection/Screen/screenshot.png")

    # Свернуть окно Internet Explorer
    pyautogui.getWindowsWithTitle(window_title)[0].minimize()