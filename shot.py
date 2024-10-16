import pygame
from constants import SHOT_RADIUS
from constants import PLAYER_SHOOT_SPEED
from circleshape import CircleShape

class Shot(CircleShape, pygame.sprite.Sprite):
    containers = None 
    def __init__(self, x, y, direction):
        super().__init__(x, y, SHOT_RADIUS)
        
        self.position = pygame.Vector2(x, y)
        self.radius = SHOT_RADIUS
        
        self.velocity = pygame.Vector2(0, -1)
        self.velocity = self.velocity.rotate(-direction) * PLAYER_SHOOT_SPEED
        
        self.add(self.containers)

        # Define a rect for positioning and collision detection
        self.rect = pygame.Rect(self.position.x, self.position.y, SHOT_RADIUS*2, SHOT_RADIUS*2)
        

        # Initialize velocity
        #self.velocity = pygame.Vector2(0, 0)
    
    def update(self, dt):
        self.position += self.velocity * dt 
        self.rect.topleft = (self.position.x, self.position.y)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), SHOT_RADIUS)

   
        