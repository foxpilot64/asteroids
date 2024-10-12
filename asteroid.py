import pygame
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity):
        super().__init__(x, y,  radius)
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
   
    def update(self, dt):
        self.position += self.velocity * dt 

    
    def draw(self, screen):
        color = (255, 255, 255) 
        width = 2
    
        pygame.draw.circle(screen, color, (self.position.x, self.position.y), self.radius, width)

