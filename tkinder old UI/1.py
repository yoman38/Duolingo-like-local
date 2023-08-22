import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys
print(sys.path)


# Content Creation Interface
class ContentCreation:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Content Creation")
        
        self.title_label = tk.Label(self.window, text="Lesson Title")
        self.title_label.pack()
        
        self.title_entry = tk.Entry(self.window)
        self.title_entry.pack()
        
        self.desc_label = tk.Label(self.window, text="Description")
        self.desc_label.pack()
        
        self.desc_entry = tk.Entry(self.window)
        self.desc_entry.pack()
        
        self.video_label = tk.Label(self.window, text="YouTube Link")
        self.video_label.pack()
        
        self.video_entry = tk.Entry(self.window)
        self.video_entry.pack()
        
        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit)
        self.submit_button.pack()
        
        self.lessons = []
        
        self.window.mainloop()

    def submit(self):
        lesson_title = self.title_entry.get()
        lesson_desc = self.desc_entry.get()
        lesson_video = self.video_entry.get()
        
        if not all([lesson_title, lesson_desc, lesson_video]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        self.lessons.append({
            "title": lesson_title,
            "description": lesson_desc,
            "video": lesson_video
        })
        
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.video_entry.delete(0, tk.END)

# Simple Dashboard
class Dashboard:
    def __init__(self, lessons):
        self.window = tk.Tk()
        self.window.title("Dashboard")

        for lesson in lessons:
            lesson_label = tk.Label(self.window, text=lesson["title"])
            lesson_label.pack()

        self.window.mainloop()

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ENEMY_SPEED = 2
BULLET_SPEED = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Basic Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.path = path
        self.current_point = 0
        self.rect.x, self.rect.y = self.path[self.current_point]

    def update(self):
        # Move the enemy along the path
        if self.current_point < len(self.path) - 1:
            dest_x, dest_y = self.path[self.current_point + 1]
            dir_x = dest_x - self.rect.x
            dir_y = dest_y - self.rect.y
            distance = (dir_x**2 + dir_y**2)**0.5
            if distance != 0:
                dir_x /= distance
                dir_y /= distance

            self.rect.x += dir_x * ENEMY_SPEED
            self.rect.y += dir_y * ENEMY_SPEED

            # Check if reached the next point
            if abs(self.rect.x - dest_x) < ENEMY_SPEED and abs(self.rect.y - dest_y) < ENEMY_SPEED:
                self.current_point += 1

# Basic Tower Class
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.range = 100
        self.bullets = pygame.sprite.Group()

    def update(self, enemies):
        # Check for enemies within range and shoot
        for enemy in enemies:
            distance = ((enemy.rect.x - self.rect.x)**2 + (enemy.rect.y - self.rect.y)**2)**0.5
            if distance < self.range:
                bullet = Bullet(self.rect.centerx, self.rect.centery, enemy.rect.centerx, enemy.rect.centery)
                self.bullets.add(bullet)
                break  # Only shoot one enemy at a time

    def draw(self, screen):
        # Draw tower and bullets
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        # Calculate bullet direction
        dir_x = end_x - start_x
        dir_y = end_y - start_y
        distance = (dir_x**2 + dir_y**2)**0.5
        self.dir_x = dir_x / distance
        self.dir_y = dir_y / distance

    def update(self):
        # Move the bullet
        self.rect.x += self.dir_x * BULLET_SPEED
        self.rect.y += self.dir_y * BULLET_SPEED

# Basic Tower Defense Game
class TowerDefense:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense")

        self.clock = pygame.time.Clock()

        # Enemy path
        self.path = [(0, 300), (SCREEN_WIDTH//3, 300), (SCREEN_WIDTH//3, SCREEN_HEIGHT//2), 
                     (2*SCREEN_WIDTH//3, SCREEN_HEIGHT//2), (2*SCREEN_WIDTH//3, 2*SCREEN_HEIGHT//3), 
                     (SCREEN_WIDTH, 2*SCREEN_HEIGHT//3)]

        self.enemies = pygame.sprite.Group()
        self.towers = [Tower(SCREEN_WIDTH//4, SCREEN_HEIGHT//4), Tower(3*SCREEN_WIDTH//4, 3*SCREEN_HEIGHT//4)]

        # Main loop
        self.run()

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Add enemy periodically
            if pygame.time.get_ticks() % 2000 == 0:
                enemy = Enemy(self.path)
                self.enemies.add(enemy)

            # Update
            self.enemies.update()
            for tower in self.towers:
                tower.update(self.enemies)
                tower.bullets.update()
                tower.bullets.draw(self.screen)

            # Draw
            for point in self.path:
                pygame.draw.circle(self.screen, BLACK, point, 5)
            for i in range(len(self.path)-1):
                pygame.draw.line(self.screen, BLACK, self.path[i], self.path[i+1], 5)

            self.enemies.draw(self.screen)
            for tower in self.towers:
                tower.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

# Uncomment below to start the game
# TowerDefense()


# Main Execution
content_creation = ContentCreation()
Dashboard(content_creation.lessons)
# Uncomment below to start game
TowerDefense()
