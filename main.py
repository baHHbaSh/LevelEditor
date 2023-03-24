"""
export code
повторяющиеся имена44
"""
from traceback import format_exc
from kivy.config import Config;
Config.set("graphics", "show_cursor", "1");
Config.set('kivy', 'exit_on_escape', '0');
try:
	Config.set('input', 'mouse', 'mouse,multitouch_on_demand');
	from win32api import GetSystemMetrics;
	Config.set('graphics', 'width',  GetSystemMetrics(0));
	Config.set('graphics', 'height', GetSystemMetrics(1));
	Config.set("graphics", "fullscreen", 1)
except:print(format_exc())
from kivy.app import App;
from kivy.animation import Animation, AnimationTransition;
from kivy.uix.popup import Popup;
from kivy.uix.widget import Widget;
from kivy.uix.gridlayout import GridLayout;
from kivy.uix.button import Button as KButton;
from kivy.uix.label import Label;
from kivy.uix.scatter import Scatter;
from kivy.uix.checkbox import CheckBox;
from kivy.uix.textinput import TextInput;
from kivy.uix.screenmanager import*;
from kivy.uix.carousel import Carousel;
from kivy.uix.filechooser import FileChooserIconView;
from kivy.uix.colorpicker import ColorPicker;
from kivy.clock import Clock;
from random import randint;
import json
from ObjectControl import*;
Window.clearcolor = .333, .3, .5, 1

temp_files = {}
try:
	with open("tmpf", "r", encoding="utf-8") as file:
		temp_files = json.load(file)
except:
	with open("tmpf", "w", encoding="utf-8") as file:
		json.dump(temp_files,file)

Frame = []

try:
	with open("frames", "r", encoding="utf-8") as file:
		Frame = json.load(file)
except:
	with open("frames", "w", encoding="utf-8") as file:
		json.dump(Frame, file)

def printpath(*_):
	print(Explorer.path, Explorer.selection)

Explorer = FileChooserIconView()
Explorer.filters = ["*.kivyedit"]
Explorer.multiselect = False

PathExplorer = FileChooserIconView()
PathExplorer.filters = ["*.kivyedit"]
PathExplorer.multiselect = False

class Button(KButton):
	def __init__(self, **kw) -> None:
		color_txt = (.3, .35, 1, 1);
		color_bg  = (.35,.3,.7, 1);
		super(Button, self).__init__(color = color_txt, background_color = color_bg, **kw)

class KivyEditor(App):
	def build(self):
		self.screens = [MainScreen("main"), LevelsScreen("edit")]
		self.scmanager = ScreenManager(transition=NoTransition())
		for screen in self.screens:
			self.scmanager.add_widget(screen)
		self.title = "Level editor by The_EnG1nE"
		self.icon = "icon.ico"
		return self.scmanager
	def AddScreen(self, MScreen:Screen):
		self.scmanager.add_widget(MScreen)
		self.screens.append(Screen)
	def DelScreen(self, Screen):
		self.screens.pop(self.screens.index(Screen))
		self.scmanager.remove_widget(Screen)
	def open_settings(self, *_): pass

app = KivyEditor()

KeyboardMap = {}

class MainScreen(Screen):
	#Menu
	def __init__(self, name="Menu"):
		super(MainScreen, self).__init__(name=name)
		Window.bind(on_keyboard=self.Android_back_click);
		lay =		   GridLayout(rows = 4, padding = 200)
		but_start =	 Button(text ="[color=FF4157]К сценам[/color]",font_size = 50, markup = True)
		self.but_quit = Button(text ="[color=FF4157]Свалить из Саратова[/color]",font_size = 50, markup = True)
		lay.add_widget(Label(text ="[color=FFEE00]Kivy[/color][color=F4CA16]Editor[/color]",font_size = 80, markup = True))
		
		#Техническая хуета
		lay.add_widget(but_start)
		but_start.on_release =self.start_game
		lay.add_widget(self.but_quit)

		self.but_quit.on_release = self.quiting
		self.add_widget(lay)
	def start_game(self):
		self.manager.current = "edit"
	def quiting(self):
		self.but_quit.text = "[color=3B0000]Вы были пойманы[/color]"
	def Android_back_click(self, window, key, *largs):
		if self.manager.current == "main" and key == 27:
			return True;

class GameEditor(Widget):
	def __init__(self, data, filename, scatter, **kwargs):
		super(GameEditor, self).__init__(**kwargs)
		self.Data = data
		self.Filename=filename
		self.MovingScatter = scatter
		self.o = {}
		self.c = {}
		self.a = {}
		self.MiddleButtonStartPos = (0,0)
		with self.canvas:
			for sprite in data["Sprite"]:
				o = data["Sprite"][sprite]
				self.o[sprite] = Sprite(sprite, o["size"], o["source"])
				self.o[sprite].pos = o["pos"]
			for collider in data["Collider"]:
				c = data["Collider"][collider]
				self.c[collider] = coliders(0,0,0,0,sprite)
				self.c[collider].pos = c["pos"]
				self.c[collider].size = c["size"]
				self.c[collider].Name = collider
				self.c[collider].UpdateVisual()
		self.UpdateA()
		self.SelectedObject = None
		self.MovingObj = (None, (None, None))
		self.PPLay = GridLayout(cols=2)
		self.Name = TextInput(multiline = False, text="Name")
		self.XChange = TextInput(multiline= False, text="0")
		self.YChange = TextInput(multiline= False, text="0")
		self.WidthChange = TextInput(multiline= False, text="0")
		self.HeightChange = TextInput(multiline=False, text="0")
		self.DelBut = KButton(text="Удалить", color=(1,0,0,1), background_color = (.35,.3,.7, 1))
		self.Source = TextInput(multiline=False, text="none.png")
		assain = Button(text="Применить")
		assain.on_release = self.SetPropertis
		l1 = [self.Name, self.XChange, self.YChange, self.WidthChange, self.HeightChange,self.Source, self.DelBut, assain]
		l2 = ["Name", "x", "y", "Ширина", "Высота", "Картинка", "Удалить", ""]
		for i in range(len(l1)):
			self.PPLay.add_widget(Label(text=l2[i]))
			self.PPLay.add_widget(l1[i])
		self.EditObject = Popup(title="Изменение свойств объекта", content=self.PPLay, size_hint=(.7,.7))
	def UpdateA(self):
		self.a = self.o | self.c
	def CreateSprite(self):
		with self.canvas:
			name = str(randint(0,99999999))
			self.o[name] = Sprite(name, pos = (0,0))
		self.UpdateA()

	def CreateCollider(self):
		with self.canvas:
			name = str(randint(0,99999999))
			self.c[name] = coliders(0,0,100,100, name)
		self.UpdateA()
	#TextInput
	def SetPropertis(self):
		self.EditObject.dismiss();
		if self.SelectedObject == None:
			return
		obj = self.SelectedObject
		if not (self.Name.text in self.o or self.Name.text in self.c):########
			obj.Name = self.Name.text
		obj.pos = (round(float(self.XChange.text)), round(float(self.YChange.text)))
		obj.size = (round(float(self.WidthChange.text)),round(float(self.HeightChange.text)))
		try:
			obj.source = self.Source.text
		except:pass
	def GetPropertis(self, obj):
		self.Name.text = str(obj.Name)
		self.XChange.text = str(obj.pos[0])
		self.YChange.text = str(obj.pos[1])
		self.WidthChange.text = str(obj.size[0])
		self.HeightChange.text = str(obj.size[1])
		self.SelectedObject = obj
		try:
			self.Source.text = str(obj.source)
		except:pass
	
	def DeleteObject(self, *_):
		if type(self.SelectedObject) == type(Sprite):
			self.o.pop(self.SelectedObject.Name)
		else:
			self.o.pop(self.SelectedObject.Name)
		self.canvas.remove(self.SelectedObject)
	
	def GetObjOnXY(self,pos):
		mouse = coliders(pos[0]+1, pos[1]+1, 2, 2, "")
		for collider in self.c:
			if is_touching(self.c[collider], mouse):
				return self.c[collider]
		for sprite in self.o:
			if is_touching(self.o[sprite], mouse):
				return self.o[sprite]
		return None
	
	def on_touch_down(self, touch):
		touch.pos = (touch.pos[0]*self.MovingScatter.scale, touch.pos[1]*self.MovingScatter.scale)
		print(touch.button)
		if touch.button == "middle":
			self.MiddleButtonStartPos = touch.pos
		try:
			if touch.button == "scrolldown":
				self.MovingScatter.scale *= 2
			if touch.button == "scrollup":
				self.MovingScatter.scale /= 2
		except:pass
		
		data = self.GetObjOnXY((touch.x, touch.y))
		if data == None:
			return
		if touch.button == "right":
			self.GetPropertis(data)
			self.EditObject.open()
		elif touch.button == "left":
			self.MovingObj = (data, (data.x-touch.x, data.y-touch.y))
			self.MovingScatter.scale = 1
	
	def on_touch_move(self, touch):
		touch.pos = (touch.pos[0]*self.MovingScatter.scale, touch.pos[1]*self.MovingScatter.scale)
		if touch.button == "middle":
			self.MovingScatter.x -= self.MiddleButtonStartPos[0] - touch.pos[0]
			self.MovingScatter.y -= self.MiddleButtonStartPos[1] - touch.pos[1]
		try:
			if KeyboardMap["ctrl"]:
				self.MovingObj[0].pos = round(touch.x + self.MovingObj[1][0], -1), round(touch.y + self.MovingObj[1][1], -1)
			else:
				self.MovingObj[0].pos = round(touch.x + self.MovingObj[1][0]), round(touch.y + self.MovingObj[1][1])
			self.MovingObj[0].UpdateVisual()
		except:pass

	def on_touch_up(self, *_):
		self.MovingObj = (None, (None, None))

	def SaveFile(self):
		NewSprites = {}
		NewCollider = {}
		for Sprite in self.o:
			o = self.o[Sprite]
			NewSprites[Sprite] = {"pos":o.pos, "size":o.size, "source":o.source}
			print(NewSprites[Sprite])
		for Collider in self.c:
			c = self.c[Collider]
			NewCollider[Collider] = {"pos":c.pos, "size":c.size}
			print(NewCollider[Collider])
		NewData = {"Name":self.Data["Name"], "Sprite":NewSprites,"Collider":NewCollider}
		with open(self.Filename, "w", encoding="utf-8") as file:
			json.dump(NewData, file)

class TextPopup(Popup):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		MainLay = GridLayout(cols=1)
		ObjBeenCopy = Label(text="Скопированно", size_hint_y = .2, color = (1,0,0,1))
		MainLay.add_widget(ObjBeenCopy)
		self.Text = TextInput()
		MainLay.add_widget(self.Text)
		self.content = MainLay
		self.title = "Code"
		self.size_hint = (.5,.5)
TextPP = TextPopup()

class ExportPopup(Popup):
	def __init__(self, **kwargs) -> None:
		"AllObjects включает в себя и sprite и colliders"
		super().__init__(**kwargs)
		self.AllObjects={}
		MainLay = GridLayout(cols=1)
		MainLay.add_widget(Label(text="Формат кода, замену указывать через префикс, вы пишите строчку, остальное сгенерируется само \"$\"\n пример \"Object($name,$x, $y, $w, $h, $source)\"", color=(0,1,0,1)))
		self.Code = TextInput(text = "Object($name,$x, $y, $w, $h, $source)")
		MainLay.add_widget(self.Code)
		SettingLayout = GridLayout(rows=1)
		self.TypeOfPos = Carousel()
		self.typeposlist = ["left_bottom", "left_top", "center"]
		for i in self.typeposlist:
			self.TypeOfPos.add_widget(Label(text = i))
		self.TypeExportData = Carousel()
		for i in ["list", "dict(coming soon)"]:
			self.TypeExportData.add_widget(Label(text = i))
		SettingLayout.add_widget(self.TypeOfPos)
		MainLay.add_widget(SettingLayout)
		GenerateButton = Button(text = "Генерировать")
		GenerateButton.on_release = self.Generate
		MainLay.add_widget(GenerateButton)
		self.content = MainLay
		self.title = "Настройки экспорта"
		self.size_hint = (.8,.8)
	def Generate(self):
		print(All_a)
		result = ""
		for Type in All_a:
			result += Type + " = ["
			print("p")
			for Obj in All_a[Type]:
				print("q")
				seg = self.Code.text
				match self.typeposlist.index(self.TypeOfPos.current_slide.text):
					case 0:
						seg = seg.replace("$x", str(All_a[Type][Obj]. pos[0]))
						seg = seg.replace("$y", str(All_a[Type][Obj]. pos[1]))
						seg = seg.replace("$w", str(All_a[Type][Obj].size[0]))
						seg = seg.replace("$h", str(All_a[Type][Obj].size[1]))
						seg = seg.replace("$name", Obj)
					case 1:
						seg = seg.replace("$x", str(All_a[Type][Obj].pos[0]))
						seg = seg.replace("$y", str(Window.size[1] - (All_a[Type][Obj].pos[1] + All_a[Type][Obj]["size"[1]])))
						seg = seg.replace("$w", str(All_a[Type][Obj].size[0]))
						seg = seg.replace("$h", str(All_a[Type][Obj].size[1]))
						seg = seg.replace("$name", Obj)
					case 2:
						seg = seg.replace("$x", str(All_a[Type][Obj].pos[0] + Window.size[0]/2 - All_a[Type][Obj].size[0]/2))
						seg = seg.replace("$y", str(All_a[Type][Obj].pos[1] + Window.size[1]/2 + All_a[Type][Obj].size[1]/2))
						seg = seg.replace("$w", str(All_a[Type][Obj].size[0]))
						seg = seg.replace("$h", All_a[Type][Obj].size[1])
						seg = seg.replace("$name", Obj)
				if Type == "Sprite":
					seg = seg.replace("$source", All_a[Type][Obj].source).replace("None", "")
				else:
					seg = seg.replace("$source", "")
				seg += ",\n"
				result += seg
			result += "]\n"
		print("end")
		TextPP.Text.text = result
		TextPP.open()
		self.dismiss()

ExportPP = ExportPopup()

All_a = {}

class OpenScene(Screen):
	def __init__(self, data, filename, **kw):
		name = data["Name"]
		temp_files[name] = str(filename)
		with open("tmpf", "w", encoding="utf-8") as file:
			json.dump(temp_files, file)
		super(OpenScene, self).__init__(name=name)
		Window.bind(on_key_down = self.Android_back_click, on_key_up = self.Android_back_click_u);
		self.name = name
		scat = Scatter(do_rotation=False, do_scale=False, do_translation_y=False, do_translation_x=False)
		self.scene = GameEditor(data, filename, scat)
		scat.add_widget(self.scene)
		self.MPPLay = GridLayout(cols=2)
		ExportCode = Button(text = "Export")
		ExportCode.on_release = self.ExportAsCode
		AddSprite   = Button(text="Создать Sprite")
		AddSprite.on_release=self.CreateS
		AddCollider = Button(text="Создать Collider")
		AddCollider.on_release=self.CreateC
		self.SetColor = ColorPicker()
		self.SetColor.set_color((.333, .3, .5, 1))
		self.SetColor.bind(color=self.SetBackGround)
		SaveBut = Button(text="Сохранить")
		SaveBut.on_release=self.Save
		BackToMenuNotSave = Button()
		BackToMenu = Button(text="Сохранить и выйти")
		BackToMenu.on_release=self.SaveAndLeave
		for wid in [self.SetColor, ExportCode, AddSprite, AddCollider, SaveBut, BackToMenu]:
			self.MPPLay.add_widget(wid)
		self.MenuPP = Popup(title="Меню", content = self.MPPLay, size_hint=(.35,.9))
		self.add_widget(scat)
		Clock.schedule_once(self.OpenSelf, 1)
	def CreateS(self):
		self.MenuPP.dismiss()
		self.scene.CreateSprite()
		self.scene.UpdateA()
	def CreateC(self):
		self.MenuPP.dismiss()
		self.scene.CreateCollider()
		self.scene.UpdateA()
	def OpenSelf(self, *_):
		self.manager.current = self.name
	def SetBackGround(self, i, rgba):
		Window.clearcolor=rgba
	def SaveAndLeave(self):
		self.Save()
		self.manager.current = "main"
	def Save(self):
		self.scene.SaveFile()
		self.MenuPP.dismiss()
	def ExportAsCode(self):
		global All_a
		All_a = {"Sprite":self.scene.o, "Collider":self.scene.c}
		ExportPP.open()
	def Android_back_click(self, window, key, *largs):
		if self.manager.current == self.name:
			if key == 305:
				KeyboardMap["ctrl"] = True
			else:
				KeyboardMap["ctrl"] = False
			if key == 27:
				self.MenuPP.open()
				return True;
			if key == 103:
				self.scene.MovingScatter.pos = (0,0)
				self.scene.MovingScatter.scale = 1
	def Android_back_click_u(self, window, key, *largs):
		if self.manager.current == self.name:
			if key == 305:
				KeyboardMap["ctrl"] = False
			else:
				KeyboardMap["ctrl"] = True

class LevelsScreen(Screen):
	def __init__(self,name) -> None:
		global temp_files
		super(LevelsScreen,self).__init__(name=name)
		Window.bind(on_keyboard=self.Android_back_click);
		self.Levels = GridLayout(cols = 3)
		Back = Button(text="Назад")
		Back.on_release = self.back
		self.Levels.add_widget(Back)

		Open = Button(text="Открыть")
		Open.on_release = self.ExplorerOpen
		self.Levels.add_widget(Open)

		Create = Button(text="Создать")
		Create.on_release = self.CreateOpen
		self.Levels.add_widget(Create)

		for temp in temp_files:
			NBut = Button(text=f"{temp}\n{temp_files[temp]}")
			NBut.bind(on_release = self.OpenLevelWithButton)
			self.Levels.add_widget(NBut)
		
		self.add_widget(self.Levels)
	def OpenLevelWithButton(self, Self):
		path = Self.text.split("\n")[1]
		with open(path, "r", encoding="utf-8") as file:
			app.AddScreen(OpenScene(json.load(file), path))
	def CreateLevel(self):
		LevelName = self.LevelName.text
		data = {"Name":LevelName, "Sprite":{},"Collider":{}}
		with open(PathExplorer.path + "/" + LevelName + ".kivyedit", "w", encoding="utf-8") as file:
			json.dump(data, file)
		app.AddScreen(OpenScene(data, PathExplorer.path + "/" + LevelName + ".kivyedit"))
	def ExplorerOpen(self, next = False):#open
		global Explorer
		SelBut = Button(text="Открыть", size_hint_y = .2)
		SelBut.on_release = self.OpenLvl
		content = GridLayout(cols=1)
		content.add_widget(Explorer)
		content.add_widget(SelBut)
		Popup(title="open", content=content, size_hint=(.6,.6)).open()
	def CreateOpen(self):
		global Explorer
		self.LevelName = TextInput(text="lvl", size_hint_y=.2)
		SelBut = Button(text="Создать", size_hint_y = .2)
		SelBut.on_release = self.CreateLevel
		content = GridLayout(cols=1)
		content.add_widget(self.LevelName)
		content.add_widget(PathExplorer)
		content.add_widget(SelBut)
		Popup(title="Сохранение", content=content, size_hint=(.6,.6)).open()
	def OpenLvl(self):
		with open(Explorer.selection[0], "r", encoding="utf-8") as file:
			app.AddScreen(OpenScene(json.load(file), Explorer.selection[0]))
	def back(self):
		self.manager.current = "main"
	def Android_back_click(self, window, key, *largs):
		if self.manager.current == "edit" and key == 27:
			self.manager.current = "main"
			return True;

app.run()