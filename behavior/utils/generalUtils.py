import data.globalvars as globalvars
from pygame import quit
from sys import exit
from behavior.settings import SAVE_DATA_PATH
import json

#Updates pause states to new values
def update_pause_states():
    globalvars.pause_states = [globalvars.menu_state["pause"], globalvars.menu_state["credits"], globalvars.menu_state["mainMenu"], globalvars.menu_state["settings"]]

#Resets all menu states to False
def reset_menu_state():
    if any(globalvars.menu_state.values()):
        for btn in globalvars.menu_state:
            globalvars.menu_state[btn] = False

    update_pause_states()

#Resets all menu flags to False
def reset_menu_flags():
    if any(globalvars.flags.values()):
        for flag in globalvars.flags:
            globalvars.flags[flag] = False

#Update stats on globalvars
def update_stats(name, amount):
    globalvars.stats[name] += amount #Update stat
    globalvars.visuals.rebuild_stat_gui()

#update debug stats
def update_debug_stats(name, amount, callback_fb):
    globalvars.debug_stats[name] = amount
    callback_fb()

#Does as the name suggests
def update_global_settings_value(category: str, name: str, value: any):
    globalvars.settings[category][name] = value

#updates timers
def update_timers(timers:dict):
    new_timers = timers
    for timer in new_timers.values():
        timer.update()
    return new_timers

#Completely resets data
def reset_game_data():
    globalvars.flags["reset_flag"] = True

#Exit the entire program
def quit_game():
    quit()
    exit()

#change game difficulty
def change_difficulty(difficulty=0):
    globalvars.difficulty = difficulty
    globalvars.flags["difficulty_change"] = True

#changes game speed
def change_game_speed(speed=1):
    if any([globalvars.menu_state["pause"], globalvars.menu_state["credits"], globalvars.menu_state["mainMenu"], globalvars.menu_state["settings"]]):
        globalvars.game_speed = 0
        return
    elif not globalvars.menu_state["pause"]:
        globalvars.game_speed = speed