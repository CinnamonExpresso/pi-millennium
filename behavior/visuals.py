from behavior.gui.guiEngine import GUI, FullMenu, Popup
from behavior.settings import *
from behavior.utils.generalUtils import quit_game, reset_menu_state, change_difficulty, update_global_settings_value, reset_game_data, activate_cooldown, is_web_asm
import data.globalvars as globalvars

class Visuals:
    def __init__(self, screen, btn_cmds):
        self.btn_cmds = btn_cmds
        self.surface = screen
        self.achievement_titles_lst = []

        #build guis
        self.mainGui = GUI(surface=screen) #Gui used on gameover screen
        self.settingsGui = FullMenu(surface=self.surface, menu_header="Settings", menu_state_type="settings", bg_overlay=False, tabs_enabled=True) #gui when player clicks settings
        self.pauseGui = FullMenu(surface=self.surface, menu_header="Pi Millennium", menu_state_type="pause", bg_overlay=False) #gui when player presses escape
        self.mainMenuGui = FullMenu(surface=self.surface, menu_header="Pi Millennium", menu_state_type="main", bg_overlay=False) #Main menu when player starts the game
        self.creditsGui = FullMenu(surface=self.surface, menu_header="Credits", menu_state_type="credits", bg_overlay=False)
        self.achievementsGui = FullMenu(surface=self.surface, menu_header="Achievements", menu_state_type="achievements", bg_overlay=False)

        #Build rects
        self.mainMenuGui.create_menu_rects("center")
        self.pauseGui.create_menu_rects("center")
        self.creditsGui.create_menu_rects("center")
        self.achievementsGui.create_menu_rects("center")
        self.settingsGui.create_menu_rects("top")

        self.rebuild_popupGui()

    # Just to handle the back button double click issue
    def back_btn(self):
        reset_menu_state()
        globalvars.menu_state["mainMenu"] = True
        activate_cooldown()

    # Start the game from the main menu gui
    def start_btn(self):
        globalvars.flags["main"] = False
        self.mainMenuGui.close_menu()
        self.btn_cmds["restart_game"]

    def achievement_titles(self):
        for achievement in globalvars.achievements:
            self.achievement_titles_lst.append(achievement["title"])
    
    #reublids debug stats
    def rebuild_debug_gui(self):
        self.debugGui = GUI(surface=self.surface)
        self.debugGui.txt_list.clear()
        self.debugGui.create_text(
                        pos = (20, HEIGHT - 40),
                        text_content = f"FPS: {globalvars.debug_stats["FPS"]}",
                        text_color = COLORS["WHITE"],
                        font_name=None,
                        font_size=32
        )

    def close_popup(self):
        self.popupGuiMain.close_menu()
        self.settingsGui.open_menu()
        activate_cooldown()

    def open_popup(self):
        self.popupGuiMain.open_menu()
        activate_cooldown()
    
    def rebuild_popupGui(self):
        self.popupGuiBg = FullMenu(surface=self.surface, menu_header="", menu_state_type="popup", bg_overlay=True)
        self.popupGuiMain = Popup(surface=self.surface, menu_header="Reset Game?", menu_state_type="popup", bg_overlay=False, menu_background_color=(255,255,255,255), menu_background=True, menu_height=400, menu_width=400, header_color=(0,0,0), rounded_corners=(True, 20))
        self.popupGuiBg.create_menu_rects("center")
        self.popupGuiMain.create_menu_rects("center")

        #Popup
        self.popupGuiMain.create_text(
            pos = ((self.popupGuiMain.menu_rect.centerx//2)+70,  self.popupGuiMain.menu_rect.top + 60),
            text_content = "Are you sure you want to reset? All of your progress will be erased",
            text_color = COLORS["BLACK"],
            font_name=None,
            font_size=24
        )

        self.popupGuiMain.create_btn(
            pos=((self.popupGuiMain.menu_width//2) + (200//2) - 80,  self.popupGuiMain.menu_rect.top + 290),
            width = 170,
            height = 60,
            text = "Accept",
            color = COLORS["LIGHT_GREEN"],
            hover_color = COLORS["GREEN"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=reset_game_data
        )
        self.popupGuiMain.create_btn(
            pos=(self.popupGuiMain.btn_list[0].pos[0] + 190,  self.popupGuiMain.btn_list[0].pos[1]),
            width = 170,
            height = 60,
            text = "Decline",
            color = COLORS["LIGHT_RED"],
            hover_color = COLORS["CRIMSON"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.close_popup
        )

    def return_to_main_menu(self):
        globalvars.flags["pause_to_main"] = True
        activate_cooldown()

    def build_gui(self):
        self.achievement_titles()

        #Main menu gui
        self.mainMenuGui.create_btn(
            pos=((WIDTH//2) - (480//2),  self.mainMenuGui.menu_rect.top + 80),
            width = 480,
            height = 60,
            text = "Start",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.start_btn
        )
        self.mainMenuGui.create_btn(
            pos=(self.mainMenuGui.btn_list[0].pos[0],  self.mainMenuGui.btn_list[0].pos[1] + 70),
            width = 230,
            height = 60,
            text = "Achievements",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.achievementsGui.open_menu
        )
        self.mainMenuGui.create_btn(
            pos=(self.mainMenuGui.btn_list[1].pos[0]+250,  self.mainMenuGui.btn_list[0].pos[1] + 70),
            width = 230,
            height = 60,
            text = "Credits",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.creditsGui.open_menu
        )
        self.mainMenuGui.create_btn(
            pos=(self.mainMenuGui.btn_list[0].pos[0],  self.mainMenuGui.btn_list[1].pos[1] + 70),
            width = 480,
            height = 60,
            text = "Settings",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.settingsGui.open_menu
        )

        if not is_web_asm():
            self.mainMenuGui.create_btn(
                pos=(self.mainMenuGui.btn_list[0].pos[0],  self.mainMenuGui.btn_list[3].pos[1] + 70),
                width = 480,
                height = 60,
                text = "Quit",
                color = COLORS["WHITE"],
                hover_color = COLORS["GRAY"],
                text_color = COLORS["BLACK"],
                border_color=COLORS["BLACK"],
                funct=quit_game
            )
        #--Achievements gui
        #--row 1
        self.achievementsGui.create_text(
            pos = (20,  self.achievementsGui.menu_rect.top + 90),
            text_content = "First steps",
            text_color = (COLORS["WHITE"] if "First steps" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=32
        )
        self.achievementsGui.create_text(
            pos = (20,  self.achievementsGui.txt_list[0].text_pos[1] + 30),
            text_content = "Reach the first 10 digits of Pi",
            text_color = (COLORS["WHITE"] if "First steps" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=26
        )

        self.achievementsGui.create_text(
            pos = (180,  self.achievementsGui.txt_list[0].text_pos[1]),
            text_content = "Semicentennial",
            text_color = (COLORS["WHITE"] if "Semicentennial" in self.achievement_titles_lst else COLORS["GRAY"]),
            align="right",
            font_name=None,
            font_size=32
        )
        self.achievementsGui.create_text(
            pos = (self.achievementsGui.txt_list[2].text_pos[0],  self.achievementsGui.txt_list[0].text_pos[1] + 30),
            text_content = "half way to the first 100 digits",
            text_color = (COLORS["WHITE"] if "Semicentennial" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=26
        )
        #--row 2
        self.achievementsGui.create_text(
            pos = (20,  self.achievementsGui.txt_list[1].text_pos[1] + 30),
            text_content = "Triple digits",
            text_color = (COLORS["WHITE"] if "Triple digits" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=32
        )
        self.achievementsGui.create_text(
            pos = (20,  self.achievementsGui.txt_list[4].text_pos[1] + 30),
            text_content = "reach 100 digits of pi",
            text_color = (COLORS["WHITE"] if "Triple digits" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=26
        )

        self.achievementsGui.create_text(
            pos = (260,  self.achievementsGui.txt_list[3].text_pos[1] + 30),
            text_content = "500 club",
            text_color = (COLORS["WHITE"] if "500 club" in self.achievement_titles_lst else COLORS["GRAY"]),
            align="right",
            font_name=None,
            font_size=32
        )
        self.achievementsGui.create_text(
            pos = (self.achievementsGui.txt_list[2].text_pos[0],  self.achievementsGui.txt_list[4].text_pos[1] + 30),
            text_content = "reach 500 digits of pi",
            text_color = (COLORS["WHITE"] if "500 club" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=26
        )

        #--row 3
        self.achievementsGui.create_text(
            pos = (20,  self.achievementsGui.txt_list[5].text_pos[1] + 30),
            text_content = "Pi Millennium",
            text_color = (COLORS["WHITE"] if "Pi Millennium" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=32
        )
        self.achievementsGui.create_text(
            pos = (self.achievementsGui.txt_list[0].text_pos[0],  self.achievementsGui.txt_list[8].text_pos[1] + 30),
            text_content = "Reach 1000 digits (thus beating the game)",
            text_color = (COLORS["WHITE"] if "Pi Millennium" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=26
        )

        self.achievementsGui.create_text(
            pos = (200,  self.achievementsGui.txt_list[8].text_pos[1]),
            text_content = "High Achiever",
            text_color = (COLORS["WHITE"] if "High Achiever" in self.achievement_titles_lst else COLORS["GRAY"]),
            align="right",
            font_name=None,
            font_size=32
        )
        self.achievementsGui.create_text(
            pos = (self.achievementsGui.txt_list[10].text_pos[0],  self.achievementsGui.txt_list[9].text_pos[1]),
            text_content = "Beat your high score for the first time",
            text_color = (COLORS["WHITE"] if "High Achiever" in self.achievement_titles_lst else COLORS["GRAY"]),
            font_name=None,
            font_size=26
        )
        #--Bottom btn
        self.achievementsGui.create_btn(
            pos=((WIDTH//2) - (480//2),  self.achievementsGui.txt_list[9].text_pos[1] + 90),
            width = 480,
            height = 60,
            text = "Back",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=(self.back_btn if globalvars.flags["main"] else self.pauseGui.open_menu)
        )

        #--Credits gui
        self.creditsGui.create_btn(
            pos=((WIDTH//2) - (480//2),  self.creditsGui.menu_rect.top + 220),
            width = 480,
            height = 60,
            text = "Back",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=(self.back_btn if globalvars.flags["main"] else self.pauseGui.open_menu)
        )
        self.creditsGui.create_text(
            pos = ((self.creditsGui.menu_rect.centerx)//2,  self.creditsGui.menu_rect.top + 60),
            text_content = "Developer: pumped.dev",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32
        )
        self.creditsGui.create_text(
            pos = (self.creditsGui.txt_list[0].text_pos[0],  self.creditsGui.txt_list[0].text_pos[1] + 60),
            text_content = "Textures: FreePik",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32
        )
        self.creditsGui.create_text(
            pos = (self.creditsGui.txt_list[0].text_pos[0],  self.creditsGui.txt_list[1].text_pos[1] + 60),
            text_content = "Music: No Place To Go - pixabay",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32
        )

        #Settings gui
        #--create tabs
        self.settingsGui.add_tabs(["General", "Audio"])
        #--content 1
        self.settingsGui.create_btn(
            pos=(20,  self.settingsGui.menu_rect.top + 60),
            width = (WIDTH//2) - 20,
            height = 60,
            text = "General",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.settingsGui.change_tab_state,
            funct_args_enabled=True,
            funct_args=0
        )
        self.settingsGui.create_btn(
            pos=((WIDTH // 2),  self.settingsGui.menu_rect.top + 60),
            width = (WIDTH//2) - 20,
            height = 60,
            text = "Audio",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.settingsGui.change_tab_state,
            funct_args_enabled=True,
            funct_args=1
        )
        #---Settings tab content
        self.settingsGui.create_text(
            pos = (self.settingsGui.btn_list[0].pos[0] + 20,  self.settingsGui.btn_list[0].pos[1]+90),
            text_content = "Difficulty: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=0,
            text_attr=("selectionbox", 0)
        )
        self.settingsGui.create_selectionbox(
            pos=(self.settingsGui.tab_content[0]["text"][0].text_pos[0],  self.settingsGui.tab_content[0]["text"][0].text_pos[1]),
            options=["Easy", "Normal", "Hard"],
            select_val_main="difficulty",
            def_index=globalvars.difficulty,
            tab_content_id=0,
            is_tab_content=True,
            has_arrows=True,
            callback_fn=change_difficulty
        )
        self.settingsGui.create_text(
            pos = (self.settingsGui.btn_list[0].pos[0] + 20,  self.settingsGui.btn_list[0].pos[1]+90),
            text_content = "FPS Cap: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=0,
            text_attr=("input_box", 0)
        )
        self.settingsGui.create_input_box(
            pos = (self.settingsGui.tab_content[0]["text"][1].text_pos[0],  self.settingsGui.tab_content[0]["text"][1].text_pos[1]),
            size=(64, 32),
            is_tab_content=True,
            tab_content_id=0,
            text_type="int",
            def_text=globalvars.settings["graphics"]["fps_cap"],
            fn_callback=update_global_settings_value,
            fn_args=["graphics", "fps_cap"]
        )
        self.settingsGui.create_text(
            pos = (self.settingsGui.btn_list[0].pos[0] + 20,  self.settingsGui.btn_list[0].pos[1]+90),
            text_content = "Debug Mode: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=0,
            text_attr=("checkbox", 0)
        )
        self.settingsGui.create_checkbox(
            pos = (self.settingsGui.tab_content[0]["text"][2].text_pos[0],  self.settingsGui.tab_content[0]["text"][2].text_pos[1]),
            size=(32, 32),
            is_tab_content=True,
            def_value=globalvars.settings["general"]["debug_mode"],
            tab_content_id=0,
            check_val_main="general",
            check_val_sub="debug_mode"
        )
        self.settingsGui.create_text(
            pos = (self.settingsGui.btn_list[0].pos[0] + 20,  self.settingsGui.btn_list[0].pos[1]+90),
            text_content = "Reset Game: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=0,
            text_attr=("button", 0)
        )
        self.settingsGui.create_btn(
            pos=(self.settingsGui.tab_content[0]["text"][2].text_pos[0],  self.settingsGui.tab_content[0]["text"][2].text_pos[1]),
            width = 100,
            height = 36,
            text = "Reset",
            color = COLORS["LIGHT_RED"],
            hover_color = COLORS["CRIMSON"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.open_popup,
            funct_args_enabled=False,
            is_tab_content=True,
            tab_content_id=0
        )

        #----Audio
        self.settingsGui.create_text(
            pos = (self.settingsGui.btn_list[0].pos[0] + 20,  self.settingsGui.btn_list[0].pos[1]+90),
            text_content = "Music Enabled: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=1,
            text_attr=("checkbox", 0)
        )
        self.settingsGui.create_checkbox(
            pos = (self.settingsGui.tab_content[1]["text"][0].text_pos[0],  self.settingsGui.tab_content[1]["text"][0].text_pos[1]),
            size=(32, 32),
            is_tab_content=True,
            def_value=globalvars.settings["audio"]["music_enabled"],
            tab_content_id=1,
            check_val_main="audio",
            check_val_sub="music_enabled"
        )
        self.settingsGui.create_text(
            pos = (self.settingsGui.btn_list[0].pos[0] + 20,  self.settingsGui.btn_list[0].pos[1]+90),
            text_content = "Sound Enabled: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=1,
            text_attr=("checkbox", 1)
        )
        self.settingsGui.create_checkbox(
            pos = (self.settingsGui.tab_content[1]["text"][1].text_pos[0],  self.settingsGui.tab_content[1]["text"][1].text_pos[1]),
            size=(32, 32),
            is_tab_content=True,
            def_value=globalvars.settings["audio"]["sound_enabled"],
            tab_content_id=1,
            check_val_main="audio",
            check_val_sub="sound_enabled"
        )

        self.settingsGui.create_text(
            pos = (self.settingsGui.btn_list[0].pos[0] + 20,  self.settingsGui.btn_list[0].pos[1]+90),
            text_content = "Sound Volume: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=1,
            text_attr=("slider", 0)
        )
        self.settingsGui.create_slider(
            pos = (self.settingsGui.tab_content[1]["text"][0].text_pos[0],  self.settingsGui.tab_content[1]["text"][0].text_pos[1]),
            is_tab_content=True,
            tab_content_id=1,
            bar_width=128,
            filled_percentage=globalvars.settings["audio"]["sound_vol"],
            callback_fn=update_global_settings_value,
            callback_fn_args=["audio", "sound_vol"],
            thumb_radius=24
        )

        self.settingsGui.create_text(
            pos = (self.settingsGui.btn_list[0].pos[0] + 20,  self.settingsGui.btn_list[0].pos[1]+90),
            text_content = "Music Volume: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=1,
            text_attr=("slider", 1)
        )
        self.settingsGui.create_slider(
            pos = (self.settingsGui.tab_content[1]["text"][1].text_pos[0],  self.settingsGui.tab_content[1]["text"][1].text_pos[1]),
            is_tab_content=True,
            tab_content_id=1,
            bar_width=128,
            filled_percentage=globalvars.settings["audio"]["music_vol"],
            callback_fn=update_global_settings_value,
            callback_fn_args=["audio", "music_vol"],
            thumb_radius=24
        )

        #Main
        self.mainGui.create_btn(
            pos=(WIDTH//2 - 60 //2, 60 + HEIGHT//2),
            width = 60,
            height = 60,
            text = "Restart",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["WHITE"],
            img="resources/icons/restart.png",
            border_color=COLORS["BLACK"],
            funct=self.btn_cmds["restart_game"]
        )

        self.pauseGui.create_btn(
            pos=((WIDTH//2) - (480//2),  self.pauseGui.menu_rect.top + 80),
            width = 480,
            height = 60,
            text = "Resume",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.pauseGui.close_menu
        )
        self.pauseGui.create_btn(
            pos=(self.pauseGui.btn_list[0].pos[0],  self.pauseGui.btn_list[0].pos[1] + 70),
            width = 480,
            height = 60,
            text = "Settings",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.settingsGui.open_menu
        )
        self.pauseGui.create_btn(
            pos=(self.pauseGui.btn_list[0].pos[0],  self.pauseGui.btn_list[1].pos[1] + 70),
            width = 480,
            height = 60,
            text = "Quit",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=self.return_to_main_menu
        )