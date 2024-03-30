import pygame
import pygame_gui
from pygame.locals import *
from pygame_gui.elements import UIButton, UIPanel 
from pygame_gui.windows import UIColourPickerDialog

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import tools
from engine.app import Application
from canvas import UICanvas

class PaintApp(Application):
    def __init__(self):
        super().__init__((1600, 900), 'Paint')
        self.ui_manager = pygame_gui.UIManager(self.screen.get_size())
        control_panel_height = self.screen.get_height() * 0.25
        canvas_height = self.screen.get_height() - control_panel_height
        self.control_panel = UIPanel(Rect(0, 0, self.screen.get_width(), control_panel_height), 
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

        self.canvas = UICanvas(Rect(0, control_panel_height, self.screen.get_width(), canvas_height), 
                               manager=self.ui_manager)
    
    def _on_event(self, event): 
        if event.type == pygame.QUIT:
            self.is_running = False
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
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
        self.ui_manager.update(self.delta_time)
        
    def _on_redraw(self):
        self.ui_manager.draw_ui(self.screen)

def main():
    paint_app = PaintApp()
    paint_app.run()

if __name__ == '__main__':
    main()
