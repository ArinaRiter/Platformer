import pygame
pygame.init()

window = pygame.display.set_mode((800, 480))
clock = pygame.time.Clock()
background_image = pygame.image.load("background.png").convert()

platforms = []
frame_count = 0

pygame.mixer.music.load("music.ogg")

volume = 0.3
pygame.mixer.music.set_volume(volume)

# Воспроизведите музыку (повторить один раз)
pygame.mixer.music.play(1)

class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(255, 0, 0), image=None):
        # Инициализация атрибутов
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.gravity = 0
        self.isGrounded = False
        self.isLeft = False
        self.image = image
        self.imageR = pygame.image.load("IdleR.png")
        self.imageL = pygame.image.load("IdleL.png")
        self.image = self.imageR

        self.imageRunAnimationR = [10, pygame.image.load("Run_1R.png"),
                                   pygame.image.load("Run_2R.png"),
                                   pygame.image.load("Run_3R.png")]

        self.imageRunAnimationL = [10, pygame.image.load("Run_1L.png"),
                                   pygame.image.load("Run_2L.png"),
                                   pygame.image.load("Run_3L.png")]
        self.imageJumpAnimationR = [5, pygame.image.load("Jump_1R.png"),
                                    pygame.image.load("Jump_2R.png"),
                                    pygame.image.load("Jump_3R.png")]

        self.imageJumpAnimationL = [5, pygame.image.load("Jump_1L.png"),
                                    pygame.image.load("Jump_2L.png"),
                                    pygame.image.load("Jump_3L.png")]
    def animate(self):
        global frame_count
        # Увеличиваем счетчик кадров
        frame_count += 1
        if self.isLeft:
            # Выбираем кадр анимации в зависимости от счетчика кадров
            frame = frame_count // self.imageRunAnimationL[0] % len(self.imageRunAnimationL[1:])
            self.image = self.imageRunAnimationL[1:][frame]
        else:
            frame = frame_count // self.imageRunAnimationR[0] % len(self.imageRunAnimationR[1:])
            self.image = self.imageRunAnimationR[1:][frame]

    def animate_jump(self):
        global frame_count
        # Увеличиваем счетчик кадров
        frame_count += 1
        if self.isLeft:
            # Выбираем кадр анимации в зависимости от счетчика кадров
            frame = frame_count // self.imageJumpAnimationL[0] % len(self.imageJumpAnimationL[1:])
            self.image = self.imageJumpAnimationL[1:][frame]
        else:
            frame = frame_count // self.imageJumpAnimationR[0] % len(self.imageJumpAnimationR[1:])
            self.image = self.imageJumpAnimationR[1:][frame]
    def picture(self):
        if self.isLeft:
            return self.imageL
        else:
            return self.imageR
    def show(self):
        if not self.isGrounded:
            if self.isLeft:
                frame = frame_count // self.imageJumpAnimationL[0] % len(self.imageJumpAnimationL[1:])
                self.image = self.imageJumpAnimationL[1:][frame]
            else:
                frame = frame_count // self.imageJumpAnimationR[0] % len(self.imageJumpAnimationR[1:])
                self.image = self.imageJumpAnimationR[1:][frame]
            # Анимация бега
            if self.isLeft:
                frame = frame_count // self.imageRunAnimationL[0] % len(self.imageRunAnimationL[1:])
                self.image = self.imageRunAnimationL[1:][frame]
            else:
                frame = frame_count // self.imageRunAnimationR[0] % len(self.imageRunAnimationR[1:])
                self.image = self.imageRunAnimationR[1:][frame]
            self.gravity += 1
            self.rect.y += self.gravity
            coll = False
            for plat in platforms:
                if self.rect.colliderect(plat.rect):
                    self.isGrounded = True
                    self.rect.y -= self.gravity
                    self.gravity = 0
        else:
            self.rect.y += 1
            coll = False
            for plat in platforms:
                if self.rect.colliderect(plat.rect):
                    coll = True
            if not coll:
                self.isGrounded = False
            else:
                self.rect.y -= 1

        window.blit(self.image, (self.rect.x, self.rect.y))

clock = pygame.time.Clock()

class Platform():
    def __init__(self, x, y, width, height, color=(0, 200, 200)):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def show(self):
        self.rect.x = self.x
        pygame.draw.rect(window, self.color, self.rect)

player = Unit(30, 100, 50, 70, image=pygame.image.load("IdleR.png").convert_alpha())

platforms.append(Platform(0, 450, 150, 20))
platforms.append(Platform(200, 350, 200, 20))
platforms.append(Platform(500, 380, 80, 20))

class Finish():
    def __init__(self, x, y, width, height, image=None):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

    def show(self):
        self.rect.x = self.x
        window.blit(self.image, (self.rect.x, self.rect.y))

finish = Finish(520, 335, 50, 50, pygame.image.load("Point.png"))

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Платформер")


class Menu:
    def __init__(self):
        # Создать кнопку "Играть"
        self.play_button = pygame.Rect(250, 250, 120, 50)
        self.play_button_color = (0, 255, 0)
        self.play_button_text = "Играть"
        self.play_button_font = pygame.font.SysFont("Arial", 30)

    def draw(self, screen):
        # Нарисовать кнопку "Играть"
        pygame.draw.rect(screen, self.play_button_color, self.play_button)
        text_surface = self.play_button_font.render(self.play_button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.play_button.center)
        screen.blit(text_surface, text_rect)

class EndScreen:
    def __init__(self):
        self.play_button = pygame.Rect(250, 250, 200, 50)
        self.play_button_color = (255, 0, 0)
        self.play_button_text = "Вы Проиграли!"
        self.play_button_font = pygame.font.SysFont("Arial", 30)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, self.play_button_color, self.play_button)
        text_surface = self.play_button_font.render(self.play_button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.play_button.center)
        screen.blit(text_surface, text_rect)

class WinScreen:
    def __init__(self):
        self.play_button = pygame.Rect(250, 250, 200, 50)
        self.play_button_color = (0, 255, 0)
        self.play_button_text = "Победа!"
        self.play_button_font = pygame.font.SysFont("Arial", 30)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, self.play_button_color, self.play_button)
        text_surface = self.play_button_font.render(self.play_button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.play_button.center)
        screen.blit(text_surface, text_rect)

class Enemy():
    def __init__(self, x, y, width, height, image=None):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

    def show(self):
        self.rect.x = self.x
        window.blit(self.image, (self.rect.x, self.rect.y))


endscreen = EndScreen()
winscreen = WinScreen()

enemy = Enemy(260, 280, 20, 20, image=pygame.image.load("Enemy.png").convert_alpha())

menu = Menu()
run = True
gaming = False

while run:

    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    if not gaming:
        menu.draw(screen)
        if e.type == pygame.MOUSEBUTTONDOWN:
            gaming = True
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                volume += 0.1
                if volume > 1.0:
                    volume = 1.0
                pygame.mixer.music.set_volume(volume)
            elif e.key == pygame.K_DOWN:
                volume -= 0.1
                if volume < 0.0:
                    volume = 0.0
                pygame.mixer.music.set_volume(volume)
        pygame.display.update()

    else:
        window.blit(background_image, (0, 0))

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                if player.isGrounded:
                    player.rect.y -= 1
                    player.gravity = -15
                    player.animate_jump()

        for platform in platforms:
            platform.show()

        finish.show()
        enemy.show()

        keys = pygame.key.get_pressed()

        if player.rect.x < 0 or player.rect.x > 800 - player.rect.width or player.rect.y < 0 or player.rect.y > 480 - player.rect.height:
            endscreen.draw(screen)
            player.image.set_alpha(0)

        elif pygame.sprite.collide_rect(player, enemy):
            endscreen.draw(screen)
            player.image.set_alpha(0)


        elif player.rect.colliderect(finish.rect) and not pygame.sprite.collide_rect(player, enemy):
            winscreen.draw(screen)
            player.image.set_alpha(0)

        elif keys[pygame.K_LEFT]:
            player.rect.x -= 5
            player.isLeft = True
            player.animate()

        elif keys[pygame.K_RIGHT]:
            player.rect.x += 5
            player.isLeft = False
            player.animate()

        player.show()
        pygame.display.update()

pygame.quit()