# pip install deepface
from deepface import DeepFace
import pandas as pd
import pathlib
import os

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
metrics = ["cosine", "euclidean", "euclidean_l2"]
backends = [
    'opencv',
    'ssd',
    'dlib',
    'mtcnn',
    'retinaface',
    'mediapipe'
]

# result = DeepFace.verify(img1_path = "C:/Users/50AdmNsk/PycharmProjects/detection/train/ss/t_08.jpg",
#                          img2_path = "C:/Users/50AdmNsk/PycharmProjects/detection/train/ss/t_18.jpg",
#                          model_name = models[6], distance_metric = metrics[2], detector_backend = backends[1])


# print(result.get('verified'))

dfs = DeepFace.find(img_path="C:/Users/50AdmNsk/PycharmProjects/detection/train/ss/Moiseeva_Ekaterina_Dm_1.jpg",
                    db_path=os.path.abspath("base/"),
                    model_name=models[2], distance_metric=metrics[1], detector_backend=backends[1],
                    enforce_detection=False
                    )
# 
# dfs
# 

dfs = dfs[0]

# dfs.to_excel('C:/Users/50AdmNsk/PycharmProjects/detection/data.txt')
# import  wx
#
# app = wx.App(redirect=True)
# top = wx.Frame(None, title="Hello World", size=(300, 200))
# top.Show()
# app.MainLoop()

import wx
import pandas as pd
from wx.lib.pubsub import pub
import wx.grid
import openpyxl
import numpy as np

filenames = dfs['identity'].values
name = dfs['identity'].str.split("/").str.get(-1)
# result = np.char.split(name.values, '_')
result = name.str.split('_').values
result = np.array([s[:-1] for s in result])
result = np.char.add(result, " ")
if len(result[0]) == 2:
    result = result.flatten()
    result = np.array([np.char.add(result[i], result[i+1]) for i in range(0, len(result)-1, 2)])
elif len(result[0]) == 3:
    result = result.flatten()
    result = np.array([np.char.add(result[i], np.char.add(result[i+1], result[i+2])) for i in range(0, len(result) - 2, 3)])
# print(result)
unique_elements, counts = np.unique(result, return_counts=True)
index = np.argmax(counts)
result = unique_elements[index]
from datetime import datetime

current_date = datetime.now().date()
current_time = datetime.now().time()

# class MyFrame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, id=wx.ID_ANY, title="Resize This Window", size=wx.Size(1500, 700))
#         panel = wx.Panel(self, -1)
#         bSizer = wx.BoxSizer(wx.HORIZONTAL)
#         self.SetBackgroundColour("white")
#
#         # Add "Identify" button
#         self.identify_button = wx.Button(panel, label="Подтверждаю", size=(100, 20))
#         self.identify_button.Bind(wx.EVT_BUTTON, self.on_identify)
#         bSizer.Add(self.identify_button, 0, wx.TOP, 50)
#         # Add "Not Recognized" button
#         self.not_recognized_button = wx.Button(panel, label="Ошибка", size=(100, 20))
#         self.not_recognized_button.Bind(wx.EVT_BUTTON, self.on_not_recognized)
#         bSizer.Add(self.not_recognized_button, 0, wx.TOP, 50)
#
#         h = 300
#         for i in range(len(filenames)):
#             self.img1 = wx.Image(filenames[i], wx.BITMAP_TYPE_JPEG)
#             self.img1 = self.img1.Scale(300, 300)
#             self.m_bitmap1 = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(self.img1))
#             self.m_staticText1 = wx.StaticText(panel, wx.ID_ANY, name[i])
#             bSizer.Add(self.m_bitmap1, 0, wx.TOP, 50)
#             self.m_staticText1.SetPosition((h, 10))
#             self.m_staticText1.SetSize((200, 30))
#             h += 300
#
#         # wx.ScrolledWindow(panel, id=-1, pos=wx.DefaultPosition, size = wx.DefaultSize, style = wx.HSCROLL | wx.VSCROLL)
#         panel.Layout()
#         panel.Show()
#         self.Centre(wx.BOTH)
#         panel.SetSizerAndFit(bSizer)
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="Resize This Window", size=wx.Size(950, 800))
        panel = wx.Panel(self, -1)
        bSizer = wx.BoxSizer(wx.VERTICAL)  # Changed to vertical sizer
        self.SetBackgroundColour("white")

        # Add "Identify" button
        self.identifybutton = wx.Button(panel, label="Подтверждаю", size=(100, 20))
        self.identifybutton.Bind(wx.EVT_BUTTON, self.on_identify)
        bSizer.Add(self.identifybutton, 0, wx.TOP, 10)

        # Add "Not Recognized" button
        self.notrecognizedbutton = wx.Button(panel, label="Ошибка", size=(100, 20))
        self.notrecognizedbutton.Bind(wx.EVT_BUTTON, self.on_not_recognized)
        bSizer.Add(self.notrecognizedbutton, 0, wx.TOP, 10)

        self.m_staticText1 = wx.StaticText(panel, wx.ID_ANY, "Мнение нейросети: "+result)
        self.m_staticText1.SetPosition((110, 10))
        self.m_staticText1.SetSize((500, 30))

        h = 300
        gridSizer = wx.GridSizer(0, 4, 10, 10)
        for i in range(len(filenames)):
            image = wx.Image(filenames[i], wx.BITMAP_TYPE_ANY)
            image = image.Scale(200, h)
            bitmap = wx.Bitmap(image)
            bitmapButton = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bitmap, pos=(10, 10))

            # Add the image name as label above the bitmapButton
            label = wx.StaticText(panel, id=wx.ID_ANY, label=name[i])

            # Create sizer for each row
            vbox = wx.BoxSizer(wx.VERTICAL)

            # Add label above bitmapButton to vbox
            vbox.Add(label, 0, wx.ALIGN_CENTER, 10)
            vbox.Add(bitmapButton, 0, wx.ALIGN_CENTER, 10)

            # Add vbox to grid sizer
            gridSizer.Add(vbox, 0, wx.EXPAND, 10)


        bSizer.Add(gridSizer, 1, wx.ALL, 10)  # Add grid sizer to the main sizer
        panel.Layout()
        panel.Show()
        panel.SetSizer(bSizer)
        self.Centre(wx.BOTH)
        panel.SetSizerAndFit(bSizer)

    def on_identify(self, event):
        # Append "1" to the excel file
        wb = openpyxl.load_workbook('filename.xlsx')
        ws = wb.active
        ws.append([result, current_date, current_time])
        wb.save('filename.xlsx')
        self.Close()
    def on_not_recognized(self, event):
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()