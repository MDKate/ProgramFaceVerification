
# pip install deepface
from deepface import DeepFace
import pandas as pd


models = [
  "VGG-Face", #Работает не очень
  "Facenet", #Работает не очень
  "Facenet512", #Работает отлично
  "OpenFace", #Работает отвратительно
  "DeepFace", #Не работает
  "DeepID", #Не работает
  "ArcFace", #Работает не очень
  "Dlib", #Не работает
  "SFace", #Удален репозиторий
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

dfs = DeepFace.find(img_path = "C:/Users/50AdmNsk/PycharmProjects/detection/train/ss/Ilia_08.jpg",
      db_path = "C:/Users/50AdmNsk/PycharmProjects/detection/train/",
      model_name = models[2], distance_metric = metrics[1], detector_backend = backends[1], enforce_detection=False
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

# print(dfs)
#
# class MyPanel(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#
#         pub.subscribe(self.update_data, 'update_data')
#
#         self.data_table = dfs
#
#         self.grid = wx.grid.Grid(self, -1)
#
#         self.update_grid()
#
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.grid, 1, wx.EXPAND)
#         self.SetSizer(sizer)
#
#     def update_data(self, data):
#         self.data_table = data
#         self.update_grid()
#
#     def update_grid(self):
#         self.grid.ClearGrid()
#
#         self.grid.CreateGrid(len(self.data_table), len(self.data_table.columns))
#
#         for i, column_name in enumerate(self.data_table.columns):
#             self.grid.SetColLabelValue(i, column_name)
#
#         for i, row in self.data_table.iterrows():
#             for j, value in enumerate(row):
#                 self.grid.SetCellValue(i, j, str(value))
#
#         self.grid.AutoSizeColumns()
#
#
# class MyFrame(wx.Frame):
#     def __init__(self, parent, title):
#         wx.Frame.__init__(self, parent, title=title, size=(1500, 300))
#
#         self.panel = MyPanel(self)
#
#         self.Show()
#
#
# if __name__ == '__main__':
#     app = wx.App(redirect=False)
#     frame = MyFrame(None, 'DataFrame')
#     app.MainLoop()

filenames = dfs['identity'].values
name = dfs['identity'].str.split("/").str.get(-1)

class MyFrame( wx.Frame ):
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="Resize This Window", size=wx.Size(1050,500))
        panel = wx.Panel(self, -1)

        bSizer=wx.BoxSizer(wx.HORIZONTAL)
        h = 0
        for i in range(len(filenames)):
            self.img1=wx.Image(filenames[i], wx.BITMAP_TYPE_JPEG)
            # self.img2=wx.Image(filenames[1], wx.BITMAP_TYPE_JPEG)
            self.img1=self.img1.Scale(300, 300)
            self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.img1))
            # self.m_bitmap2 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.img2))

            self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, name[i])
            # self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, name[1])

            self.m_staticText1.SetPosition((h, 10))
            self.m_staticText1.SetSize((200, 50))
            h += 300
            # self.m_staticText2.SetPosition((500, 750))
            # self.m_staticText2.SetSize((200, 50))

            bSizer.Add(self.m_bitmap1, 0, wx.EXPAND|wx.ALL, 0)
            # bSizer.Add(self.m_bitmap2, 0, wx.EXPAND|wx.ALL, 0)

            # self.Bind(wx.EVT_SIZE, self.onResize)
            self.Show()
            self.SetSizer(bSizer)
            self.Layout()
            self.Centre(wx.BOTH)


    def OnClick(self, event):
        self.Destroy()


if __name__ == '__main__':
        app = wx.App()
        frame = MyFrame()
        frame.Show()
        app.MainLoop()