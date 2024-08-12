import pygame
import pandas as pd
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os

# Initialize pygame
pygame.init()

# Dimensions of the window
width, height = 800, 600
win = pygame.display.set_mode((width, height))

# Colors
black = (0, 0, 0)
orange = (255, 165, 0)
blue = (0, 123, 255)
red = (255, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)

# Load sprites
sprite_chico = pygame.image.load('chico.png')
sprite_chica = pygame.image.load('chica.png')
sprite_wind = pygame.image.load('wind.png')  # Load the wind image

# Resize the sprites
sprite_chico = pygame.transform.scale(sprite_chico, (40, 40))
sprite_chica = pygame.transform.scale(sprite_chica, (40, 40))
sprite_wind = pygame.transform.scale(sprite_wind, (50, 50))  # Resize wind sprite as needed

# Load the data
file_carla = 'StrydCarla3k.csv'
file_colo = 'StrydColo3k.csv'

data_carla = pd.read_csv(file_carla)
data_colo = pd.read_csv(file_colo)

# Function to convert pace (min/km) to speed (km/h)
def pace_to_speed(pace):
    minutes, seconds = map(int, pace.split(':'))
    total_minutes = minutes + seconds / 60
    speed = 60 / total_minutes
    return speed

data_carla['speed'] = data_carla['pace'].apply(pace_to_speed)
data_colo['speed'] = data_colo['pace'].apply(pace_to_speed)

# Define custom scales
min_power = 100
max_power = 400
min_speed = 5
max_speed = 20

# Scaling factors for the data to fit on screen
scale_factor = (height - 50) / (max_power - min_power)
speed_scale_factor = (height - 50) / (max_speed - min_speed)

# Initial configuration
clock = pygame.time.Clock()
running = True
frame = 0

# Lists to store previous positions (trails)
carla_trail = []
colo_trail = []
carla_speed_trail = []
colo_speed_trail = []

# Folder to save frames
frame_folder = "frames"
os.makedirs(frame_folder, exist_ok=True)

# Function to adjust wind sprite transparency based on wind speed
def adjust_wind_sprite(wind_value, sprite):
    if wind_value < 10:
        return None  # Don't display the wind sprite if wind < 10
    
    alpha = max(0, min(255, int((wind_value / max(data_carla['wind'].max(), data_colo['wind'].max())) * 255)))
    sprite_with_alpha = sprite.copy()
    sprite_with_alpha.set_alpha(alpha)
    return sprite_with_alpha

# Function to draw a glow effect around sprites
def draw_glow(surface, x, y, color, radius):
    glow_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, color + (100,), (radius, radius), radius)
    surface.blit(glow_surface, (x - radius, y - radius))

# Main animation loop
while running:
    win.fill(black)
    
    # Check if we're within bounds for both data sets
    if frame < len(data_carla) and frame < len(data_colo):
        # Calculate positions
        carla_x = frame * (width / len(data_carla))
        carla_y = height - 50 - (data_carla['stryd'].iloc[frame] - min_power) * scale_factor
        carla_speed_y = height - 50 - (data_carla['speed'].iloc[frame] - min_speed) * speed_scale_factor
        
        # Draw Carla's power (stryd)
        carla_trail.append((int(carla_x), int(carla_y)))
        if len(carla_trail) > 1:
            pygame.draw.lines(win, orange, False, carla_trail, 6)  # Orange for stryd
        
        # Draw Carla's speed on the right Y-axis
        carla_speed_trail.append((int(carla_x), int(carla_speed_y)))
        if len(carla_speed_trail) > 1:
            pygame.draw.lines(win, blue, False, carla_speed_trail, 2)  # Blue for speed
        
        # Draw glow effect around Carla's sprite
        #draw_glow(win, int(carla_x), int(carla_y), blue, 50)
        
        # Display Carla's sprite
        win.blit(sprite_chica, (int(carla_x) - 20, int(carla_y) - 20))
        
        # Adjust wind sprite based on Carla's wind value
        wind_value_carla = data_carla['wind'].iloc[frame]
        wind_sprite_carla = adjust_wind_sprite(wind_value_carla, sprite_wind)
        
        # Display wind sprite if applicable, in front of Carla
        if wind_sprite_carla:
            win.blit(wind_sprite_carla, (int(carla_x) - 60, int(carla_y) - 60))  # Position it directly in front
        
        # Calculate positions for Colo
        colo_x = frame * (width / len(data_colo))
        colo_y = height - 50 - (data_colo['stryd'].iloc[frame] - min_power) * scale_factor
        colo_speed_y = height - 50 - (data_colo['speed'].iloc[frame] - min_speed) * speed_scale_factor
        
        # Draw Colo's power (stryd)
        colo_trail.append((int(colo_x), int(colo_y)))
        if len(colo_trail) > 1:
            pygame.draw.lines(win, orange, False, colo_trail, 6)  # Orange for stryd
        
        # Draw Colo's speed on the right Y-axis
        colo_speed_trail.append((int(colo_x), int(colo_speed_y)))
        if len(colo_speed_trail) > 1:
            pygame.draw.lines(win, red, False, colo_speed_trail, 2)  # Red for speed
        
        # Draw glow effect around Colo's sprite
        #draw_glow(win, int(colo_x), int(colo_y), red, 50)
        
        # Display Colo's sprite
        win.blit(sprite_chico, (int(colo_x) - 20, int(colo_y) - 20))
        
        # Adjust wind sprite based on Colo's wind value
        wind_value_colo = data_colo['wind'].iloc[frame]
        wind_sprite_colo = adjust_wind_sprite(wind_value_colo, sprite_wind)
        
        # Display wind sprite if applicable, in front of Colo
        if wind_sprite_colo:
            win.blit(wind_sprite_colo, (int(colo_x) - 60, int(colo_y) - 60))  # Position it directly in front
    
        # Dynamic Annotations
        font = pygame.font.SysFont(None, 28)
        speed_text_carla = font.render(f"Ritmo de ella: {data_carla['speed'].iloc[frame]:.1f} km/h", True, blue)
        power_text_carla = font.render(f"Stryd de ella: {data_carla['stryd'].iloc[frame]:.0f} W", True, orange)
        speed_text_colo = font.render(f"Ritmo de el: {data_colo['speed'].iloc[frame]:.1f} km/h", True, red)
        power_text_colo = font.render(f"Stryd de el: {data_colo['stryd'].iloc[frame]:.0f} W", True, orange)
        
        # Positioning annotations in the bottom right corner
        win.blit(speed_text_carla, (width - speed_text_carla.get_width() - 15, height - 200))
        win.blit(power_text_carla, (width - power_text_carla.get_width() - 15, height - 150))
        win.blit(speed_text_colo, (width - speed_text_colo.get_width() - 15, height - 100))
        win.blit(power_text_colo, (width - power_text_colo.get_width() - 15, height - 50))
        
        # Draw the time axis
        pygame.draw.line(win, white, (0, height - 30), (width, height - 30), 2)
        
        # Draw time markers
        for i in range(0, len(data_carla), len(data_carla) // 10):  # Place 10 time markers
            x_pos = i * (width / len(data_carla))
            pygame.draw.line(win, white, (int(x_pos), height - 35), (int(x_pos), height - 25), 2)
            time_label = f"{i}s"
            font = pygame.font.SysFont(None, 24)
            img = font.render(time_label, True, white)
            win.blit(img, (int(x_pos) - 10, height - 20))
    
    # Save the frame as an image
    pygame.image.save(win, f"{frame_folder}/frame_{frame:04d}.png")
    
    pygame.display.update()
    clock.tick(60)  # Increased FPS to 60 for smoother animation
    
    frame += 1
    if frame >= max(len(data_carla), len(data_colo)):
        running = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
