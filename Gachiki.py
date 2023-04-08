from pygame import *
from time import sleep
from random import randint

window = display.set_mode((700,500))
display.set_caption('Gachiki 2')

background = transform.scale(image.load('gachi_fon.jpg'), (700,500))
death = transform.scale(image.load('Borba.jpeg'), (700,500))
win = transform.scale(image.load('drink.jpg'), (700,500))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('Gachi.mp3')
mixer.music.play()
takeitboy = mixer.Sound('take-it-boy.mp3')
turnson = mixer.Sound('that-turns-me-on.mp3')
spank = mixer.Sound('spank.mp3')
kingdom = mixer.Sound('demons.mp3')
swallow = mixer.Sound('swallow.mp3')

bullets = sprite.Group()
s_bullets = sprite.Group()



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50,50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_a] and self.rect.x>0:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x<650:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('white.png', 10, self.rect.x, self.rect.top)
        bullets.add(bullet)

    def super_fire(self):
        super_bullet = Bullet('blue.png', 8, self.rect.x, self.rect.top)
        s_bullets.add(super_bullet)
            
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            global lost
            self.rect.x = randint(0,650)
            self.rect.y = -50
            lost += 1

class Other(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(0,650)
            self.rect.y = -50

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



score = 0
lost = 0
lives = 15
count = 0

van = Player('gachi.png', 10, 350, 400)

gachiki = sprite.Group()
for i in range(5):
    gachik = Enemy('gachi2.png', 3, randint(0,650), randint(-300,0))
    gachiki.add(gachik)

preps = sprite.Group()
for i in range(3):
    prep = Other('no-porn.png', 5, randint(0,650), randint(-300,0))
    preps.add(prep)

health = sprite.Group()
for i in range(1):
    milk = Other('milk.png', 2, randint(0,650), randint(-300,0))
    health.add(milk)

armors = sprite.Group()
for i in range(1):
    armor_s = Other('cap.png', 2, randint(0,650), randint(-300,0))
    armors.add(armor_s)

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 96)

van_run = True
armor = False
armor_count = 0



run = True
while run:

    if count != 300:
        count += 1

    text_score = font1.render('Cum inside: ' + str(score), 1, (255,255,255))
    text_lost = font1.render('Убежало: ' + str(lost), 1, (255,255,255))
    text_lives = font2.render(str(lives), 1, (255,255,255))
    text_count = font1.render('Заряд: ' + str(count), 1, (255,255,255))
    text_win = font1.render('YOU WIN!', 1, (255,255,255))
    text_lose = font1.render('YOU LOSE!', 1, (255,255,255))
    text_armor = font1.render('Броня: ' + str(armor_count) + ' сек.', 1, (255,255,255))

    window.blit(background, (0,0))
    window.blit(text_score, (10,10))
    window.blit(text_lost, (10,50))
    window.blit(text_lives, (600,0))
    window.blit(text_count, (550,470))
    s_bullets.draw(window)
    bullets.draw(window)
    gachiki.draw(window)
    preps.draw(window)
    health.draw(window)
    armors.draw(window)
    van.reset()


    if van_run:
        gachiki.update()
        van.update()
        bullets.update()
        preps.update()
        health.update()
        s_bullets.update()
        armors.update()

    if sprite.spritecollide(van, armors, True):
        armor_s = Other('cap.png', 2, randint(0,650), randint(-300,0))
        armors.add(armor_s)
        armor_count = 100
        armor = True

    if armor_count != 0:
        armor_count -= 1
        window.blit(text_armor, (20,470))
    elif armor_count <= 0:
        armor = False

    if armor == False:

        if sprite.spritecollide(van, gachiki, True):
            lives -= 1
            takeitboy.play()
            gachik = Enemy('gachi2.png', 5, randint(0,650), randint(-300,0))
            gachiki.add(gachik)

        if sprite.spritecollide(van, preps, True):
            lives -= 1
            takeitboy.play()
            prep = Other('no-porn.png', 5, randint(0,650), randint(-300,0))
            preps.add(prep)

    if sprite.spritecollide(van, health, True):
        lives += 1
        swallow.play()
        milk = Other('milk.png', 2, randint(0,650), randint(-300,0))
        health.add(milk)

    if sprite.groupcollide(gachiki, bullets, True, True):
        spank.play()
        gachik = Enemy('gachi2.png', 5, randint(20,620), randint(-300,0))
        gachiki.add(gachik)
        score += 1

    if sprite.groupcollide(preps, s_bullets, True, False):
        prep = Other('no-porn.png', 5, randint(0,650), randint(-300,0))
        preps.add(prep)
        score += 1

    if sprite.groupcollide(gachiki, s_bullets, True, False):
        gachik = Enemy('gachi2.png', 5, randint(20,620), randint(-300,0))
        gachiki.add(gachik)
        score += 1

    if sprite.groupcollide(preps, bullets, False, True):
        score += 1

    if score >= 100:
        window.blit(win, (0,0))
        window.blit(text_win, (300,20))
        van_run = False

    if lives <= 0:
        window.blit(death, (0,0))
        window.blit(text_lose, (280,20))
        van_run = False



    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                van.fire()
            if count >= 300:
                if e.key == K_LSHIFT:
                    kingdom.play()
                    van.super_fire()
                    count = 0

    clock.tick(FPS)
    display.update()