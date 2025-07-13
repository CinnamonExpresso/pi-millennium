from behavior.gui.guiEngine import GUI, FullMenu
from behavior.settings import *
from behavior.utils.generalUtils import quit_game
import data.globalvars as globalvars

class Visuals:
    def __init__(self, screen, btn_cmds):
        self.btn_cmds = btn_cmds
        self.surface = screen

        #build guis
        self.mainGui = GUI(surface=screen)
        self.settingsGui = FullMenu(surface=self.surface, menu_header="Settings", menu_state_type="settings", bg_overlay=True, tabs_enabled=True)
        self.pauseGui = FullMenu(surface=self.surface, menu_header="Pi Counter", menu_state_type="pause", bg_overlay=True)

        #Build rects
        self.pauseGui.create_menu_rects("center")
        self.settingsGui.create_menu_rects("top")

    def build_gui(self):
        #Settings gui
        #--create tabs
        self.settingsGui.add_tabs(["General", "Audio"])
        #--content 1
        self.settingsGui.create_btn(
            pos=(20,  self.settingsGui.menu_rect.top + 60),
            width = 230,
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
            pos=((self.settingsGui.btn_list[0].pos[0] + 240),  self.settingsGui.menu_rect.top + 60),
            width = 230,
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
            text_content = "Debug Mode: ",
            text_color = COLORS["WHITE"],
            font_name=None,
            font_size=32,
            is_tab_content=True,
            tab_content_id=0,
            text_attr=("checkbox", 0)
        )
        self.settingsGui.create_checkbox(
            pos = (self.settingsGui.tab_content[0]["text"][0].text_pos[0],  self.settingsGui.tab_content[0]["text"][0].text_pos[1]),
            size=(32, 32),
            is_tab_content=True,
            def_value=globalvars.settings["general"]["debug_mode"],
            tab_content_id=0,
            check_val_main="general",
            check_val_sub="debug_mode"
        )

        #----Audio
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
            callback_fn=self.settingsGui.update_global_settings_value,
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
            callback_fn=self.settingsGui.update_global_settings_value,
            callback_fn_args=["audio", "music_vol"],
            thumb_radius=24
        )

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

        #Main
        self.mainGui.create_btn(
            pos=(WIDTH//2 - 60 //2, 60 + HEIGHT//2),
            width = 60,
            height = 60,
            text = "Restart",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["WHITE"],
            img="restart.png",
            border_color=COLORS["BLACK"],
            funct=self.btn_cmds["restart_game"]
        )

        self.pauseGui.create_btn(
            pos=((self.pauseGui.menu_rect.centerx)//2,  self.pauseGui.menu_rect.top + 80),
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
            text = "Exit",
            color = COLORS["WHITE"],
            hover_color = COLORS["GRAY"],
            text_color = COLORS["BLACK"],
            border_color=COLORS["BLACK"],
            funct=quit_game
        )