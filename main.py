import pygame
import sys
import time
from behavior.settings import *
from behavior.utils.audio_controller import MusicManager
from behavior.utils.save_data import Data
from behavior.gui.guiEngine import GUI

# Initialize pygame
pygame.init()

# Constants
FONT = pygame.font.SysFont("consolas", 48)
INPUT_FONT = pygame.font.SysFont("consolas", 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pi Memory Game")

class PiMemoryGame:
    def __init__(self):
        self.pi_digits = list("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989")
        self.cur_index = 0
        self.state = "show"  # states: "show", "wait", "input", "gameover"
        self.display_time = 1.5  # seconds to show the sequence
        self.last_switch_time = time.time()
        self.user_input = ""
        self.message = ""
        self.score = 0 #current player score
        self.high_score = 0
        self.musicManager = MusicManager() #Manages the music
        self.milestones = {
            10: "You reached the first 10 digits of Pi!",
            50: "Half-way to 100 digits!",
            100: "Amazing! 100 digits memorized!",
            500: "500 memorized! can you reach 1000?",
            1000: "Wild! you have 1000 digits memorized!"
        }
        self.achievements = [] #list of player achievements
        self.animated_seq = ""
        self.animation_index = 0
        self.char_display_interval = 0.2  # seconds between characters
        self.last_char_time = time.time()
        self.data = Data()

        #GUI stuff
        self.mainGui = GUI(surface=screen)

    def restart_game(self):
        print("hi")

    def build_gui(self):
        self.mainGui.create_btn(
            pos=(10, 10),
            width = 60,
            height = 60,
            text = "Restart",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["WHITE"],
            img="restart.png",
            border_color=COLORS["BLACK"],
            funct=self.restart_game
        )

    def get_current_sequence(self):
        return ''.join(self.pi_digits[:self.cur_index + 1])
    
    def toast_notification(self):
        pass

    def update(self):
        now = time.time()

        if self.state == "show":
            full_seq = self.get_current_sequence()

            # Animate one character at a time
            if self.animation_index < len(full_seq):
                if now - self.last_char_time >= self.char_display_interval:
                    self.animated_seq += full_seq[self.animation_index]
                    self.animation_index += 1
                    self.last_char_time = now
            else:
                # Once animation is done, switch to input mode after delay
                if now - self.last_char_time > 1:  # pause after full sequence is shown
                    self.state = "input"
                    self.user_input = ""
                    self.animated_seq = ""
                    self.animation_index = 0
                    self.last_switch_time = now

        elif self.state == "input":
            if self.user_input == self.get_current_sequence():
                self.message = "Correct!"
                self.state = "wait"
                self.last_switch_time = now
                self.score += 1

            elif not self.get_current_sequence().startswith(self.user_input):
                self.message = "Wrong! Game Over."
                self.state = "gameover"
                self.data.save_score(score=self.score)

        elif self.state == "wait":
            if now - self.last_switch_time > 1:
                self.cur_index += 1
                if self.cur_index >= len(self.pi_digits):
                    self.message = "You completed all digits! Congrats!"
                    self.state = "gameover"
                else:
                    self.state = "show"
                    self.last_switch_time = now
        
        #Play audio
        self.play_audio()

    def handle_event(self, event):
        if self.state == "input" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                pass  # ignore enter
            elif event.unicode:
                self.user_input += event.unicode

    def draw(self):
        screen.fill(BG_COLOR)

        if self.state == "show" or self.state == "input":
            score_text = INPUT_FONT.render(f"Score: {self.score}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))

        # Show message or sequence
        if self.state == "show":
            text = FONT.render(self.animated_seq, True, TEXT_COLOR)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
            msg = INPUT_FONT.render("Memorize the sequence!", True, TEXT_COLOR)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        elif self.state == "input":
            input_text = FONT.render(self.user_input, True, TEXT_COLOR)
            screen.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, HEIGHT // 3))
            prompt = INPUT_FONT.render("Type the full sequence:", True, TEXT_COLOR)
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
        else:
            end_text = FONT.render(self.message, True, SUCCESS_COLOR if "Correct" in self.message or "Congrats" in self.message else ERROR_COLOR)
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 3))
            score_text = INPUT_FONT.render(f"Score: {self.score}", True, TEXT_COLOR)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        #Update gui's
        self.mainGui.update()
        pygame.display.flip()

    def play_audio(self):
        if MUSIC_ENABLED and self.musicManager.is_playing == False:
            self.musicManager.play_loop(sound_name="main")


def main():
    clock = pygame.time.Clock()
    game = PiMemoryGame()
    game.data.load_data()
    game.build_gui()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update()
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()
