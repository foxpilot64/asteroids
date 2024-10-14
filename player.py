import pygame
from constants import PLAYER_RADIUS
from constants import PLAYER_TURN_SPEED
from constants import PLAYER_SPEED
from circleshape import CircleShape

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

   
    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = forward.rotate(90)
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right * self.radius / 1.5
        c = self.position - forward * self.radius + right * self.radius / 1.5
        return [a, b, c]

    # Overriding the draw method from the CircleShape base class:
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation -= PLAYER_TURN_SPEED * dt

    def update(self, dt):
        # Check if mvt and rotation keys are pressed
        keys = pygame.key.get_pressed()
        
        # Handle fwd and back mvt
        if keys[pygame.K_w]:
            self.move(dt) 
        
        if keys[pygame.K_s]:
            self.move(-dt) 

        # Handle rotation
        if keys[pygame.K_a]:
            self.rotate(PLAYER_TURN_SPEED * dt) # Rotate Left
        elif keys[pygame.K_d]:
            self.rotate(PLAYER_TURN_SPEED * dt) # Rotate Right

    def move(self, dt):
        # Starts with a vector facing up from (0,1) which represents the default fwd direction.
        # Then rotate the vector by the player's rotation attribute.
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        #Scale the vector to account for speed and time.
        self.position += forward * PLAYER_SPEED * dt