import pygame
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
        self.kill()

        if self.size == 'large':
            medium_radius, medium_velocity = self.get_asteroid_properties('large')
            med_asteroid1 = Asteroid(self.position.x, self.position.y, medium_radius, medium_velocity, size='medium')
            med_asteroid2 = Asteroid(self.position.x, self.position.y, medium_radius, medium_velocity, size='medium')
            self.containers[0].add(med_asteroid1, med_asteroid2)
        elif self.size == 'medium':
            small_radius, small_velocity = self.get_asteroid_properties('medium')
            small_asteroid1 = Asteroid(self.position.x, self.position.y, small_radius, small_velocity, size='small')
            small_asteroid2 = Asteroid(self.position.x, self.position.y, small_radius, small_velocity, size='small')
            self.containers[0].add(small_asteroid1, small_asteroid2)
        elif self.size ==  'small':
            # No further splitting, asteroids just dissapear.
                pass

        # Call self.kill() to remove the original asteroid    
        self.kill()




     