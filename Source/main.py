import pygame
import sys
import os
import math

pygame.init()
screenWidth = 1000
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('3D Renderer')

#remove window icon
transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 0))
pygame.display.set_icon(transparent_surface)

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
        #get projected points
        pp1 = project(self.point1, FOV)
        pp2 = project(self.point2, FOV)
        pp3 = project(self.point3, FOV)

        #get projected points in a list
        projectedPoints = [pp1, pp2, pp3]

        #draw polygon
        pygame.draw.polygon(screen, self.color, projectedPoints)

    def rotate_y(self, angle):
        # Convert angle to radians for math functions
        rad = math.radians(angle)
        # Rotation matrix for Y-axis
        cos = math.cos(rad)
        sin = math.sin(rad)
        
        # Rotate each point around world center (baseX, baseZ)
        def rotate_point(point):
            # Translate to origin by subtracting base coordinates
            x = point[0] - baseX
            z = point[2] - baseZ
            # Apply rotation
            new_x = x * cos - z * sin
            new_z = x * sin + z * cos
            # Translate back by adding base coordinates
            return (new_x + baseX, point[1], new_z + baseZ)
        
        self.point1 = rotate_point(self.point1)
        self.point2 = rotate_point(self.point2)
        self.point3 = rotate_point(self.point3)
    
    def rotate_x(self, angle):
        # Convert angle to radians for math functions
        rad = math.radians(angle)
        # Rotation matrix for X-axis
        cos = math.cos(rad)
        sin = math.sin(rad)
        
        def rotate_point(point):
            # Translate to origin by subtracting base coordinates
            y = point[1] - baseY
            z = point[2] - baseZ
            
            # Apply rotation
            new_y = y * cos - z * sin
            new_z = y * sin + z * cos
            
            # Translate back by adding base coordinates
            return (point[0], new_y + baseY, new_z + baseZ)
        
        self.point1 = rotate_point(self.point1)
        self.point2 = rotate_point(self.point2)
        self.point3 = rotate_point(self.point3)

    def rotate_z(self, angle):
        # Convert angle to radians for math functions
        rad = math.radians(angle)
        # Rotation matrix for Z-axis
        cos = math.cos(rad)
        sin = math.sin(rad)
        
        def rotate_point(point):
            # Translate to origin by subtracting base coordinates
            x = point[0] - baseX
            y = point[1] - baseY
            
            # Apply rotation
            new_x = x * cos - y * sin
            new_y = x * sin + y * cos
            
            # Translate back by adding base coordinates
            return (new_x + baseX, new_y + baseY, point[2])
        
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
rotationSpeed = 0.05
movementSpeed = 0.20

#get all faces and bodies
faces = []

cubeX = 0
cubeY = 250
cubeZ = 250

cubeVertz=[
    (cubeX -100, cubeY -100, cubeZ -100),      #top    #dl     #0
    (cubeX -100, cubeY -100, cubeZ +100),               #tl     #1
    (cubeX +100, cubeY -100, cubeZ +100),                #tr     #2
    (cubeX +100, cubeY -100, cubeZ -100),               #dr     #3

    (cubeX -100, cubeY +100, cubeZ -100),       #bottom #dl     #4
    (cubeX -100, cubeY +100, cubeZ +100),                #tl     #5
    (cubeX +100, cubeY +100, cubeZ +100),                 #tr     #6
    (cubeX +100, cubeY +100, cubeZ -100)                #dr     #7
]

#cube faces
face = Face((255, 0, 0), cubeVertz[5], cubeVertz[4], cubeVertz[7])  #top
face = Face((255, 0, 0), cubeVertz[5], cubeVertz[6], cubeVertz[7])

face = Face((0, 0, 255), cubeVertz[1], cubeVertz[0], cubeVertz[3])  #bottom
face = Face((0, 0, 255), cubeVertz[1], cubeVertz[2], cubeVertz[3])

face = Face((255, 255, 0), cubeVertz[1], cubeVertz[0], cubeVertz[4])    #left
face = Face((255, 255, 0), cubeVertz[1], cubeVertz[5], cubeVertz[4])

face = Face((0, 255, 255), cubeVertz[3], cubeVertz[2], cubeVertz[6])   #right
face = Face((0, 255, 255), cubeVertz[3], cubeVertz[7], cubeVertz[6])

face = Face((0, 255, 0), cubeVertz[1], cubeVertz[2], cubeVertz[6]) #back
face = Face((0, 255, 0), cubeVertz[1], cubeVertz[5], cubeVertz[6])

face = Face((255, 0, 255), cubeVertz[0], cubeVertz[3], cubeVertz[7]) #front
face = Face((255, 0, 255), cubeVertz[0], cubeVertz[4], cubeVertz[7])

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
            face.rotate_x(-rotationSpeed)
        if keys[pygame.K_DOWN]:
            face.rotate_x(rotationSpeed)

        if keys[pygame.K_LEFT]:
            face.rotate_y(-rotationSpeed)
        if keys[pygame.K_RIGHT]:
            face.rotate_y(rotationSpeed)

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

    screen.fill((18, 18, 18))

    #update faces, sorted by distance from screen, to draw closer faces on top
    for face in sorted(faces, key=lambda x: x.depth, reverse=True):

        #recalculate facedepth
        face.depth = (face.point1[2] + face.point2[2] + face.point3[2]) / 3

        #draw when in front
        if face.depth > 0:
            face.draw()

    pygame.display.flip()
