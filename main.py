import os
import psutil
import time
import threading
import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

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


        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable,) #When you define a tuple with a single element, include comma after that element.

        # Instantiate the Player object
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()

        #Start the resource monitor in a thread:
        monitor_thread = threading.Thread(target=resource_monitor, daemon=True)
        monitor_thread.start()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            

            # Call tick() to manage FPS and calculate dt
            dt = clock.tick(60) / 1000.0

            # Update game state
            updatable.update(dt)

            # Check for collisions
            for asteroid in asteroids:
                 if player.collision_detect(asteroid):
                      print("Game over!")
                      sys.exit()
                 
            

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