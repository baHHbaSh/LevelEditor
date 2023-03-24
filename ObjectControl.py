from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Rectangle, PopMatrix, Rotate, PushMatrix
from kivy.core.window import Window
from kivy.uix.image import Image
class Sprite(Image):#Класс картинки c вращениem
	def __init__(self, Name="None", size = [100,100], source = "None", rotate = 0, **kwargs ):
		super(Sprite, self).__init__( **kwargs )
		with self.canvas.before:
			PushMatrix()
			self.rot = Rotate()
			self.rot.angle  = rotate
			self.rot.origin = self.center
			self.rot.axis = (0, 0, 1)
		with self.canvas.after:
			PopMatrix()
		self.size_hint = (None, None)# tell the layout not to size me
		self.source = source
		self.size = size
		self.rot.origin= self.center # Reset the center of the Rotate canvas instruction
		self.Name = Name

	def RotateOrigin(self):
		self.rot.origin = self.pos[0]+self.size[0]/2, self.pos[1] + self.size[1]/2

	@property
	def rotate(self):
		return self.rot.angle
	@rotate.setter
	def rotate(self, value):
		self.RotateOrigin()
		self.rot.angle = value
	@property
	def X(self):
		return self.pos[0]
	@X.setter
	def X(self, value):
		self.pos[0] += value

	@property
	def Y(self):
		return self.pos[1]
	@Y.setter
	def Y(self, value):
		self.pos[1] += value
	
	@property
	def Width(self):
		return self.size[0]
	@Width.setter
	def Width(self, value):
		self.size[0] += value
	
	@property
	def Height(self):
		return self.size[1]
	@Height.setter
	def Height(self, value):
		self.size[1] += value
	
	@property
	def Image(self):
		return self.source
	@Image.setter
	def Image(self, value):
		self.source = value
	
def txt_to_texture(text = "text", font = 30, color = (1,1,1,1)) -> tuple:
	#Возващает [0] = texture; [1] = texture_size
	mylbl = CoreLabel(text = text, font_size = font, color = color)
	mylbl.refresh()
	return mylbl.texture, list(mylbl.texture.size)
class pr:
	def __init__(self):#Суём "глобальные" переменные
		self.game = False
		self.prop = Window.width, Window.height
class coliders:
	#Этот отрывок кода тебя ебать не должен!
	def __init__(self, x,y,width,height, Name):
		self.pos = x,y
		size = width, height
		self.rsize = (width,height)
		self.WinSize = (Window.size[0],Window.size[1])
		self.size = [int(size[0] * (self.WinSize[0]) / 1280), int(size[1] * (self.WinSize[1] / 720))]
		self.Name = Name
		Color(1,1,1,.3)
		self.obj = Rectangle(pos=self.pos, size=self.size)
	def GetRectAngle(self):
		return self.obj
	def Touch(self, obj):
		return is_touching(self, obj)
	def UpdateVisual(self):
		self.obj.pos=self.pos
		self.obj.size=self.size
	@property
	def ScreenPos(self):
		pos = []
		try:
			pos[0] = self.WinSize[0] / self.pos[0] * 2 - 1
		except ZeroDivisionError:
			pos[0] = -1
		try:
			pos[0] = self.WinSize[1] / self.pos[1] * 2 - 1
		except ZeroDivisionError:
			pos[1] = -1
		return pos
	@ScreenPos.setter
	def ScreenPos(self, value:tuple):
		self.pos[0] = self.WinSize[0] / value[0] + 1 / 2
		self.pos[1] = self.WinSize[1] / value[1] + 1 / 2
		self.UpdateVisual()
	
	@property
	def ScreenX(self):
		try:
			return self.WinSize[0] / self.pos[0] * 2 - 1
		except ZeroDivisionError:
			return -1
	@ScreenX.setter
	def ScreenX(self, value):
		self.pos[0] = self.WinSize[0] / value[0] + 1 / 2
		self.UpdateVisual()
	
	@property
	def ScreenY(self):
		try:
			return self.WinSize[1] / self.pos[1] * 2 - 1
			self.UpdateVisual()
		except ZeroDivisionError:
			return -1
	@ScreenY.setter
	def ScreenY(self, value):
		self.pos[1] = self.WinSize[1] / value[1] + 1 / 2
		self.UpdateVisual()
	@property
	def x(self):
		return self.pos[0]
	@x.setter
	def x(self, value):
		self.pos[0] += value
		self.UpdateVisual()

	@property
	def y(self):
		return self.pos[1]
	@y.setter
	def y(self, value):
		self.pos[1] += value
		self.UpdateVisual()
	
	@property
	def Width(self):
		return self.size[0]
	@Width.setter
	def Width(self, value):
		self.size[0] += value
		self.UpdateVisual()
	
	@property
	def Height(self):
		return self.size[1]
	@Height.setter
	def Height(self, value):
		self.size[1] += value
		self.UpdateVisual()
def physic_engine(a, b_returning, last_position):
	#Этот отрывок кода тебя ебать не должен!
	if not is_touching(a, b_returning): return None
	b_l=b_returning.pos[0]
	b_r=b_returning.pos[0] + b_returning.size[0]
	b_b=b_returning.pos[1]
	b_t=b_returning.pos[1] + b_returning.size[1]
	result=[]
	width= b_returning.pos[0] - b_returning.pos[0] + b_returning.size[0]
	height=b_returning.pos[1] - b_returning.pos[1] + b_returning.size[1]
	x=b_returning.pos[0]
	y=b_returning.pos[1]
	t = coliders(x=x,y=b_t,width=width,height=1)
	b = coliders(x=x,y=b_b,width=width,height=1)
	r = coliders(x=b_r,y=y+1,width=1,height=height-2)
	l = coliders(x=b_l,y=y+1,width=1,height=height-2)
	sp = list(last_position)
	while is_touching(a, b_returning):
		if is_touching(a, l): sp[0] = last_position[0] - 1; a.pos=tuple(sp)
		if is_touching(a, r): sp[0] = last_position[0] + 1; a.pos=tuple(sp)
		if is_touching(a, t): sp[1] = last_position[1] + 1; a.pos=tuple(sp)
		if is_touching(a, b): sp[1] = last_position[1] - 1; a.pos=tuple(sp)
	if last_position == sp: return False
	return True
def is_touching(a, b):
	a_l=a.pos[0]
	a_r=a.pos[0] + a.size[0]
	a_b=a.pos[1]
	a_t=a.pos[1] + a.size[1]
	try:
		a.rotate = a.rotate % 360
		if 45 < a.rotate < 135:
			a_t, a_l, a_b, a_r = a_l, a_b, a_r, a_t
		elif 135 < a.rotate < 225:
			a_t, a_b, a_r, a_l = a_b, a_t, a_l, a_r
		elif 225 < a.rotate < 315:
			a_t, a_r, a_b, a_l = a_r, a_b, a_l, a_t
	except:pass
	b_l=b.pos[0]
	b_r=b.pos[0] + b.size[0]
	b_b=b.pos[1]
	b_t=b.pos[1] + b.size[1]
	try:
		b.rotate = b.rotate % 360
		if 45 < b.rotate < 135:
			b_t, b_l, b_b, b_r = b_l, b_b, b_r, b_t
		elif 135 < b.rotate < 225:
			b_t, b_b, b_r, b_l = b_b, b_t, b_l, b_r
		elif 225 < b.rotate < 315:
			b_t, b_r, b_b, b_l = b_r, b_b, b_l, b_t
	except:pass
	if a_l >= b_r or a_r <= b_l or a_t <= b_b or a_b >= b_t: return False
	return True
def camera_move(a,objs):#Фокусит камеру на игроке
	prop = Window.width, Window.height
	d = a.pos[0] * -1 + prop[0]/2 - a.size[0]/2, a.pos[1] * -1 + prop[1]/2 - a.size[1]/2
	for i in objs:
		i = objs[i]
		c = [i.pos[0] + d[0], i.pos[1] + d[1]]
		i.pos = c