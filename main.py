# Ball Catcher - Chytač míčů
import pygame
import random


# Inicializace hry
pygame.init()

# Obrazovka
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball catcher")

# Nastavení hry
clock = pygame.time.Clock()
fps = 60

# Barvy
green = (14, 116, 0)

# Classy
class Game:
    # constructor
    def __init__(self, our_player, set_of_balls):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.slow_down_cycle = 0

        self.our_player = our_player
        self.set_of_balls = set_of_balls

        # Hudba v pozadí
        pygame.mixer.music.load("media/bg-music-bc.mp3")
        pygame.mixer.music.play(-1, 0.0)

        # fonty
        self.ball_font = pygame.font.Font("fonts/ball-c.ttf", 24)
        self.middle_ball_font = pygame.font.Font("fonts/ball-c.ttf", 60)
        self.large_ball_font = pygame.font.Font("fonts/ball-c.ttf", 100)


        # Obrázky
        soccer_image = pygame.image.load("img/soccer-ball.png")
        baseball_image = pygame.image.load("img/baseball-ball.png")
        football_image = pygame.image.load("img/football-ball.png")
        basketball_image = pygame.image.load("img/basketball-ball.png")

        self.ball_images = [soccer_image, baseball_image, football_image, basketball_image]

        # generujeme míč, který chceme chytit
        self.ball_catch_type = random.randint(0, 3)
        self.ball_catch_image = self.ball_images[self.ball_catch_type]
        self.ball_catch_image_rect = self.ball_catch_image.get_rect()
        self.ball_catch_image_rect.centerx = (width//2)
        self.ball_catch_image_rect.top = 45

    # Kód, který je opětovně volán
    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == fps:
            self.round_time += 1
            self.slow_down_cycle = 0

        # kontrola kolize
        self.check_collisions()

        # vykreslení na obrazovku
        self.draw()

    # Vykresluje vše ve hře - texty, hledaný míč
    def draw(self):
        white = (255, 255, 255)
        red = (155, 12, 12)
        brown = (58, 33, 18)
        dark_orange = (193, 92, 3)
        grey = (120, 120, 120)
        colors = [white, red, brown, dark_orange]

        # Nastavení textu
        catch_text = self.ball_font.render("Catch the ball", True, white)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = width//2
        catch_text_rect.top = 5

        score_text = self.ball_font.render(f"Score: {self.score}", True, white)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, 4)

        lives_text = self.ball_font.render(f"Lives: {self.our_player.lives}", True, white)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (10, 30)

        round_text = self.ball_font.render(f"Round: {self.round_number}", True, white)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (10, 60)

        time_text = self.ball_font.render(f"Round Time: {self.round_time}", True, white)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (width - 10, 5)

        # Počet, kolikrát se může hráč vrátit do bezpečné zóny
        back_safe_zone_text = self.ball_font.render(f"Safe Zone Returns: {self.our_player.enter_safe_zone}", True, white)
        back_safe_zone_text_rect = back_safe_zone_text.get_rect()
        back_safe_zone_text_rect.topright = (width - 10, 30)

        safe_zone_screen_text = self.middle_ball_font.render("SAFE ZONE", True, grey)
        safe_zone_screen_text_rect = safe_zone_screen_text.get_rect()
        safe_zone_screen_text_rect.center = (width//2, height - 50)

        press_space_text = self.ball_font.render("Press SPACE to get here", True, grey)
        press_space_text_rect = press_space_text.get_rect()
        press_space_text_rect.center = (180, height - 50)

        # Vykreslení (blitting) do obrazovky
        screen.blit(catch_text, catch_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text, lives_text_rect)
        screen.blit(round_text, round_text_rect)
        screen.blit(time_text, time_text_rect)
        screen.blit(back_safe_zone_text, back_safe_zone_text_rect)
        screen.blit(safe_zone_screen_text, safe_zone_screen_text_rect)
        screen.blit(press_space_text, press_space_text_rect)

        # Obrázek míče, který máme chytit
        screen.blit(self.ball_catch_image, self.ball_catch_image_rect)

        # Tvary

        # Vykreslení hřiště
        pygame.draw.line(screen, white, (width // 2, 100), (width // 2, height - 102), 4)
        pygame.draw.circle(screen, white, (width//2, 349), 80, 4)
        pygame.draw.rect(screen, white, (0, 200, 150, 300), 4)
        pygame.draw.rect(screen, white, (width - 150, 200, 150, 300), 4)
        pygame.draw.rect(screen, white, (0, 250, 60, 200), 4)
        pygame.draw.rect(screen, white, (width - 60, 250, 60, 200), 4)

        # Rámeček hřiště a zároveň herní plochy pro míče - kde se mohou míče pohybovat
        pygame.draw.rect(screen, colors[self.ball_catch_type], (0, 100, width, height - 200), 4)



        # Kontroluje kolizi hráče s míčem
    def check_collisions(self):
        # s jakým míčem jsme se srazili
        collided_ball = pygame.sprite.spritecollideany(self.our_player, self.set_of_balls)

        if collided_ball:
            # Srazili jsme se se správným míčem
            if collided_ball.type == self.ball_catch_type:
                # Přehrajeme zvuk správného chycení míče
                self.our_player.catch_sound.play()
                # Zvýšíme skóre
                self.score += 10 * self.round_number
                # Odstranění chyceného míče
                collided_ball.remove(self.set_of_balls)
                # Kontrola, zda ještě existují nějaké míče, které můžeme chytat
                if self.set_of_balls:
                    self.choose_new_target()
                else:
                    # Kolo je dokončené - všechny míče jsme chytili
                    self.our_player.reset()
                    self.start_new_round()
            else:
                self.our_player.wrong_sound.play()
                self.our_player.lives -= 1
                # kontrola, zda je hráč naživu - Konec hry
                if self.our_player.lives <= 0:
                    self.pause_game(f"Final Score: {self.score}", "Press ENTER if you want to play again")
                    self.reset_game()
                self.our_player.reset()


    # Zahájí nové kolo - s větším počtem míčů v herní ploše
    def start_new_round(self):
        # Při dokončení kola poskytneme bonus podle toho, jak rychle hráč kolo dokončí: dříve = více bodů
        self.score += int(100 * (self.round_number / (1 + self.round_time)))

        # Resetujeme hodnoty
        self.round_time = 0
        self.slow_down_cycle = 0
        self.round_number += 1
        self.our_player.enter_safe_zone += 1

        # Odebereme všechny míče, abychom mohli sadu naplnit novými míči
        for deleted_ball in self.set_of_balls:
            self.set_of_balls.remove(deleted_ball)

        # Naplníme sadu míčů novými míči
        for i in range(self.round_number):
            self.set_of_balls.add(Ball(random.randint(0, width - 64), random.randint(100, height-164), self.ball_images[0], 0))
            self.set_of_balls.add(
                Ball(random.randint(0, width - 64), random.randint(100, height - 164), self.ball_images[1], 1))
            self.set_of_balls.add(
                Ball(random.randint(0, width - 64), random.randint(100, height - 164), self.ball_images[2], 2))
            self.set_of_balls.add(
                Ball(random.randint(0, width - 64), random.randint(100, height - 164), self.ball_images[3], 3))

        # Vybíráme nový míč, který máme chytit
        self.choose_new_target()

    # Vybírá nový míč, který máme chytit
    def choose_new_target(self):
        new_ball_to_catch = random.choice(self.set_of_balls.sprites())
        self.ball_catch_type = new_ball_to_catch.type
        self.ball_catch_image = new_ball_to_catch.image

    # Pozastavení hry - pauza před zahájením nové hry, na začátku při spuštění
    def pause_game(self, main_text, subheading_text):

        global lets_continue

        # Nastavíme barvy
        white = (255, 255, 255)
        green = (14, 116, 0)

        # Hlavní text pro pauznutí
        main_text_create = self.large_ball_font.render(main_text, True, white)
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (width//2, height//2 - 50)

        # Vedlejší text pro pauznutí
        subheading_text_create = self.middle_ball_font.render(subheading_text, True, white)
        subheading_text_create_rect = subheading_text_create.get_rect()
        subheading_text_create_rect.center = (width//2, height//2 + 50)

        # Obrázky míčů
        soccer_ball_image = pygame.image.load("img/soccer-ball-big.png")
        soccer_ball_image_rect = soccer_ball_image.get_rect()
        soccer_ball_image_rect.center = (160, 120)

        baseball_ball_image = pygame.image.load("img/baseball-ball-big.png")
        baseball_ball_image_rect = baseball_ball_image.get_rect()
        baseball_ball_image_rect.center = (width-160, 120)

        football_ball_image = pygame.image.load("img/football-ball-big.png")
        football_ball_image_rect = football_ball_image.get_rect()
        football_ball_image_rect.center = (160, height-120)

        basketball_ball_image = pygame.image.load("img/basketball-ball-big.png")
        basketball_ball_image_rect = basketball_ball_image.get_rect()
        basketball_ball_image_rect.center = (width-160, height-120)

        # Zobrazení hlavního textu, podnadpisu a obrázků
        screen.fill(green)
        screen.blit(main_text_create, main_text_create_rect)
        screen.blit(subheading_text_create, subheading_text_create_rect)
        screen.blit(soccer_ball_image, soccer_ball_image_rect)
        screen.blit(baseball_ball_image, baseball_ball_image_rect)
        screen.blit(football_ball_image, football_ball_image_rect)
        screen.blit(basketball_ball_image, basketball_ball_image_rect)

        pygame.display.update()

        # Zastavení hry
        paused = True
        while paused:
            for one_event in pygame.event.get():
                if one_event.type == pygame.KEYDOWN:
                    if one_event.key == pygame.K_RETURN:
                        paused = False
                if one_event.type == pygame.QUIT:
                    paused = False
                    lets_continue = False

    # Resetuje hru do výchozího stavu
    def reset_game(self):
        self.score = 0
        self.round_number = 0
        self.our_player.lives = 5
        self.our_player.enter_safe_zone = 3
        self.start_new_round()

        # Spuštění muziky v pozadí
        pygame.mixer.music.play(-1, 0.0)


class Player(pygame.sprite.Sprite):
    # constructor
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.bottom = height

        # rychlost hráče
        self.lives = 5
        self.enter_safe_zone = 2
        self.speed = 8

        self.catch_sound = pygame.mixer.Sound("media/pick.wav")
        self.catch_sound.set_volume(0.3)

        self.wrong_sound = pygame.mixer.Sound("media/wrong.wav")
        self.wrong_sound.set_volume(0.5)

    # Kód který je opakovaně volán (updatován)
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < height:
            self.rect.y += self.speed
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < width:
            self.rect.x += self.speed

    # Návrat do bezpečné zóny
    def back_to_safe_zone(self):
        if self.enter_safe_zone > 0:
            self.enter_safe_zone -= 1
            self.rect.bottom = height

    # Vrací hráče zpět na výchozí pozici - doprostřed bezpečné zóny
    def reset(self):
        self.rect.centerx = width//2
        self.rect.bottom = height


class Ball(pygame.sprite.Sprite):
    # constructor
    def __init__(self, x, y, image, ball_type):
        super().__init__()
        # nahrajeme obrázek mozkomora a umístíme ho
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # typy míčů: 0 = fotbal(soccer), 1 = baseball, 2 = americký fotbal, 3 = basketbal
        self.type = ball_type

        # nastavení náhodného směru míče
        self.x = random.choice([-1, 1])
        self.y = random.choice([-1, 1])
        self.speed = random.randint(1, 5)


    # Kód který je opakovaně volán (updatován)
    def update(self):
        # pohyb míče
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed

        # odraz míče
        if self.rect.left < 0 or self.rect.right > width:
            self.x *= -1
        elif self.rect.bottom > height - 100 or self.rect.top < 100:
            self.y *= -1



# Sada míčů
ball_set = pygame.sprite.Group()


# Skupina hráčů
player_group = pygame.sprite.Group()
one_player = Player()
player_group.add(one_player)

# Nastavení proměnné k pokračování Hlavného cyklu
lets_continue = True

# Objekt Game
my_game = Game(one_player, ball_set)
my_game.pause_game("Ball Catcher", "Press ENTER to start the game")
my_game.start_new_round()

# Hlavní cyklus

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                one_player.back_to_safe_zone()

    # Vkládání zeleného pozadí (blitting)
    screen.fill(green)

    # Updatujeme objekt vytvořený podle classy Game
    my_game.update()

    # Updatujeme sadu míčů
    ball_set.draw(screen)
    ball_set.update()
    # Updatujeme skupinu hráčů (jeden hráč)
    player_group.draw(screen)
    player_group.update()


    # Update obrazovky
    pygame.display.update()

    # Zpomalení cyklu
    clock.tick(fps)

# Ukončení hry
pygame.quit()