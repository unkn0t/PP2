import pygame_gui
from pygame.locals import *
from pygame_gui.elements import UIButton, UIPanel 
from pygame_gui.windows import UIColourPickerDialog

import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import engine
import tools
from canvas import UICanvas

class MainScene(engine.Scene):
    def _on_load(self):
        self.ui_manager = pygame_gui.UIManager(self.app.screen.get_size())
        control_panel_height = self.app.screen.get_height() * 0.25
        canvas_height = self.app.screen.get_height() - control_panel_height
        self.control_panel = UIPanel(Rect(0, 0, self.app.screen.get_width(), control_panel_height), 
                                     manager=self.ui_manager)
        
        button_size = (150, 50)
        self.tool_circle_button = UIButton(Rect((20, 20), button_size), 'circle', 
                                           manager=self.ui_manager, container=self.control_panel)
        self.tool_square_button = UIButton(Rect((20, 20+button_size[1]), button_size), 'square', 
                                           manager=self.ui_manager, container=self.control_panel)
        self.tool_rect_button = UIButton(Rect((20, 20+2*button_size[1]), button_size), 'rect', 
                                           manager=self.ui_manager, container=self.control_panel)
        self.tool_rhombus_button = UIButton(Rect((20 + button_size[0], 20), button_size), 'rhombus', 
                                           manager=self.ui_manager, container=self.control_panel)
        self.tool_right_tr_button = UIButton(Rect((20 + button_size[0], 20+button_size[1]), button_size), 
                                             'right tr', manager=self.ui_manager, container=self.control_panel)
        self.tool_equil_tr_button = UIButton(Rect((20 + button_size[0], 20+2*button_size[1]), button_size), 
                                             'equil tr', manager=self.ui_manager, container=self.control_panel)
        
        self.colour_pick_button = UIButton(Rect(-200, 20, 150, 150), 'COLOR', 
                                           anchors={'right': 'right'},
                                           manager=self.ui_manager, 
                                           container=self.control_panel) 

        self.canvas = UICanvas(Rect(0, control_panel_height, self.app.screen.get_width(), canvas_height), 
                               manager=self.ui_manager)
    
    def _on_event(self, event): 
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.tool_circle_button:
                self.canvas.tool = tools.Circle()
            elif event.ui_element == self.tool_square_button:
                self.canvas.tool = tools.Square()
            elif event.ui_element == self.tool_rect_button:
                self.canvas.tool = tools.Rectangle()
            elif event.ui_element == self.tool_rhombus_button:
                self.canvas.tool = tools.Rhombus()
            elif event.ui_element == self.tool_right_tr_button:
                self.canvas.tool = tools.RightTriangle()
            elif event.ui_element == self.tool_equil_tr_button:
                self.canvas.tool = tools.EquilateralTriangle()
            elif event.ui_element == self.colour_pick_button:
                self.colour_pick_button.disable()
                UIColourPickerDialog(Rect(0, 0, 400, 400), 
                                           manager=self.ui_manager) 
        elif event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            self.colour_pick_button.enable()
            self.canvas.tool.color = event.colour
        
        self.ui_manager.process_events(event)
    
    def _on_update(self):
        self.ui_manager.update(self.app.delta_time)
        self.ui_manager.draw_ui(self.app.screen)

def main():
    paint_app = engine.Application((1600, 900), 'Paint')
    paint_app.scene_manager.add_scene(MainScene())
    paint_app.scene_manager.switch_to(0)
    paint_app.run()

if __name__ == '__main__':
    main()
