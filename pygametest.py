import pygame
import os
import random
import sys
import time
from pygame.math import Vector2 as V2
from pygame import mixer

pygame.mixer.init()
music=pygame.mixer.music.load("db.wav")
pygame.mixer.music.play(-1)

FPS=60

CELL_SIZE,CELL_NUMBER=15,30

WIDTH,HEIGHT=CELL_SIZE*CELL_NUMBER,CELL_SIZE*CELL_NUMBER
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SNAKE!")

GREEN=(0,255,0)
BLACK=(0,0,0)
RED=(255,0,0)

SNAKE_START_SIZE=10
START_SPEED=150

EATING_SOUND=pygame.mixer.Sound("eating_sound.wav")
GAME_OVER_SOUND=pygame.mixer.Sound("game_over_sound.wav")

class Fruit:
    def __init__(self,body):
        body_x=[x.x for x in body]
        body_y=[y.y for y in body]

        self.x=random.choice([x for x in range(CELL_NUMBER) if x not in body_x])
        self.y=random.choice([y for y in range(CELL_NUMBER) if y not in body_y])
#        self.x=random.randint(0,CELL_NUMBER-1)
#        self.y=random.randint(0,CELL_NUMBER-1)
        self.pos=V2(self.x,self.y)
    
    def draw_fruit(self):
        fruit_rect=pygame.Rect(self.pos.x*CELL_SIZE,self.pos.y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(WINDOW,RED,fruit_rect)
        return fruit_rect


class Snake:
    def __init__(self):
        x_start=random.randint(0,CELL_NUMBER-SNAKE_START_SIZE)
        y_start=random.randint(0,CELL_NUMBER-1)

        if x_start>CELL_NUMBER/2:
            dx=-1
            dy=0
        else:
            if y_start<CELL_NUMBER/2:
                dx=0
                dy=1
            else:
                dx=0
                dy=-1

        self.body=[V2(x_start+i,y_start) for i in range(SNAKE_START_SIZE)]
        self.direction=V2(dx,dy)
        self.points=0
        self.speed=START_SPEED

    def draw_snake(self):
        POINTS_FONT=pygame.font.SysFont("comicsans",40)
        for block in self.body:
            snake_rect=pygame.Rect(block.x*CELL_SIZE,block.y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
            pygame.draw.rect(WINDOW,GREEN,snake_rect)
        POINTS_TEXT=POINTS_FONT.render("Points: "+str(self.points),1,(255,255,255))
        WINDOW.blit(POINTS_TEXT,(0,0))

        return self.body

    def add_block(self):
        new_block=self.body[-1]-self.direction
        self.body.append(new_block)

    def update_snake(self,keys_pressed,start):
        if keys_pressed[pygame.K_w] and self.direction!=V2(0,1):
            self.direction=V2(0,-1)
            head=self.body[0]
            head=head+V2(0,-1)
            temp_snake=self.body[:-1]
            temp_snake.insert(0,head)
            self.body=temp_snake
        elif keys_pressed[pygame.K_a] and self.direction!=V2(1,0):
            self.direction=V2(-1,0)
            head=self.body[0]
            head=head+V2(-1,0)
            temp_snake=self.body[:-1]
            temp_snake.insert(0,head)
            self.body=temp_snake
        elif keys_pressed[pygame.K_s] and self.direction!=V2(0,-1):
            self.direction=V2(0,1)
            head=self.body[0]
            head=head+V2(0,1)
            temp_snake=self.body[:-1]
            temp_snake.insert(0,head)
            self.body=temp_snake
        elif keys_pressed[pygame.K_d] and self.direction!=V2(-1,0):
            self.direction=V2(1,0)
            head=self.body[0]
            head=head+V2(1,0)
            temp_snake=self.body[:-1]
            temp_snake.insert(0,head)
            self.body=temp_snake
        elif start==False:
            head=self.body[0]
            head=head+self.direction
            temp_snake=self.body[:-1]
            temp_snake.insert(0,head)
            self.body=temp_snake

    def collision_check(self,fruit_rect):
        for blk in self.body[1:]:
            if blk==self.body[0]:
                return "END"

        for block in self.body:
            block_rect=pygame.Rect(block.x*CELL_SIZE,block.y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
            if WIDTH<block.x*CELL_SIZE or block.x*CELL_SIZE<0 or HEIGHT<block.y*CELL_SIZE or block.y*CELL_SIZE<0:
                return "END"

            if block_rect.colliderect(fruit_rect):
                return False
            else:
                return True

    def add_points(self):
        self.points+=1

    def add_speed(self,SCREEN_UPDATE):
        if self.speed>30:
            self.speed-=2
            pygame.time.set_timer(SCREEN_UPDATE,self.speed)

def game_over_screen():
    FONT=pygame.font.SysFont("comicsansms",50)
    GAME_OVER_TEXT=FONT.render("GAME OVER!",1,(255,255,255))
    WINDOW.blit(GAME_OVER_TEXT,(WIDTH/2-GAME_OVER_TEXT.get_width()/2,HEIGHT/2-GAME_OVER_TEXT.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)





def main():
    pygame.init()



    SCREEN_UPDATE=pygame.USEREVENT
    clock=pygame.time.Clock()


    snake=Snake()
    body=snake.draw_snake()
    fruit=Fruit(body)

    start=True

    while True:
        clock.tick(FPS)
        keys_pressed=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==SCREEN_UPDATE and start==False:
                snake.update_snake(keys_pressed,start)

        if start==True:
            pygame.time.set_timer(SCREEN_UPDATE,0)
            t=3
            COUNT_FONT=pygame.font.SysFont("comicsansms",30)
            for i in range(3):
                WINDOW.fill(BLACK)
                fruit_rect=fruit.draw_fruit()
                body=snake.draw_snake()
                fruit_state=snake.collision_check(fruit_rect)

                COUNT_TEXT=COUNT_FONT.render("Game starts in: "+str(t),1,(255,255,255))
                WINDOW.blit(COUNT_TEXT,(WIDTH/2-COUNT_TEXT.get_width()/2,HEIGHT/2-COUNT_TEXT.get_height()/2))
                pygame.display.update()
                pygame.time.delay(1000)
                t-=1
            start=False
            pygame.time.set_timer(SCREEN_UPDATE,START_SPEED)


        WINDOW.fill(BLACK)
        fruit_rect=fruit.draw_fruit()
        body=snake.draw_snake()
        fruit_state=snake.collision_check(fruit_rect)



        if fruit_state==False:
            EATING_SOUND.play()
            snake.add_points()
            snake.add_block()
            snake.add_speed(SCREEN_UPDATE)
            fruit=Fruit(body)
        elif fruit_state=="END":
            pygame.mixer.music.stop()
            GAME_OVER_SOUND.play()
            game_over_screen()
            pygame.mixer.music.play(-1)
            break
        pygame.display.update()
        

if __name__=="__main__":   
    while True:
        main()