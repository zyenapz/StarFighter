import pygame, sys
from data.scripts.sprites import Player
from data.scripts.settings import *
from data.scripts.MateriaEngine import (
    load_img, 
    load_sound, 
    sort,
    read_savedata,
    write_savedata,
    Scene,
    SceneManager,
    draw_background, 
    draw_text,
    shake,
    slice_list
)

# TITLE SCENE ================================

class TitleMenu:
    def __init__(self, init_selected):
        # Surface
        # Warning - options may go beyond the surface and will be not rendered
        self.surface = pygame.Surface((WIN_RES["w"], 350))
        self.surf_rect = self.surface.get_rect()
        
        self.spacing = FONT_SIZE / 2

        # Menu
        self.options = ("PLAY", "SCORES", "OPTIONS", "CREDITS", "EXIT")
        self.act_opt = [0 for i in range(len(self.options))] # Active options
        self.act_opt[init_selected] = 1
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive menu

        # Selector
        self.selector = pygame.Surface((WIN_RES["w"], FONT_SIZE + 4))
        self.selector.fill("white")
        self.sel_y = FONT_SIZE + self.spacing
        self.sel_i = init_selected # index

    def update(self):
        self.sel_y = FONT_SIZE*(self.sel_i+1) + self.spacing*(self.sel_i+1)

    def draw(self, window):
        self.surface.fill("black")
        self.surface.set_colorkey("black")
        self.surface.blit(self.selector, (0,self.sel_y-3))
        for i in range(len(self.options)):
            draw_text(self.surface, self.options[i], FONT_SIZE, GAME_FONT, self.surf_rect.centerx, FONT_SIZE*(i+1) + self.spacing*(i+1), self.colors[self.act_opt[i]], "centered")
        window.blit(self.surface, (0,window.get_height()/2 - 32))

    def select_up(self):
        if  self.sel_i > 0:
            self.act_opt[self.sel_i] = 0
            self.sel_i -= 1
            self.act_opt[self.sel_i] = 1
        else:
            self.act_opt[self.sel_i] = 0
            self.sel_i = len(self.options) - 1
            self.act_opt[self.sel_i] = 1

    def select_down(self):
        if self.sel_i < len(self.options) - 1:
            self.act_opt[self.sel_i] = 0
            self.sel_i += 1
            self.act_opt[self.sel_i] = 1
        else:
            self.act_opt[self.sel_i] = 0
            self.sel_i = 0
            self.act_opt[self.sel_i] = 1

    def get_selected(self):
        return self.options[self.sel_i]

class TitleScene(Scene):
    def __init__(self, init_selected=0):
        # Background
        self.bg_img = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_y = 0
        self.par_img = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.bg_img.get_rect()
        self.par_y = 0

        # Images
        self.logo_img = load_img("logo.png", IMG_DIR, 4, convert_alpha=True)
        self.logo_rect = self.logo_img.get_rect()
        self.logo_hw = self.logo_rect.width / 2

        # Menu object
        self.title_menu = TitleMenu(init_selected)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.title_menu.select_up()
                elif event.key == pygame.K_DOWN:
                    self.title_menu.select_down()
                elif event.key == pygame.K_z:
                    if self.title_menu.get_selected() == "PLAY":
                        self.manager.go_to(GameScene())
                    elif self.title_menu.get_selected() == "SCORES":
                        self.manager.go_to(ScoresScene())
                    elif self.title_menu.get_selected() == "OPTIONS":
                        self.manager.go_to(OptionsScene())
                    elif self.title_menu.get_selected() == "CREDITS":
                        self.manager.go_to(CreditsScene())
                    elif self.title_menu.get_selected() == "EXIT":
                        sys.exit()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt
        self.title_menu.update()

    def draw(self, window):
        draw_background(window, self.bg_img, self.bg_rect, self.bg_y)
        draw_background(window, self.par_img, self.par_rect, self.par_y)
        window.blit(self.logo_img, (WIN_RES["w"]/2 - self.logo_hw, -32))

        # Draw menu
        self.title_menu.draw(window)
        draw_text(window, "Copydown", FONT_SIZE, GAME_FONT, window.get_rect().centerx, window.get_rect().bottom-(FONT_SIZE/2)*2, "WHITE", "centered")

# SCORES SCENE ===============================

class ScoresControlPanel():
    def __init__(self):
        # Panels
        self.sub_panels = ("DIRECTION", "BACK")
        self.active_panel = self.sub_panels[0]
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive options

        # Direction Sub-panel
        self.direction_panel = pygame.Surface((WIN_RES["w"], FONT_SIZE*2))
        self.dp_rect = self.direction_panel.get_rect()

        # Direction Sub-panel Options
        self.dp_options = ("PREV", "NEXT")
        self.dp_act_opt = [0 for i in range(len(self.dp_options))] # Active options
        self.dp_act_opt[0] = 1

        # Back Sub-panel
        self.back_panel = pygame.Surface((WIN_RES["w"], FONT_SIZE*2))
        self.bp_rect = self.back_panel.get_rect()

        # Back Sub-panel Option
        self.bp_options = ("BACK")
        self.bp_active = 0

        # Selector
        self.selector = pygame.Surface((self.dp_rect.width*0.5, self.dp_rect.height))
        self.selector.fill("WHITE")
        self.sel_i = 0 # index

    def update(self):
        pass

    def draw(self, window):
        # Set colorkeys
        self.direction_panel.fill("BLACK")
        self.direction_panel.set_colorkey("BLACK")
        self.back_panel.fill("BLACK")
        self.back_panel.set_colorkey("BLACK")

        # Selector
        if self.active_panel == self.sub_panels[0]:
            self.direction_panel.blit(self.selector, (self.dp_rect.centerx*self.sel_i,0))
        elif self.active_panel == self.sub_panels[1]:
            self.back_panel.blit(self.selector, (self.back_panel.get_rect().width/4,0))

        # Direction panel
        draw_text(self.direction_panel, self.dp_options[0], FONT_SIZE, GAME_FONT, self.dp_rect.centerx*0.5, self.dp_rect.centery*0.5, self.colors[self.dp_act_opt[0]], "centered")
        draw_text(self.direction_panel, self.dp_options[1], FONT_SIZE, GAME_FONT, self.dp_rect.centerx*1.5, self.dp_rect.centery*0.5, self.colors[self.dp_act_opt[1]], "centered")
        window.blit(self.direction_panel, (0,window.get_rect().height*0.7))

        # Back panel
        draw_text(self.back_panel, "BACK", FONT_SIZE, GAME_FONT, self.dp_rect.centerx, self.dp_rect.centery*0.5, self.colors[self.bp_active], "centered")
        window.blit(self.back_panel, (0,window.get_rect().height*0.8))

    def move_left(self):
        if self.active_panel == self.sub_panels[0]:
            if self.sel_i > 0:
                self.dp_act_opt[self.sel_i] = 0
                self.sel_i -= 1
                self.dp_act_opt[self.sel_i] = 1

        elif self.active_panel == self.sub_panels[1]:
            self.active_panel = self.sub_panels[0]
            self.sel_i = 0
            self.move_up()

    def move_right(self):
        if self.active_panel == self.sub_panels[0]:
            if self.sel_i < len(self.dp_options)-1:
                self.dp_act_opt[self.sel_i] = 0
                self.sel_i += 1
                self.dp_act_opt[self.sel_i] = 1

        elif self.active_panel == self.sub_panels[1]:
            self.active_panel = self.sub_panels[0]
            self.sel_i = len(self.dp_options)-1
            self.move_up()

    def move_up(self):
        self.active_panel = self.sub_panels[0]
        self.bp_active = 0

        self.dp_act_opt = [0 for i in range(len(self.dp_options))] # Active options
        self.dp_act_opt[self.sel_i] = 1

    def move_down(self):
        self.active_panel = self.sub_panels[1]
        self.bp_active = 1

        self.dp_act_opt = [0 for i in range(len(self.dp_options))] # Active options
        self.dp_act_opt[0] = 0

    def get_active_panel(self):
        return self.active_panel

    def get_dp_selected_option(self):
        if self.active_panel == self.sub_panels[0]:
            return self.dp_options[self.sel_i]

class ScoresTable():
    def __init__(self):
        self.spacing = FONT_SIZE / 2

        # Table
        self.table_surf = pygame.Surface((WIN_RES["w"], WIN_RES["h"] / 2))
        self.table_rect = self.table_surf.get_rect()
        #self.table_surf.fill('red')
        
        # Scores - TODO: Just an example. No sorting yet.
        self.scores = [
            ["MAN", 1000],
            ["WMN", 2100],
            ["LOL", 102],
            ["XMS", 106],
            ["EBL", 107],
            ["LOL", 102],
            ["XMS", 106],
            ["EBL", 107],
            ["LOL", 102],
            ["XMS", 106],
            ["EBL", 107],
            ["LOL", 102],
            ["XMS", 106],
            ["LOL", 102],
            ["XMS", 106],
            ["EBL", 107],
            ["LOL", 102],
            ["XMS", 106]
        ]
        self.splice_n = 5
        self.scores = slice_list(self.scores, self.splice_n)
        self.cur_tbl = 0

    def update(self):
        pass

    def draw(self, window):
        self.table_surf.fill("black")
        self.table_surf.set_colorkey("black")

        for i in range(len(self.scores[self.cur_tbl])):
            draw_text(self.table_surf, f"{(i+1)+(self.cur_tbl*self.splice_n)}.", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.5 + len(str(i)), FONT_SIZE*(i+1) + self.spacing*(i+1), "YELLOW")
            draw_text(self.table_surf, f"{self.scores[self.cur_tbl][i][0]}", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.8, FONT_SIZE*(i+1) + self.spacing*(i+1), "WHITE")
            draw_text(self.table_surf, f"{self.scores[self.cur_tbl][i][1]}", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 1.3, FONT_SIZE*(i+1) + self.spacing*(i+1), "WHITE")

        # TODO - this is just a placeholder
        draw_text(window, f"PAGE {self.cur_tbl+1} OF {len(self.scores)}", FONT_SIZE, GAME_FONT, self.table_rect.centerx, self.table_rect.bottom * 1.25, "WHITE", "centered")

        window.blit(self.table_surf,(0,WIN_RES["h"]/2 - 128))

    def next_table(self):
        if self.cur_tbl < len(self.scores) - 1:
            self.cur_tbl += 1
        
    def prev_table(self):
        if self.cur_tbl > 0:
            self.cur_tbl -= 1

class ScoresScene(Scene):
    def __init__(self):
        # Background
        self.bg_img = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_y = 0
        self.par_img = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.bg_img.get_rect()
        self.par_y = 0

        # Scores table
        self.scores_table = ScoresTable()

        # Control panel
        self.control_panel = ScoresControlPanel()
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.control_panel.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.control_panel.move_right()
                elif event.key == pygame.K_UP:
                    self.control_panel.move_up()
                elif event.key == pygame.K_DOWN:
                    self.control_panel.move_down()

                elif event.key == pygame.K_z:
                    if self.control_panel.get_active_panel() == "DIRECTION":
                        if self.control_panel.get_dp_selected_option() == "PREV":
                            self.scores_table.prev_table()
                        elif self.control_panel.get_dp_selected_option() == "NEXT":
                            self.scores_table.next_table()
                    elif self.control_panel.get_active_panel() == "BACK":
                        self.manager.go_to(TitleScene(1))
                elif event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(1))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.bg_img, self.bg_rect, self.bg_y)
        draw_background(window, self.par_img, self.par_rect, self.par_y)

        draw_text(window, "HALL OF FAME", FONT_SIZE*2, GAME_FONT, window.get_rect().centerx, 64, "WHITE", "centered")
        self.scores_table.draw(window)
        self.control_panel.draw(window)

# OPTIONS SCENE ==============================

class OptionsScene(Scene):
    def __init__(self):
        # Background
        self.bg_img = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_y = 0
        self.par_img = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.bg_img.get_rect()
        self.par_y = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(2))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.bg_img, self.bg_rect, self.bg_y)
        draw_background(window, self.par_img, self.par_rect, self.par_y)

        draw_text(window, "OPTIONS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        draw_text(window, "DEV: Not yet done.", FONT_SIZE, GAME_FONT, WIN_RES["w"]/2, WIN_RES["h"]/2, "WHITE", "centered")

# CREDITS SCENE ==============================

class CreditsScene(Scene):
    def __init__(self):
        # Background
        self.bg_img = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_y = 0
        self.par_img = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.bg_img.get_rect()
        self.par_y = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(3))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.bg_img, self.bg_rect, self.bg_y)
        draw_background(window, self.par_img, self.par_rect, self.par_y)

        draw_text(window, "CREDITS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        draw_text(window, "DEV: Not yet done.", FONT_SIZE, GAME_FONT, WIN_RES["w"]/2, WIN_RES["h"]/2, "WHITE", "centered")

# GAME SCENE =================================

class GameScene(Scene):
    def __init__(self):
        # Background
        self.bg_img = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_y = 0
        self.par_img = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.bg_img.get_rect()
        self.par_y = 0

        # Sprites
        self.player = Player()

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.player)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(0))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt
        self.sprites.update(dt, self.sprites)

    def draw(self, window):
        draw_background(window, self.bg_img, self.bg_rect, self.bg_y)
        draw_background(window, self.par_img, self.par_rect, self.par_y)
        self.sprites.draw(window)