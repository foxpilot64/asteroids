import os
import psutil
import time
import threading
import pygame
import sys
import math
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from game_groups import asteroids, updatable, drawable

running = True
# Define the resource monitoring function
def resource_monitor():
    global running
    while running:    
        cpu_usage = psutil.cpu_percent(interval=0)  # Grabbing CPU percent
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.used / (1024  * 1024) # Converts bytes to MB

        print(f"CPU usage: {cpu_usage}%")
        print(f"Memory usage: {memory_usage} MB")

        time.sleep(5)

# Created a Game Over function
def game_over(screen):
     # Font setup
    try:
         font = pygame.font.Font("Fonts/Orbitron-Bold.ttf", 74)
    except: 
        print("Font file not found. Falling back to default font.")
        font = pygame.font.Font(None, 74)


    start_time = pygame.time.get_ticks()
    duration = 10000 # Color shift duration in milliseconds

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate the color based on time:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time
        if elapsed > duration:
            running = False
     
        # Use sine waves to create smooth color transitions
        red = int(math.sin(elapsed * 0.002) * 127 + 128)
        green = int(math.sin(elapsed * 0.002 + 2) * 127 + 128)
        blue = int(math.sin(elapsed * 0.002 + 4) * 127 + 128)
     
        # Render and display the text
        text = font.render("Game Over", True, (red, green, blue))
        text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
        
        screen.fill((0, 0, 0)) # Clear the screen
        screen.blit(text, text_rect)
        pygame.display.flip()
        
     
    pygame.quit()
    sys.exit()



def main():
        global running
        pygame.init()
    
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Starting asteroids!")
        print(f"Screen width: {SCREEN_WIDTH}")
        print(f"Screen height: {SCREEN_HEIGHT}")

        clock = pygame.time.Clock()
        dt = 0

        # Create the groups
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        updatable = pygame.sprite.Group()
        shots = pygame.sprite.Group()


        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable,) #When you define a tuple with a single element, include comma after that element.
        Shot.containers = (shots, updatable, drawable)

        # Instantiate the Player object
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
        asteroid_field = AsteroidField()
        asteroid = Asteroid(x=100, y=200, radius=50, velocity=pygame.Vector2(1, -1), size='large')
      

        #Start the resource monitor in a thread:
        monitor_thread = threading.Thread(target=resource_monitor, daemon=True)
        monitor_thread.start()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot(dt)
            

            # Call tick() to manage FPS and calculate dt
            dt = clock.tick(60) / 1000.0

            # Update game state
            updatable.update(dt)


            # Check for collisions
            for asteroid in asteroids:
                 if player.collision_detect(asteroid):
                      game_over(screen)
            
            # Remove collided shots and asteroids 
            collisions = pygame.sprite.groupcollide(shots, asteroids, True, False, pygame.sprite.collide_circle)    
            if collisions:
                print("Collision detected!")
            for shot, collided_asteroids in collisions.items():
                for asteroid in collided_asteroids:
                    # debugging check
                    print(f"Splitting asteroid at {asteroid.rect.center}")
                    asteroid.split() 
                    asteroid.kill() # Remove the original asteroid after splitting. 
                    
                

                     
                      
                 
            

            # Clear screen
            screen.fill((0, 0, 0))

            #Draw all drawable objects on the screen
            for entity in drawable:
                 entity.draw(screen)
        
            # Refresh the display
            pygame.display.flip()

        



# This line ensures the main() function is only called when the file is run directly.
# It won't run if it's imported as a module.
if __name__ == "__main__":
    main()