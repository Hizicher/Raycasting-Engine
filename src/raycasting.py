import pygame
import lib

with open("textures.ppm") as f:

    data = f.read().split()

textures = [int(pixel) for pixel in data] # Could not make it to implement it

pygame.init()
pygame.display.set_caption("Raycaster")

map = [
   [1, 1, 1, 1, 1, 1, 1, 1],
   [1, 0, 1, 0, 0, 0, 0, 1],
   [1, 0, 1, 0, 0, 1, 0, 1],
   [1, 0, 0, 0, 0, 1, 0, 1],
   [1, 0, 0, 0, 0, 1, 0, 1],
   [1, 0, 1, 0, 0, 1, 1, 1],
   [1, 0, 0, 0, 0, 0, 0, 1],
   [1, 1, 1, 1, 1, 1, 1, 1]
  ]

window = pygame.display.set_mode((1024, 512))

width, height = pygame.display.get_surface().get_size()

window.fill((50, 50, 50))

clock = pygame.time.Clock()

player = lib.Player(300, 120) # Sprite

while True:
    
    all_events = pygame.event.get()

    for event in all_events:
        
      if event.type == pygame.QUIT:
           
        exit()

      player.determine_action_of_the_player(event)
  
    if player.is_clockwise:

      player.update_angle(0.1)

    if player.is_counter_clockwise:
      
      player.update_angle(-0.1)

    if player.is_forward:
      
      if player.check_valid(map, player.pos_x + player.dir_x, player.pos_y + player.dir_y): # Checks if the player touches the wall or not
        player.pos_x += player.dir_x
        player.pos_y += player.dir_y
    
    if player.is_backward:
      if player.check_valid(map, player.pos_x - player.dir_x, player.pos_y - player.dir_y):
        player.pos_x -= player.dir_x
        player.pos_y -= player.dir_y
       

    lib.draw_map(window, map)

    pygame.draw.rect(window, (255, 255, 0), (player.pos_x, player.pos_y, 10, 10))
    pygame.draw.line(window, (255, 255, 0), (player.pos_x, player.pos_y), (player.pos_x + 15 * player.dir_x, player.pos_y + 15 * player.dir_y), 5)
    lib.draw_rays(window, player, map, textures)

    pygame.display.flip()
    window.fill((50, 50, 50))
    clock.tick(45)