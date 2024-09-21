import pygame as pg
from typing import Final, TypeVar


class Car:
    ALPHA_BACKGROUND: Final[tuple[int]] = (0, 0, 0, 0)
    def __init__(self, x: int, y: int, car_heading: float | int, width: int, length: int, max_speed: int) -> None:
        """
        Initialize a Car object.
        Args:
        x (int): The center x-coordinate of the car.
        y (int): The center y-coordinate of the car.
        car_heading (float | int): The direction the car is heading in degree.
        width (int): The width of the car.
        length (int): The length of the car.
        max_speed (int): The maximum speed of the car.
        """
        self.x: int = x  # center x of the body/car
        self.y: int = y  # center y of the body/car
        self.car_heading: float | int = car_heading  # the angle in which the car is rotated
        self.image: pg.Surface = pg.Surface((length, int(width * 1.5)), pg.SRCALPHA)
        self.width: int = width  # width of the car
        self.length: int = length  # length of the car
        self.car_body: pg.Rect = pg.Rect(self.x - length // 2, self.y - width // 2, length, width)
        self.max_speed: int = max_speed
        self.speed: int = 0
        self.acceleration: float = 0.1
        self.brake: float = 0.1
        self.max_steer_angle: int = 45
        self.steer_angle: int = 0
        self.steer_speed: float = 0.1
    
    def draw(self, surf: pg.Surface) -> None:
        """
        Draw the car on the given surface.
        Args:
        surf (pg.Surface): The surface to draw the car on.
        """
        self.image.fill(self.ALPHA_BACKGROUND)
        pg.draw.rect(self.image, (255, 0, 0), (0, int(self.image.get_height() // 4), self.length, self.width))
        self.image = pg.transform.rotate(self.image, self.car_heading)
        surf.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))