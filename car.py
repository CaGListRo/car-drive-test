import pygame as pg
from typing import Final, TypeVar
import math


class Car:
    ALPHA_BACKGROUND: Final[tuple[int]] = (0, 0, 0, 0)
    def __init__(self, car_pos: tuple[int], car_heading: float | int, width: int, length: int, wheel_base: int, max_speed: int) -> None:
        """
        Initialize a Car object.
        Args:
        car_pos (tuple(int, int)) The center x and y-coordinate of the car.
        car_heading (float | int): The direction the car is heading in degree.
        width (int): The width of the car.
        length (int): The length of the car.
        wheel_base (int): the distance between the front and the back wheel.
        max_speed (int): The maximum speed of the car.
        """
        # self.car_pos: pg.Vector2 = pg.Vector2(car_pos)
        self.car_heading: float | int = car_heading  # the angle in which the car is rotated
        self.image: pg.Surface = pg.Surface((length, int(width * 1.5)), pg.SRCALPHA)
        self.width: int = width  # width of the car
        self.length: int = length  # length of the car
        self.wheel_base: int = wheel_base  # distance between the front and the back axle
        front_x_pos: float = car_pos[0] + math.cos(math.radians(self.car_heading)) * self.wheel_base / 2
        front_y_pos: float = car_pos[1] + math.sin(math.radians(self.car_heading)) * self.wheel_base / 2
        self.front_wheel_pos: pg.Vector2 = pg.Vector2(int(front_x_pos), int(front_y_pos))
        rear_x_pos: float = car_pos[0] - math.cos(math.radians(self.car_heading + 180)) * self.wheel_base / 2
        rear_y_pos: float = car_pos[1] - math.sin(math.radians(self.car_heading + 180)) * self.wheel_base / 2
        self.back_wheel_pos: pg.Vector2 = pg.Vector2(int(rear_x_pos), int(rear_y_pos))
        self.calculate_car_position()
        self.car_body: pg.Rect = pg.Rect(car_pos[0] - self.length // 2, car_pos[1] - self.width // 2, self.length, self.width)
        wheel_size: tuple[int] = (15, 7)
        self.front_wheel: pg.Surface = pg.Surface(wheel_size)
        self.back_wheel: pg.Surface = pg.Surface(wheel_size)
        self.max_speed: int = max_speed
        self.speed: int = 0
        self.acceleration: float = 0.1
        self.brake_strength: float = 0.1
        self.max_steer_angle: int = 45
        self.steer_angle: int = 0
        self.steer_speed: float = 0.1

    def calculate_car_position(self) -> None:
        """ Calculates the position of the car. """
        car_pos_x = (self.front_wheel_pos.x + self.back_wheel_pos.x) / 2
        car_pos_y = (self.front_wheel_pos.y + self.back_wheel_pos.y) / 2
        self.car_pos: pg.Vector2 = pg.Vector2(car_pos_x, car_pos_y)

    def accelerate(self) -> None:
        """ Accelerates the car. """
        self.speed += self.acceleration

    def brake(self) -> None:
        """ Brakes the car. """
        self.speed -= self.brake_strength

    def steer(self, direction: int, dt) -> None:
        """ Steers the car. """
        self.steer_angle += direction * self.steer_speed# * dt
        if abs(self.steer_angle) > self.max_steer_angle:
            self.steer_angle = self.max_steer_angle * direction

    def update(self, dt) -> None:
        """ Updates the car's position and rotation. """
        # Calculate the rotation angle based on the steering angle and car speed
        if self.steer_angle != 0:
            turning_radius = self.wheel_base / math.sin(math.radians(self.steer_angle))
            angular_velocity = self.speed / turning_radius
        else:
            angular_velocity = 0

        # Update the car heading (rotation of the car)
        self.car_heading += math.degrees(angular_velocity) * dt
        
        # Update front and back wheel positions based on the updated car heading
        self.front_wheel_pos.x += math.cos(math.radians(self.car_heading + self.steer_angle)) * self.speed * dt
        self.front_wheel_pos.y += math.sin(math.radians(self.car_heading + self.steer_angle)) * self.speed * dt
        self.back_wheel_pos.x += math.cos(math.radians(self.car_heading)) * self.speed * dt
        self.back_wheel_pos.y += math.sin(math.radians(self.car_heading)) * self.speed * dt
        self.calculate_car_position()
        self.car_heading += (self.steer_angle * dt * self.speed) / self.wheel_base
            
    def draw(self, surf: pg.Surface) -> None:
        """
        Draw the car on the given surface.
        Args:
        surf (pg.Surface): The surface to draw the car on.
        """
        # fill image with "nothing"
        self.image.fill(self.ALPHA_BACKGROUND)
        # draw car body
        pg.draw.rect(self.image, (255, 0, 0), (0, int(self.image.get_height() // 4), self.length, self.width))
        
        # Rotate the car
        rotated_image = pg.transform.rotate(self.image, -self.car_heading)
        
        # Blit the rotated car image
        surf.blit(rotated_image, (self.car_pos.x - rotated_image.get_width() / 2, self.car_pos.y - rotated_image.get_height() / 2))
        
        # rotate the wheels
        rotated_front_wheel = pg.transform.rotate(self.front_wheel, -(self.car_heading + self.steer_angle))
        rotated_back_wheel = pg.transform.rotate(self.back_wheel, -self.car_heading)
        
        # Blit the rotated wheels
        surf.blit(rotated_front_wheel, (self.front_wheel_pos.x - rotated_front_wheel.get_width() / 2, self.front_wheel_pos.y - rotated_front_wheel.get_height() / 2))
        surf.blit(rotated_back_wheel, (self.back_wheel_pos.x - rotated_back_wheel.get_width() / 2, self.back_wheel_pos.y - rotated_back_wheel.get_height() / 2))
