"""
Moving Squares Pygame Application

A simple pygame program that displays 10 randomly positioned squares
that move around the screen and bounce off the edges.
"""

import pygame
import random
from typing import Tuple, List

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
NUM_SQUARES = 100
MIN_SQUARE_SIZE = 20
MAX_SQUARE_SIZE = 80
MIN_VELOCITY = 1
MAX_VELOCITY = 5


class Square:
    """Represents a single moving square on the screen."""

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize a square with random position and velocity.

        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)

        # Random starting position (ensuring square stays within bounds)
        self.x = random.randint(0, screen_width - self.size)
        self.y = random.randint(0, screen_height - self.size)

        # Random velocity (-MAX_VELOCITY to MAX_VELOCITY for both x and y)
        self.vx = random.choice([-1, 1]) * random.uniform(MIN_VELOCITY, MAX_VELOCITY)
        self.vy = random.choice([-1, 1]) * random.uniform(MIN_VELOCITY, MAX_VELOCITY)

        # Random color (RGB)
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def update(self) -> None:
        """Update square position and handle bouncing off walls."""
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Bounce off right and left walls
        if self.x <= 0:
            self.x = 0
            self.vx = -self.vx  # Reverse direction
        elif self.x >= self.screen_width - self.size:
            self.x = self.screen_width - self.size
            self.vx = -self.vx  # Reverse direction

        # Bounce off top and bottom walls
        if self.y <= 0:
            self.y = 0
            self.vy = -self.vy  # Reverse direction
        elif self.y >= self.screen_height - self.size:
            self.y = self.screen_height - self.size
            self.vy = -self.vy  # Reverse direction

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

        # Create squares
        self.squares: List[Square] = [
            Square(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(NUM_SQUARES)
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

    def update(self) -> None:
        """Update game logic (move squares, check collisions, etc.)."""
        for square in self.squares:
            square.update()

    def draw(self) -> None:
        """Draw all game objects on the screen."""
        # Clear screen with black background
        self.screen.fill((0, 0, 0))

        # Draw all squares
        for square in self.squares:
            square.draw(self.screen)

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
