import pygame
import sys
import os
import math
import numpy as np

import shapes
import polyRasterizer as ras

pygame.init()
screenWidth = 200
screenHeight = 100
bigScreenWidth = 1000
bigScreenHeight = 500
screen = pygame.Surface((screenWidth, screenHeight))
bigScreen = pygame.display.set_mode((bigScreenWidth, bigScreenHeight))
pygame.display.set_caption('3D Renderer')

#remove window icon
transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 0))
pygame.display.set_icon(transparent_surface)

###################################################################################################################################

class Face:
    def __init__(self, color, point1, point2, point3):
        faces.append(self)
        self.color = color
        self.point1 = (baseX + point1[0], baseY + point1[1], baseZ + point1[2])
        self.point2 = (baseX + point2[0], baseY + point2[1], baseZ + point2[2])
        self.point3 = (baseX + point3[0], baseY + point3[1], baseZ + point3[2])

        #calculate depth
        self.depth = (self.point1[2] + self.point2[2] + self.point3[2]) / 3

    def draw(self):
        #get projected screen points - only required for drawing 2d poylgon on screen
        #pp1 = project(self.point1, FOV)
        #pp2 = project(self.point2, FOV)
        #pp3 = project(self.point3, FOV)

        #get projected points in a list - required only for draw polygon without z buffer
        #projectedPoints = [pp1, pp2, pp3]

        #draw polygon replaced with rasterize triangle with scanline and zbuffer
        #pygame.draw.polygon(screen, self.color, projectedPoints)
        ras.rasterize_triangle(pixels, z_buffer, modified_mask, self.point1, self.point2, self.point3, self.color)

    def rotate_y(self, angle, center):
        # Convert angle to radians for math functions
        rad = math.radians(angle)
        # Rotation matrix for Y-axis
        cos = math.cos(rad)
        sin = math.sin(rad)
        
        # Rotate each point around world center (baseX, baseZ)
        def rotate_point(point):
            # Translate to origin by subtracting base coordinates
            x = point[0] - center[0]
            z = point[2] - center[2]
            # Apply rotation
            new_x = x * cos - z * sin
            new_z = x * sin + z * cos
            # Translate back by adding base coordinates
            return (new_x + center[0], point[1], new_z + center[2])
        
        self.point1 = rotate_point(self.point1)
        self.point2 = rotate_point(self.point2)
        self.point3 = rotate_point(self.point3)
    
    def rotate_x(self, angle, center):
        # Convert angle to radians for math functions
        rad = math.radians(angle)
        # Rotation matrix for X-axis
        cos = math.cos(rad)
        sin = math.sin(rad)
        
        def rotate_point(point):
            # Translate to origin by subtracting base coordinates
            y = point[1] - center[1]
            z = point[2] - center[2]
            
            # Apply rotation
            new_y = y * cos - z * sin
            new_z = y * sin + z * cos
            
            # Translate back by adding base coordinates
            return (point[0], new_y + center[1], new_z + center[2])
        
        self.point1 = rotate_point(self.point1)
        self.point2 = rotate_point(self.point2)
        self.point3 = rotate_point(self.point3)

    def rotate_z(self, angle, center):
        # Convert angle to radians for math functions
        rad = math.radians(angle)
        # Rotation matrix for Z-axis
        cos = math.cos(rad)
        sin = math.sin(rad)
        
        def rotate_point(point):
            # Translate to origin by subtracting base coordinates
            x = point[0] - center[0]
            y = point[1] - center[2]
            
            # Apply rotation
            new_x = x * cos - y * sin
            new_y = x * sin + y * cos
            
            # Translate back by adding base coordinates
            return (new_x + center[0], new_y + center[2], point[2])
        
        self.point1 = rotate_point(self.point1)
        self.point2 = rotate_point(self.point2)
        self.point3 = rotate_point(self.point3)
    
    def movePoints(self, speedX, speedY, speedZ):
        self.point1 = (self.point1[0] + speedX, self.point1[1] + speedY, self.point1[2] + speedZ)
        self.point2 = (self.point2[0] + speedX, self.point2[1] + speedY, self.point2[2] + speedZ)
        self.point3 = (self.point3[0] + speedX, self.point3[1] + speedY, self.point3[2] + speedZ)

def project(point, FOV):
    x, y, z = point
    # Calculate screen coordinates relative to center
    screen_x = (x * FOV / (z + FOV))
    screen_y = (y * FOV / (z + FOV))
    # Add screen center offset
    return (screen_x + screenWidth/2, screen_y + screenHeight/2)

###################################################################################################################################
#camera position  (center of rotation for the camera)
baseX = 0
baseY = 0
baseZ = 0

FOV = 220          #optimal starting fov
zoom = 5
rotationSpeed = 0.5
movementSpeed = 0.4

#get pixels for z buffer
pixels = pygame.PixelArray(screen)
z_buffer = np.full((screen.get_width(), screen.get_height()), np.finfo(np.float32).max)
modified_mask = np.zeros_like(z_buffer, dtype=bool) #to prevent comparing float to  when comparing z depths

#get all faces and bodies
faces = []

#initialize cubes 
cube = shapes.Cube(0, 0, 250, 0.2, 0.2, 0.2, 0, 0, 0)

###################################################################################################################################

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #fov zoom
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0 and FOV >= 0:
                FOV += zoom
            if event.y < 0 and FOV >= 0:
                FOV -= zoom

            #clamp zoom
            if FOV < 0:
                FOV = 0

        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

    keys = pygame.key.get_pressed()
    for face in faces:
        #rotating
        if keys[pygame.K_UP]:
            face.rotate_x(-rotationSpeed, (baseX, baseY, baseZ))
        if keys[pygame.K_DOWN]:
            face.rotate_x(rotationSpeed, (baseX, baseY, baseZ))

        if keys[pygame.K_LEFT]:
            face.rotate_y(-rotationSpeed, (baseX, baseY, baseZ))
        if keys[pygame.K_RIGHT]:
            face.rotate_y(rotationSpeed, (baseX, baseY, baseZ))

        #movement
        if keys[pygame.K_w]:
            face.movePoints(0, 0, -movementSpeed)
        if keys[pygame.K_s]:
            face.movePoints(0, 0, movementSpeed)

        if keys[pygame.K_a]:
            face.movePoints(movementSpeed, 0, 0)
        if keys[pygame.K_d]:
            face.movePoints(-movementSpeed, 0, 0)

        if keys[pygame.K_SPACE]:
            face.movePoints(0, movementSpeed, 0)
        if keys[pygame.K_LSHIFT]:
            face.movePoints(0, -movementSpeed, 0)

    #clear screen and z buffer and z buffers modification mask
    screen.fill((18, 18, 18))
    z_buffer.fill(np.finfo(np.float32).max)
    modified_mask = np.zeros_like(z_buffer, dtype=bool)

    bigScreen.fill((18, 18, 18))

    #update faces, sorted by distance from screen, to draw closer faces on top
    for face in faces:
        face.draw()

    scaled_surface = pygame.transform.scale(screen, (bigScreenWidth, bigScreenHeight))
    bigScreen.blit(scaled_surface, (0, 0))

    pygame.display.flip()