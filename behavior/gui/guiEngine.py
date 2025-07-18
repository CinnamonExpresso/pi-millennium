import pygame
import data.globalvars as globalvars
from behavior.utils.timer import Timer
from behavior.settings import WIDTH, HEIGHT, COLORS
from behavior.utils.generalUtils import reset_menu_state, change_game_speed, update_pause_states, update_timers

#Made this for an old project, so some of the ui here may be a bit verbose

#Class for handeling gui buttons
class GuiBtn:
    def __init__(self, pos, height, surface, width, text, color, hover_color, text_color, img=None, border_color=None, border_width=2, funct=None, tooltip_color=COLORS["WHITE"], funct_args=None, flags:list[bool]=[False]):
        self.pos = pos
        self.height = height
        self.surface = surface
        self.width = width
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.border_color = border_color
        self.border_width = border_width
        self.funct = funct #Executes function when clicked
        self.tooltip_color = tooltip_color
        self.funct_args = funct_args #optional callback function arguments
        self.flags = {
            "tooltips_enabled": flags[0],
            "tooltip_active": False
        }
        self.timers = {
            "btn_click": Timer(100), #Prevents click spam
            "tooltip_hover": Timer(2000), #Time needed for tool tip appearing
            "tooltip_hover_recent": Timer(2000) #Timer to prevent flickering on the tooltip
        }

        if img:
            self.img = pygame.image.load(f"./{img}")
        else: 
            self.img = None

    def apply_clicked_tab(self):
        base_color = self.color
        clicked_color = tuple(max(0, int(c * 0.7)) for c in base_color[:3])
        pygame.draw.rect(self.surface, clicked_color, self.rect.inflate(-self.border_width * 2, -self.border_width * 2), border_radius=5)

    def input(self, recent_click):
        if pygame.mouse.get_pressed()[0] and (not self.timers["btn_click"].active or not recent_click):
            self.timers["btn_click"].activate()

            if self.funct:
                if self.funct_args:
                    self.funct(self.funct_args)
                else:
                    self.funct()

    def change_state(self):
        pass

    def draw(self, recent_click):
        #Draw border
                    if self.border_color:
                        pygame.draw.rect(self.surface, self.border_color, self.rect, border_radius=5)
                    
                    # Draw main button (with hover effect)
                    if self.rect.collidepoint(self.mouse_pos):
                        pygame.draw.rect(self.surface, self.hover_color, self.rect.inflate(-self.border_width * 2, -self.border_width * 2), border_radius=5)
                    else:
                        pygame.draw.rect(self.surface, self.color, self.rect.inflate(-self.border_width * 2, -self.border_width * 2), border_radius=5)

                    # Draw image if available
                    if self.img:
                        # Resize the image if needed to fit inside the button
                        img = pygame.transform.scale(self.img, (self.height - 16, self.height - 16))  # square fit
                        img_rect = img.get_rect(midleft=(self.rect.left + 8, self.rect.centery))
                        self.surface.blit(img, img_rect)
                    else:
                        # No image: just center the text
                        text_surf = self.font.render(self.text, True, self.text_color)
                        text_rect = text_surf.get_rect(center=self.rect.center)
                        self.surface.blit(text_surf, text_rect)
                    
                    #Apply tooltips
                    if self.rect.collidepoint(self.mouse_pos):
                        if self.flags["tooltips_enabled"]:
                            if  self.timers["tooltip_hover_recent"].active:
                                self.timers["tooltip_hover_recent"].update()

                            if self.timers["tooltip_hover_recent"].finished():
                                if not self.timers["tooltip_hover"].active and not self.flags["tooltip_active"]:
                                    self.timers["tooltip_hover"].activate()
                                else:
                                    self.timers["tooltip_hover"].update()

                            # If hover timer is finished, mark tooltip as active
                            if not self.timers["tooltip_hover"].active:
                                self.flags["tooltip_active"] = True

                            # Show tooltip after timer has ended
                            if self.flags["tooltip_active"]:
                                # Render the text
                                text_surf = self.font.render(self.text, True, self.tooltip_color)
                                text_rect = text_surf.get_rect()

                                # Padding around the text
                                padding = 6
                                tooltip_width = text_rect.width + padding * 2
                                tooltip_height = text_rect.height + padding * 2

                                # Tooltip position (above the button)
                                tooltip_x = self.rect.centerx + tooltip_width // 2
                                tooltip_y = self.rect.centery - tooltip_height // 2

                                # Draw tooltip background (black with border radius)
                                tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
                                pygame.draw.rect(self.surface, (0, 0, 0), tooltip_rect, border_radius=5)

                                # Blit the text centered in the tooltip
                                text_pos = (tooltip_rect.centerx - text_rect.width // 2, tooltip_rect.centery - text_rect.height // 2)
                                self.surface.blit(text_surf, text_pos)

                        #Execute function on click
                        self.input(recent_click)

    def update(self, recent_click=False):
        self.mouse_pos = pygame.mouse.get_pos()
        self.draw(recent_click=recent_click)

        if self.timers["btn_click"].active:
            self.timers["btn_click"].update()

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class GuiText:
    def __init__(self, pos, text_content, text_color=(0,0,0,1), font_size=42, font_name="./resources/fonts/consolas.ttf", text_attr=None):
        self.text_pos = pos
        self.text_content = text_content
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, font_size)
        self.font_name = font_name
        self.text_attr=text_attr #tuple for pairing checkboxes, sliders, etc with text. index 0: type, index 1: the corrasponding index where type is located

    def create_text(self, align:str="center"):
        self.text_surf = self.font.render(self.text_content, True, self.text_color)
        if align == "right":
            text_width = self.text_surf.get_width()
            new_pos = list(self.text_pos)
            new_pos[0] = WIDTH - text_width - new_pos[0]
            self.text_pos = (new_pos[0], new_pos[1])
        elif align == "left":
            self.text_rect = self.text_surf.get_rect()
            self.text_rect.topleft = self.text_pos
        else:
            self.text_rect = self.text_surf.get_rect()
            self.text_rect.center = self.text_pos

    #Changes font
    def change_font(self, font_size:int, font_name:bool|str=None):
        self.font_size = font_size
        self.font_name = font_name
        self.font = pygame.font.Font(self.font_name, self.font_size)

#For checkboxes
class GuiCheckbox:
    def __init__(self, pos, surface, check_val_main, def_value=False, check_val_sub=None, size=64, checked_color=(0, 167, 16, 1), unchecked_color=(255,255,255,1), border_color=(22, 22, 22, 1), border_width:int=3):
        self.pos = pos
        self.surface = surface
        self.size = size
        self.checked_color = checked_color
        self.unchecked_color = unchecked_color
        self.is_active = def_value
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.border_color = border_color
        self.check_val_main = check_val_main #value that is changed on checked
        self.check_val_sub = check_val_sub #optional field for nested dicts
        self.border_width = border_width

    #Change value of checkval
    def change_checkval_value(self):
        if self.check_val_sub:
            globalvars.settings[self.check_val_main][self.check_val_sub] = self.is_active
        else:
            globalvars.settings[self.check_val_main] = self.is_active

    #draw rect
    def draw(self):
        pygame.draw.rect(surface=self.surface, color=self.border_color, rect=self.rect, width=self.border_width, border_radius=5)
        #render checkbox
        if self.is_active:
            pygame.draw.rect(surface=self.surface, color=self.checked_color, rect=self.rect.inflate(-self.border_width*2, -self.border_width*2), border_radius=5)
        else:
            pygame.draw.rect(surface=self.surface, color=self.unchecked_color, rect=self.rect.inflate(-self.border_width*2, -self.border_width*2), border_radius=5)

    #Change check state
    def change_state(self):
        self.is_active = not self.is_active
        self.change_checkval_value()

#For sliders
class GuiSlider:
    def __init__(self, surface, pos: tuple[int], bg_color=(62, 62, 62), filled_color=(0, 82, 255), thumb_radius=6, filled_percentage=0.0,
                 bar_width=128, bar_height=16, border_color=(22, 22, 22), callback_fn=None, callback_fn_args=None,
                 thumb_color=(65, 126, 255)):
        self.surface = surface
        self.pos = pos
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = 2
        self.filled_color = filled_color
        self.thumb_radius = thumb_radius
        self.thumb_color = thumb_color
        self.filled_percentage = max(0.0, min(1.0, filled_percentage))
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.bar_width, self.bar_height)  # Bar rect
        self.thumb_rect = pygame.Rect(self.pos[0], self.pos[1], self.thumb_radius, self.thumb_radius)
        self.callback_fn = callback_fn
        self.callback_fn_args = callback_fn_args
        self.timers = {
            "keys": Timer(duration=100),
            "submit": Timer(duration=100)
        }

        self.dragging = False

    def update_thumb_position(self):
        self.filled_percentage = max(0.0, min(1.0, self.filled_percentage))
        
        # Position the center of the thumb at the end of the filled bar
        center_x = self.rect.left + int(self.filled_percentage * self.rect.width)

        self.thumb_rect.x = center_x - self.thumb_rect.width // 2
        self.thumb_rect.y = self.rect.centery - self.thumb_rect.height // 2

    def draw(self):
        self.timers = update_timers(self.timers)

        pygame.draw.rect(self.surface, self.border_color, self.rect, width=self.border_width, border_radius=5) #border
        pygame.draw.rect(self.surface, self.bg_color, self.rect.inflate(-self.border_width * 2, -self.border_width * 2), border_radius=5) #bar BG

        # Filled portion
        filled_width = int(self.filled_percentage * self.rect.width)
        filled_rect = pygame.Rect(self.rect.left, self.rect.top, filled_width, self.rect.height)
        pygame.draw.rect(self.surface, self.filled_color, filled_rect, border_radius=5)

        pygame.draw.rect(self.surface, self.thumb_color, self.thumb_rect, border_radius=self.thumb_radius) #thumb

    def change_state(self):
        pass
    
    def change_slider_pos(self, type, value):
        # Change filled_percentage by a relative amount
        if type == "keys":
            self.filled_percentage = max(0.0, min(1.0, self.filled_percentage + value))
        else: #otherwise we can assume it was a mouse click
            self.filled_percentage = max(0.0, min(1.0, value / self.rect.width))
        self.update_thumb_position()

        # Optional: trigger callback
        if self.callback_fn and not self.timers["submit"].active:
            self.timers["submit"].activate()
            if self.callback_fn_args:
                self.callback_fn(*self.callback_fn_args, self.filled_percentage)
            else:
                self.callback_fn(self.filled_percentage)

    def handle_event(self): #user input
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if self.thumb_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]: #switch on slider click
            self.dragging = True
        if not self.thumb_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]: #turn false if player clicks out
            self.dragging = False
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]: #update slider to mouse click pos
            rel_x = mouse_pos[0] - self.rect.left
            self.change_slider_pos(type="mouse", value=rel_x)

        if self.dragging:
            if keys[pygame.K_LEFT] and not self.timers["keys"].active:
                self.timers["keys"].activate()
                self.change_slider_pos(type="keys", value=-0.05)  # decrease by 5%

            if keys[pygame.K_RIGHT] and not self.timers["keys"].active:
                self.timers["keys"].activate()
                self.change_slider_pos(type="keys", value=0.05) # increase by 5%

            #submit
            if keys[pygame.K_RETURN] and not self.timers["submit"].active:
                self.change_slider_pos()
                self.dragging = False

    def update(self):
        self.draw()
        self.handle_event()

#Selection box, user can click the box to cycle through different options
class GuiSelectionBox:
    def __init__(self, pos, surface, options, select_val_main, def_index=0, select_val_sub=None, size=(100, 36), text_color=(0, 0, 0), box_color=(255, 255, 255), border_color=(22, 22, 22), border_width=3, font=None, callback_fn=None, has_arrows=False):
        self.pos = pos
        self.surface = surface
        self.options = options #List of selection options Ex: ["easy", "medium", "hard"]
        self.size = size
        self.select_val_main = select_val_main
        self.select_val_sub = select_val_sub
        self.text_color = text_color
        self.box_color = box_color
        self.border_color = border_color
        self.border_width = border_width
        self.current_index = def_index #represents the starting options
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.font = font or pygame.font.Font(None, 32)
        self.update_selected_value()
        self.timers = {
            "selection_cooldown": Timer(duration=100) #prevent spam, can be adjust obv
        }
        self.flags= {
            "has_arrows": has_arrows #shows arrow images
        }
        self.callback_fn = callback_fn #Call back function that executes when a change in state occurs

        if self.flags["has_arrows"]:
            self.__create_arrows()

    #Generate arrow img
    def __create_arrows(self):
        self.__left_arrow_img = pygame.image.load(f"./resources/icons/left-arrow.png").convert_alpha()
        self.__right_arrow_img = pygame.image.load(f"./resources/icons/right-arrow.png").convert_alpha()

    def update_selected_value(self):
        selected_value = self.options[self.current_index]
        if self.select_val_sub:
            globalvars.settings[self.select_val_main][self.select_val_sub] = selected_value
        else:
            globalvars.settings[self.select_val_main] = selected_value

    def draw(self):
        # Draw border
        pygame.draw.rect(surface=self.surface, color=self.border_color, rect=self.rect, width=self.border_width, border_radius=5)
        # Draw box
        inner_rect = self.rect.inflate(-self.border_width*2, -self.border_width*2)
        pygame.draw.rect(surface=self.surface, color=self.box_color, rect=inner_rect, border_radius=5)

        # Render current option text
        text_surf = self.font.render(str(self.options[self.current_index]), True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surface.blit(text_surf, text_rect)

        # Show arrow icons
        if self.flags["has_arrows"] and self.rect.collidepoint(self.mouse_pos):
            size = list(self.size)
            left_arrow_img = pygame.transform.scale(self.__left_arrow_img, (size[1] - 20, size[1] - 20))  # square fit
            self.surface.blit(left_arrow_img, self.__left_arrow_rect)

            right_arrow_img = pygame.transform.scale(self.__right_arrow_img, (size[1] - 20, size[1] - 20))  # square fit
            self.surface.blit(right_arrow_img, self.__right_arrow_rect)

    def change_state(self, click_type=None):
        if not click_type:
            self.current_index = (self.current_index + 1) % len(self.options)
        elif click_type == "Right":
            self.current_index = (self.current_index + 1) % len(self.options)
        elif click_type == "Left":
            self.current_index = (self.current_index - 1) % len(self.options)

        self.update_selected_value()
        self.timers["selection_cooldown"].activate()

        if self.callback_fn:
            self.callback_fn(self.current_index)

    def __update_arrow_rects(self):
        size = list(self.size)
        if self.flags["has_arrows"]:
            self.__left_arrow_rect = pygame.transform.scale(
                self.__left_arrow_img, (size[1] - 20, size[1] - 20)
            ).get_rect(midleft=(self.rect.left + 2, self.rect.centery))

            self.__right_arrow_rect = pygame.transform.scale(
                self.__right_arrow_img, (size[1] - 20, size[1] - 20)
            ).get_rect(midright=(self.rect.right - 2, self.rect.centery))

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.__update_arrow_rects()
        self.handle_event()
        self.draw()
        self.timers["selection_cooldown"].update()

    def handle_event(self):
        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] and not self.timers["selection_cooldown"].active:
            if self.rect.collidepoint(mouse_pos) and not self.flags["has_arrows"]:
                self.change_state()
            elif self.flags["has_arrows"]:
                if self.__right_arrow_rect.collidepoint(mouse_pos):
                    self.change_state(click_type="Right")
                elif self.__left_arrow_rect.collidepoint(mouse_pos):
                    self.change_state(click_type="Left")

#For input boxes
class GuiInputBox:
    def __init__(self, surface, pos:tuple[int], size:tuple[int]=(64,20), color:tuple[int|float]=(255,255,255,1), border_color:tuple[int|float]=(22, 22, 22, 1), clicked_border_color:tuple[int|float]=(0, 90, 152, 1), border_width:int=3, font_color:tuple[int|float]=(0,0,0,1), font_size:int=32, font_name:str=None, text_type:str="int", def_text:str="", text_length_limit:tuple[int]=(1,3), fn_callback=None, fn_args=None, auto_submit:bool=False):
        self.pos = pos
        self.surface = surface
        self.size = size
        self.color = color
        self.clicked_border_color = clicked_border_color
        self.border_color = border_color
        self.border_width = border_width
        self.font_color = font_color
        self.font_size = font_size
        self.font_name = font_name
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.font = pygame.font.Font(font_name, font_size)
        self.text_type = text_type
        self.def_text = def_text
        self.text_input = str(def_text)
        self.text = GuiText(pos=(self.rect.left + 5, self.rect.top + (self.rect.height//2)//2), text_content=self.def_text, text_color=self.border_color, font_size=self.font_size, font_name=self.font_name, text_attr=None)
        self.text_rect = None
        self.text_pos = len(self.text_input) #keeps track of text cursor position
        self.text_length_limit = text_length_limit #(0, 0) = min and max allowed length of text
        self.fn_callback = fn_callback #call back function that calls when text input if modified
        self.fn_args = fn_args #[arg1, arg2, etc]: optional call back arguments
        self.timers = {
            "blink": Timer(duration=500),
            "keys": Timer(duration=100),
            "submit": Timer(duration=100)
        }
        #Flags
        self.is_active = False #Flag for detecting input box click state
        self.auto_submit = False #Flag for auto submitting

        #blink attr
        self.blink_visible = True
        self.blink_rect = None

    #Blink effect
    def blink_effect(self):
        if self.timers["blink"].active:
            if self.blink_visible:
                self.change_blinker()
                pygame.draw.rect(surface=self.surface, color=self.border_color, rect=self.blink_rect, border_radius=5)
        else:
            self.blink_visible = not self.blink_visible
            self.timers["blink"].activate()

    #submits text
    def submit(self):
        if self.fn_callback and not self.timers["submit"].active: #Execute callback function if it exists
                if self.text_length_limit[0] <= len(self.text_input) <= self.text_length_limit[1]:
                    self.timers["submit"].activate()
                    if self.text_type == "int":
                        if self.fn_args:
                            self.fn_callback(*self.fn_args, int(self.text_input))
                        else:
                            self.fn_callback(int(self.text_input))

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["keys"].active:
            if keys[pygame.K_LEFT]: #move txt cursor left
                self.timers["keys"].activate()

                if self.text_pos > 0:
                    self.text_pos -= 1
            elif keys[pygame.K_RIGHT]: #move txt cursor right
                self.timers["keys"].activate()

                if self.text_pos <= len(self.text_input):
                    self.text_pos += 1
            elif keys[pygame.K_BACKSPACE]: #delete char
                if self.text_pos <= 0:
                    self.text_pos = 0
                elif self.text_pos <= len(self.text_input):
                    self.timers["keys"].activate()

                    txt = list(self.text_input)
                    txt.pop(self.text_pos-1)

                    if self.text_pos > 0:
                        self.text_pos -= 1
                    
                    self.text_input = "".join(txt)
            
            #get key input
            if len(self.text_input) <= self.text_length_limit[1]:
                if "int" in self.text_type:
                    #numbers 0-9
                    for i in range(10):
                        if keys[pygame.K_0 + i]:
                            self.timers["keys"].activate()
                            txt = list(self.text_input)
                            txt.insert(self.text_pos, str(i))
                            self.text_input = "".join(txt)

                            if self.text_pos < len(self.text_input):
                                self.text_pos += 1
                            break 
                if "char" in self.text_type:
                    #get a-z
                    shift_held = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

                    for i in range(pygame.K_a, pygame.K_z + 1):
                        if keys[i]:
                            self.timers["keys"].activate()
                            char = chr(i).upper() if shift_held else chr(i) #account for upper/lower case

                            txt = list(self.text_input)
                            txt.insert(self.text_pos, char)
                            self.text_input = "".join(txt)

                            if self.text_pos < len(self.text_input):
                                self.text_pos += 1
                            break 
        else:
            if self.auto_submit: #If auto submitting is enabled
                self.submit()

        #handle submit
        if keys[pygame.K_RETURN]:
            self.submit()

    def update(self):
        if self.is_active:
            self.input()
        self.draw()

    #draw rect
    def draw(self):
        self.timers = update_timers(self.timers)

        if self.is_active:
            pygame.draw.rect(surface=self.surface, color=self.clicked_border_color, rect=self.rect, width=self.border_width, border_radius=5) #Render border
        else:
            pygame.draw.rect(surface=self.surface, color=self.border_color, rect=self.rect, width=self.border_width, border_radius=5)

        pygame.draw.rect(surface=self.surface, color=self.color, rect=self.rect.inflate(-self.border_width*2, -self.border_width*2))
        
        if self.is_active:
            self.blink_effect()

        # Render the text
        text_surf = self.text.font.render(str(self.text_input), True, self.border_color)
        self.text_rect = text_surf.get_rect()
        self.surface.blit(text_surf, (self.rect.left + 5, self.rect.top + (self.rect.height - self.text_rect.height)//2))

    #Changes font
    def change_font(self, font_size:int, font_name:bool|str=None):
        self.font_size = font_size
        self.font_name = font_name
        self.font = pygame.font.Font(self.font_name, self.font_size)
    
    def change_blinker(self):
        substring = self.text_input[:self.text_pos]
        cursor_x_offset = self.font.size(substring)[0]
        
        text_surf = self.text.font.render(str(self.text_input), True, self.border_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (self.rect.left + 5, self.rect.top + (self.rect.height - text_rect.height) // 2)
        self.text_rect = text_rect

        self.blink_rect = pygame.Rect(
            self.rect.left + 5 + cursor_x_offset,  # small space to the right of text
            self.rect.top + (self.rect.height - self.text.font.get_height()) // 2,  # vertical centering
            2,  # cursor width
            self.text.font.get_height()     # match cursor height to text height
        )

    #Indicates the input box is being used
    def change_state(self):
        if self.text_input:
            self.change_blinker()
        else:
            self.blink_rect = pygame.Rect(self.rect.left + 5, self.rect.top + (self.rect.height//2)//2, 2, self.rect.height//2)
        self.is_active = not self.is_active

#Main GUI class for menu management
class GUI:
    def __init__(self, surface, tabs_enabled=False):
        self.font = pygame.font.Font(None, 42)
        self.btn_list = []
        self.txt_list = []
        self.slider_list = []
        self.input_box_list = []
        self.checkbox_list = []
        self.timers = {
            "btn_click": Timer(100), #Prevents click spam
            "tooltip_hover": Timer(2000), #Time needed for tool tip appearing
            "tooltip_hover_recent": Timer(2000) #Timer to prevent flickering on the tooltip
        }
        self.surface = surface
        self.menu_rect = None
        self.flags = {
            "tooltip_active": False, #Flag for checking if a tooltip is active
            "menu_open": False, #Menu opened flag
            "tabs_enabled": tabs_enabled #Flag for enableing tabs
        }

        if tabs_enabled:
            self.tab_state:list[str] = []
            self.cur_tab:int = 0

            self.tab_content = {}

    #add tabs
    def add_tabs(self, tabs:list[str]):
        if self.flags["tabs_enabled"]:
            for tab in tabs:
                self.tab_state.append(tab)
    
    #changes the tab state
    def change_tab_state(self, tab:int=0):
        if self.flags["tabs_enabled"]:
            self.cur_tab = tab

    #Opens menu
    def open_menu(self):
        self.flags["menu_open"] = not self.flags["menu_open"]
        self.timers["btn_click"].activate()
        update_pause_states()

    #Updates gui
    def update(self):
        self.draw()

        #Update timers as long as a timer is active
        if any(timer.active for timer in self.timers.values()):
            self.timers = update_timers(self.timers)
    
    #append tab content
    def new_tab_content(self, type, obj, tab_content_id):
        new_content_lst = []
        if tab_content_id in self.tab_content and self.tab_content[tab_content_id][type]:
            for item in self.tab_content[tab_content_id][type]:
                new_content_lst.append(item)
        else:
            if tab_content_id not in self.tab_content:
                self.tab_content[tab_content_id] = {
                    "text": None,
                    "checkbox": None,
                    "input_box": None,
                    "selectionbox": None,
                    "slider": None,
                    "button": None,
                }
            elif len(self.tab_content[tab_content_id]) == 0:
                self.tab_content[tab_content_id] = {
                    "text": None,
                    "checkbox": None,
                    "input_box": None,
                    "selectionbox": None,
                    "slider": None,
                    "button": None
                }
            elif type not in self.tab_content[tab_content_id]:
                self.tab_content[tab_content_id][type] = None

        new_content_lst.append(obj)

        self.tab_content[tab_content_id][type] = new_content_lst

    def create_selectionbox(self, pos, options, select_val_main, def_index=0, select_val_sub=None, size=(100, 36), text_color=(0, 0, 0), box_color=(255, 255, 255), border_color=(22, 22, 22), border_width=3, font=None, is_tab_content:bool=False, tab_content_id:int=0, callback_fn=None, has_arrows=False):
        selection_box = GuiSelectionBox(
            pos=pos,
            surface=self.surface,  # Pygame surface
            options=options,
            select_val_main=select_val_main,
            def_index=def_index,
            select_val_sub=select_val_sub,
            size=size,
            text_color=text_color,
            box_color=box_color,
            border_color=border_color,
            border_width=border_width,
            font=font,
            callback_fn=callback_fn,
            has_arrows=has_arrows
        )

        if is_tab_content and self.flags["tabs_enabled"]: #IF this is tab content
            self.new_tab_content(type="selectionbox", obj=selection_box, tab_content_id=tab_content_id)
        else:
            self.checkbox_list.append(selection_box)

    #create text
    def create_text(self, pos, text_content, font_name="./resources/fonts/consolas.ttf", text_color=(0,0,0,1), font_size=42, is_tab_content:bool=False, tab_content_id:int=0, text_attr:tuple[str,int]=None, align:str="center"):
        new_text = GuiText(pos=pos, text_content=text_content, text_color=text_color, font_size=font_size, font_name=font_name, text_attr=text_attr)
        new_text.create_text(align=align)
        
        if is_tab_content and self.flags["tabs_enabled"]: #IF this is tab content
            if text_attr:
                self.new_tab_content(type="text", obj=new_text, tab_content_id=tab_content_id)
            else:
                self.new_tab_content(type="text", obj=new_text, tab_content_id=tab_content_id)
        else:
            self.txt_list.append(new_text)

    #Helper function for rending text attributes
    def __render_text_attr(self, content, mouse_pos, index=0, horizontal_spacing=300, txt_vert_spacing=60):
        if not hasattr(content, "text_attr_pos"):
            pos_x = content.pos[0] + (horizontal_spacing)
            pos_y = content.pos[1] + (txt_vert_spacing*index)
            content.rect.topleft = (pos_x, pos_y)
            content.pos = content.rect.topleft
            content.text_attr_pos = True
                                        
        if content.rect.collidepoint(mouse_pos):
            globalvars.is_hovering = True

            #Execute function on click
            if pygame.mouse.get_pressed()[0] and not self.timers["btn_click"].active:
                self.timers["btn_click"].activate()
                content.change_state()

    #draw sprites
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        globalvars.is_btn_hover = any(btn.rect.collidepoint(mouse_pos) for btn in self.btn_list)
        globalvars.is_hovering = globalvars.is_btn_hover

        #Render texts
        if len(self.txt_list) >= 1:
            for txt in self.txt_list:
                self.surface.blit(txt.text_surf, txt.text_pos)

        #Render tab content
        if self.flags["tabs_enabled"]:
            txt_vert_spacing = 60 #verticle spacing in pixels

            if self.cur_tab in self.tab_content:
                    content = self.tab_content[self.cur_tab]
                    if content["text"]:
                        for index, text in enumerate(content["text"]):
                            pos_x = text.text_pos[0]
                            pos_y = text.text_pos[1] + (index*txt_vert_spacing)

                            self.surface.blit(text.text_surf, (pos_x, pos_y))

                            #Render additonal content
                            if text.text_attr:
                                #render checkboxes
                                if content["checkbox"] and text.text_attr[0] == "checkbox":
                                        checkbox = content["checkbox"][text.text_attr[1]]
                                        self.__render_text_attr(
                                            content=checkbox,
                                            mouse_pos=mouse_pos,
                                            index=index
                                        )
                                        checkbox.draw()
                                #render selectionbox
                                if content["selectionbox"] and text.text_attr[0] == "selectionbox":
                                    selectionbox = content["selectionbox"][text.text_attr[1]]
                                    self.__render_text_attr(
                                        content=selectionbox,
                                        mouse_pos=mouse_pos,
                                        index=index
                                    )
                                    selectionbox.update()
                                #Render inputBoxes
                                if content["input_box"] and text.text_attr[0] == "input_box":
                                    input_Box = content["input_box"][text.text_attr[1]]
                                    self.__render_text_attr(
                                        content=input_Box,
                                        mouse_pos=mouse_pos,
                                        index=index
                                    )

                                    if pygame.mouse.get_pressed()[0] and not self.timers["btn_click"].active and input_Box.is_active:
                                        self.timers["btn_click"].activate()
                                        input_Box.is_active = False

                                    input_Box.update()
                                #render sliders
                                if content["slider"] and text.text_attr[0] == "slider":
                                    slider = content["slider"][text.text_attr[1]]
                                    self.__render_text_attr(
                                        content=slider,
                                        mouse_pos=mouse_pos,
                                        index=index
                                    )
                                    slider.update_thumb_position()
                                    slider.update()
                                #render buttons
                                if content["button"] and text.text_attr[0] == "button":
                                    button = content["button"][text.text_attr[1]]
                                    self.__render_text_attr(
                                        content=button,
                                        mouse_pos=mouse_pos,
                                        index=index
                                    )
                                    button.update(recent_click=self.timers["btn_click"].active)

        #Render checkboxes
        if len(self.checkbox_list) >= 1:
            for checkbox in self.checkbox_list:
                pygame.draw.rect(self.surface, checkbox.border_color, checkbox.rect, border_radius=5)

        #Render buttons
        if len(self.btn_list) >= 1:
            for i, btn in enumerate(self.btn_list):
                if self.flags["tabs_enabled"] and self.cur_tab == i:
                    btn.apply_clicked_tab()
                btn.update(recent_click=self.timers["btn_click"].active)

    #Creates btns from specified input
    def create_btn(self, pos, height, width, text, color, hover_color, text_color, img=None, border_color=None, border_width=2, funct=None, funct_args_enabled=False, funct_args=None, is_tab_content:bool=False, tab_content_id:int=0,flags:list[bool]=[False]):
        btn = None
        if funct_args_enabled:
            btn = GuiBtn(pos=pos, surface=self.surface, height=height, width=width, text=text, color=color, hover_color=hover_color, text_color=text_color, img=img, border_color=border_color, border_width=border_width, funct=funct, flags=flags, funct_args=funct_args)
        else:
            btn = GuiBtn(pos=pos, surface=self.surface, height=height, width=width, text=text, color=color, hover_color=hover_color, text_color=text_color, img=img, border_color=border_color, border_width=border_width, flags=flags, funct=funct)

        
        if is_tab_content and self.flags["tabs_enabled"]: #IF this is tab content
            self.new_tab_content(type="button", obj=btn, tab_content_id=tab_content_id)
        else:
            self.btn_list.append(btn)

    #Checkbox
    def create_checkbox(self, pos, check_val_main, check_val_sub=None, size=64, checked_color=(0, 167, 16, 1), unchecked_color=(255,255,255,1), border_color=(22, 22, 22, 1), is_tab_content=False, tab_content_id=0, def_value=False, border_width:int=3):
        new_checkbox = GuiCheckbox(
            surface=self.surface,
            pos=pos,
            def_value=def_value,
            check_val_main=check_val_main,
            check_val_sub=check_val_sub,
            size=size,
            checked_color=checked_color,
            unchecked_color=unchecked_color,
            border_color=border_color,
            border_width=border_width
        )

        if is_tab_content and self.flags["tabs_enabled"]: #IF this is tab content
            self.new_tab_content(type="checkbox", obj=new_checkbox, tab_content_id=tab_content_id)
        else:
            self.checkbox_list.append(new_checkbox)

    #Sliders
    def create_slider(self, pos:tuple[int], bg_color:tuple[int]=(62, 62, 62, 1), filled_color:tuple[int]=(0, 82, 255, 1), thumb_radius:int=6, filled_percentage:int|float=0.0, bar_width:int=128, bar_height:int=16, is_tab_content=False,tab_content_id=0, border_color:tuple[int|float]=(22, 22, 22, 1), callback_fn:str=None, callback_fn_args:str=None, thumb_color:tuple[int|float]=(65, 126, 255, 1)):
        new_slider = GuiSlider(
            surface=self.surface,
            pos=pos,
            bg_color=bg_color,
            filled_color=filled_color,
            thumb_radius=thumb_radius,
            filled_percentage=filled_percentage,
            bar_width=bar_width,
            bar_height=bar_height,
            border_color=border_color,
            callback_fn=callback_fn,
            callback_fn_args=callback_fn_args,
            thumb_color=thumb_color
        )

        if is_tab_content and self.flags["tabs_enabled"]: #IF this is tab content
            self.new_tab_content(type="slider", obj=new_slider, tab_content_id=tab_content_id)
        else:
            self.slider_list.append(new_slider)

    #Text input field
    def create_input_box(self, pos:tuple[int], size:tuple[int]=(64,20), color:tuple[int|float]=(255,255,255,1), border_color:tuple[int|float]=(22, 22, 22, 1), clicked_border_color:tuple[int|float]=(0, 90, 152, 1), border_width:int=3, font_color:tuple[int|float]=(0,0,0,1), font_size:int=32, font_name:str=None, is_tab_content=False, tab_content_id=0, text_type:str="int", def_text:str="", text_length_limit:tuple[int]=(1,3), fn_callback=None, fn_args=None, auto_submit:bool=False):
        new_input_box = GuiInputBox(
            surface=self.surface,
            pos=pos,
            size=size,
            color=color,
            border_color=border_color,
            clicked_border_color=clicked_border_color,
            border_width=border_width,
            font_color=font_color,
            font_size=font_size,
            font_name=font_name,
            text_type=text_type,
            def_text=def_text,
            text_length_limit=text_length_limit,
            fn_callback=fn_callback,
            fn_args=fn_args,
            auto_submit=auto_submit
        )

        if is_tab_content and self.flags["tabs_enabled"]: #IF this is tab content
            self.new_tab_content(type="input_box", obj=new_input_box, tab_content_id=tab_content_id)
        else:
            self.input_box_list.append(new_input_box)

#FullMenu and Submenu inheirts from this
class GuiMenu(GUI):
    def __init__(self, surface, menu_header, menu_state_type, menu_height, menu_width, menu_background=None, menu_background_color=(255,255,255,255), tabs_enabled=False, header_color=(255,255,255)):
        super().__init__(surface, tabs_enabled)
        self.menu_header = menu_header
        self.menu_state_type = menu_state_type
        self.menu_height = menu_height
        self.menu_width = menu_width
        self.menu_background = menu_background
        self.menu_background_color = menu_background_color
        self.header_color = header_color
    
    def update(self):
        self.display_menu()
        super().update()
    
    #create menu div
    def create_menu_rects(self, pos:str):
        if pos == "top":
            self.menu_rect = pygame.Rect(
                (WIDTH - self.menu_width) // 2,
                10,
                self.menu_width,
                self.menu_height
            )
        if pos == "center":
            self.menu_rect = pygame.Rect(
                (WIDTH - self.menu_width) // 2,
                (HEIGHT - self.menu_height) // 2,
                self.menu_width,
                self.menu_height
            )
        elif pos == "bottom":
            self.menu_rect = pygame.Rect(
                (WIDTH - self.menu_width) // 2,
                (HEIGHT - self.menu_height),
                self.menu_width,
                self.menu_height
            )

    #Closes the whole menu
    def close_menu(self):
        reset_menu_state()
        change_game_speed()

    #Opens up the menu
    def open_menu(self):
        super().open_menu()
        reset_menu_state()

        globalvars.menu_state[self.menu_state_type] = True
        change_game_speed()
        
        #Show menu
        if any(globalvars.menu_state.values()):
            self.display_menu()
            update_pause_states()

#A menu that takes up the entire window
class FullMenu(GuiMenu):
    def __init__(self, surface, menu_header, menu_state_type, menu_height=550, menu_width=400, menu_background=None, menu_background_color=(255,255,255,255), bg_overlay=False, tabs_enabled=False, header_color=(255,255,255)):
        super().__init__(surface, menu_header, menu_state_type, menu_height, menu_width, menu_background, menu_background_color, tabs_enabled, header_color)
        self.bg_overlay = bg_overlay
    
    def display_menu_background(self):
        bg_surf = pygame.Surface((self.menu_width, self.menu_height)).convert_alpha()
        bg_surf.fill(self.menu_background_color) 
        self.surface.blit(bg_surf, (0, 0))

    def display_menu(self):
        if any(globalvars.menu_state.values()):
            # Render the text
            text_surf = self.font.render(self.menu_header, True, (255, 255, 255))
            text_rect = text_surf.get_rect()

            if self.menu_background:
                self.display_menu_background()
            elif self.bg_overlay:
                #Background
                bg_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, int(0.55 * 255))) 
                self.surface.blit(bg_surface, (0, 0))
                
            # Blit the text
            text_rect.centerx = self.menu_rect.centerx
            text_rect.top = self.menu_rect.top + 20
            
            self.surface.blit(text_surf, text_rect)

#A popup
class Popup(FullMenu):
    def __init__(self, surface, menu_header, menu_state_type, menu_height=200, menu_width=200, menu_background=None, menu_background_color=(255,255,255,255), bg_overlay=False, tabs_enabled=False, header_color=(255,255,255), rounded_corners=(False, 0)):
        super().__init__(surface, menu_header, menu_state_type, menu_height, menu_width, menu_background, menu_background_color, tabs_enabled, bg_overlay, header_color)
        self.rounded_corners = list(rounded_corners)
    
    def open_menu(self):
        self.flags["menu_open"] = True
        self.timers["btn_click"].activate()
        
        globalvars.menu_state[self.menu_state_type] = True
        change_game_speed()
        
        #Show menu
        if any(globalvars.menu_state.values()):
            self.display_menu()
            update_pause_states()

    def display_menu_background(self):
        bg_surf = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA).convert_alpha()
        
        if self.rounded_corners[0]:
            radius = self.rounded_corners[1]
            pygame.draw.rect(
                bg_surf,
                self.menu_background_color,
                (0, 0, self.menu_width, self.menu_height),
                border_radius=radius
            )
        else:
            bg_surf.fill(self.menu_background_color)
            
        self.surface.blit(
            bg_surf,
            ((WIDTH // 2) - (self.menu_width // 2), (HEIGHT // 2) - (self.menu_height // 2))
        )

    def display_menu(self):
        if any(globalvars.menu_state.values()):
            # Render the text
            text_surf = self.font.render(self.menu_header, True, self.header_color)
            text_rect = text_surf.get_rect()

            if self.menu_background:
                self.display_menu_background()
            elif self.bg_overlay:
                #Background
                bg_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, int(0.55 * 255))) 
                self.surface.blit(bg_surface, ((WIDTH//2)-(self.menu_width//2), (HEIGHT//2)-(self.menu_height//2)))
                
            # Blit the text
            text_rect.centerx = self.menu_rect.centerx
            text_rect.top = self.menu_rect.top + 20
            
            self.surface.blit(text_surf, text_rect)

#A menu that dosent take up the whole screen
class BottomMenu(GuiMenu):
    def __init__(self, surface, menu_header, menu_state_type, menu_height=180, menu_width=400, menu_background=None, menu_background_color=(255,255,255,200), tabs_enabled=False):
        super().__init__(surface, menu_header, menu_state_type, menu_height, menu_width, menu_background, menu_background_color, tabs_enabled)

    def display_menu_background(self):
        bg_surf = pygame.Surface((self.menu_width, self.menu_height)).convert_alpha()
        bg_surf.fill(self.menu_background_color) 
        self.surface.blit(bg_surf, self.menu_rect.topleft)

    def display_menu(self):
        if any(globalvars.menu_state.values()):
            # Render the text
            text_surf = self.font.render(self.menu_header, True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            
            if self.menu_background:
                self.display_menu_background()

            # Blit the text
            text_rect.centerx = text_rect.width
            text_rect.top = self.menu_rect.top + 20
            
            self.surface.blit(text_surf, text_rect)