from math import sin, cos, atan, sqrt
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from random import randint

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
Initial_velocity = 100
Frame_rate = 20.0
Free_fall_acceleration = 9.81


class PongBall(Widget):
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)
    pos = ReferenceListProperty(pos_x, pos_y)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.velocity = self.velocity_x, self.velocity_y - (Free_fall_acceleration / Frame_rate)
        self.pos = Vector(*self.velocity) + self.pos


# noinspection PyGlobalUndefined
class PongGame(Widget):
    obstacle = ObjectProperty(None)
    ball = ObjectProperty(None)
    ball_released = False
    start = False
    after = False
    obstacles_added = False

    def startGame(self):
        self.start = True
        but = self.ids["start_button"]
        but.pos = randint(0,SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)

    def obstacle_collision(self):
        if self.obstacle.widget_collide(self.ball):
            self.obstacle.remove_widget()

    def addObstacles(self):
        print("obstacles added")
        self.obstacle = Widget()
        self.add_widget(self.obstacle)
        with self.obstacle.canvas:
            Rectangle(pos = (600, 600), size = (100, 100))
        self.obstacles_added = True
    def serve_ball(self, ang, coef):
        self.ball_released = True
        self.ball.pos_x = SCREEN_WIDTH / 3
        self.ball.pos_y = SCREEN_HEIGHT / 3
        Initial_vertical_velocity = Initial_velocity * sin(ang) * coef
        Initial_horizontal_velocity = Initial_velocity * cos(ang) * coef
        self.ball.velocity = (Initial_horizontal_velocity, Initial_vertical_velocity)
        self.ball.center = self.center
    def spawn_ball(self):
        self.ball.pos_x = SCREEN_WIDTH / 3
        self.ball.pos_y = SCREEN_HEIGHT / 3
        self.ball.velocity = (0, 0)
        self.ball_released = False

    def update(self, dt):
        if self.ball_released == True:
            self.ball.move()
        if self.start:
            print("game started")
            but = self.ids["start_button"]
            self.remove_widget(but)
            self.start = False
            self.after = True
        if self.obstacles_added:
            self.obstacle.obstacle_collision()

    # def on_touch_down(self, touch):
    #     if start == True:
    #         self.spawn_ball()
    def on_touch_down(self, touch):
        if self.after:
            self.spawn_ball()
        else:
            Clock.schedule_once(lambda dt: self.on_touch_down(touch))
            return super(PongGame, self).on_touch_down(touch)
    def on_touch_up(self, touch):
        if ((touch.x < self.width / 3) and (touch.y < self.height / 3)):
            angle = atan((self.height / 3 - touch.y) / (self.width / 3 - touch.x))
            c = sqrt(((self.height / 3) - touch.y)**2 + (self.width / 3 - touch.x)**2) / sqrt(((self.height / 3)**2 + (self.width / 3)**2))
            self.serve_ball(ang=angle, coef=c)

class PongApp(App):
    def build(self):
        Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        game = PongGame()
        Clock.schedule_interval(game.update, 1.0 / Frame_rate)
        return game


if __name__ == '__main__':
    PongApp().run()