from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label

oven_length = 0.0
biscuit_length = 0.0
pitch = 0.0
cup_length = 0.0
cup_width = 0.0
baking_time_mins = 0.0
baking_time_secs = 0.0
rpm = 0.0
production_per_min = 0.0
mass = 0.0

class MainScreen(Screen):
    oven_length = ObjectProperty(None)
    biscuit_length = ObjectProperty(None)
    mass = ObjectProperty(None)
    pitch = ObjectProperty(None)
    cup_length = ObjectProperty(None)
    cup_width = ObjectProperty(None)
    baking_time_mins = ObjectProperty(None)
    baking_time_secs = ObjectProperty(None)

    def calculate(self):
        flag = evaluate(self.oven_length.text, self.biscuit_length.text, self.mass.text, self.pitch.text, self.cup_length.text, self.cup_width.text, self.baking_time_mins.text, self.baking_time_secs.text)
        if(flag):
            sm.current = "result"
            self.reset()
        else:
            errorMessage("Invalid Input please check again")

    def previous_value(self):
        self.oven_length.text = str(globals()['oven_length'])
        self.biscuit_length.text = str(globals()['biscuit_length'])
        self.mass.text =  str(globals()['mass'])
        self.pitch.text = str(globals()['pitch'])
        self.cup_length.text = str(globals()['cup_length'])
        self.cup_width.text = str(globals()['cup_width'])
        self.baking_time_mins.text = str(int(globals()['baking_time_mins']))
        self.baking_time_secs.text = str(int(globals()['baking_time_secs']))


    def reset(self):
        self.oven_length.text = ""
        self.biscuit_length.text = ""
        self.mass.text = ""
        self.cup_length.text = ""
        self.cup_width.text = ""
        self.baking_time_mins.text = ""
        self.baking_time_secs.text = ""

class ResultScreen(Screen):
    oven_length = ObjectProperty(None)
    biscuit_length = ObjectProperty(None)
    mass = ObjectProperty(None)
    pitch = ObjectProperty(None)
    cup = ObjectProperty(None)
    baking_time = ObjectProperty(None)
    rpm = ObjectProperty(None)
    production_per_min = ObjectProperty(None)

    def on_enter(self, *args):
        self.oven_length.text = "Oven_length: " + str(globals()['oven_length'])
        self.biscuit_length.text = "Biscuit Lenght or Diameter: " + str(globals()['biscuit_length'])
        self.mass.text = "Mass: " + str(globals()['mass'])
        self.pitch.text = "Pitch: " + str(globals()['pitch'])
        self.cup.text = "Cup no: " + str(globals()['cup_length']) + " X " + str(globals()['cup_width'])
        self.baking_time.text = "Baking time: " + str(int(globals()['baking_time_mins'])) + " : " + str(int(globals()['baking_time_secs']))
        self.rpm.text = "RPM: " + str(globals()['rpm'])
        self.production_per_min.text = "Production per Min: " + str(globals()['production_per_min'])

    def go_back(self):
        sm.current = "main"

class WindowManager(ScreenManager):
    pass

def evaluate(ol,bl, m, p, cl,cw,btm,bts):
    global oven_length, biscuit_length, mass, pitch, cup_length, cup_width, baking_time_secs, baking_time_mins, rpm, production_per_min

    try:
        oven_length = float(ol)
        biscuit_length = float(bl)
        mass = float(m)
        pitch = float(p)
        cup_length = float(cl)
        cup_width = float(cw)
        baking_time_mins = float(btm)
        baking_time_secs = float(bts)

        bt = baking_time_mins + baking_time_secs/60

        rpm = 304.8*oven_length/((biscuit_length + pitch)*cup_width)/bt

        production_per_min = rpm*(cup_length*cup_width)*mass/1000
    except:
        return False

    return True


def errorMessage(text):
    pop = Popup(title='Message',
                  content=Label(text=text),
                  size_hint=(0.3,0.3), size=(400, 400))
    pop.open()

kv = Builder.load_file("custom_analysis.kv")
sm = WindowManager()
screens = [MainScreen(name="main"), ResultScreen(name="result")]
for screen in screens:
    sm.add_widget(screen)
sm.current = "main"


class CustomAnalysisApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    CustomAnalysisApp().run()
