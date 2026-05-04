"""
Moving Squares Pygame Application

A simple pygame program that displays any randomly positioned squares
that move around the screen and bounce off the edges.
"""

import pygame
import random
import math
from typing import List, Optional

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
MIN_SQUARE_SIZE = 4
MAX_SQUARE_SIZE = 80
MIN_VELOCITY = 1
MAX_VELOCITY = 5
FLEE_RADIUS = 180
FLEE_STRENGTH = 0.35
CHASE_RADIUS = 200
CHASE_STRENGTH = 0.25
RANDOM_JITTER = 0.12
MIN_DYNAMIC_SPEED = 0.7
MAX_DYNAMIC_SPEED = 6.0

# Square mixing
SQUARE_MIX = [
    (5, 25),
    (10, 10),
    (30, 4),
]


class Square:
    """Represents a single moving square on the screen."""

    def __init__(self, screen_width: int, screen_height: int, size: Optional[int] = None):
        """
        Initialize a square with random position and velocity.

        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
            size: Fixed pixel size for this square. If None, a random size is chosen.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size if size is not None else random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)

        # Random starting position (ensuring square stays within bounds)
        self.x = random.randint(0, max(0, screen_width - self.size))
        self.y = random.randint(0, max(0, screen_height - self.size))

        # Random velocity (-MAX_VELOCITY to MAX_VELOCITY for both x and y)
        self.vx = random.choice([-1, 1]) * random.uniform(MIN_VELOCITY, MAX_VELOCITY)
        self.vy = random.choice([-1, 1]) * random.uniform(MIN_VELOCITY, MAX_VELOCITY)

        # Random color (RGB)
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def target_speed(self) -> float:
        """Compute the preferred speed from the square's size."""
        size_ratio = (self.size - MIN_SQUARE_SIZE) / max(1, MAX_SQUARE_SIZE - MIN_SQUARE_SIZE)
        return MAX_DYNAMIC_SPEED - size_ratio * (MAX_DYNAMIC_SPEED - MIN_DYNAMIC_SPEED)

    def _check_collision(self, other: "Square") -> bool:
        # returns true if self and other collide
        return pygame.Rect(self.x, self.y, self.size, self.size).colliderect(
            pygame.Rect(other.x, other.y, other.size, other.size)
        )

    def respawn(self) -> None:
        """Reset position and velocity while keeping size and color unchanged."""
        self.x = random.randint(0, max(0, self.screen_width - self.size))
        self.y = random.randint(0, max(0, self.screen_height - self.size))
        self.vx = random.choice([-1, 1]) * random.uniform(MIN_VELOCITY, MAX_VELOCITY)
        self.vy = random.choice([-1, 1]) * random.uniform(MIN_VELOCITY, MAX_VELOCITY)

    def update(self, all_squares: List["Square"]) -> None:
        """Update position with random drift and flee from larger nearby squares, and chase smaller ones."""
        # Keep trajectories feeling organic with slight random drift.
        self.vx += random.uniform(-RANDOM_JITTER, RANDOM_JITTER)
        self.vy += random.uniform(-RANDOM_JITTER, RANDOM_JITTER)

        # Smaller squares steer away from nearby larger squares.
        flee_x = 0.0
        flee_y = 0.0

        # Larger squares chase nearby smaller squares
        chase_x = 0.0
        chase_y = 0.0

        self_center_x = self.x + self.size / 2
        self_center_y = self.y + self.size / 2

        for other in all_squares:
            if other is self:
                continue

            other_center_x = other.x + other.size / 2
            other_center_y = other.y + other.size / 2
            dx = self_center_x - other_center_x
            dy = self_center_y - other_center_y
            distance_sq = dx * dx + dy * dy

            # Fleeing: smaller squares run away from larger ones
            if other.size > self.size and 0.0 < distance_sq < FLEE_RADIUS * FLEE_RADIUS:
                distance = math.sqrt(distance_sq)
                influence = (FLEE_RADIUS - distance) / FLEE_RADIUS
                flee_x += (dx / distance) * influence
                flee_y += (dy / distance) * influence

            # Chasing: larger squares chase smaller ones
            if (
                other.size < self.size
                and 0.0 < distance_sq < CHASE_RADIUS * CHASE_RADIUS
            ):
                distance = math.sqrt(distance_sq)
                influence = (CHASE_RADIUS - distance) / CHASE_RADIUS
                # Chase towards the other square (opposite direction of flee)
                chase_x -= (dx / distance) * influence
                chase_y -= (dy / distance) * influence

        self.vx += flee_x * FLEE_STRENGTH
        self.vx += chase_x * CHASE_STRENGTH
        self.vy += flee_y * FLEE_STRENGTH
        self.vy += chase_y * CHASE_STRENGTH

        # Keep speed near the size-based target so larger squares move slower.
        speed = math.hypot(self.vx, self.vy)
        target_speed = self.target_speed()
        if speed > target_speed:
            scale = target_speed / speed
            self.vx *= scale
            self.vy *= scale
        elif 0.0 < speed < target_speed:
            scale = target_speed / speed
            self.vx *= scale
            self.vy *= scale

        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Wrap around right and left walls
        if self.x + self.size <= 0:
            self.x = self.screen_width  # Re-enter from the right wall
        elif self.x >= self.screen_width:
            self.x = -self.size  # Re-enter from the left wall

        # Wrap around top and bottom walls
        if self.y + self.size <= 0:
            self.y = self.screen_height  # Re-enter from the bottom wall
        elif self.y >= self.screen_height:
            self.y = -self.size  # Re-enter from the top wall

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the square on the given surface.

        Args:
            surface: The pygame surface to draw on
        """
        # Render on integer pixel coordinates to reduce visual jitter.
        pygame.draw.rect(
            surface,
            self.color,
            (int(self.x), int(self.y), self.size, self.size),
        )


class Game:
    """Main game class that handles initialization, updates, and rendering."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()

        # Create the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moving Squares - Pygame Demo")

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)

        # Create squares and mix squares
        self.squares: List[Square] = [
            Square(SCREEN_WIDTH, SCREEN_HEIGHT, size=size)
            for count, size in SQUARE_MIX
            for _ in range(count)
        ]

        # Game state
        self.running = True

    def handle_events(self) -> None:
        """Handle user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def check_collisions(self) -> None:
        """Respawn any smaller square that is fully overlapped by a larger one.

        A "kill" is registered when the bounding boxes of a larger and a smaller
        square intersect.  The smaller square immediately respawns at a new random
        position with the same size, preserving the population mix.
        """
        eaten: set[int] = set()
        for i, small in enumerate(self.squares):
            if i in eaten:
                continue
            for j, large in enumerate(self.squares):
                if i == j or j in eaten:
                    continue
                if large.size <= small.size:
                    continue
                # AABB overlap test
                if small._check_collision(large):
                    eaten.add(i)
                    break  # one kill per frame per square is enough

        for i in eaten:
            self.squares[i].respawn()

    def update(self) -> None:
        """Update game logic (move squares, check collisions, etc.)."""
        for square in self.squares:
            square.update(self.squares)
        self.check_collisions()

    def draw(self) -> None:
        """Draw all game objects on the screen."""
        # Clear screen with black background
        self.screen.fill((0, 0, 0))

        # Draw all squares
        for square in self.squares:
            square.draw(self.screen)

        # Draw FPS in the top-left corner.
        fps_text = self.font.render(
            f"FPS: {self.clock.get_fps():.1f}", True, (255, 0, 0)
        )
        self.screen.blit(fps_text, (0, 0))

        # Update the display
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            # Handle input
            self.handle_events()

            # Update game state
            self.update()

            # Render/draw
            self.draw()

            # Control frame rate (60 FPS)
            self.clock.tick(FPS)

        # Clean up
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()