import pygame
import random
from os import path


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def mes(msg,color,x,y,font_name,size):
    font_style = pygame.font.SysFont(font_name,size)
    mes1 = font_style.render(msg,True,color)
    dis.blit(mes1,[x,y])

def eating_check(xcor,ycor,foodx,foody):
    if foodx - snake_block <= xcor <= foodx + snake_block:
        if foody - snake_block <= ycor <= foody + snake_block:
            return True
    else:
        return False

def draw_head(i,snake_list):
    snake_head_img = head_img[i]
    snake_head = pygame.transform.scale(snake_head_img,(snake_block,snake_block))
    snake_head.set_colorkey(BLACK)
    snake_head_rect = snake_head.get_rect(x=snake_list[-1][0],y=snake_list[-1][1])
    dis.blit(snake_head,snake_head_rect)

def tail_draw(i,snake_list):
    snake_tail_img = tail_img[i]
    snake_tail = pygame.transform.scale(snake_tail_img,(snake_block,snake_block))
    snake_tail.set_colorkey(WHITE)
    snake_tail_rect = snake_tail.get_rect(x=snake_list[0][0],y=snake_list[0][1])
    dis.blit(snake_tail,snake_tail_rect)



width = 800
height = 600
pygame.init()
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('змейка')
clock = pygame.time.Clock()
FPS = 5

snake_block = 30
snake_step = 30


dir = path.join(path.dirname(__file__),'snake')
pygame.mixer.music.load(path.join(dir,'2.mp3'))
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)
am = pygame.mixer.Sound(path.join(dir,'1.ogg'))
am.set_volume(0.5)
b = pygame.mixer.Sound(path.join(dir,'3.ogg'))
b.set_volume(0.5)

bg = pygame.image.load(path.join(dir,'фон.jpg')).convert()
bg = pygame.transform.scale(bg,(width,height))
bg_rect = bg.get_rect()

food_img = [
    pygame.image.load(path.join(dir,'арбух.png')).convert(),
    pygame.image.load(path.join(dir,'банан.png')).convert(),
    pygame.image.load(path.join(dir,'виноград.png')).convert(),
    pygame.image.load(path.join(dir,'вишня.png')).convert(),
    pygame.image.load(path.join(dir,'клубника.png')).convert(),
    pygame.image.load(path.join(dir,'яблоко.png')).convert()
]

head_img = [
    pygame.image.load(path.join(dir,'hl.png')).convert(),
    pygame.image.load(path.join(dir,'hr.png')).convert(),
    pygame.image.load(path.join(dir,'hu.png')).convert(),
    pygame.image.load(path.join(dir,'hd.png')).convert()
]

tail_img = [
    pygame.image.load(path.join(dir,'tl.png')).convert(),
    pygame.image.load(path.join(dir,'tr.png')).convert(),
    pygame.image.load(path.join(dir,'tu.png')).convert(),
    pygame.image.load(path.join(dir,'td.png')).convert()
]


def play():
    i = 0
    foodx = random.randrange(0, width - snake_block)
    foody = random.randrange(0, height - snake_block)
    food = pygame.transform.scale(random.choice(food_img),(snake_block,snake_block))
    food.set_colorkey(WHITE)
    food_rect = food.get_rect(x=foodx,y=foody)
    snake_list = []
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    length = 2
    run = True
    game_close = False
    while run:
        while game_close:
            dis.fill(RED)
            mes('Вы проиграли',WHITE,250,200,'Arial',50)
            mes('Нажмите q для выхода или e для повторной игры', WHITE, 20, 300, 'Arial', 40)
            mes(f'текущий счёт: {length - 2}',WHITE,275,250, 'Arial', 40)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_close = False
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = False
                        run = False
                    elif event.key == pygame.K_e:
                        play()
        clock.tick(FPS)
        dis.fill(GREEN)
        dis.blit(bg,bg_rect)
        dis.blit(food,food_rect)
       #pygame.draw.rect(dis,RED,[foodx,foody,snake_block,snake_block])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change -= snake_step
                    y1_change = 0
                    i = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_step
                    y1_change = 0
                    i = 1
                if event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change -= snake_step
                    i = 2
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_step
                    i = 3
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
            b.play()


        x1 += x1_change
        y1 += y1_change

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]
        for k in snake_list[1:-1]:
            if k == snake_head:
                game_close = True
        for x in snake_list[1:]:
           # pygame.draw.rect(dis, BLACK, [x[0], x[1], snake_block, snake_block])
            snake_imd = pygame.image.load(path.join(dir,'b.png')).convert()
            snake = pygame.transform.scale(snake_imd,(snake_block,snake_block))
            snake.set_colorkey(WHITE)
            dis.blit(snake,(x[0],x[1]))
        draw_head(i,snake_list)
        if length > 2:
            tail_draw(i,snake_list)
        mes(f'текущий счёт: {length - 2}',RED,650,10, 'Arial', 20)
        if eating_check(x1,y1,foodx,foody):
            foodx = random.randrange(0, width - snake_block)
            foody = random.randrange(0, height - snake_block)
            food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
            food.set_colorkey(WHITE)
            food_rect = food.get_rect(x=foodx, y=foody)
            length += 1
            am.play()


        pygame.display.flip()
        pygame.display.update()
play()