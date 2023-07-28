import wx
import subprocess
import wx.lib.agw.pygauge as PG
import pyautogui
import time
import pathlib
import os

#Создаем функцию, которая открывает Internet Explorer и делает скриншот области в определенной странице
def screen():
    pyautogui.FAILSAFE = False
    #Открыть браузер
    pyautogui.hotkey('win', 's')
    pyautogui.typewrite('Internet Explorer')
    pyautogui.press('enter')
    #Подсветить страничку
    time.sleep(0.5)
    #Закрыть приветственную страничку
    pyautogui.hotkey('ctrl', 'w')

    # Активация нужной вкладки
    window_title = "Орландо Блум (Orlando Bloom): фильмы, биография, семья, фильмография — Кинопоиск"
    pyautogui.getWindowsWithTitle(window_title)[0].activate()
    # Определение координат и размеров области для обрезки
    left = 0
    top = 0
    width = 910
    height = 950
    # Создание скриншота экрана и обрезка по указанным размерам
    screenshot = pyautogui.screenshot()
    cropped_screenshot = screenshot.crop((left, top, width, height))
    # Сохранение обрезанного скриншота в файл
    cropped_screenshot.save(os.path.abspath("Screen/screenshot.jpg"))
    # Свернуть окно Internet Explorer
    pyautogui.getWindowsWithTitle(window_title)[0].minimize()

#Создадим всплывающее окно
class MyFrame(wx.Frame):
    #Инициирование всплывающего окна
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="Resize This Window", size=wx.Size(520, 500))
        panel = wx.Panel(self, -1)
        bSizer = wx.BoxSizer(wx.VERTICAL)  # Changed to vertical sizer
        #Цвет фона
        self.SetBackgroundColour("white")

        # Создаем кноку "Распознать сотрудника"
        self.identifybutton = wx.Button(panel, label="Распознать сотрудника", size=(500, 100))
        self.identifybutton.Bind(wx.EVT_BUTTON, self.on_identify)
        # Задаем координаты кнопки
        bSizer.Add(self.identifybutton, 0, wx.TOP, 50)
        #Определяем и применяем шрифт
        font = wx.Font(34, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.identifybutton.SetFont(font)

        # Создаем кнопку "Завершить"
        self.notrecognizedbutton = wx.Button(panel, label="Завершить", size=(500, 100))
        self.notrecognizedbutton.Bind(wx.EVT_BUTTON, self.on_not_recognized)
        #Заадаем координаты кнопки
        bSizer.Add(self.notrecognizedbutton, 0, wx.TOP, 50)
        #Применяем шрифт
        self.notrecognizedbutton.SetFont(font)
        #Выводим панель и все элементы
        panel.Layout()
        panel.Show()
        panel.SetSizer(bSizer)
        self.Centre(wx.BOTH)

    #Определяем функции кнопки распознавания
    def on_identify(self, event):
        #Делаем скриншот
        screen()
        #Вызываем форму верификации
        subprocess.call(os.path.abspath("start_gallery_deepface.bat"), shell=True)

    #Определяем функции кнопки ошибки
    def on_not_recognized(self, event):
        #Закрываем кнопку
        self.Close()

#Вызываем всплывающее окно в постоянном потоке
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
