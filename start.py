import wx
import subprocess
import wx.lib.agw.pygauge as PG
import pyautogui
import time
import pathlib
import os
# class ProgressDialog(wx.Dialog):
#     def __init__(self, parent):
#         wx.Dialog.__init__(self, parent, title="Окно с баром загрузки", size=(300, 200))
#
#         panel = wx.Panel(self)
#         # bSizer = wx.BoxSizer(wx.VERTICAL)
#         # Создаем бар загрузки
#         self.gauge = wx.Gauge(panel, range=10)
#
#         # Создаем таймер для обновления бара загрузки
#         self.timer = wx.Timer(self)
#         self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
#         self.count = 0
#
#         # Размещаем элементы на панели
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.gauge, 0, wx.EXPAND | wx.ALL, 20)
#         panel.SetSizer(sizer)
#
#         # Устанавливаем размеры окна
#         self.SetSize(300, 200)
#
#         # Запускаем таймер
#         self.timer.Start(500)
#         panel.Layout()
#         panel.Show()
#         self.Centre(wx.BOTH)
#         # panel.SetSizer(bSizer)
#
#
#     def on_timer(self, event):
#         # Обновляем значение бара загрузки
#         self.count += 1
#         if self.count > 10:
#             self.count = 0
#         self.gauge.SetValue(self.count)
#         self.Close()
def screen():
    pyautogui.FAILSAFE = False
    pyautogui.hotkey('win', 's')
    pyautogui.typewrite('Internet Explorer')
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'w')

    # Активация окна Internet Explorer
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
    cropped_screenshot.save(os.path.abspath("Screen/screenshot.png"))
    # Свернуть окно Internet Explorer
    pyautogui.getWindowsWithTitle(window_title)[0].minimize()

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="Resize This Window", size=wx.Size(520, 500))
        panel = wx.Panel(self, -1)
        bSizer = wx.BoxSizer(wx.VERTICAL)  # Changed to vertical sizer
        self.SetBackgroundColour("white")

        # Add "Identify" button
        self.identifybutton = wx.Button(panel, label="Распознать сотрудника", size=(500, 100))
        self.identifybutton.Bind(wx.EVT_BUTTON, self.on_identify)
        bSizer.Add(self.identifybutton, 0, wx.TOP, 50)
        font = wx.Font(34, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.identifybutton.SetFont(font)

        # Add "Not Recognized" button
        self.notrecognizedbutton = wx.Button(panel, label="Завершить", size=(500, 100))
        self.notrecognizedbutton.Bind(wx.EVT_BUTTON, self.on_not_recognized)
        bSizer.Add(self.notrecognizedbutton, 0, wx.TOP, 50)
        self.notrecognizedbutton.SetFont(font)

        panel.Layout()
        panel.Show()
        panel.SetSizer(bSizer)
        self.Centre(wx.BOTH)
        # panel.SetSizerAndFit(bSizer)


    def on_identify(self, event):
        screen()
        subprocess.call(os.path.abspath("start_gallery_deepface.bat"), shell=True)

    def on_not_recognized(self, event):
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()