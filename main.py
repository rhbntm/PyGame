import pygame
import sys
import random
from PIL import Image

pygame.init()
pygame.mixer.init()


Width, Height = 600, 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("MATHching Game")
clock = pygame.time.Clock()
White = (255, 255, 255)
Black = (0, 0, 0)
Gray = (128, 128, 128)
num_cards = 12
cards = []
selected_cards = []
current_operation = "Addition"
user_input = ''
Easy = 120
Medium = 60
Hard = 30
game_state = 'start'
start_time = None



correct_sound = pygame.mixer.Sound("Sounds/Correct.mp3")
incorrect_sound = pygame.mixer.Sound("Sounds/pipe.mp3")
lose = pygame.mixer.Sound("Sounds/Cat Laughing At You.mp3")
win = pygame.mixer.Sound("Sounds/win.mp3")
cheers = pygame.mixer.Sound("Sounds/cheers.mp3")
applause = pygame.mixer.Sound("Sounds/applause.mp3")

correct_sound.set_volume(0.9) 
incorrect_sound.set_volume(0.05)  
lose.set_volume(0.8)  
win.set_volume(0.5)  
cheers.set_volume(0.6)  
applause.set_volume(0.6) 


card_image = pygame.Surface((100, 140))
card_image.fill(White)


def add(a, b):
    return a + b


operations = {
    "Addition": add,
}



def initialize_cards():
    numbers = random.sample(range(1, 100), num_cards)
    for i in range(num_cards):
        pos = (i % 4 * 120 + 70, i // 4 * 150 + 50)
        card_data = {
            'number': numbers[i],
            'pos': pos,
            'flipped': False,
            'rect': pygame.Rect(pos[0], pos[1], 100, 140)
        }
        cards.append(card_data)

def draw_text(text, pos, font_size=32, color=Black):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)  
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)

initialize_cards()

def handle_input(event):
    global user_input, game_state, selected_cards, difficulty
    if game_state == 'start':
        if event.key == pygame.K_e:
            difficulty = Easy
            game_state = 'main_game'
        elif event.key == pygame.K_m:
            difficulty = Medium
            game_state = 'main_game'
        elif event.key == pygame.K_h:
            difficulty = Hard
            game_state = 'main_game'
    elif game_state == 'main_game' or game_state == 'answer_question':
        if event.key == pygame.K_BACKSPACE:
            user_input = user_input[:-1]
        elif event.key == pygame.K_RETURN:
            num1 = selected_cards[0]['number']
            num2 = selected_cards[1]['number']
            result = operations[current_operation](num1, num2)
            pygame.mixer.stop()
            pygame.mixer.Sound.play(correct_sound)
            if user_input.strip() == str(result).strip():
                pygame.display.flip()
                user_input = ''
                selected_cards = []
                game_state = 'main_game'
                check_win_condition()  
            else:
                pygame.display.flip()
                user_input = ''  
                pygame.mixer.stop()
                pygame.mixer.Sound.play(incorrect_sound)    
        else:

            if event.unicode.isdigit():
                user_input += event.unicode
            
def draw_backgrounds():
    top_menu = pygame.draw.rect(screen, Black, [0, 0, Width, 100], )
    bottom_menu = pygame.draw.rect(screen, Black, [0, Height - 100, Width, 100],)




def draw_timer(game_state):
    global start_time
    if game_state == 'main_game' or game_state == 'answer_question':
        if start_time is None:
            start_time = pygame.time.get_ticks() // 1000  

        timer_font = pygame.font.Font(None, 36)
        timer_x, timer_y = Width // 2 - 60, 16

        current_time = pygame.time.get_ticks() // 1000
        elapsed_time = (difficulty - (current_time - start_time))  
        
        timer_surface = timer_font.render(f"Time: {elapsed_time} s", True, [0, 0, 0])
        screen.blit(timer_surface, (timer_x, timer_y))

        if elapsed_time <= 0:
            print("Elapsed time is zero. Changing game state to 'finished'")  
            return 'finished'  
    return game_state  



def check_win_condition():
    global game_state
    all_matched = all(card['flipped'] for card in cards)
    if all_matched:
        pygame.mixer.Sound.play(win)
        game_state = 'win'


gif_path = "Assets/omedetou.gif"
gif_image = Image.open(gif_path)
frames = []
try:
    while True:
        frame = gif_image.copy()
        frames.append(frame)
        gif_image.seek(gif_image.tell() + 1)
except EOFError:
    pass
    
pygame_frames = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode).convert() for frame in frames]


def display_gif(frames, position, size):
    frame_index = 0
    user_clicked = False
    screen.fill(Gray)
    while not user_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                user_clicked = True  
                break  

        resized_frame = pygame.transform.scale(frames[frame_index], size)
        screen.blit(resized_frame, position)
        print("Frame Index:", frame_index)
        frame_index = (frame_index + 1) % len(frames)
        draw_text('Congratulations you won!!!', (Width // 2, Height // 2), color=[0, 255, 0], font_size=60)
        draw_text('Click to play again', (Width // 2, Height // 2 + 50), color=Black, font_size=60)
        pygame.display.flip()
        clock.tick(15)
    
    return True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and (game_state == 'start' or game_state == 'main_game' or game_state == 'answer_question'):
            handle_input(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'main_game':
            for card in cards:
                if card['rect'].collidepoint(event.pos) and not card['flipped']:
                    card['flipped'] = True
                    selected_cards.append(card)
                    if len(selected_cards) == 2:
                        game_state = 'answer_question'

    screen.fill(Gray)
    if game_state == 'start':
        pygame.mixer.stop()
        draw_backgrounds()
        draw_text('MATHching', (Width // 2 + 10, Height - 550), font_size = 69, color=White)
        draw_text('Choose Difficulty:', (Width // 2, Height // 2 - 150), font_size=43)
        draw_text('Press E for Easy', (Width // 2, Height // 2 - 30))
        draw_text('Press M for Medium', (Width // 2, Height // 2 + 20))
        draw_text('Press H for Hard', (Width // 2, Height // 2 + 70))
    
    elif game_state == 'main_game' or game_state == 'answer_question':
        bottom_menu = pygame.draw.rect(screen, Black, [0, Height - 100, Width, 100])
        for card in cards:
            if card['flipped']:
                draw_text(str(card['number']), (card['rect'].centerx, card['rect'].centery))
            else:
                screen.blit(card_image, card['rect'].topleft)

        if game_state == 'answer_question':
            question = f"What is {selected_cards[0]['number']} + {selected_cards[1]['number']}? {user_input}"
            draw_text(question, (Width // 2 - 15, Height - 50), color=White)

    elif game_state == 'finished':
        pygame.mixer.stop()
        pygame.mixer.Sound.play(lose)
        car = pygame.image.load("assets/point.webp")
        car = pygame.transform.scale(car, (600, 600))
        screen.blit(car, (0, 0))

        draw_text('You lost!' , (Width // 2, Height // 2), color=[255, 0, 0], font_size=60)
        draw_text('Click to play again', (Width // 2, Height // 2 + 50), font_size=60)
        pygame.display.flip()
        
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
 
                    selected_cards = []  
                    cards = [] 
                    initialize_cards()
                    game_state = 'start'
                    start_time = None 
                    waiting_for_restart = False

    elif game_state == 'win':
        print("Before")
        pygame.mixer.stop()
        pygame.mixer.Sound.play(win)
        pygame.mixer.Sound.play(cheers)
        pygame.mixer.Sound.play(applause)

        gif_displayed = display_gif(pygame_frames, (0, 0), (600, 600))
        if gif_displayed:
            print("After")

            selected_cards = []  
            cards = []  
            initialize_cards()
            game_state = 'start'
            start_time = None  

    game_state = draw_timer(game_state)  
    pygame.display.flip()

pygame.quit()
sys.exit()
