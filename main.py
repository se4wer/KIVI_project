import math
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
from Obstacle import Obstacle
from Bullet import Bullet
import cannon_constants as CONST

SCREEN_WIDTH = CONST.SCREEN_WIDTH
SCREEN_HEIGHT = CONST.SCREEN_HEIGHT
Initial_velocity = 100
Frame_rate = 20.0

class Game(Widget):
    ball = ObjectProperty(None)
    ball_released = False
    start = False
    after = False
    obstacles_added = False
    obstacle = ObjectProperty(None)
    obstacles = ListProperty([])

    def bullet_blast(self, target_block):
        pos = target_block.pos
        for obstacle in self.obstacles:
            distance = sqrt((pos[0] - obstacle.pos[0])**2 + (pos[1] - obstacle.pos[1])**2)
            print(distance)
            print(CONST.BULLET_RADIUS)
            if distance < CONST.BULLET_RADIUS:
                print("deleted")
                self.remove_obstacle(obstacle)
            print()
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
            for j in range(n_of_obstacles):
                obstacle = Obstacle(pos=(500 + 30 * i, 400 + 30 * j), object_id=f"{i}{j}",
                                    texture_path='textures/stone texture.png')
                self.add_widget(obstacle)
                self.obstacles.append(obstacle)
        self.obstacles_added = True

    def update(self, dt):
        if self.obstacles_added:
            for obstacle in self.obstacles:
                if obstacle.obstacle_collision(self.ball):
                    self.bullet_blast(obstacle)
                    # self.remove_obstacle(obstacle)
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
            return super(Game, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if (touch.x < self.width / 3) and (touch.y < self.height / 3):
            angle = atan((self.height / 3 - touch.y) / (self.width / 3 - touch.x))
            c = sqrt(((self.height / 3) - touch.y) ** 2 + (self.width / 3 - touch.x) ** 2) / sqrt(
                ((self.height / 3) ** 2 + (self.width / 3) ** 2))
            self.serve_ball(ang=angle, coef=c)


class CannonApp(App):
    def build(self) -> Widget():
        Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        game = Game()
        Clock.schedule_interval(game.update, 1.0 / Frame_rate)
        return game


if __name__ == '__main__':
    CannonApp().run()
