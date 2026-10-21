import os
import random
import subprocess
import time

#Import the Turtle Module
import turtle
#Required by MacOSX to show the window
turtle.fd(0)
#Set the animations speed to the max
turtle.speed(0)
#Change the bg color
turtle.bgcolor("black")
#Change the window title
turtle.title("Galactic Battle")
#Change the background image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
background = os.path.join(BASE_DIR, "galaxy.gif")
turtle.bgpic(background)

#Hide the default turtle
turtle.ht()
#This saves memory
turtle.setundobuffer(1)
#This speeds up drawing
turtle.tracer(0)

#SPRITE CLASS
class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #Boundary Detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self,other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False
    
        
#CHILD OF THE SPRITE CLASS
class Player(Sprite): 
     def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None) 
        self.speed = 4
        self.lives = 3  

     def turn_left(self):
         self.lt(45)

     def turn_right(self):
         self.rt(45)

     def accelerate(self):
         self.speed += 1

     def decelerate(self):
         self.speed -= 1

#ENEMY CLASS
class Enemy(Sprite): 
     def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty) 
        self.speed = 6
        self.setheading(random.randint(0,360))

#ALLY CLASS
class Ally(Sprite): 
     def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty) 
        self.speed = 8
        self.setheading(random.randint(0,360))

     def move(self):
         self.fd(self.speed)

         #Boundary Detection
         if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

         if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

         if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

         if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

#Making the missile
class Missile(Sprite): 
     def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty) 
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

     def fire(self):
         if self.status == "ready":
             #Play missile sound
             sound_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"boom.mp3")
             subprocess.Popen(["afplay", sound_file])
             self.goto(player.xcor(), player.ycor())
             self.setheading(player.heading())
             self.status = "firing"

     def move(self):
         
         if self.status == "ready":
             self.goto(-1000, 1000)
            
         if self.status == "firing":
             self.fd(self.speed)

        #Border check
         if self.xcor() < -290 or self.xcor() > 290 or \
             self.ycor()< -290 or self.ycor()> 290:
             self.goto(-1000,1000)
             self.status = "ready"

#Create Particle
class Particle(Sprite): 
     def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None) 
        self.goto(-1000,-1000)
        self.frame = 0

     def explode(self, startx, starty):
         self.goto(startx,starty)
         self.setheading(random.randint(0,360))
         self.frame = 1

     def move(self):
         if self.frame > 0:
             self.fd(10)
             self.frame += 1

         if self.frame > 15:
             self.frame = 0
             self.goto(-1000, -1000)

class Game():
     def __init__(self):
         self.level = 1
         self.score = 0
         self.state = "playing"
         self.pen = turtle.Turtle()
         self.lives = 3

     def draw_border(self):
         #Draw border
         self.pen.speed(0)
         self.pen.color("white")
         self.pen.pensize(3)
         self.pen.penup()
         self.pen.goto(-300, 300)
         self.pen.pendown()
         for side in range(4):
             self.pen.fd(600)
             self.pen.rt(90)
         self.pen.penup()
         self.pen.ht()
         self.pen.pendown()

#Show score and remaining lives
     def show_status(self):         
         self.pen.undo()
         msg = "Score: {}  Lives: {}".format(self.score, self.lives)
         self.pen.penup()
         self.pen.goto(-300, 310)
         self.pen.color("white")
         self.pen.write(msg, font=("Arial", 16, "normal"))

     def game_over(self):
         self.state = "gameover"

         # Play game-over sound
         sound_file = os.path.join(BASE_DIR, "fahh.mp3")
         subprocess.Popen(["afplay", sound_file])

         # Display Game Over message
         self.pen.clear()
         self.pen.penup()
         self.pen.color("red")
         self.pen.goto(0, 40)
         self.pen.write(
            "GAME OVER",
            align="center",
            font=("Arial", 32, "bold"))

         self.pen.goto(0, -10)
         self.pen.color("white")
         self.pen.write(
            "Final Score: {}".format(self.score),
            align="center",
            font=("Arial", 18, "normal"))

         self.pen.goto(0, -60)
         self.pen.color("yellow")
         self.pen.write("PLAY AGAIN? Press Y or N", align="center",font=("Arial", 18, "bold"))       


#Create game object
game = Game()

#Draw the game border
game.draw_border()

#Show the game status
game.show_status()

#Create my sprites
player = Player("triangle", "white", 0, 0)
#enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
#ally = Ally("square", "blue", 100, 0)

enemies =[]
for i in range(6):
    enemies.append(Enemy("circle", "red", -100, 0))

allies =[]
for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0))

#Restart Game when gameover
def restart_game():
    if game.state != "gameover":
        return

    # Reset game information
    game.score = 0
    game.lives = 3
    game.state = "playing"

    # Reset player
    player.goto(0, 0)
    player.setheading(0)
    player.speed = 4

    # Reset missile
    missile.status = "ready"
    missile.goto(-1000, 1000)

    # Reset enemies
    for enemy in enemies:
        enemy.goto(
            random.randint(-250, 250),
            random.randint(-250, 250)
        )
        enemy.setheading(random.randint(0, 360))

    # Reset allies
    for ally in allies:
        ally.goto(
            random.randint(-250, 250),
            random.randint(-250, 250)
        )
        ally.setheading(random.randint(0, 360))

    # Hide particles
    for particle in particles:
        particle.frame = 0
        particle.goto(-1000, -1000)

    # Redraw game screen
    game.pen.clear()
    game.draw_border()
    game.show_status()



#Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()
turtle.onkey(restart_game, "y")
turtle.onkey(restart_game, "Y")
turtle.onkey(turtle.bye, "n")
turtle.onkey(turtle.bye, "N")

#Main game loop
while True:
    turtle.update()
    time.sleep(0.04)

    if game.state == "playing":
        player.move()
        missile.move()

    for enemy in enemies:
        enemy.move()

        #Check for collision with the player
        if player.is_collision(enemy):
            #Play explosion sound
            sound_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"explode.mp3")
            subprocess.Popen(["afplay", sound_file]) 
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.lives -= 1
            game.score -= 100
            game.show_status()
            if game.lives <= 0:
                game.game_over()
                break

        #Check for collision between the missile & the enemy
        if missile.is_collision(enemy):
            #Play explosion sound
            sound_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"explode.mp3")
            subprocess.Popen(["afplay", sound_file])

            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            #Increase the score
            game.score += 100
            game.show_status()
            #Do the explosion
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    for ally in allies:
        ally.move()

        #Check for collision between the missile & ally
        if missile.is_collision(ally):
            #Play explosion sound
            sound_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"ahsound.mp3")
            subprocess.Popen(["afplay", sound_file])
            
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            #Decrease the score
            game.score -=50
            game.show_status()

    for particle in particles:
        particle.move()

turtle.done()