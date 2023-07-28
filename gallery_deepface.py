# pip install deepface
from deepface import DeepFace
import pandas as pd
import pathlib
import os
import wx
import pandas as pd
from wx.lib.pubsub import pub
import wx.grid
import openpyxl
import numpy as np
from datetime import datetime

#Перечисляем возможные компоненты нейросети
#Модель
models = [
    "VGG-Face",  # Работает не очень
    "Facenet",  # Работает не очень
    "Facenet512",  # Работает отлично
    "OpenFace",  # Работает отвратительно
    "DeepFace",  # Не работает
    "DeepID",  # Не работает
    "ArcFace",  # Работает не очень
    "Dlib",  # Не работает
    "SFace",  # Удален репозиторий
]
#Метрика
metrics = ["cosine", "euclidean", "euclidean_l2"]
#Детекция лица
backends = [
    'opencv',
    'ssd',
    'dlib',
    'mtcnn',
    'retinaface',
    'mediapipe'
]

#Ищем скриншот в папке
folder_path = os.path.abspath('Screen/')
# Получаем список имен всех файлов в папке
files = os.listdir(folder_path)
# Фильтруем список, оставляя только файлы с расширением '.jpg'
image_files = [file for file in files if file.endswith('.jpg')][0]
#Компонуем нейросеть и делаем предсказание для скриншота
dfs = DeepFace.find(img_path=os.path.abspath("Screen/"+image_files),
# dfs = DeepFace.find(img_path="C:/Users/50AdmNsk/PycharmProjects/detection/train/ss/Moiseeva_Ekaterina_Dm_1.jpg",
                    db_path=os.path.abspath("base/"),
                    model_name=models[2], distance_metric=metrics[1], detector_backend=backends[1],
                    enforce_detection=False
                    )

dfs = dfs[0]

#Считываем пути к картинкам из базы
filenames = dfs['identity'].values
#Определяем имена из названий файлов
name = dfs['identity'].str.split("/").str.get(-1)
#Убираем лишнее из названий файлов
result = name.str.split('_').values
result = np.array([s[:-1] for s in result])
#Добавляем пробелы к элементам ФИО
result = np.char.add(result, " ")
#Если имя и отчество
if len(result[0]) == 2:
    #Формируем массив из Имен и отчеств
    result = result.flatten()
    result = np.array([np.char.add(result[i], result[i+1]) for i in range(0, len(result)-1, 2)])
#Если ФИО
elif len(result[0]) == 3:
    #Формируем массив из ФИО
    result = result.flatten()
    result = np.array([np.char.add(result[i], np.char.add(result[i+1], result[i+2])) for i in range(0, len(result) - 2, 3)])
#Находим самое частое ФИО
unique_elements, counts = np.unique(result, return_counts=True)
index = np.argmax(counts)
#Фиксируем его как мнение нейросети
result = unique_elements[index]
#Запоминаем текущие дату и время
current_date = datetime.now().date()
current_time = datetime.now().time()

#Создаем всплывающее окно детекции
class MyFrame(wx.Frame):
    #Определяем всплывающее окно
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="Resize This Window", size=wx.Size(950, 800))
        panel = wx.Panel(self, -1)
        bSizer = wx.BoxSizer(wx.VERTICAL)  # Changed to vertical sizer
        #Фон окна
        self.SetBackgroundColour("white")

        #Создаем кнопку "Подтверждаю"
        self.identifybutton = wx.Button(panel, label="Подтверждаю", size=(100, 20))
        self.identifybutton.Bind(wx.EVT_BUTTON, self.on_identify)
        #Задаем ее положение
        bSizer.Add(self.identifybutton, 0, wx.TOP, 10)

        #Создаем кнопку "Ошибка"
        self.notrecognizedbutton = wx.Button(panel, label="Ошибка", size=(100, 20))
        self.notrecognizedbutton.Bind(wx.EVT_BUTTON, self.on_not_recognized)
        #Опредедляем ее положение
        bSizer.Add(self.notrecognizedbutton, 0, wx.TOP, 10)

        #Выводим фразу о мнении нейросети
        self.m_staticText1 = wx.StaticText(panel, wx.ID_ANY, "Мнение нейросети: "+result)
        #Задаем координаты и размер фразы
        self.m_staticText1.SetPosition((110, 10))
        self.m_staticText1.SetSize((500, 30))

        #Определяем ширину линий вывода изображений (4 фото в ряд)
        h = 300
        gridSizer = wx.GridSizer(0, 4, 10, 10)
        #Перебираем все предсказания нейросети
        for i in range(len(filenames)):
            #Считываем изображение
            image = wx.Image(filenames[i], wx.BITMAP_TYPE_ANY)
            #Обрезаем изображение
            image = image.Scale(200, h)
            #Переводим изображение в битовый формат
            bitmap = wx.Bitmap(image)
            #Выводим изображение в виде кнопки
            bitmapButton = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bitmap, pos=(10, 10))
            #Выводим ФИО к картинке
            label = wx.StaticText(panel, id=wx.ID_ANY, label=name[i])
            #Формируем линию
            vbox = wx.BoxSizer(wx.VERTICAL)
            #Выводим кнопки
            vbox.Add(label, 0, wx.ALIGN_CENTER, 10)
            vbox.Add(bitmapButton, 0, wx.ALIGN_CENTER, 10)
            #Меняем размеры в зависимости от ширины окна
            gridSizer.Add(vbox, 0, wx.EXPAND, 10)

        #Отрисовываем все элементы
        bSizer.Add(gridSizer, 1, wx.ALL, 10)
        panel.Layout()
        panel.Show()
        panel.SetSizer(bSizer)
        self.Centre(wx.BOTH)
        panel.SetSizerAndFit(bSizer)

    #Создаем функции для кнопки "Подтверждаю"
    def on_identify(self, event):
        #Открываем базу
        wb = openpyxl.load_workbook('filename.xlsx')
        ws = wb.active
        #Записываем в базу ФИО, дату и время
        ws.append([result, current_date, current_time])
        #Сохраняем базу
        wb.save('filename.xlsx')
        #Закрываем всплывающее окно
        self.Close()

    #Создаем функции для кнопки "Ошибка"
    def on_not_recognized(self, event):
        #Закрывем всплывающее окно
        self.Close()

#Вызываем всплывающее окно в постоянном потоке
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()