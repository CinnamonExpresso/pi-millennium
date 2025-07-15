#Values that are subject to change during the simulation can be found here

#Dicts
debug_stats = {
    "FPS": 0 #the current fps of the program
}

settings = {
    "general": {
        "debug_mode": False
    },
    "graphics": {
        "fps_cap": 60 #fps cap to prevent overloading the system
    },
    "audio": {
        "music_enabled": True,
        "sound_enabled": True,
        "music_vol": 0.2,
        "sound_vol": 1.0
    }
}

menu_state = { #Used for tracking which menu is open
    "pause": False,
    "credits": False,
    "mainMenu": True,
    "settings": False,
    "achievements": False
}

flags = {
    "main": True, #Credits/settings menu accessed from main
    "pause": False, #Credits/settings menu accessed from pause
    "difficulty_change": False #Checks if the difficulty has been changed recently
}

cool_down = {
    "inputCooldownUntil": 0  # milliseconds
}

pause_states = [menu_state["pause"], menu_state["credits"], menu_state["mainMenu"], menu_state["settings"], menu_state["achievements"]] #menus that "pause the game"

#ints
game_speed:int = 1 #Game speed 0 = Paused, 1 = normal, 2 = x2 speed, 3 = x3 speed
difficulty = 0 #0 = easy, 1 = medium, 2 = hard

#lists
achievements = [] #list of player achievements

#Floats
dt = 1 / 60 #delta time

#booleans
is_btn_hover:bool = False
is_hovering:bool = False