from dataclasses import dataclass


@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int

    @property
    def left(self) -> int:
        return self.x

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def top(self) -> int:
        return self.y

    @property
    def bottom(self) -> int:
        return self.y + self.height

    def intersects(self, other: "Rectangle") -> bool:
        return (
            self.left < other.right
            and self.right > other.left
            and self.top < other.bottom
            and self.bottom > other.top
        )


class Player:
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, screen_width: int) -> None:
        self.rect = Rectangle(x, y, width, height)
        self.speed = speed
        self.screen_width = screen_width

    def move(self, direction_x: int) -> None:
        if direction_x < 0 and self.rect.left > 0:
            self.rect.x = max(0, self.rect.x + direction_x * self.speed)
        elif direction_x > 0 and self.rect.right < self.screen_width:
            self.rect.x = min(self.screen_width - self.rect.width, self.rect.x + direction_x * self.speed)


class Enemy:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect = Rectangle(x, y, width, height)

    def move(self, direction_x: int, distance_y: int) -> None:
        self.rect.x += direction_x
        self.rect.y += distance_y


class Bullet:
    def __init__(self, x: int, y: int, width: int, height: int, speed: int) -> None:
        self.rect = Rectangle(x, y, width, height)
        self.speed = speed

    def update(self) -> None:
        self.rect.y += self.speed
