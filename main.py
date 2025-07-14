import pygame
import sys
import time
from behavior.settings import *
from behavior.utils.audio_controller import MusicManager, SoundManager
from behavior.utils.save_data import Data
from behavior.gui.fontEngine import render_text_with_border
from behavior.gui.guiToast import Toast
from behavior.visuals import Visuals
import data.globalvars as globalvars
from behavior.utils.generalUtils import reset_menu_state, update_pause_states, change_game_speed, update_debug_stats, update_timers
from behavior.utils.timer import Timer

# Initialize pygame
pygame.init()

# Constants
FONT = pygame.font.SysFont("consolas", 48)
INPUT_FONT = pygame.font.SysFont("consolas", 36)
SUB_FONT = pygame.font.SysFont("consolas", 26)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pi Millennium")

"""
TODO:
-Maybe some graphical changes
-Optimize code
-Translate to c++ and compile to web-asymebly
-Add difficulty toggle
"""

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
        self.musicManager = MusicManager() #Manages the music
        self.soundManager = SoundManager()
        self.milestones = {
            "digits": {
                10: {"title": "First steps", "description": "You reached the first 10 digits of Pi!"},
                50: {"title": "Semicentennial", "description": "Half way to the first 100 digits"},
                100: {"title": "Triple digits", "description": "Amazing! 100 digits memorized!"},
                500: {"title": "500 club", "description": "500 memorized! can you reach 1000?"},
                1000: {"title": "Pi Millennium", "description": "Wild! you have 1000 digits memorized!"}
            },
            "misc": {
                1: {"title": "High Achiever", "description": "You beat your high score for the first time."}
            }
        } #the sub-key is the condition for the achievment
        self.animated_seq = ""
        self.animation_index = 0
        self.char_display_interval = 0.2  # seconds between characters
        self.last_char_time = time.time()
        self.data = Data()
        self.high_score = self.data.data["high_score"]

        self.paused_at = None #used to keep track for how long the game was paused
        self.total_paused_duration = 0
        
        #Flags
        self.flags = {
            "high_score_reached": False
        }

        #GUI stuff
        self.toasts = []  # toast notifications
        self.visuals = Visuals(screen=screen, btn_cmds={"restart_game": self.restart_game})

    def restart_game(self):
        self.score = 0
        self.animated_seq = ""
        self.animation_index = 0
        self.user_input = ""
        self.message = ""
        self.state = "show"
        self.cur_index = 0
        self.last_char_time = time.time()
        self.data.load_data()
        self.high_score = self.data.data["high_score"]
        self.flags = {
            "high_score_reached": False
        }

    def get_current_sequence(self):
        return ''.join(self.pi_digits[:self.cur_index + 1])
    
    def post_achievement(self, achievement: dict):
        globalvars.achievements.append(achievement)
        self.toasts.append(Toast(achievement["title"], achievement["description"]))
        self.soundManager.play("achievement")

    def check_achievement(self, flag:list=None):
        if self.score in self.milestones["digits"]:
            # Check if we've already added this achievement
            if not any(a.get("tag") == self.score for a in globalvars.achievements):
                achievement = self.milestones["digits"][self.score]
                achievement["tag"] = self.score  # Tag the score for tracking
                self.post_achievement(achievement)
        #Other achievements
        if flag and flag[0] == "other":
            if flag[1] == "highscore":
                if not any(a.get("tag") == "1m" for a in globalvars.achievements):
                    achievement = self.milestones["misc"][1]
                    achievement["tag"] = "1m"  # Tag the score for tracking
                    self.post_achievement(achievement)

    def update(self):
        # Play audio
        self.play_audio()
        #Check highscore
        self.check_highscore()

        if globalvars.game_speed != 0:
            self.now = time.time()

        # If game is paused
        if any(state for state in globalvars.pause_states):
            # Mark when the game was paused
            if self.paused_at is None:
                self.paused_at = self.now
            return  # Don't proceed with game logic during pause

        # Game just resumed
        if self.paused_at is not None:
            pause_duration = self.now - self.paused_at
            self.last_char_time += pause_duration
            self.last_switch_time += pause_duration
            self.paused_at = None

        if self.state == "show":
            full_seq = self.get_current_sequence()

            # Animate one character at a time
            if self.animation_index < len(full_seq):
                if self.now - self.last_char_time >= self.char_display_interval:
                    self.animated_seq += full_seq[self.animation_index]
                    self.animation_index += 1
                    self.last_char_time = self.now
            else:
                # Once animation is done, switch to input mode after delay
                if self.now - self.last_char_time > 1:
                    self.state = "input"
                    self.user_input = ""
                    self.animated_seq = ""
                    self.animation_index = 0
                    self.last_switch_time = self.now

        elif self.state == "input":
            if self.user_input == self.get_current_sequence():
                self.message = "Correct!"
                self.state = "wait"
                self.last_switch_time = self.now
                self.score += 1

            elif not self.get_current_sequence().startswith(self.user_input):
                self.message = "Game Over"
                self.state = "gameover"
                new_data = {
                    "score": self.score,
                    "achievements": globalvars.achievements
                }
                self.data.save_data(input_data=new_data)

            # Check for achievements
            self.check_achievement()

        elif self.state == "wait":
            if self.now - self.last_switch_time > 1:
                self.cur_index += 1
                if self.cur_index >= len(self.pi_digits):
                    self.message = "You completed all digits! Congrats!"
                    self.state = "gameover"
                else:
                    self.state = "show"
                    self.last_switch_time = self.now

        # Clean up expired toasts
        self.toasts = [t for t in self.toasts if not t.is_expired()]

    # A function just to handle that weird double click bug with the buttons
    def handle_input(self):
        current_time = pygame.time.get_ticks()
        # If still on cooldown, block input
        if current_time < globalvars.cool_down["inputCooldownUntil"]:
            return True  # Input is blocked (still in cooldown)
        return False  # Input is allowed

    #Handles controls
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #pause the game
                    reset_menu_state()
                    if not globalvars.flags["main"]:
                        globalvars.menu_state["pause"] = not globalvars.menu_state["pause"]
                    else:
                        globalvars.menu_state["mainMenu"] = True
                    update_pause_states()
                    change_game_speed()

        if not any(state for state in globalvars.pause_states) and self.state == "input" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                pass  # ignore enter
            elif event.key == pygame.K_ESCAPE:
                pass  # ignore enter
            elif event.unicode:
                self.user_input += event.unicode
            
    def draw(self):
        screen.fill(BG_COLOR)
        if self.handle_input():
            return

        if not any(state for state in globalvars.pause_states) and not globalvars.flags["main"]:
            if self.state == "show" or self.state == "input":
                globalvars.flags["main"] = False

                score_text_surf = render_text_with_border(f"Score: {self.score}", SUB_FONT, text_color=TEXT_COLOR, border_color=(48, 48, 48), border_width=2)
                screen.blit(score_text_surf, (10, 10))

                high_score_text_surf = render_text_with_border(f"High-Score: {self.high_score}", SUB_FONT, text_color=TEXT_COLOR, border_color=(48, 48, 48), border_width=2)
                screen.blit(high_score_text_surf, (10, score_text_surf.get_height() + 10))

            # Show message or sequence
            if self.state == "show":
                text_surf = render_text_with_border(self.animated_seq, FONT, text_color=TEXT_COLOR, border_color=(48, 48, 48), border_width=2)
                screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 3))

                msg_surf = render_text_with_border("Memorize the sequence!", SUB_FONT, text_color=TEXT_COLOR, border_color=(48, 48, 48), border_width=2)
                screen.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, HEIGHT // 2))

            elif self.state == "input":
                input_surf = render_text_with_border(self.user_input, INPUT_FONT, text_color=TEXT_COLOR, border_color=(48, 48, 48), border_width=2)
                screen.blit(input_surf, (WIDTH // 2 - input_surf.get_width() // 2, (HEIGHT // 3)))

                prompt_surf = render_text_with_border("Type the full sequence", SUB_FONT, text_color=TEXT_COLOR, border_color=(48, 48, 48), border_width=2)
                screen.blit(prompt_surf, (WIDTH // 2 - prompt_surf.get_width() // 2, HEIGHT // 2))
            else:
                msg_surf = render_text_with_border(self.message, FONT, text_color=TEXT_COLOR, border_color=(48, 48, 48), border_width=2)
                screen.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, (HEIGHT // 3)))
                score_surf = render_text_with_border(f"Score: {self.score}", SUB_FONT, text_color=TEXT_COLOR, border_color=(48, 48, 48), border_width=2)
                screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, (HEIGHT // 3)+60))

            #Update gui's
            if self.state == "gameover":
                self.visuals.mainGui.update()
        elif  globalvars.menu_state["pause"]:
            self.visuals.pauseGui.update()
            globalvars.flags["pause"] = True
            globalvars.flags["main"] = False
        elif globalvars.menu_state["settings"]:
            self.visuals.settingsGui.update()
        elif  globalvars.menu_state["credits"]:
            self.visuals.creditsGui.update()
        elif  globalvars.menu_state["achievements"]:
            self.visuals.achievementsGui.update()
        elif  globalvars.menu_state["mainMenu"]:
            self.visuals.mainMenuGui.update()

        if globalvars.settings["general"]["debug_mode"]:
            self.visuals.rebuild_debug_gui()
            self.visuals.debugGui.update()

        # Draw active toasts
        for i, toast in enumerate(self.toasts):
            toast.draw(screen, i, len(self.toasts))

        pygame.display.flip()

    def check_highscore(self):
        #Check if player surpassed their highscore
        if self.score > self.high_score and self.soundManager.is_playing == False and not self.flags["high_score_reached"]:
            if globalvars.settings["audio"]["sound_enabled"]:
                self.soundManager.play("new_high_score")
                
            self.flags["high_score_reached"] = True
            self.toasts.append(Toast("New High-Score!", "You reached a new high score!"))

            self.check_achievement(flag=["other", "highscore"])

    def play_audio(self):
        if globalvars.settings["audio"]["music_enabled"] and self.musicManager.is_playing == False:
            self.musicManager.play_loop(sound_name="main")
        
        #Check settings
        if globalvars.settings["audio"]["music_vol"] < 0.025:
            globalvars.settings["audio"]["music_enabled"] == False
        if globalvars.settings["audio"]["sound_vol"] < 0.025:
            globalvars.settings["audio"]["sound_enabled"] == False

        if globalvars.settings["audio"]["music_enabled"] == False:
            self.musicManager.stop("main")

        #Set volumnes
        self.musicManager.set_volume("main", globalvars.settings["audio"]["music_vol"])
        self.soundManager.set_volume("main", globalvars.settings["audio"]["sound_vol"])

def main():
    clock = pygame.time.Clock()
    timers = {
        "debug_stat_update": Timer(100)
    }

    game = PiMemoryGame()
    globalvars.achievements = game.data.data["achievements"] #load saved achievement data
    game.visuals.build_gui()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update()
        game.draw()
        clock.tick(60)

        if globalvars.settings["general"]["debug_mode"] and not timers["debug_stat_update"].active:
            update_debug_stats("FPS", round(clock.get_fps()), game.visuals.rebuild_debug_gui)
            timers["debug_stat_update"].activate()

        if any(timer.active for timer in timers.values()):
            timers = update_timers(timers)
                                   
if __name__ == "__main__":
    main()
