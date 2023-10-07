from pygame import *

class GameSprite(sprite.Sprite):

    def __init__(self,player_image,player_x,player_y,size_x,size_y):

        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x,size_y))

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_x_speed,player_y_speed):

        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,
                                     p.rect.right)  # если коснулись нескольких стен, то левый край - максимальный
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # идем вниз
            for p in platforms_touched:
                self.y_speed = 0
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:  # идем вверх
            for p in platforms_touched:
                self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                self.rect.top = max(self.rect.top,
                                    p.rect.bottom)  # выравниваем верхний край по нижним краям стенок, на которые наехали

    def fire(self):
        bullet = Bullet("virus.png",self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = "left"
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):

        GameSprite.__init__(self,player_image,player_x,player_y,size_x,size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):

        GameSprite.__init__(self,player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed

        if self.rect.x > win_width + 10:
            self.kill()

win_width = 700
win_height = 500

display.set_caption('Лабиринт')
window = display.set_mode((win_width,win_height))
window.fill((119, 210, 223))



barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

w1 = GameSprite('brick-wall - Copy.png', win_width/2 - win_width/3, win_height/2,300,50)
w2 = GameSprite('brick-wall - Copy.png', 370,100,50,400)

barriers.add(w1)
barriers.add(w2)

packman = Player('bread.png',5,win_height - 80,80,80,0,0)
final_sprite = GameSprite('pryanik.png',win_width - 85,win_height - 100,80,80)

monster1 = Enemy('rolls.png',win_width - 80,150,80,80,5)
monster2 = Enemy('rolls.png',win_width - 80,150,80,80, 5)

monsters.add(monster1)
monsters.add(monster2)

back = (250, 250, 255)

finish = False
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if not finish:
        window.fill(back)

        packman.update()
        bullets.update()

        packman.reset()

        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()

        sprite.groupcollide(monsters, bullets,True,True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, monsters, True, False)

        if sprite.spritecollide(packman,monsters,False):
            finish = True
            ing = image.load('ю дэд.jpg')
            d = ing.get_width() // ing.get_height()
            window.fill((255,255,255))
            window.blit(transform.scale(ing,(win_height + d, win_height)),(90,0))

        if sprite.collide_rect (packman,final_sprite):
            finish = True
            ing = image.load('ю вииин.jpg')
            d = ing.get_width() // ing.get_height()
            window.fill((255,255,255))
            window.blit(transform.scale(ing,(win_width,win_height)),(0,0))
    display.update()

