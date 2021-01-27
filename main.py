#################
# IMPORT MODULES
#################
import pygame, sys, random


###################
# INITIALIZE GAME
###################
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19__.TTF', 25)


#################
# GAMES VARIABLES
#################
# GRAVITY
gravity = 0.10
bird_movement = 0
game_active = True
score = 0
high_score = 0


##################
# GAME ELEMENTS
##################
# background image
bg_surface = pygame.image.load('assets/background-day.png')

# floor
floor_surface = pygame.image.load('assets/base.png')
floor_x_pos = 0

# bird
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 2
bird_surface = bird_frames[bird_index]
bird_rec = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png')
# bird_rec = bird_surface.get_rect(center = (75, 256))

# pipes
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 400, 300]

game_over_surface = pygame.image.load('assets/message.png')
game_over_rect = game_over_surface.get_rect(center=(144, 240))

flap_sound = pygame.mixer.Sound('sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sounds/sfx_point.wav')
score_sound_countdown = 100

#############
# FUNCTIONS
#############
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (320, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (320, random_pipe_pos - 120))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def checkCollisions(pipes):
    for pipe in pipes:
        if bird_rec.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rec.top <= -100 or bird_rec.bottom >= 900:
        death_sound.play()
        return False
    else:
        return True

def rotated_bird(bird, movement):
    new_bird = pygame.transform.rotozoom(bird, -movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rec = new_bird.get_rect(center=(100, bird_rec.centery))
    return new_bird,new_bird_rec

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 35))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render('Score: {}'.format(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 35))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render('High Score: {}'.format(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 420))
        screen.blit(high_score_surface, high_score_rect)

def updateScore(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#############
# MAIN LOOP
#############
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP and game_active == True:
            bird_movement = 0
            bird_movement -= 3.2
            flap_sound.play()
        if event.type == pygame.MOUSEBUTTONUP and game_active == False:
            game_active = True
            pipe_list.clear()
            bird_rec.center = (75, 206)
            bird_movement = 0
            score = 0
            score_sound_countdown = 0


        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rec = bird_animation()

    # background image
    screen.blit(bg_surface, (0,0))

    if game_active == True:
        # bird
        bird_movement += gravity
        # rotated_bird = rotated_bird(bird_surface, bird_movement)
        bird_rec.centery += bird_movement
        screen.blit(bird_surface, bird_rec)
        game_active = checkCollisions(pipe_list)
        # pipes
        pipe_list = move_pipes(pipe_list)
        drawPipes(pipe_list)
        score += 0.01
        score_display('game_over')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = updateScore(score, high_score)
        score_display('game_over')

    # floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
