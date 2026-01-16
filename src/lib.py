import pygame
import math

class Player:

    def __init__(self, pos_x, pos_y):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = 2
        self.dir_y = 5 * math.sin(self.angle)
        self.dir_x = 5 * math.cos(self.angle)
        self.is_forward = False
        self.is_backward = False
        self.is_clockwise = False
        self.is_counter_clockwise = False 
    
    def determine_action_of_the_player(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
            
                self.is_forward = True

            if event.key == pygame.K_s:
            
                self.is_backward = True

            if event.key == pygame.K_a:
                
                self.is_counter_clockwise = True

            if event.key == pygame.K_d:

                self.is_clockwise = True

        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_w:
                
                self.is_forward = False
            
            if event.key == pygame.K_s:

                self.is_backward = False

            if event.key == pygame.K_a:
                
                self.is_counter_clockwise = False
            
            if event.key == pygame.K_d:

                self.is_clockwise = False

    def update_angle(self, angle: int):

        self.angle += angle

        if self.angle < 0:
            self.angle = 2 * math.pi + self.angle
        
        if self.angle > 2 * math.pi:
            self.angle %= (2 * math.pi)

        self.dir_x = 5 * math.cos(self.angle)
        self.dir_y = 5 * math.sin(self.angle)
    
    def check_valid(self, map: list, new_pos_x: int, new_pos_y: int):

        if self.angle > math.pi:

            map_y = int((new_pos_y - 1)// 64) 

        else:
            map_y = int((new_pos_y) // 64)
        
        if self.angle > math.pi / 2 and self.angle < 3 * math.pi / 2:

            map_x = int((new_pos_x - 1 )// 64)

        else:
            map_x = int((new_pos_x) // 64)

        
        if map[map_y][map_x] == 0:

            return True

        return False


def draw_map(window, map: list):

    position_to_draw = [0, 0]

    for y in map:

        for x in y:

            color = (0, 0, 0) if x == 0 else (255, 255, 255) 
            pygame.draw.rect(window, color, (position_to_draw[0], position_to_draw[1], 64, 64))
            pygame.draw.rect(window, (70, 70, 70), (position_to_draw[0], position_to_draw[1], 64, 64), 1)

            position_to_draw[0] += 64

        position_to_draw[1] += 64
        position_to_draw[0] = 0

def draw_rays(window, player_sprite: Player, map: list, textures: list):

    one_degree = math.pi / 180
    ray_angle = player_sprite.angle - math.pi / 6 # Turning the angle 30 degrees so that I can blit rays in a scope of 60 degrees

    if ray_angle < 0:
        ray_angle = 2 * math.pi + ray_angle
    
    if ray_angle > 2 * math.pi:
        ray_angle %= (2 * math.pi)

    for i in range(60):

        dof = 0

        if ray_angle % math.pi == 0:

            ray_pos_x = player_sprite.pos_x
            ray_pos_y = player_sprite.pos_y
            dof = 8

        else:

            atan = -1 / math.tan(ray_angle)

            if ray_angle > math.pi:

                ray_pos_y =  player_sprite.pos_y // 64 * 64 # A lof of math which is for determining the next square on the way of the ray horizontally
                ray_pos_x = (player_sprite.pos_y - ray_pos_y) * atan + player_sprite.pos_x 
                y_offset = -64
                x_offset = -1 * y_offset * atan

            elif ray_angle < math.pi:

                ray_pos_y = player_sprite.pos_y // 64 * 64 + 64
                ray_pos_x = (player_sprite.pos_y - ray_pos_y) * atan + player_sprite.pos_x
                y_offset = 64
                x_offset = -1 * y_offset * atan
            

        while dof < 8:
            map_x = int(ray_pos_x // 64)

            if y_offset < 0:
                map_y = int((ray_pos_y - 1) // 64) # When a ray clashes with a side of a corner we shall check the square if it is a wall or not, but as the square we have to check depends on the angle we should substract one, otherwise the squares might share the same side and the ray can basically determine it one wrong way

            else:
                map_y = int((ray_pos_y) // 64)
    
            if not 0 <= map_x < 8 or not 0 <= map_y < 8:

                break

            if map[map_y][map_x] != 0:

                break
            
            ray_pos_x += x_offset
            ray_pos_y += y_offset
            dof += 1
        horizontal_x = ray_pos_x
        horizontal_y = ray_pos_y
        distance_h = math.sqrt((ray_pos_x - player_sprite.pos_x) ** 2 + (ray_pos_y - player_sprite.pos_y) ** 2) 

        dof = 0
        ntan = -1 * math.tan(ray_angle)

        if ray_angle > math.pi / 2 and ray_angle < 3 * math.pi / 2:

            ray_pos_x =  player_sprite.pos_x // 64 * 64 # Again, determinin the next square on the way but vertically
            ray_pos_y = (player_sprite.pos_x - ray_pos_x) * ntan + player_sprite.pos_y
            x_offset = -64
            y_offset = -1 * x_offset * ntan

        elif ray_angle < math.pi / 2 or ray_angle > 3 * math.pi / 2:

            ray_pos_x = player_sprite.pos_x // 64 * 64 + 64
            ray_pos_y = (player_sprite.pos_x - ray_pos_x) * ntan + player_sprite.pos_y
            x_offset = 64
            y_offset = -1 * x_offset * ntan
            
        else:

            ray_pos_x = player_sprite.pos_x
            ray_pos_y = player_sprite.pos_y
            dof = 8

        while dof < 8:

            map_y = int((ray_pos_y) // 64)

            if x_offset < 0:
                map_x = int((ray_pos_x - 1) // 64)

            else:
                map_x = int((ray_pos_x) // 64)

            if not 0 <= map_x < 8 or not 0 <= map_y < 8:

                break

            if map[map_y][map_x] != 0:

                break
            ray_pos_x += x_offset
            ray_pos_y += y_offset
            dof += 1
        
        vertical_x = ray_pos_x
        vertical_y = ray_pos_y
        distance_v = math.sqrt((ray_pos_x - player_sprite.pos_x) ** 2 + (ray_pos_y - player_sprite.pos_y) ** 2)

        if distance_v < distance_h: # The minimum ray is the one we need so we compare the legnths
            pygame.draw.line(window, (255, 0, 0), (player_sprite.pos_x + 8, player_sprite.pos_y), (vertical_x, vertical_y), 3)
            color = (230, 0, 0)
            distance_final = distance_v

        else:
            pygame.draw.line(window, (255, 0, 0), (player_sprite.pos_x + 8, player_sprite.pos_y), (horizontal_x, horizontal_y), 3)
            distance_final = distance_h
            color = (170, 0, 0)
        

        ray_angle += one_degree

        if ray_angle > 2 * math.pi:

            ray_angle -= 2 * math.pi
        
        elif ray_angle < 0:

            ray_angle += 2 * math.pi
        
        fish_eye_avoider_angle = player_sprite.angle - ray_angle

        if fish_eye_avoider_angle > 2 * math.pi:

            fish_eye_avoider_angle -= 2 * math.pi
        
        if fish_eye_avoider_angle < 0:

            fish_eye_avoider_angle = 2 * math.pi + fish_eye_avoider_angle

        distance_final *= math.cos(fish_eye_avoider_angle)

        line_height = (64 * 350) / distance_final 
        
        if line_height > 350:

            line_height = 350 


        line_offset = 160 - line_height / 2

        pygame.draw.line(window, (0, 0, 155), (512 + i * 8 , 0), (512 + i * 8, line_offset), 8) # Ceiling
        pygame.draw.line(window, color, (512 + i * 8 , line_offset), (512 + i * 8, line_offset + line_height), 8) # The wall
        pygame.draw.line(window, (0, 0, 0), (512 + i * 8 , line_offset + line_height), (512 + i * 8, 350), 8) # Floor

        