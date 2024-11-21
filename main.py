import pygame
import random
import math  
from settings import *

pygame.init()
pygame.mixer.init()  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circus Escape")

font = pygame.font.Font(join('font', 'Carnevalee Freakshow.ttf'), 36)
story_font = pygame.font.Font(join('font', 'Carnevalee Freakshow.ttf'), 28)

background_img = pygame.image.load(join('image', 'background.jpg'))  

scene = 1
score = 0
balloons = []
level = 1  
time_limit = 10  
start_time = 0  
game_over = False
has_key = False  

dart_img = pygame.image.load(join('image', 'dart.png'))  
dart_img = pygame.transform.scale(dart_img, (180, 120))  
dart_rect = dart_img.get_rect()  

player_speed = 5
monster_speed = 3
player = pygame.Rect(100, 500, 50, 50)
monster = pygame.Rect(WIDTH - 100, 500, 50, 50)
key = pygame.Rect(400, 300, 30, 30)

blocks = [pygame.Rect(100, 300, 50, 50), pygame.Rect(WIDTH // 2, 300, 50, 50), pygame.Rect(WIDTH - 150, 300, 50, 50)]
hints = [63, 58]  
input_code = ''  
code_required = '6358'  

home_music = join('audio', 'test.mp3')
story_music = join('audio', 'test.mp3')
dart_game_music = join('audio', 'test.mp3')
horror_game_music = join('audio', 'horror.mp3')

suara_mbledos = pygame.mixer.Sound(join('audio', 'mbledos.mp3'))

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)  

def stop_music():
    pygame.mixer.music.stop()  

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) * 2 + (point1[1] - point2[1]) * 2)

def show_home_screen():
    screen.blit(background_img, (0, 0))  
    title = font.render("Circus Escape", True, BLACK)
    screen.blit(title, (WIDTH // 2 - 100, HEIGHT // 2 - 100))

    start_text = font.render("Press ENTER to Start", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - 150, HEIGHT // 2))

    pygame.display.flip()

def show_story_1():
    screen.fill(WHITE)
    story_lines = [
        "You are on your way to the famous circus in town.",
        "While walking through the entrance, you notice a game booth.",
        "You decide to try your luck at the Balloon Dart game.",
        "Press SPACE to start the game."
    ]

    for i, line in enumerate(story_lines):
        story_text = story_font.render(line, True, BLACK)
        screen.blit(story_text, (50, 100 + i * 40))

    pygame.display.flip()

def balloon_dart_game():
    global score, balloons, level, time_limit, start_time, game_over, scene
    screen.fill(WHITE)

    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = time_limit - elapsed_time // 1000

    if remaining_time <= 0:
        game_over = True
        scene = 4

    if not game_over:

        dart_rect.center = pygame.mouse.get_pos()
        screen.blit(dart_img, dart_rect)

        if not balloons:
            for _ in range(level * 5):  
                x = random.randint(100, WIDTH - 100)
                y = random.randint(100, HEIGHT - 300)
                balloons.append(pygame.Rect(x, y, 50, 50))

        for balloon in balloons[:]:  
            if dart_rect.colliderect(balloon):
                balloons.remove(balloon)  
                score += 1  
                suara_mbledos.play()
                break  

        for balloon in balloons:
            pygame.draw.ellipse(screen, YELLOW, balloon)

        score_text = font.render(f"Score: {score}", True, BLACK)
        time_text = font.render(f"Time left: {remaining_time}s", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 50))

    else:

        end_text = font.render("Time's up! Press SPACE to Continue", True, BLACK)
        screen.blit(end_text, (WIDTH // 2 - 200, HEIGHT // 2))

    pygame.display.flip()

def reset_balloon_game():
    global balloons, level, time_limit, start_time, game_over
    balloons = []
    start_time = pygame.time.get_ticks()
    time_limit = 20 + level * 5  
    game_over = False
 
def show_story_2():
    screen.fill(WHITE)
    story_lines = [
        "After playing the Balloon Dart game, you continue to explore the circus.",
        "You decide to sit down and watch the performance.",
        "But as the show goes on, you feel drowsy and slowly fall asleep.",
        "Press SPACE to continue."
    ]

    for i, line in enumerate(story_lines):
        story_text = story_font.render(line, True, BLACK)
        screen.blit(story_text, (50, 100 + i * 40))

    pygame.display.flip()

def horror_game():
    global has_key, game_over, input_code
    running = True
    while running:
        pygame.time.Clock().tick(80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

            if event.type == pygame.KEYDOWN:

                if event.unicode.isdigit() and len(input_code) < 4:
                    input_code += event.unicode

                if input_code == code_required:
                    has_key = True
                    input_code = ''  

                if event.key == pygame.K_BACKSPACE:
                    input_code = ''

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_UP] and player.top >  0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += player_speed

        if player.x < monster.x:
            monster.x -= monster_speed
        if player.x > monster.x:
            monster.x += monster_speed
        if player.y < monster.y:
            monster.y -= monster_speed
        if player.y > monster.y:
            monster.y += monster_speed

        if player.colliderect(key) and not has_key:
            has_key = True  
            key.x, key.y = -50, -50  

        if player.colliderect(monster):
            game_over = True  
            game_over_screen()
            running = False

        if has_key and player.colliderect(pygame.Rect(WIDTH - 150, 50, 50, 50)):
            win_game()
            running = False

        screen.fill(BLACK)
        screen.blit(dart_img, player.topleft)
        pygame.draw.rect(screen, GREEN, pygame.Rect(WIDTH - 150, 50, 50, 50))  
        pygame.draw.rect(screen, WHITE, key)  
        pygame.draw.rect(screen, RED, monster)  

        for block in blocks:
            pygame.draw.rect(screen, GREEN, block)

        input_display = font.render(input_code, True, WHITE)
        screen.blit(input_display, (WIDTH // 2 - 50, HEIGHT - 50))

        pygame.display.flip()

def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over! Press SPACE to restart.", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()  
                    waiting = False

def win_game():
    screen.fill(GREEN)
    win_text = font.render("You found the exit! You win!", True, BLACK)
    screen.blit(win_text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()  
                    waiting = False

def reset_game():
    global scene, score, level, balloons, time_limit, start_time, game_over, has_key, input_code
    scene = 1
    score = 0
    level = 1
    balloons = []
    time_limit = 60
    start_time = 0
    game_over = False
    has_key = False
    input_code = ''
    play_music(home_music)  

play_music(home_music)

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and scene == 1:
                stop_music()  
                scene = 2
                play_music(story_music)  
            if event.key == pygame.K_SPACE:
                if scene == 2:
                    reset_balloon_game()
                    stop_music()  
                    scene = 3
                    play_music(dart_game_music)  
                elif scene == 3 and game_over:
                    reset_balloon_game()
                elif scene == 3 and not game_over:
                    scene = 4
                elif scene == 4:
                    stop_music()  
                    scene = 5
                    play_music(story_music)  
                elif scene == 5:
                    stop_music()  
                    scene = 6  
                    play_music(horror_game_music)  

    if scene == 1:
        show_home_screen()
    elif scene == 2:
        show_story_1()
    elif scene == 3:
        balloon_dart_game()
    elif scene == 4:
        show_story_2()
    elif scene == 6:
        horror_game()

pygame.quit()