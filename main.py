# class for creating apps but not fom scratch
from kivy.app import App
# widget class
from kivy.uix.widget import Widget
# for velocity as it will be numeric value
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
# for ball movement we want Velocity and velocity should be in vector form
from kivy.vector import Vector
# for clock method
from kivy.clock import Clock
# for random integer
from random import randint

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1

class PongBall(Widget):
    # 0 here is default value
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # movement of the ball, Latest Position = Current Velocity + Current Position
    def move(self):
        self.pos = Vector(self.velocity) + self.pos

# Update =moving the ball by calling the move function and the other stuff

# on_touch_down() - When our finger/mouse touches the screen
# on touch_up() - When we lift our finger off the screen after touching it
# on_touch_move() - When we drag our finger on the screen

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.y > self.height - 50):
            self.ball.velocity_y *= -1

        # bounce off left
        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player1.score += 1

        # bounce off right
        if self.ball.x > self.width - 50:
            self.ball.velocity_x *= -1
            self.player2.score += 1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y

        if touch.x > self.width * 3/4:
            self.player2.center_y = touch.y

# class for main application
# 60.0 is 60 fps
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

# It will create a window and it will run the program
PongApp().run()