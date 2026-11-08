from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget

# RED SHADOW EXTREME — safe, standalone visual sandbox.
# It does not read Roblox memory, inspect other apps, or control a live game.

Window.clearcolor = (0.035, 0.035, 0.045, 1)

class ToggleButton(Button):
    active = BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.bind(active=self.refresh)
        self.refresh()
    def refresh(self, *args):
        self.background_color = (0.65, 0.04, 0.10, 1) if self.active else (0.13, 0.13, 0.16, 1)
        self.color = (1, 1, 1, 1)
    def on_release(self):
        self.active = not self.active
        self.text = ("ON  " if self.active else "OFF ") + self.text.split("  ", 1)[-1]

class Arena(Widget):
    esp_box = BooleanProperty(True)
    esp_health = BooleanProperty(True)
    esp_distance = BooleanProperty(True)
    esp_skeleton = BooleanProperty(False)
    show_fov = BooleanProperty(True)
    aim_assist = BooleanProperty(False)
    wall_demo = BooleanProperty(True)
    fov = NumericProperty(110)
    smooth = NumericProperty(35)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw, esp_box=self.draw, esp_health=self.draw,
                  esp_distance=self.draw, esp_skeleton=self.draw, show_fov=self.draw,
                  aim_assist=self.draw, wall_demo=self.draw, fov=self.draw)
        Clock.schedule_interval(self.draw, 1/15)
    def draw(self, *args):
        self.canvas.clear()
        w, h = self.size
        if w < 10 or h < 10: return
        with self.canvas:
            Color(0.055, 0.055, 0.07, 1); Rectangle(pos=self.pos, size=self.size)
            # Subtle grid
            Color(0.15, 0.15, 0.18, 0.45)
            for x in range(int(self.x), int(self.right), int(dp(28))):
                Line(points=[x, self.y, x, self.top], width=0.5)
            for y in range(int(self.y), int(self.top), int(dp(28))):
                Line(points=[self.x, y, self.right, y], width=0.5)
            cx, cy = self.center
            # FOV visualization
            if self.show_fov:
                Color(1, 0.16, 0.22, 0.85)
                Line(circle=(cx, cy, min(self.fov, min(w,h)*0.42)), width=1.2)
                Line(points=[cx-7,cy,cx+7,cy], width=1)
                Line(points=[cx,cy-7,cx,cy+7], width=1)
            # Example obstacle / wall
            Color(0.25, 0.25, 0.29, 1)
            Rectangle(pos=(self.x+w*0.56, self.y+h*0.24), size=(w*0.10,h*0.42))
            Color(0.55, 0.55, 0.62, 1)
            Line(rectangle=(self.x+w*0.56, self.y+h*0.24, w*0.10,h*0.42), width=1)
            # Demo targets only
            targets = [
                (self.x+w*0.28, self.y+h*0.58, "TARGET A", "24 m", False, 0.78),
                (self.x+w*0.73, self.y+h*0.57, "TARGET B", "38 m", True, 0.52),
            ]
            for tx, ty, name, dist, behind, health in targets:
                bw, bh = w*0.13, h*0.32
                bx, by = tx-bw/2, ty-bh/2
                col = (1,0.22,0.27,1) if not behind else (1,0.55,0.2,1)
                if self.esp_box:
                    Color(*col); Line(rectangle=(bx,by,bw,bh), width=1.4)
                if self.esp_health:
                    Color(0.12,0.12,0.14,1); Rectangle(pos=(bx-dp(8),by), size=(dp(4),bh))
                    Color(0.2,0.9,0.38,1); Rectangle(pos=(bx-dp(8),by), size=(dp(4),bh*health))
                if self.esp_skeleton:
                    Color(1,0.35,0.4,1)
                    Line(points=[tx,ty+bh*.27,tx,ty,tx-bw*.25,ty-bh*.2], width=1)
                    Line(points=[tx,ty,tx+bw*.25,ty-bh*.2], width=1)
                    Line(points=[tx,ty,tx-bw*.18,ty-bh*.42], width=1)
                    Line(points=[tx,ty,tx+bw*.18,ty-bh*.42], width=1)
                if self.esp_distance:
                    Color(1,1,1,0.95)
                    # Labels use Kivy canvas text-free visual tags; status is shown in legend below.
                    Line(points=[tx-dp(18),by-dp(10),tx+dp(18),by-dp(10)], width=1)
                # Head marker
                Color(*col); Ellipse(pos=(tx-dp(5),ty+bh*.30), size=(dp(10),dp(10)))
                if behind and self.wall_demo:
                    Color(1,0.55,0.2,0.9)
                    Line(circle=(tx,ty,dp(13)), width=1.2)
            # Aim assist is visual-only: line to nearest sample target
            if self.aim_assist:
                Color(1,0.15,0.2,0.9)
                Line(points=[cx,cy,self.x+w*.28,self.y+h*.58], width=1.1)

class RedShadowApp(App):
    def build(self):
        self.title = "RED SHADOW EXTREME"
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(9))
        header = BoxLayout(size_hint_y=None, height=dp(58), spacing=dp(8))
        title = Label(text="[b]RED SHADOW[/b] [color=#ff303b]EXTREME[/color]\\n[size=10]ANDROID • VISUAL SANDBOX[/size]",
                      markup=True, halign="left", valign="middle", color=(1,1,1,1))
        title.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        header.add_widget(title)
        badge = Label(text="[color=#ff5059]DEMO[/color]", markup=True, size_hint_x=None, width=dp(62))
        header.add_widget(badge); root.add_widget(header)
        self.arena = Arena(size_hint_y=0.58)
        root.add_widget(self.arena)
        status = Label(text="[color=#ff5059]●[/color]  TEST ARENA     [color=#aaaaaa]Alvos fictícios • sem conexão ao Roblox[/color]",
                       markup=True, size_hint_y=None, height=dp(25), font_size="11sp")
        root.add_widget(status)
        controls = GridLayout(cols=2, spacing=dp(7), size_hint_y=None, height=dp(164))
        items = [
            ("ESP BOX", "esp_box"), ("ESP VIDA", "esp_health"),
            ("ESP DISTÂNCIA", "esp_distance"), ("ESP SKELETON", "esp_skeleton"),
            ("FOV CIRCLE", "show_fov"), ("AIM ASSIST (DEMO)", "aim_assist"),
            ("WALL DEMO", "wall_demo")
        ]
        for label, attr in items:
            b = ToggleButton(text="ON  "+label if getattr(self.arena, attr) else "OFF "+label,
                             active=getattr(self.arena, attr), font_size="11sp", size_hint_y=None, height=dp(38))
            b.bind(active=lambda inst, val, a=attr: setattr(self.arena, a, val))
            controls.add_widget(b)
        root.add_widget(controls)
        sliders = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(84), spacing=dp(3))
        self.fov_label = Label(text="FOV SIZE  •  110", size_hint_y=None, height=dp(20), font_size="11sp", color=(1,.45,.48,1))
        fov_slider = Slider(min=35, max=220, value=110)
        fov_slider.bind(value=self.set_fov)
        self.smooth_label = Label(text="AIM SMOOTHING  •  35%  (visual demo)", size_hint_y=None, height=dp(20), font_size="11sp", color=(1,.45,.48,1))
        smooth_slider = Slider(min=1, max=100, value=35)
        smooth_slider.bind(value=self.set_smooth)
        sliders.add_widget(self.fov_label); sliders.add_widget(fov_slider)
        sliders.add_widget(self.smooth_label); sliders.add_widget(smooth_slider)
        root.add_widget(sliders)
        footer = Label(text="RED SHADOW EXTREME  •  build 1.0.0  •  Offline demo",
                       size_hint_y=None, height=dp(20), font_size="9sp", color=(.5,.5,.55,1))
        root.add_widget(footer)
        return root
    def set_fov(self, instance, value):
        self.arena.fov = value
        self.fov_label.text = f"FOV SIZE  •  {int(value)}"
    def set_smooth(self, instance, value):
        self.arena.smooth = value
        self.smooth_label.text = f"AIM SMOOTHING  •  {int(value)}%  (visual demo)"

if __name__ == "__main__":
    RedShadowApp().run()
