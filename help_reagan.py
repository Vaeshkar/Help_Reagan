import pygame
import random
import time
import os
import sys

# Initialisierung
pygame.init()
pygame.mixer.init()
## Define base_path for both frozen and regular script use
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Help Reagan")
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Global Variables
global frame_count
frame_count = 0  
game_over = False

# Bilder laden 
background = pygame.image.load(os.path.join(base_path, "assets", "background.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
ground = pygame.image.load(os.path.join(base_path, "assets", "ground.png")).convert()
ground = pygame.transform.scale(ground, (WIDTH, 60))
start_screen_image = pygame.image.load(os.path.join(base_path, "assets", "help_reagan_startscreen.jpg")).convert()
start_screen_image = pygame.transform.scale(start_screen_image, (WIDTH, HEIGHT))
endscreen_image = pygame.image.load(os.path.join(base_path, "assets", "endscreen.jpg")).convert()
endscreen_image = pygame.transform.scale(endscreen_image, (WIDTH, HEIGHT))
press_space_img = pygame.image.load(os.path.join(base_path, "assets", "press_space.png")).convert_alpha()
print("Image size:", press_space_img.get_size())
bg_music_path = os.path.join(base_path, "sounds", "background_sound.wav")
pygame.mixer.music.load(bg_music_path)
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1, 0.0)


jump_sound = pygame.mixer.Sound(os.path.join(base_path, "sounds", "jump.wav"))
jump_sound.set_volume(0.3)
hit_sound = pygame.mixer.Sound(os.path.join(base_path, "sounds", "hitHurt.wav"))
endgame_sound = pygame.mixer.Sound(os.path.join(base_path, "sounds", "endgame_sound.wav"))
walk_sound = pygame.mixer.Sound(os.path.join(base_path, "sounds", "walk.wav"))
walk_sound.set_volume(0.8)

# Dino Lauf- und Sprunganimation
dino_run_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, f"assets/Reagan_run_{i}.png")).convert_alpha(), (40, 60)) for i in range(1, 4)]
dino_jump_frames = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, f"assets/Reagan_jump_{i}.png")).convert_alpha(), (40, 60)) for i in range(1, 4)]

# Kaktus Designs
cactus_designs = [pygame.transform.scale(pygame.image.load(os.path.join(base_path, f"assets/cactus_{i}.png")).convert_alpha(), (40, 60)) for i in range(1, 7)]

speech_bubble_texts = [
    ("Alright people...", "hands up!"),
    ("I’ll be asking you all...", "this later in the course!"),
    ("Learn for yourself...", "not for me."),
    ("Does everyone understand it...", "Yuliia?"),
]

# Dino Klasse
class Dino:
    def __init__(self):
        self.x = 50
        self.base_y = HEIGHT - 115 # Reagan position im spiel.
        self.y = self.base_y
        self.vel_y = 0
        self.jump_vel = -16
        self.width = 40
        self.height = 60
        self.is_jumping = False
        self.run_frame = 0
        self.jump_frame = 0
        self.animation_speed = 0.083
        self.jump_count = 0
        self.speech_bubble_timer = 0
        self.current_speech_text = None

    def jump(self):
        if self.y == self.base_y:
            self.vel_y = self.jump_vel
            self.is_jumping = True
            self.jump_count += 1
            if self.jump_count % 7 == 0:
                self.speech_bubble_timer = 150
                self.current_speech_text = random.choice(speech_bubble_texts)
                print(f"Sprechblasen-Text: {self.current_speech_text}")
            jump_sound.play()

    def update(self):
        self.vel_y += 1
        self.y += self.vel_y
        if self.y >= self.base_y:
            self.y = self.base_y
            self.vel_y = 0
            self.is_jumping = False

        if self.is_jumping:
            self.jump_frame += self.animation_speed
            if self.jump_frame >= len(dino_jump_frames):
                self.jump_frame = 0
        else:
            self.run_frame += self.animation_speed
            if self.run_frame >= len(dino_run_frames):
                self.run_frame = 0

        if self.is_jumping or game_over:
            pygame.mixer.Channel(1).stop()  # Stop walking sound immediately when game is over
        else:
            if not pygame.mixer.Channel(1).get_busy():
                pygame.mixer.Channel(1).play(walk_sound, loops=-1)

        if self.speech_bubble_timer > 0:
            self.speech_bubble_timer -= 1

    def draw(self):
        if self.is_jumping:
            frame = dino_jump_frames[int(self.jump_frame)]
        else:
            frame = dino_run_frames[int(self.run_frame)]
        screen.blit(frame, (self.x, self.y))

        if self.speech_bubble_timer > 0 and self.current_speech_text:
            bubble_x = self.x + self.width + 10
            bubble_y = self.y - 50
            bubble_width = 330
            if isinstance(self.current_speech_text, tuple) and len(self.current_speech_text) == 2:
                    text1 = self.current_speech_text[0]
                    text2 = self.current_speech_text[1]
                    has_second_line = bool(text2.strip()) 
                    bubble_height = 80 if has_second_line else 40 
            else:
                    text1 = self.current_speech_text if isinstance(self.current_speech_text, str) else self.current_speech_text[0]
                    text2 = ""
                    has_second_line = False
                    bubble_height = 40
            pygame.draw.rect(screen, WHITE, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
            pygame.draw.rect(screen, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2, border_radius=10)
            pygame.draw.polygon(screen, WHITE, [(bubble_x, bubble_y + bubble_height//2), 
                                                (bubble_x - 10, bubble_y + bubble_height//2 + 10), 
                                                (bubble_x - 10, bubble_y + bubble_height//2 - 10)])
            pygame.draw.polygon(screen, BLACK, [(bubble_x, bubble_y + bubble_height//2), 
                                                (bubble_x - 10, bubble_y + bubble_height//2 + 10), 
                                                (bubble_x - 10, bubble_y + bubble_height//2 - 10)], 2)
            font = pygame.font.SysFont("Arial", 20)
            text_surface1 = font.render(text1, True, BLACK)
            text_rect1 = text_surface1.get_rect(topleft=(bubble_x + 5, bubble_y + 5))
            screen.blit(text_surface1, text_rect1)

            if has_second_line:
                    text_surface2 = font.render(text2, True, BLACK)
                    text_rect2 = text_surface2.get_rect(topleft=(bubble_x + 5, bubble_y + 35))
                    screen.blit(text_surface2, text_rect2)

# Kaktus Klasse
class Cactus:
    def __init__(self, speed):
        self.x = WIDTH
        self.y = HEIGHT - 115 # Students position on the ground
        self.width = 40
        self.height = 60
        self.speed = speed
        self.design = random.choice(cactus_designs)

    def update(self):
        self.x -= self.speed

    def draw(self):
        screen.blit(self.design, (self.x, self.y))

# Fragen und Antworten
questions = [
    {
        "question": ["What is the output of this code?", 
                     "x = 5", 
                     "y = 3", 
                     "print(x + y)"],
        "answers": ["6", "7", "8", "9"],
        "correct": 2
    },
    {
        "question": ["What is the output of this code?", 
                     "for i in range(3):", 
                     "    print(i)"],
        "answers": ["0 1 2", "1 2 3", "0 1", "1 2"],
        "correct": 0
    },
    {
        "question": ["What is the output of this code?", 
                     "a = 'Hello'", 
                     "print(a[1])"],
        "answers": ["H", "e", "l", "o"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "if 5 > 3:", 
                     "    print('Yes')", 
                     "else:", 
                     "    print('No')"],
        "answers": ["Yes", "No", "5", "3"],
        "correct": 0
    },
    {
        "question": ["What is the output of this code?", 
                     "nums = [1, 2, 3]", 
                     "print(len(nums))"],
        "answers": ["1", "2", "3", "4"],
        "correct": 2
    },
    {
        "question": ["What is the output of this code?", 
                     "x = 10", 
                     "print(x // 3)"],
        "answers": ["3", "4", "3.33", "10"],
        "correct": 0
    },
    {
        "question": ["What is the output of this code?", 
                     "s = 'Python'", 
                     "print(s[2:4])"],
        "answers": ["Py", "th", "yt", "on"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "x = 2", 
                     "y = 3", 
                     "print(x ** y)"],
        "answers": ["5", "6", "8", "9"],
        "correct": 2
    },
    {
        "question": ["What is the output of this code?", 
                     "lst = [1, 2, 3]", 
                     "lst.append(4)", 
                     "print(lst)"],
        "answers": ["[1, 2, 3]", "[1, 2, 3, 4]", "[4, 1, 2, 3]", "[1, 2, 4]"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "x = 7", 
                     "if x % 2 == 0:", 
                     "    print('Even')", 
                     "else:", 
                     "    print('Odd')"],
        "answers": ["Even", "Odd", "7", "2"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "for i in range(2, 5):", 
                     "    print(i, end=' ')"],
        "answers": ["2 3 4", "2 3 4 5", "1 2 3", "3 4 5"],
        "correct": 0
    },
    {
        "question": ["What is the output of this code?", 
                     "s = 'Code'", 
                     "print(len(s))"],
        "answers": ["3", "4", "5", "6"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "x = [0, 1, 2]", 
                     "print(x[-1])"],
        "answers": ["0", "1", "2", "-1"],
        "correct": 2
    },
    {
        "question": ["What is the output of this code?", 
                     "def add(a, b):", 
                     "    return a + b", 
                     "print(add(4, 5))"],
        "answers": ["8", "9", "10", "45"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "x = 3", 
                     "while x > 0:", 
                     "    print(x)", 
                     "    x -= 1"],
        "answers": ["3 2 1", "1 2 3", "3 2", "2 1"],
        "correct": 0
    },
    {
        "question": ["What is the output of this code?", 
                     "s = 'Test'", 
                     "print(s.upper())"],
        "answers": ["test", "TEST", "Test", "tEST"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "lst = [5, 6, 7]", 
                     "lst.pop(1)", 
                     "print(lst)"],
        "answers": ["[5, 7]", "[5, 6]", "[6, 7]", "[5, 6, 7]"],
        "correct": 0
    },
    {
        "question": ["What is the output of this code?", 
                     "x = 4", 
                     "y = 2", 
                     "print(x % y)"],
        "answers": ["0", "1", "2", "4"],
        "correct": 0
    },
    {
        "question": ["What is the output of this code?", 
                     "d = {'a': 1, 'b': 2}", 
                     "print(d['b'])"],
        "answers": ["1", "2", "'b'", "None"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "x = 10", 
                     "y = 5", 
                     "print(x > y and y < 10)"],
        "answers": ["True", "False", "10", "5"],
        "correct": 0
    },
    {
        "question": ["What is the output of this code?", 
                     "lst = [1, 2, 3, 4]", 
                     "print(lst[1:3])"],
        "answers": ["[1, 2]", "[2, 3]", "[2, 3, 4]", "[1, 2, 3]"],
        "correct": 1
    },
    {
        "question": ["What is the output of this code?", 
                     "s = 'abc'", 
                     "print(s * 2)"],
        "answers": ["abc", "abcabc", "aabbcc", "2abc"],
        "correct": 1
    }
]

# Startbildschirm
def start_screen():
    global frame_count
    start_game = False

    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game = True

        # draw start background
        screen.blit(start_screen_image, (0, 0))

        # blink overlay with press-space prompt already in correct position
        if (frame_count // 30) % 2 == 0:
            screen.blit(press_space_img, (0, 0))  # full screen
            
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
    
    return True

# Spiel-Loop
def game():
    while True:
        # Startbildschirm anzeigen
        if not start_screen():
            return  # Beende das Spiel, wenn der Startbildschirm geschlossen wird
            pygame.mixer.music.play(-1, 0.0)

        dino = Dino()
        cacti = []
        score = 0
        game_over = False
        paused = False
        base_speed = 5
        speed_increase = 0.001
        min_distance = 6 * dino.width  
        max_distance = 500  
        last_score_checkpoint = 0
        resume_timer = 0
        feedback_timer = 0  

        # Erster Kaktus
        cacti.append(Cactus(base_speed))

        while not game_over:
            if score // 10 > last_score_checkpoint and not paused and resume_timer <= 0 and feedback_timer <= 0:
                paused = True
                last_score_checkpoint = score // 10
                current_question = random.choice(questions)
                selected_answer = None
                answer_feedback = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not paused and resume_timer <= 0 and feedback_timer <= 0:
                        dino.jump()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(f"Maus geklickt bei: {mouse_pos}")
                    if paused and answer_feedback is None:
                        for i in range(4):
                            answer_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20 + i*40, 300, 30)
                            print(f"Antwort {i} Rechteck: {answer_rect}")
                            if answer_rect.collidepoint(mouse_pos):
                                print(f"Antwort {i} ausgewählt")
                                selected_answer = i
                                if selected_answer == current_question["correct"]:
                                    answer_feedback = (i, GREEN)
                                    feedback_timer = 60
                                    resume_timer = 80
                                else:
                                    answer_feedback = (i, RED)
                                    feedback_timer = 60
                                    game_over = True

            if not paused and resume_timer <= 0 and feedback_timer <= 0:
                dino.update()
                if score == 0:
                    pygame.mixer.music.set_volume(0.15)
                
                if cacti:
                    last_cactus = cacti[-1]
                    current_speed = base_speed + (score * speed_increase * 60)
                    distance_to_spawn = random.randint(min_distance, max_distance)
                    if last_cactus.x <= WIDTH - distance_to_spawn:
                        cacti.append(Cactus(current_speed))

                for cactus in cacti[:]:
                    cactus.update()
                    if (cactus.x < dino.x + dino.width and 
                        cactus.x + cactus.width > dino.x and 
                        cactus.y < dino.y + dino.height):
                        hit_sound.play()
                        pygame.mixer.Channel(2).set_volume(0.0)  # Start silent
                        pygame.mixer.Channel(2).play(endgame_sound, loops=-1)
                        game_over = True
                    if cactus.x < -cactus.width:
                        cacti.remove(cactus)
                        score += 1

            # Timer herunterzählen
            if feedback_timer > 0:
                feedback_timer -= 1
                if feedback_timer <= 0 and not game_over:
                    paused = False

            if resume_timer > 0 and feedback_timer <= 0:
                resume_timer -= 1

            # Zeichnen
            screen.blit(background, (0, 0))
            screen.blit(ground, (0, HEIGHT - 60))
            dino.draw()
            for cactus in cacti:
                cactus.draw()
            
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            if paused or feedback_timer > 0:
                pygame.draw.rect(screen, LIGHT_BLUE, (WIDTH//2 - 200, HEIGHT//2 - 150, 400, 340), border_radius=15)
                pygame.draw.rect(screen, BLACK, (WIDTH//2 - 200, HEIGHT//2 - 150, 400, 340), 3, border_radius=15)
                
                # Frage und Code anzeigen
                font = pygame.font.Font(None, 24)
                for i, line in enumerate(current_question["question"]):
                    question_text = font.render(line, True, BLACK)
                    question_rect = question_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 120 + i*20))
                    screen.blit(question_text, question_rect)
                
                # Antworten anzeigen
                for i, answer in enumerate(current_question["answers"]):
                    answer_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20 + i*40, 300, 30)
                    if answer_feedback and answer_feedback[0] == i:
                        pygame.draw.rect(screen, answer_feedback[1], answer_rect, border_radius=5)
                    else:
                        pygame.draw.rect(screen, WHITE, answer_rect, border_radius=5)
                    pygame.draw.rect(screen, BLACK, answer_rect, 2, border_radius=5)
                    answer_text = font.render(answer, True, BLACK)
                    answer_rect_text = answer_text.get_rect(center=answer_rect.center)
                    screen.blit(answer_text, answer_rect_text)
            
            pygame.display.flip()
            clock.tick(60)

        while game_over:
            pygame.mixer.Channel(1).stop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Channel(2).stop()
                        endgame_sound.stop()
                        try:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(bg_music_path)
                            pygame.mixer.music.set_volume(1.0)
                            pygame.mixer.music.play(-1, 0.0)
                            print("Background music restarted.")
                        except pygame.error as e:
                            print("Music restart failed:", e)

                        game_over = False
                        break

            screen.blit(endscreen_image, (0, 0))
            font = pygame.font.SysFont("arial", 26, bold=True)
            restart_text = font.render("Press 'space' to Restart", True, BLACK)
            final_score_text = font.render("Score: {}".format(score), True, BLACK)
            
            screen.blit(final_score_text, (WIDTH//2 - 50, 160))  # Score a bit above center
            screen.blit(restart_text, (WIDTH//2 - 135, 190))     # Restart below it
            pygame.mixer.music.stop()
            
            # Fade in endgame sound
            vol = pygame.mixer.Channel(2).get_volume()
            if vol < 1.0:
                pygame.mixer.Channel(2).set_volume(min(1.0, vol + 0.01))  # Adjust fade speed here
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game()