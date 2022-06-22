import math
import time
import pygame
from pygame.locals import *
import os

pygame.init()


WIDTH = 800
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class vec3d():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Triangle():
    def __init__(self, points=[vec3d(),vec3d(),vec3d()], color=((255,255,255))):
        self.points = points
        self.color = color

class Mesh():
    def __init__(self, triangles):
        self.triangles = triangles

    def loadFromObjectFile(self, filename):
        try:
            with open(filename, "r") as obj:
                verts = []
                tris = []
                for line in obj:
                    if line[0] == "v":
                        
                        v = vec3d()
                        val = str(line)
                        v.x = int(float(val.split(" ")[1]))
                        v.y = int(float(val.split(" ")[2]))
                        v.z = int(float(val.split(" ")[3]))
                        verts.append(v)

                    if line[0] == "f":

                        v = vec3d()
                        val = str(line)
                        v.x = int(float(val.split(" ")[1]))
                        #print("v.x: " + str(v.x))
                        v.y = int(float(val.split(" ")[2]))
                        v.z = int(float(val.split(" ")[3]))

                        #print(verts[v.x-1])
                        tris.append(Triangle([verts[v.x-1], verts[v.y-1], verts[v.z-1]]))

            self.triangles = tris
            
        except Exception as e:
            print(e)
            return False

class GAME_LOGIC():
    def __init__(self, cubemesh):
        self.cubeMesh = cubemesh

class mat4x4():
    def __init__(self, matrix=[[0,0,0,0] for i in range(4)]):
        self.matrix = matrix

mesh_triangles = [
			Triangle([ vec3d(0.0, 0.0, 0.0),    vec3d(0.0, 1.0, 0.0),    vec3d(1.0, 1.0, 0.0) ]),
			Triangle([ vec3d(0.0, 0.0, 0.0),    vec3d(1.0, 1.0, 0.0),    vec3d(1.0, 0.0, 0.0) ]),
                                       
			Triangle([ vec3d(1.0, 0.0, 0.0),    vec3d(1.0, 1.0, 0.0),    vec3d(1.0, 1.0, 1.0)]),
			Triangle([ vec3d(1.0, 0.0, 0.0),    vec3d(1.0, 1.0, 1.0),   vec3d(1.0, 0.0, 1.0) ]),
                                                 
			Triangle([ vec3d(1.0, 0.0, 1.0),    vec3d(1.0, 1.0, 1.0),    vec3d(0.0, 1.0, 1.0) ]),
			Triangle([ vec3d(1.0, 0.0, 1.0),    vec3d(0.0, 1.0, 1.0),    vec3d(0.0, 0.0, 1.0) ]),
                                                
			Triangle([ vec3d(0.0, 0.0, 1.0),   vec3d( 0.0, 1.0, 1.0),    vec3d(0.0, 1.0, 0.0) ]),
			Triangle([ vec3d(0.0, 0.0, 1.0),   vec3d( 0.0, 1.0, 0.0),  vec3d(  0.0, 0.0, 0.0) ]),
                                           
			Triangle([vec3d( 0.0, 1.0, 0.0),   vec3d( 0.0, 1.0, 1.0),   vec3d( 1.0, 1.0, 1.0) ]),
			Triangle([vec3d( 0.0, 1.0, 0.0),   vec3d( 1.0, 1.0, 1.0),    vec3d(1.0, 1.0, 0.0) ]),
                                               
		    Triangle(	[ vec3d(1.0, 0.0, 1.0),  vec3d(  0.0, 0.0, 1.0),  vec3d(  0.0, 0.0, 0.0) ]),
		    Triangle(	[vec3d( 1.0, 0.0, 1.0),  vec3d(  0.0, 0.0, 0.0), vec3d(   1.0,0.0, 0.0) ]),]

fNear = 0.1
fFar = 1000.0
fFov = 90.0
fAspectRatio = float(HEIGHT) / float(WIDTH)
fFovRad = 1.0 / float( math.tan(fFov * 0.5 / 180.0 * math.pi) )

game_logic = GAME_LOGIC(Mesh(mesh_triangles))
game_logic.cubeMesh.loadFromObjectFile("VideoShip.obj")


matProjected = mat4x4()
matProjected.matrix[0][0] = fAspectRatio * fFovRad
matProjected.matrix[1][1] = fFovRad
matProjected.matrix[2][2] = fFar / (fFar-fNear)
matProjected.matrix[3][2] = (-fFar * fNear) / (fFar-fNear)
matProjected.matrix[2][3] = 1.0
matProjected.matrix[3][3] = 0.0

vectorCamera = vec3d()


def DrawTriangle(p1, p2, p3):
    pygame.draw.line(SCREEN, ((0,0,0)), (p1.x, p1.y), (p2.x, p2.y))
    pygame.draw.line(SCREEN, ((0,0,0)), (p2.x, p2.y), (p3.x, p3.y))
    pygame.draw.line(SCREEN, ((0,0,0)), (p3.x, p3.y), (p1.x, p1.y))

def MultiplyMatrixVector(i, o, m):
    #print(i.x)
    o.x = i.x * m.matrix[0][0] + i.y * m.matrix[1][0] + i.z * m.matrix[2][0] + m.matrix[3][0] 
    o.y = i.x * m.matrix[0][1] + i.y * m.matrix[1][1] + i.z * m.matrix[2][1] + m.matrix[3][1]
    o.z = i.x * m.matrix[0][2] + i.y * m.matrix[1][2] + i.z * m.matrix[2][2] + m.matrix[3][2]
    w = i.x * m.matrix[0][3] + i.y * m.matrix[1][3] + i.z * m.matrix[2][3] + m.matrix[3][3]
    if (int(w) != 0) and (float(w) != 0.0):
        o.x /= w
        o.y /= w
        o.z /= w
    return o

def fillTriangle(v1,v2,v3,c):
    p1, p2, p3 = (v1.x,v1.y),(v2.x,v2.y),(v3.x,v3.y)
    pygame.draw.polygon(SCREEN,c, (p1,p2,p3))

def convertRGBtoLUM(rgb):
    R = rgb[0]
    G = rgb[1]
    B = rgb[2]
    return (0.2126*R + 0.7152*G + 0.0722*B)/255

def YtoLstar(Y):
        # Send this function a luminance value between 0.0 and 1.0,
        # and it returns L* which is "perceptual lightness"

    if ( Y <= (216/24389)): #       // The CIE standard states 0.008856 but 216/24389 is the intent for 0.008856451679036
       return Y * (24389/27) # // The CIE standard states 903.3, but 24389/27 is the intent, making 903.296296296296296
    else:
        return pow(Y,(1/3)) * 116 - 16;

def avrgZ(z1, z2, z3):
    return float(z1+z2+z3)/3.0

fTheta = 0.0

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    SCREEN.fill((0,0,0))


    fTheta += 0.02


    matRotZ = mat4x4(matrix=[[0,0,0,0] for i in range(4)])
    matRotX = mat4x4(matrix=[[0,0,0,0] for i in range(4)])

    # Rotasjon Z
    matRotZ.matrix[0][0] = float(math.cos(fTheta))
    matRotZ.matrix[0][1] = float(math.sin(fTheta))
    matRotZ.matrix[1][0] = float(-math.sin(fTheta))
    matRotZ.matrix[1][1] = float(math.cos(fTheta))
    matRotZ.matrix[2][2] = 1
    matRotZ.matrix[3][3] = 1

    # Rotasjon X
    matRotX.matrix[0][0] = 1
    matRotX.matrix[1][1] = math.cos(fTheta * 0.5)
    matRotX.matrix[1][2] = math.sin(fTheta * 0.5)
    matRotX.matrix[2][1] = -math.sin(fTheta * 0.5)
    matRotX.matrix[2][2] = math.cos(fTheta * 0.5)
    matRotX.matrix[3][3] = 1

    vecTrianglesToRaster = []

    
    iteration = 0
    for triangle in game_logic.cubeMesh.triangles:
        old_posZ1 = triangle.points[0].z
        old_posZ2 = triangle.points[1].z
        old_posZ3 = triangle.points[2].z

        triProjected = Triangle()
        triTranslated = Triangle()
        triRotatedZ = Triangle()
        triRotatedZX = Triangle()

        triRotatedZ.points[0] = MultiplyMatrixVector(triangle.points[0], triRotatedZ.points[0], matRotZ)
        triRotatedZ.points[1] = MultiplyMatrixVector(triangle.points[1], triRotatedZ.points[1], matRotZ)
        triRotatedZ.points[2] = MultiplyMatrixVector(triangle.points[2], triRotatedZ.points[2], matRotZ)

        triRotatedZX.points[0] = MultiplyMatrixVector(triRotatedZ.points[0], triRotatedZX.points[0], matRotX)
        triRotatedZX.points[1] = MultiplyMatrixVector(triRotatedZ.points[1], triRotatedZX.points[1], matRotX)
        triRotatedZX.points[2] = MultiplyMatrixVector(triRotatedZ.points[2], triRotatedZX.points[2], matRotX)

        triTranslated = triRotatedZ
        triTranslated.points[0].z = triRotatedZ.points[0].z + 8.0
        triTranslated.points[1].z = triRotatedZ.points[1].z + 8.0
        triTranslated.points[2].z = triRotatedZ.points[2].z + 8.0

        normal = vec3d()
        line1 = vec3d()
        line2 = vec3d()
        line1.x = triTranslated.points[1].x - triTranslated.points[0].x
        line1.y = triTranslated.points[1].y - triTranslated.points[0].y
        line1.z = triTranslated.points[1].z - triTranslated.points[0].z

        line2.x = triTranslated.points[2].x - triTranslated.points[0].x
        line2.y = triTranslated.points[2].y - triTranslated.points[0].y
        line2.z = triTranslated.points[2].z - triTranslated.points[0].z

        normal.x = line1.y * line2.z - line1.z * line2.y
        normal.y = line1.z * line2.x - line1.x * line2.z
        normal.z = line1.x * line2.y - line1.y * line2.x

        l = float(math.sqrt(normal.x*normal.x + normal.y*normal.y + normal.z*normal.z))
        if l != 0:
            normal.x /= l
            normal.y /= l
            normal.z /= l

        if (normal.x * (triTranslated.points[0].x - vectorCamera.x) + 
            normal.y * (triTranslated.points[0].y - vectorCamera.y) +
            normal.z * (triTranslated.points[0].z - vectorCamera.z) < 0.0):

            light_direction = vec3d(0.0, 0.0, -1.0)
            length = float(math.sqrt(light_direction.x*light_direction.x + light_direction.y*light_direction.y + light_direction.z*light_direction.z))
            light_direction.x /= l
            light_direction.y /= l
            light_direction.z /= l
            dp = normal.x * light_direction.x + normal.y * light_direction.y + normal.z * light_direction.z
            colourVal = int( YtoLstar(dp)*2.55 )
            if colourVal < 0:
                colourVal = 0
            elif colourVal > 255:
                colourVal = 255
            triProjected.color = ((colourVal,colourVal,colourVal))


            triProjected.points[0] = MultiplyMatrixVector(triTranslated.points[0], triProjected.points[0], matProjected)
            triProjected.points[1] = MultiplyMatrixVector(triTranslated.points[1], triProjected.points[1], matProjected)
            triProjected.points[2] = MultiplyMatrixVector(triTranslated.points[2], triProjected.points[2], matProjected)

            triProjected.points[0].x += 1.0
            triProjected.points[0].y += 1.0
            triProjected.points[1].x += 1.0
            triProjected.points[1].y += 1.0
            triProjected.points[2].x += 1.0
            triProjected.points[2].y += 1.0

            triProjected.points[0].x *= 0.5 * float(WIDTH)
            triProjected.points[0].y *= 0.5 * float(HEIGHT)
            triProjected.points[1].x *= 0.5 * float(WIDTH)
            triProjected.points[1].y *= 0.5 * float(HEIGHT)
            triProjected.points[2].x *= 0.5 * float(WIDTH)
            triProjected.points[2].y *= 0.5 * float(HEIGHT)

            """
            DrawTriangle(triProjected.points[0], triProjected.points[1], triProjected.points[2])
            fillTriangle(triProjected.points[0], triProjected.points[1], triProjected.points[2], triProjected.color)
            """
            vecTrianglesToRaster.append(triProjected)

        

        for triprojected in vecTrianglesToRaster:
            DrawTriangle(triProjected.points[0], triProjected.points[1], triProjected.points[2])
            fillTriangle(triProjected.points[0], triProjected.points[1], triProjected.points[2], triProjected.color)

        triangle.points[0].z = old_posZ1
        triangle.points[1].z = old_posZ2
        triangle.points[2].z = old_posZ3
    
    pygame.display.update()
    clock.tick(60)