import pygame
import sys
import os
import math

class Cube():
    def __init__(self, x, y, z, sX, sY, sZ, rX, rY, rZ):
        self.x = x
        self.y = y
        self.z = z

        self.sX = sX
        self.sY = sY
        self.sZ = sZ

        self.rX = rX
        self.rY = rY
        self.rZ = rZ

        cubeVertz=[
            (self.x -100 *self.sX, self.y -100 *self.sY, self.z -100 *self.sZ),        #top        #dl     #0
            (self.x -100 *self.sX, self.y -100 *self.sY, self.z +100 *self.sZ),                    #tl     #1
            (self.x +100 *self.sX, self.y -100 *self.sY, self.z +100 *self.sZ),                    #tr     #2
            (self.x +100 *self.sX, self.y -100 *self.sY, self.z -100 *self.sZ),                    #dr     #3
            (self.x -100 *self.sX, self.y +100 *self.sY, self.z -100 *self.sZ),        #bottom     #dl     #4
            (self.x -100 *self.sX, self.y +100 *self.sY, self.z +100 *self.sZ),                    #tl     #5
            (self.x +100 *self.sX, self.y +100 *self.sY, self.z +100 *self.sZ),                    #tr     #6
            (self.x +100 *self.sX, self.y +100 *self.sY, self.z -100 *self.sZ)                     #dr     #7
        ]

        #cube faces
        import main
        face0 = main.Face((255, 0, 0), cubeVertz[5], cubeVertz[4], cubeVertz[7])  #top
        face1 = main.Face((255, 0, 0), cubeVertz[5], cubeVertz[6], cubeVertz[7])

        face2 = main.Face((0, 0, 255), cubeVertz[1], cubeVertz[0], cubeVertz[3])  #bottom
        face3 = main.Face((0, 0, 255), cubeVertz[1], cubeVertz[2], cubeVertz[3])

        face4 = main.Face((255, 255, 0), cubeVertz[1], cubeVertz[0], cubeVertz[4])    #left
        face5 = main.Face((255, 255, 0), cubeVertz[1], cubeVertz[5], cubeVertz[4])

        face6 = main.Face((0, 255, 255), cubeVertz[3], cubeVertz[2], cubeVertz[6])   #right
        face7 = main.Face((0, 255, 255), cubeVertz[3], cubeVertz[7], cubeVertz[6])

        face8 = main.Face((0, 255, 0), cubeVertz[1], cubeVertz[2], cubeVertz[6]) #back
        face9 = main.Face((0, 255, 0), cubeVertz[1], cubeVertz[5], cubeVertz[6])

        face10 = main.Face((255, 0, 255), cubeVertz[0], cubeVertz[3], cubeVertz[7]) #front
        face11 = main.Face((255, 0, 255), cubeVertz[0], cubeVertz[4], cubeVertz[7])

        #get faces
        faces = []
        faces.append(face0)
        faces.append(face1)
        faces.append(face2)
        faces.append(face3)
        faces.append(face4)
        faces.append(face5)
        faces.append(face6)
        faces.append(face7)
        faces.append(face8)
        faces.append(face9)
        faces.append(face10)
        faces.append(face11)

        #get body center of rotation
        cX = 0
        cY = 0
        cZ = 0
        for face in faces:
            #get each face avarage
            cX += (face.point1[0] + face.point2[0] + face.point3[0]) / 3
            cY += (face.point1[1] + face.point2[1] + face.point3[1]) / 3
            cZ += (face.point1[2] + face.point2[2] + face.point3[2]) / 3
        #get all faces avarage
        center = (cX/len(faces), cY/len(faces), cZ/len(faces))

        #rotate faces by rotation
        for face in faces:
            face.rotate_x(self.rX, center)
            face.rotate_y(self.rY, center)
            face.rotate_z(self.rZ, center)

class Slope():
    def __init__(self, x, y, z, sX, sY, sZ, rX, rY, rZ):
        self.x = x
        self.y = y
        self.z = z

        self.sX = sX
        self.sY = sY
        self.sZ = sZ

        self.rX = rX
        self.rY = rY
        self.rZ = rZ

        slopeVertz=[
            (self.x -100 *self.sX, self.y +100 *self.sY, self.z +100 *self.sZ),     #btl    #0
            (self.x +100 *self.sX, self.y +100 *self.sY, self.z +100 *self.sZ),     #btr    #1
            (self.x -100 *self.sX, self.y +100 *self.sY, self.z -100 *self.sZ),     #bbl    #2
            (self.x +100 *self.sX, self.y +100 *self.sY, self.z -100 *self.sZ),     #bbr    #3

            (self.x -100 *self.sX, self.y -100 *self.sY, self.z +100 *self.sZ),     #ttl    #4
            (self.x -100 *self.sX, self.y -100 *self.sY, self.z -100 *self.sZ)      #tbl    #5
        ]

        #cube faces
        import main
        face0 = main.Face((255, 0, 0), slopeVertz[0], slopeVertz[1], slopeVertz[3])  #bottom
        face1 = main.Face((255, 0, 0), slopeVertz[0], slopeVertz[2], slopeVertz[3])

        face2 = main.Face((0, 0, 255), slopeVertz[4], slopeVertz[5], slopeVertz[2])  #side
        face3 = main.Face((0, 0, 255), slopeVertz[4], slopeVertz[0], slopeVertz[2])

        face4 = main.Face((255, 255, 0), slopeVertz[2], slopeVertz[5], slopeVertz[3])    #front
        face5 = main.Face((255, 255, 0), slopeVertz[4], slopeVertz[0], slopeVertz[1])    #back

        face6 = main.Face((0, 255, 255), slopeVertz[4], slopeVertz[5], slopeVertz[3])   #slope
        face7 = main.Face((0, 255, 255), slopeVertz[4], slopeVertz[1], slopeVertz[3])

        #get faces
        faces = []
        faces.append(face0)
        faces.append(face1)
        faces.append(face2)
        faces.append(face3)
        faces.append(face4)
        faces.append(face5)
        faces.append(face6)
        faces.append(face7)

        #get body center of rotation
        cX = 0
        cY = 0
        cZ = 0
        for face in faces:
            #get each face avarage
            cX += (face.point1[0] + face.point2[0] + face.point3[0]) / 3
            cY += (face.point1[1] + face.point2[1] + face.point3[1]) / 3
            cZ += (face.point1[2] + face.point2[2] + face.point3[2]) / 3
        #get all faces avarage
        center = (cX/len(faces), cY/len(faces), cZ/len(faces))

        #rotate faces by rotation
        for face in faces:
            face.rotate_x(self.rX, center)
            face.rotate_y(self.rY, center)
            face.rotate_z(self.rZ, center)