from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import Projeto


class CameraClick(BoxLayout):
    min = 0
    max = 255
    minY = 0
    minCr = 60
    minCb = 100
    maxY = 245
    maxCr = 175
    maxCb = 135

    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.atualizaImagem,
                                1.0 / 30.0)

    def bufferiza(self, frame, color):
        buf1 = cv2.flip(frame, 0)  # inverte para não ficar de cabeça para baixo
        buf = buf1.tostring()  # converte em textura

        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt=color)
        texture1.blit_buffer(buf, colorfmt=color, bufferfmt='ubyte')
        return texture1

    def atualizaImagem(self, dt):
        ret, frame = self.capture.read()  # captura uma imagem da camera
        piso = np.array([self.ids['minY'].value, self.ids['minCr'].value, self.ids['minCb'].value], dtype=np.uint8)
        teto = np.array([self.ids['maxY'].value, self.ids['maxCr'].value, self.ids['maxCb'].value], dtype=np.uint8)
        # frame2 = Projeto.tentativa2(frame, piso, teto)

        frame2 = Projeto.tentativa3(frame)

        texture1 = self.bufferiza(frame, 'bgr')
        texture2 = self.bufferiza(frame2, 'luminance')

        self.ids['cam1'].texture = texture1  # apresenta a imagem
        self.ids['cam2'].texture = texture2  # apresenta a imagem


class CameraApp(App):

    def build(self):
        return CameraClick()


CameraApp().run()
