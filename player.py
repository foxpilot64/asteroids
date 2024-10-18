import pygame
from constants import PLAYER_RADIUS
from constants import PLAYER_TURN_SPEED
from constants import PLAYER_SPEED
from constants import PLAYER_SHOOT_SPEED
from constants import PLAYER_SHOOT_COOLDOWN
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.angle = 180
        self.timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 200  # pixels per second squared
        self.max_speed = 300  # maximum speed in pixels per second

        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    
  
    def shoot(self, dt):
        # Ensure your player has a direction attribute representing its current facing angle
        direction = self.angle
        

        if self.timer <= 0:
            x, y = self.position
            # Create a Shot instance at the player's current position
            new_shot = Shot(x, y, direction)

            # Calculate and set the velocity for the shot
            velocity = pygame.Vector2(0, 1) # Initial vector pointing up
            velocity.rotate_ip(direction)   # Rotate based on player's direction
            velocity *= PLAYER_SHOOT_SPEED  # Scale by shooting speed
            new_shot.velocity = velocity    # Assign the velocity to the shot

            # Set the time to start the cooldown
            self.timer = PLAYER_SHOOT_COOLDOWN
        

   
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.angle)
        right = forward.rotate(90)
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right * self.radius / 1.5
        c = self.position - forward * self.radius + right * self.radius / 1.5
        return [a, b, c]

    # Overriding the draw method from the CircleShape base class:
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

  

    def update(self, dt):
        # Check if mvt and rotation keys are pressed
        keys = pygame.key.get_pressed()
        
       

        # Handle rotation
        if keys[pygame.K_a]:
            self.angle += PLAYER_TURN_SPEED * dt 
        elif keys[pygame.K_d]:
            self.angle -= PLAYER_TURN_SPEED * dt 
            self.angle %= 360

       
         # Handle acceleration
        acceleration = pygame.Vector2(0, 0) 
        if keys[pygame.K_w]:
            acceleration = pygame.Vector2(0, self.acceleration).rotate(self.angle)
        elif keys[pygame.K_s]:
            acceleration = pygame.Vector2(0, -self.acceleration).rotate(self.angle)
            #Movement Debug:
            print(f"Angle: {self.angle}, Acceleration: {acceleration}, Velocity: {self.velocity}, Position: {self.position}")
     
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        friction = 0.96 # Adjust for feeling u want
        self.velocity *= friction 
        
        # Limit speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        
        # Update position:
        self.position += self.velocity * dt
        self.rect.center = self.position
    

        # Handle shots
        if keys[pygame.K_SPACE]:
            self.shoot(dt)
        
        # Decrease the timer if it's above zero:
        if self.timer > 0:
            self.timer -= dt

        # Screen wrapping
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.position.x %= screen_width
        self.position.y %= screen_height
        self.rect.center = self.position
    
    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360
        #self.image = pygame.transform.rotate(self.original_image, self.angle)
        #self.rect = self.image.get_rect(center=self.rect.center)
    
     # def rotate(self, dt):
        #self.rotation -= PLAYER_TURN_SPEED * dt
        

    def move(self, dt):
        # Starts with a vector facing up from (0,1) which represents the default fwd direction.
        # Then rotate the vector by the player's rotation attribute.
        forward = pygame.Vector2(0, -1).rotate(-self.angle)
        #Scale the vector to account for speed and time.
        self.position += forward * PLAYER_SPEED * dt