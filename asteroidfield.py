import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):

    # This defines the edges of the screen and functions to determine spawn positions
    edges = [
        [
            pygame.Vector2(1, 0), # Direction vector to the right
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT), # Spawn position along the left edge
        ],
        [
            pygame.Vector2(-1, 0), # Direction vector to the left
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT), # Spawn position along the right edge
        ],
        [
            pygame.Vector2(0, 1), # Direction vector downward
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS), #Spawn position along the top edge
                
        ],
        [
            pygame.Vector2(0, -1), # Direction vector upward
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS #Spawn position along the bottom edge
            ),
               
        ],
    ]
    # Initializes the sprite and sets up a spawn timer to keep track of asteroid generation.
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0 # Time elapsed since the last asteroid was spawned

    
    def spawn(self, radius, position, velocity):
        # Create and configure a new asteroid
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity # Assign velocity for mvt

    # Called each frame to update the asteroid field, it increments the spawn_timer based on dt to track passage of time.
    #Once the spawn_timer exceeds ASTEROID_SPAWN_RATE, it resets and spawns a new asteroid.
    def update(self, dt):
        self.spawn_timer += dt # Increment the timer by frame time
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0 # Reset the timer after spawning

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed =random.randint(40, 100) # Random speed for the asteroid
            velocity = edge[0] * speed # Determine velocity vector
            velocity = velocity.rotate(random.randint(-30, 30)) # Rotate the velocity slightly
            position = edge[1](random.uniform(0,1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)  