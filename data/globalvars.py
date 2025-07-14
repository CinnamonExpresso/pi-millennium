#Values that are subject to change during the simulation can be found here

#Dicts
debug_stats = {
    "FPS": 0
}

settings = {
    "general": {
        "debug_mode": True
    },
    "graphics": {
        "fps_cap": 60
    },
    "audio": {
        "music_enabled": True,
        "sound_enabled": True,
        "music_vol": 1.0,
        "sound_vol": 1.0
    }
}

menu_state = { #Used for tracking which menu is open
    "pause": False,
    "credits": False,
    "mainMenu": True,
    "settings": False
}

flags = {
    "main": True, #Credits/settings menu accessed from main
    "pause": False #Credits/settings menu accessed from pause
}

cool_down = {
    "inputCooldownUntil": 0  # milliseconds
}

pause_states = [menu_state["pause"], menu_state["credits"], menu_state["mainMenu"], menu_state["settings"]] #menus that "pause the game"

#ints
game_speed:int = 1 #Game speed 0 = Paused, 1 = normal, 2 = x2 speed, 3 = x3 speed

#Floats
dt = 1 / 60

#booleans
is_btn_hover:bool = False
is_hovering:bool = False