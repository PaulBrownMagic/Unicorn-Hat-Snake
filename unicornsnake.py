''' -----------------------------
Classic game of snake written
for the Pimoroni Unicorn Hat
using the pygame library.

Authored by Paul Brown, Dec 2014
-------------------------------'''

import unicornhat as unicorn
from random import randint
import time, pygame

'''
To Do:
add sound for eating,
background image for play,
'''
# -- CONSTANTS
#set the fps, which determines the speed of the snake
SPEED = 5
#screen size, used for pygame input events and to display instructions 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450
#colours     r       g     b
BLACK =  (    0,     0,     0)
WHITE = ( 255, 255, 255)
GREEN = (     0, 255,     0)
RED =     ( 255,     0,      0)
BLUE = (     0,       0,  255)
YELLOW =(255, 255,    0)
PURPLE = (255,    0, 255)
CYAN =   (     0, 255, 255)
COLOURS = (GREEN, RED, BLUE, YELLOW, PURPLE, CYAN)

# --- CLASSES
#snake class for player
class Snake():
    #attributes
    body_list = None #snake segmant locations
    change_x = None #movement on x-axis
    change_y = None #movement on y-axis
    eaten = None #has the snake eaten some food?
    g_over = False #holds value for game over if snake goes off the screen or eats itself
#methods
    def __init__(self):
        self.body_list = [[2,1],[2,2]] #starting location
        self.change_x = 1
        self.change_y = 0
        self.eaten = False
    def update(self, food):
        #remove old segmant
        old_segmant=self.body_list.pop()
        self.eaten = False
        #find new segmant
        x = self.body_list[0][0] + self.change_x
        y = self.body_list[0][1] + self.change_y
        segmant = [x,y]
        self.body_list.insert(0, segmant)
        #check for eaten food
        if segmant[0] == food.x_pos and segmant[1] == food.y_pos:
            unicorn.set_pixel(old_segmant[0],old_segmant[1],food.r,food.g,food.b)
            self.body_list.append(old_segmant)
            self.eaten = True
            unicorn.show() # this makes the new segmant quickly glisten with the food colour
        else:
            unicorn.set_pixel(old_segmant[0],old_segmant[1],BLACK[0],BLACK[1],BLACK[2])
        #prepare segmants for display on unicorn hat, use try to prevent exception from crashing the game
        for segmant in self.body_list:
            try:
                unicorn.set_pixel(segmant[0],segmant[1],WHITE[0],WHITE[1],WHITE[2])
            except:
                self.g_over = True
    #movement controls
    def go_left(self):
        self.change_x = 1
        self.change_y = 0
    def go_right(self):
        self.change_x = -1
        self.change_y = 0
    def go_up(self):
        self.change_x = 0
        self.change_y = 1
    def go_down(self):
        self.change_x = 0
        self.change_y = -1
    #check for game over, returned to game class
    def game_over(self):
        if self.body_list[0] in self.body_list[1::] or self.g_over == True:
            return True
        return False

#Class for food
class Food():
    #attributes
    eaten = None
    x_pos = None
    y_pos = None
    r = None
    g = None
    b = None
#methods
    def __init__(self):
        self.eaten = True #set to true so that it is reset at start

    def update(self, snake):
        if self.eaten:
            #inside checks to ensure food isn't draw in the same location as the snakes body
            inside = True
            while inside:
                self.x_pos = randint(0,7)
                self.y_pos = randint(0,7)
                if [self.x_pos, self.y_pos] in snake.body_list:
                    inside = True
                else:
                    inside = False
            #give food a random colour from list of colours. List ensures visible strong colours
            colour = randint(0,len(COLOURS)-1)
            self.r = COLOURS[colour][0]
            self.g = COLOURS[colour][1]
            self.b = COLOURS[colour][2]
        #prepare for display on unicorn hat    
        unicorn.set_pixel(self.x_pos,self.y_pos,self.r,self.g,self.b)
        self.eaten = False

#game class
class Game(object):
    #attributes
    snake = None
    food = None
    game_over = None
    start = True #used to start the game in the same conditions as game over
#methods
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True #exits main game loop
            if event.type == pygame.KEYDOWN and (self.game_over or self.start):
                #start or restart the game
                self.__init__()
                self.start = False
            if event.type == pygame.KEYDOWN:
                #movement
                if event.key == pygame.K_LEFT and self.snake.change_x != -1:
                    self.snake.go_left()
                if event.key == pygame.K_RIGHT and self.snake.change_x != 1:
                    self.snake.go_right()
                if event.key == pygame.K_UP and self.snake.change_y != -1:
                    self.snake.go_up()
                if event.key == pygame.K_DOWN and self.snake.change_y != 1:
                    self.snake.go_down()
        return False #stay in main game loop

    def run_logic(self):
        #check for game over first
        self.game_over = self.snake.game_over()
        #only if it is not the first game and not game over update the food and snake
        if not self.game_over and not self.start:
            self.food.update(self.snake)
            self.snake.update(self.food)
            self.food.eaten = self.snake.eaten

    def display_frame(self, screen):
        #screen used to display information to the player, also required to detect pygame events
        #Unicorn hat display is also handled here
        if self.game_over or self.start:
            screen.fill(WHITE)
            font = pygame.font.SysFont('serif', 25)
            title = font.render('Unicorn Snake.', True, BLACK)
            text = font.render('Press any key to play.', True, BLACK)
            instructions = font.render('Use the arrow keys to control your snake on the unicorn hat', True, BLACK)
            title_center_x = (SCREEN_WIDTH // 2) - (title.get_width() // 2)
            text_center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            instructions_center_x = (SCREEN_WIDTH // 2) - (instructions.get_width() // 2)
            top_y = title.get_height() * 2
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            bottom_y = SCREEN_HEIGHT - (instructions.get_height() * 2)
            screen.blit( title, [title_center_x, top_y] )
            screen.blit( text, [text_center_x, center_y] )
            screen.blit( instructions, [instructions_center_x, bottom_y] )
            unicorn.clear() # removes last snake image from unicorn hat
        else:
            screen.fill(BLACK)
            font = pygame.font.SysFont('serif', 25)
            title = font.render('Unicorn Snake.', True, WHITE)
            text = font.render('Game on', True, WHITE)
            title_center_x = (SCREEN_WIDTH // 2) - (title.get_width() // 2)
            text_center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            top_y = title.get_height() * 2
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit( title, [title_center_x, top_y] )
            screen.blit( text, [text_center_x, center_y] )
            unicorn.show() # display the snake and food on the unicorn hat

        pygame.display.flip()

#main game function and loop
def main():
    pygame.init()

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('Unicorn Snake')

    done = False
    clock = pygame.time.Clock()

    game = Game()
    
    while not done:
        done = game.process_events()

        game.run_logic()

        game.display_frame(screen)

        clock.tick(SPEED)

    pygame.quit()

if __name__ == '__main__':
    main()
