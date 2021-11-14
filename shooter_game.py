from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((700, 500))
display.set_caption(".")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
FPS = 144
score = 0
lost = 0 

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, playerx_size, playery_size, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (playerx_size, playery_size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 20, 25, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 530:
            self.rect.y = self.rect.y + self.speed
        else:
            self.rect.y = -10
            self.rect.x = randint(20, 450)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

players = sprite.Group()
player = Player("rocket.png", 65, 65, 350, 400, 10)
players.add(player)

monsters = sprite.Group()
for i in range (1,6):
    monster = enemy("ufo.png",65, 65,randint(50,650),10,randint(1,3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,4):
    asteroid = enemy("asteroid.png", 65, 65, randint(50, 650), 10, 3)
    asteroids.add(asteroid)

bullets = sprite.Group()

font.init()
font = font.SysFont("Arial", 36)

num_fire = 0 
rel_time = False

game = True
while game:
    clock = time.Clock()
    clock.tick(FPS)

    player.update()
    monsters.update()
    bullets.update()
    asteroids.update()
    window.blit(background,(0, 0))

    players.draw(window)
    monsters.draw(window)
    bullets.draw(window)
    asteroids.draw(window)

    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
        score = score + 1 
        monster = enemy("ufo.png",65, 65,randint(50,650),10, 2)
        
    monsters.add(monster)

    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            
    if rel_time == True:
        now_time = timer()
        if now_time - last_time < 3:
            reload = font.render("Перезарядка", 1, (150,0,0))
            window.blit(reload, (200, 460))
        else:
            num_fire = 0
            rel_time = False
            
    if sprite.collide_rect(player, asteroid):
        lose = font.render("Поражение", 5, (150,0,0))
        window.blit(lose, (200, 200))     

    key_pressed = key.get_pressed()
    text = font.render("Пропущено: " + str(lost), 1, (255,255,255))
    text1 = font.render("Счёт: " + str(score), 1, (255,255,255))
    window.blit(text, (10,50))
    window.blit(text1, (10, 20))   
           
    display.update() 
    time.delay(30)

