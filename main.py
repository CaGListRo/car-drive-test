from car import Car

import pygame as pg
from time import time
from typing import Final, TypeVar



class CarDriveTest:
    WINDOW_WIDTH: Final[int] = 1600
    WINDOW_HEIGHT: Final[int] = 900
    ASPHALT_GREY: Final[tuple[int]] = (82, 82, 87)

    def __init__(self) -> None:
        """ The initializer of the main game class. """
        pg.init()
        self.screen = pg.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.fps: int = 0
        self.run: bool = True

        # create a car
        self.car = Car(x=800, y=450, car_heading=45, width=50, length=100, max_speed=300)

    
    def handle_events(self) -> None:
        """ Handle all events. """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

    def draw_screen(self) -> None:
        """ Draw the window. """
        # setting the caption with fps-display
        pg.display.set_caption(f"    Car Drive Test     FPS:{self.fps}")
        self.screen.fill(self.ASPHALT_GREY)

        self.car.draw(self.screen)
        
        
        pg.display.flip()

    def main(self) -> None:
        """ The main method of the game. """
        old_time = time()
        frame_counter: int = 0
        frame_timer: float = 0
        while self.run:
            
            # calculating delta time
            dt = time() - old_time
            old_time = time()

            # counting frames per second
            frame_counter += 1
            frame_timer += dt
            if frame_timer >= 1:
                self.fps = frame_counter
                frame_counter = 0
                frame_timer = 0

            self.handle_events()


            self.draw_screen()          


pg.quit()


if __name__ == "__main__":
    game = CarDriveTest()
    game.main()