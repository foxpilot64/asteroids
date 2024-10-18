import pygame
import random
from circleshape import CircleShape
from game_groups import asteroids, updatable, drawable
from constants import *

class Asteroid(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, radius, velocity, size):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity)
        self.containers = (asteroids, updatable, drawable)
        self.size = size
        self.add(self.containers)

        # Define a rect for positioning and collision detection:
        self.rect = pygame.Rect(self.position.x - radius, self.position.y -radius * 2, radius * 2, radius * 2)
        self.radius = self.rect.width / 2

        

    def update(self, dt):
        # Calculate scaled velocity
        scaled_velocity = self.velocity * dt

        # Update position using the scaled veloctiy
        self.position += scaled_velocity

        # Update the rect's position to match the new position:
        self.rect.topleft = (self.position.x - self.radius, self.position.y - self.radius)

    
    def draw(self, screen):
        color = (255, 255, 255) 
        width = 2
    
        pygame.draw.circle(screen, color, (self.position.x, self.position.y), self.radius, width)



    def get_asteroid_properties(self, size):
        if size == 'large':
        # Return properties for medium asteroids
             return MEDIUM_RADIUS, MEDIUM_VELOCITY
        elif size == 'medium':
        # Return properties for small asteroids
             return SMALL_RADIUS, SMALL_VELOCITY
        return None, None

    def split(self):
        self.kill() # Kill the original asteroid

        if self.radius <= ASTEROID_MIN_RADIUS:
            return # Don't split if it's already at minimum size.
        
        # Generate random angle between 20 and 50 degrees.
        random_angle = random.uniform(20, 50)

        # Create two new velocity vectors
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)

        # Scale up the new velocities:
        new_velocity1 *= 1.2
        new_velocity2 *= 1.2

        # Calculate new radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_size = new_radius * 2 # size is diameter

       
        # Create two new asteroids
        Asteroid(self.rect.centerx, self.rect.centery, new_radius, new_velocity1, new_size) 
        Asteroid(self.rect.centerx, self.rect.centery, new_radius, new_velocity2, new_size)

       

      
      


        

      
        




     