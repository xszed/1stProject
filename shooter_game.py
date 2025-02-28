from pygame import *
from random import randint
import time as ticktime
#screen set-up
window = display.set_mode((700, 500))
display.set_caption("Shooter / Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700,500))
keys_pressed = key.get_pressed()
#value's;
num_fire = 0
lost = 0
points = 0
hurt = 3

Reloading = False
rel_time = False


class GameSprite(sprite.Sprite):
    """Main constructor for sprites"""
    def __init__(self, player_image, player_x, player_y, player_speed, size_1, size_2):
        super().__init__() # ! making method a super method
        self.image = transform.scale(image.load(player_image), (size_1, size_2)) #sprite image
        self.speed = player_speed #speed

        """Coordinates of the player """
        self.rect = self.image.get_rect() #getting coords
        self.rect.x = player_x #x
        self.rect.y = player_y #y
    
    def reset(self): 
        """showing sprite on the point with setted coordinates"""
        window.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
    """Movement system for the player."""
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] or keys_pressed[K_a] and self.rect.x >= 50:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] or keys_pressed[K_d] and self.rect.x <= 650:
            self.rect.x += self.speed

    def fire(self):
        """player shooting"""
        bullet = Bullet("bullet.png", self.rect.x+22, self.rect.y, 4, 20, 20)
        bullets.add(bullet)



            
class Enemy(GameSprite):
    """Infinity movement down for the Enemy"""
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 490:
            self.rect.y = 0
            self.rect.x = randint(50, 650)
            lost = lost + 1



class Asteroids1(GameSprite):
    """Infinity movement down for the Enemy"""
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 490:
            self.rect.y = 0
            self.rect.x = randint(10, 650)




class Bullet(GameSprite): 
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()


        


"""music"""
mixer.init() #music sys
mixer.music.load("space.ogg") #what music to load
mixer.music.play() #turn on space.ogg
fire = mixer.Sound('fire.ogg') #sound @fire.ogg for bullets
"""font"""
font.init() #font sys
font1 = font.SysFont("Arial", 36) #default font


"""Charracters"""
#Main Players
sprite_player = Player("rocket.png", 325, 400, 4, 80, 100) 

#Monsters - 
monsters = sprite.Group() #Creating group
def spawning_mobs(ammount):
    for i in range(ammount):
        sprite_enemy = Enemy("ufo.png", randint(50, 450), 100, randint(1, 3), 80, 100)
        monsters.add(sprite_enemy)

asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroids1 ("asteroid.png", randint(50, 500), 100, randint(1, 3), 80, 100)
    asteroids.add(asteroid)

bullets = sprite.Group()

clock = time.Clock()
FPS = 60 #FPS
finish = False
run = True
spawning_mobs(2)
while run:
    for e in event.get():    #Key event
        if e.type == KEYDOWN: #Key down
            if e.key == K_SPACE: #if key = space

                if num_fire < 5 and not Reloading: # if numfire lower than 5
                    sprite_player.fire() #shooting
                    num_fire += 1 #numfire +1
                    fire.play() #sound

                elif num_fire >= 5 and not Reloading:
                    rel_time = True
                    start_time = ticktime.time()
                    

        elif e.type == QUIT:
           run = False
    
    if finish != True:
                    
        """Text's"""
        text_lose = font1.render(
            "Пропущено: " + str(lost), 1, (255, 255, 255)
        )
        text_points = font1.render(
            "Счет: " + str(points), 1, (255, 255, 255)
        )
        text_hurt = font1.render(
            "HP: " + str(hurt), 1, (136, 8, 8)
        )

        window.blit(background,(0,0)) #background
        sprite_player.update()
        monsters.update()
        asteroids.update()
        sprite_player.reset()
        asteroids.draw(window)
        monsters.draw(window)

        window.blit(text_points, (30, 50))
        window.blit(text_lose, (30, 80))
        window.blit(text_hurt, (600, 50))
        bullets.update()
        bullets.draw(window)

        """Collision check"""
        enemy_collision_bullet = sprite.groupcollide(monsters, bullets, True, True) #collision list
        enemy_collision_player = sprite.spritecollide(sprite_player, monsters, True) #collision list
        asteroid_collission = sprite.spritecollide(sprite_player, asteroids, True) #collision list
        if enemy_collision_player: #checking if player collided with player
            lost += 1
            hurt -= 1
        if enemy_collision_bullet: #checking if enemy collided with the bullet
            points += 1
            spawning_mobs(1)
        if asteroid_collission: #Checking if player collided with asteroid
            hurt -= 1

        if rel_time == True:
            end_time = ticktime.time()
            total = end_time - start_time
            print(start_time)
            if total < 1:
                text_reload = font1.render("wait, reloading...", 1, (255, 255, 255))
                window.blit(text_reload, (100,100))
            else:
                rel_time = False
                num_fire = 0
                print(1)
                
        
        #Win/Lose
        if lost >= 5 or hurt <= 0:
            lost1 = font1.render(
            "Вы проиграли!", 1, (255, 255, 255))
            window.blit(lost1, (150, 150))
            finish = True
        elif points >= 10:
            win1 = font1.render(
            "Вы Выиграли!", 1, (175, 225, 175))
            window.blit(win1, (150, 150)) 
            finish = True
    #Other setup options        
    display.update()
    clock.tick(FPS)