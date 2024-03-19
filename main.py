from math import sin, cos, atan, sqrt
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
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


class Obstacle(Widget):
    def __init__(self, pos = None, object_id = 1, **kwargs):
        super().__init__(**kwargs)
        if pos == None:
            pos = 0,0
        self.id = object_id
        self.pos = pos
        self.size = 10, 100
    def obstacle_collision(self, ball):
        if self.collide_widget(ball):
            print(f"collision with {self.id}")
            return True



class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.velocity = self.velocity_x, self.velocity_y - (Free_fall_acceleration / Frame_rate)
        self.pos = Vector(*self.velocity) + self.pos


# noinspection PyGlobalUndefined
class PongGame(Widget):
    ball = ObjectProperty(None)
    ball_released = False
    start = False
    after = False
    obstacles_added = False
    obstacle: Obstacle() = ObjectProperty(None)
    obstacles: [Obstacle()] = ListProperty([])

    def startGame(self):
        self.start = True

    def remove_obstacle(self, obstacle):
        self.remove_widget(obstacle)
        self.obstacles.remove(obstacle)

    def serve_ball(self, ang, coef):
        self.ball_released = True
        self.ball.pos = SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3
        self.ball.velocity = (Initial_velocity * cos(ang) * coef, Initial_velocity * sin(ang) * coef)

    def spawn_ball(self):
        self.ball.pos = SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3
        self.ball.velocity = (0, 0)
        self.ball_released = False
    def addObstacles(self, pos, object_id, n_of_obstacles):
        print("obstacles added")
        for i in range(n_of_obstacles):
            obstacle = Obstacle(pos = (500 + 40 * i, 400), object_id = i)
            self.add_widget(obstacle)
            self.obstacles.append(obstacle)
        self.obstacles_added = True

    def update(self, dt):
        if self.obstacles_added:
            for obstacle in self.obstacles:
                if obstacle.obstacle_collision(self.ball):
                    self.remove_obstacle(obstacle)
        if self.ball_released:
            self.ball.move()
        if self.start:
            print("game started")
            but = self.ids["start_button"]
            self.remove_widget(but)
            self.start = False
            self.after = True

    def on_touch_down(self, touch):
        if self.after:
            self.spawn_ball()
        else:
            Clock.schedule_once(lambda dt: self.on_touch_down(touch))
            return super(PongGame, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if (touch.x < self.width / 3) and (touch.y < self.height / 3):
            angle = atan((self.height / 3 - touch.y) / (self.width / 3 - touch.x))
            c = sqrt(((self.height / 3) - touch.y) ** 2 + (self.width / 3 - touch.x) ** 2) / sqrt(
                ((self.height / 3) ** 2 + (self.width / 3) ** 2))
            self.serve_ball(ang=angle, coef=c)


class PongApp(App):
    def build(self) -> Widget():
        Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        game = PongGame()
        Clock.schedule_interval(game.update, 1.0 / Frame_rate)
        return game


if __name__ == '__main__':
    PongApp().run()
