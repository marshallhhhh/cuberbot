from concurrent.futures.thread import BrokenThreadPool
import discord
import os
import uuid
import json
from tempfile import gettempdir
from random import randint
from discord.ext import commands
from PIL import Image, ImageDraw

# load data from config.json
with open('config.json') as f:
    data = json.load(f)
    TOKEN = data["TOKEN"]
    PREFIX = data["PREFIX"]
    EMOJI = data["EMOJI"]

IMAGEPATH = gettempdir()+'\\%s.png' 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = PREFIX, intents=intents)

validcubes = ['2x2', '3x3']
moves2x2 = [['U', 'U2',  'U\''], ['R', 'R2', 'R\''], ['F', 'F2', 'F\'']]
moves3x3 = [['U', 'U2', 'U\''], ['L', 'L2', 'L\''],  
            ['F', 'F2', 'F\''], ['R', 'R2', 'R\''],  
            ['B', 'B2', 'B\''], ['D', 'D2', 'D\'']]
opposite_faces = {
    0: 5, # up (0) and down(5) 
    1: 3, # left (1) and right(3)
    2: 4, # front (2) and back (4)
    3: 1,
    4: 2, 
    5: 1
}

# checks if 2 faces are opposite one another
def is_opposite(face1, face2):
    if face1 != None and face2 != None:
        a = moves3x3.index(face1)
        b = moves3x3.index(face2)
        return (opposite_faces[a] == b)
    else:
        return False
 
# generates a 20 move scramble for 3x3 cube
def generate_3x3_scramble():
    last_face = None
    next_last_face = None
    scramble = []
    i = 0

    while i < 20:
        face = moves3x3[randint(0,len(moves3x3)-1)]
        if face != last_face: 
            if not (is_opposite(face, last_face) and face == next_last_face):
                scramble.append(face[randint(0,2)])
                next_last_face = last_face
                last_face = face
                i += 1

    return scramble

# generates a 10 move scramble for 2x2 cube
def generate_2x2_scramble():
    last_face = None
    scramble = []
    i = 0

    while i < 10:
        face = moves2x2[randint(0,len(moves2x2)-1)] # chooses a random face to move
        if face != last_face:
            scramble.append(face[randint(0,2)]) # appends a random value from the face generated above
            last_face = face
            i += 1

    return scramble

# 3x3 cube object
class Cube3x3:
    def __init__(self):
        self.cube = [
        [['white', 'white', 'white'],
        ['white', 'white', 'white'],
        ['white', 'white', 'white']], # up 0

        [['darkorange', 'darkorange', 'darkorange'],
        ['darkorange', 'darkorange', 'darkorange'],
        ['darkorange', 'darkorange', 'darkorange']], # left 1

        [['limegreen', 'limegreen', 'limegreen'],
        ['limegreen', 'limegreen', 'limegreen'],
        ['limegreen', 'limegreen', 'limegreen']], # front 2

        [['red', 'red', 'red'],
        ['red', 'red', 'red'],
        ['red', 'red', 'red']], # right 3

        [['deepskyblue', 'deepskyblue', 'deepskyblue'],
        ['deepskyblue', 'deepskyblue', 'deepskyblue'],
        ['deepskyblue', 'deepskyblue', 'deepskyblue']], # back 4

        [['yellow', 'yellow', 'yellow'],
        ['yellow', 'yellow', 'yellow'],
        ['yellow', 'yellow', 'yellow']] # down 5
        ]

    # transform the array representing the cube based on the face and how many times to move it
    def _move_face(self, face, amount):
        cube = self.cube
        if face == 0: 
            for i in range(amount):
                newcube = [[['', '', ''],['', '', ''],['', '', '']] for x in range(6)]

                newcube[0][0][0] = cube[0][2][0] #
                newcube[0][0][1] = cube[0][1][0] #
                newcube[0][0][2] = cube[0][0][0] #
                newcube[0][1][0] = cube[0][2][1] #
                newcube[0][1][1] = cube[0][1][1]
                newcube[0][1][2] = cube[0][0][1] #
                newcube[0][2][0] = cube[0][2][2] #
                newcube[0][2][1] = cube[0][1][2] #
                newcube[0][2][2] = cube[0][0][2] #

                newcube[1][0][0] = cube[2][0][0] #
                newcube[1][0][1] = cube[2][0][1] #
                newcube[1][0][2] = cube[2][0][2] #
                newcube[1][1] = cube[1][1]
                newcube[1][2] = cube[1][2]

                newcube[2][0][0] = cube[3][0][0] #
                newcube[2][0][1] = cube[3][0][1] #
                newcube[2][0][2] = cube[3][0][2] #
                newcube[2][1] = cube[2][1]
                newcube[2][2] = cube[2][2]

                newcube[3][0][0] = cube[4][0][0] #
                newcube[3][0][1] = cube[4][0][1] #
                newcube[3][0][2] = cube[4][0][2] #
                newcube[3][1] = cube[3][1]
                newcube[3][2] = cube[3][2]

                newcube[4][0][0] = cube[1][0][0] #
                newcube[4][0][1] = cube[1][0][1] #
                newcube[4][0][2] = cube[1][0][2] #
                newcube[4][1] = cube[4][1]
                newcube[4][2] = cube[4][2]

                newcube[5] = cube[5]
                cube = newcube

        if face == 1: # L working
            for i in range(amount):
                newcube = [[['', '', ''],['', '', ''],['', '', '']] for x in range(6)]

                newcube[0][0][0] = cube[4][2][2] #
                newcube[0][0][1] = cube[0][0][1]
                newcube[0][0][2] = cube[0][0][2]
                newcube[0][1][0] = cube[4][1][2] #
                newcube[0][1][1] = cube[0][1][1]
                newcube[0][1][2] = cube[0][1][2]
                newcube[0][2][0] = cube[4][0][2] #
                newcube[0][2][1] = cube[0][2][1]
                newcube[0][2][2] = cube[0][2][2]

                newcube[1][0][0] = cube[1][2][0] #
                newcube[1][0][1] = cube[1][1][0] #
                newcube[1][0][2] = cube[1][0][0] #
                newcube[1][1][0] = cube[1][2][1] #
                newcube[1][1][1] = cube[1][1][1]
                newcube[1][1][2] = cube[1][0][1] #
                newcube[1][2][0] = cube[1][2][2] #
                newcube[1][2][1] = cube[1][1][2] #
                newcube[1][2][2] = cube[1][0][2] #

                newcube[2][0][0] = cube[0][0][0] #
                newcube[2][0][1] = cube[2][0][1]
                newcube[2][0][2] = cube[2][0][2]
                newcube[2][1][0] = cube[0][1][0] #
                newcube[2][1][1] = cube[2][1][1]
                newcube[2][1][2] = cube[2][1][2]
                newcube[2][2][0] = cube[0][2][0] #
                newcube[2][2][1] = cube[2][2][1]
                newcube[2][2][2] = cube[2][2][2]

                newcube[3] = cube[3]

                newcube[4][0][0] = cube[4][0][0]
                newcube[4][0][1] = cube[4][0][1]
                newcube[4][0][2] = cube[5][2][0] #
                newcube[4][1][0] = cube[4][1][0]
                newcube[4][1][1] = cube[4][1][1]
                newcube[4][1][2] = cube[5][1][0] #
                newcube[4][2][0] = cube[4][2][0]
                newcube[4][2][1] = cube[4][2][1]
                newcube[4][2][2] = cube[5][0][0] #

                newcube[5][0][0] = cube[2][0][0] #
                newcube[5][0][1] = cube[5][0][1]
                newcube[5][0][2] = cube[5][0][2]
                newcube[5][1][0] = cube[2][1][0] #
                newcube[5][1][1] = cube[5][1][1]
                newcube[5][1][2] = cube[5][1][2]
                newcube[5][2][0] = cube[2][2][0] #
                newcube[5][2][1] = cube[5][2][1]
                newcube[5][2][2] = cube[5][2][2]

                cube = newcube

        if face == 2: # F working
            for i in range(amount):
                newcube = [[['', '', ''],['', '', ''],['', '', '']] for x in range(6)]
                newcube[0][0] = cube[0][0]
                newcube[0][1] = cube[0][1]
                newcube[0][2][0] = cube[1][2][2] #
                newcube[0][2][1] = cube[1][1][2] #
                newcube[0][2][2] = cube[1][0][2] #

                newcube[1][0][0] = cube[1][0][0]
                newcube[1][0][1] = cube[1][0][1]
                newcube[1][0][2] = cube[5][0][0] #
                newcube[1][1][0] = cube[1][1][0]
                newcube[1][1][1] = cube[1][1][1]
                newcube[1][1][2] = cube[5][0][1] #
                newcube[1][2][0] = cube[1][2][0]
                newcube[1][2][1] = cube[1][2][1]
                newcube[1][2][2] = cube[5][0][2] #

                newcube[2][0][0] = cube[2][2][0] #
                newcube[2][0][1] = cube[2][1][0] #
                newcube[2][0][2] = cube[2][0][0] #
                newcube[2][1][0] = cube[2][2][1] #
                newcube[2][1][1] = cube[2][1][1]
                newcube[2][1][2] = cube[2][0][1] #
                newcube[2][2][0] = cube[2][2][2] #
                newcube[2][2][1] = cube[2][1][2] #
                newcube[2][2][2] = cube[2][0][2] #

                newcube[3][0][0] = cube[0][2][0] #
                newcube[3][0][1] = cube[3][0][1]
                newcube[3][0][2] = cube[3][0][2]
                newcube[3][1][0] = cube[0][2][1] #
                newcube[3][1][1] = cube[3][1][1]
                newcube[3][1][2] = cube[3][1][2]
                newcube[3][2][0] = cube[0][2][2] #
                newcube[3][2][1] = cube[3][2][1]
                newcube[3][2][2] = cube[3][2][2]

                newcube[4] = cube[4]

                newcube[5][0][0] = cube[3][2][0] #
                newcube[5][0][1] = cube[3][1][0] #
                newcube[5][0][2] = cube[3][0][0] #
                newcube[5][1] = cube[5][1]
                newcube[5][2] = cube[5][2]

                cube = newcube

        if face == 3: # R working
            for i in range(amount):
                newcube = [[['', '', ''],['', '', ''],['', '', '']] for x in range(6)]
                newcube[0][0][0] = cube[0][0][0]
                newcube[0][0][1] = cube[0][0][1]
                newcube[0][0][2] = cube[2][0][2] #
                newcube[0][1][0] = cube[0][1][0]
                newcube[0][1][1] = cube[0][1][1]
                newcube[0][1][2] = cube[2][1][2] #
                newcube[0][2][0] = cube[0][2][0]
                newcube[0][2][1] = cube[0][2][1]
                newcube[0][2][2] = cube[2][2][2] #

                newcube[1] = cube[1]

                newcube[2][0][0] = cube[2][0][0]
                newcube[2][0][1] = cube[2][0][1]
                newcube[2][0][2] = cube[5][0][2] #
                newcube[2][1][0] = cube[2][1][0]
                newcube[2][1][1] = cube[2][1][1]
                newcube[2][1][2] = cube[5][1][2] #
                newcube[2][2][0] = cube[2][2][0]
                newcube[2][2][1] = cube[2][2][1]
                newcube[2][2][2] = cube[5][2][2] #

                newcube[3][0][0] = cube[3][2][0] #
                newcube[3][0][1] = cube[3][1][0] #
                newcube[3][0][2] = cube[3][0][0] #
                newcube[3][1][0] = cube[3][2][1] #
                newcube[3][1][1] = cube[3][1][1]
                newcube[3][1][2] = cube[3][0][1] #
                newcube[3][2][0] = cube[3][2][2] #
                newcube[3][2][1] = cube[3][1][2] #
                newcube[3][2][2] = cube[3][0][2] #

                newcube[4][0][0] = cube[0][2][2] #
                newcube[4][0][1] = cube[4][0][1]
                newcube[4][0][2] = cube[4][0][2]
                newcube[4][1][0] = cube[0][1][2] #
                newcube[4][1][1] = cube[4][1][1]
                newcube[4][1][2] = cube[4][1][2]
                newcube[4][2][0] = cube[0][0][2] #
                newcube[4][2][1] = cube[4][2][1]
                newcube[4][2][2] = cube[4][2][2]

                newcube[5][0][0] = cube[5][0][0]
                newcube[5][0][1] = cube[5][0][1]
                newcube[5][0][2] = cube[4][2][0] #
                newcube[5][1][0] = cube[5][1][0]
                newcube[5][1][1] = cube[5][1][1]
                newcube[5][1][2] = cube[4][1][0] #
                newcube[5][2][0] = cube[5][2][0]
                newcube[5][2][1] = cube[5][2][1]
                newcube[5][2][2] = cube[4][0][0] #

                cube = newcube

        if face == 4: # B working
            for i in range(amount):
                newcube = [[['', '', ''],['', '', ''],['', '', '']] for x in range(6)]
                newcube[0][0][0] = cube[3][0][2] #
                newcube[0][0][1] = cube[3][1][2] #
                newcube[0][0][2] = cube[3][2][2] #
                newcube[0][1][0] = cube[0][1][0]
                newcube[0][1][1] = cube[0][1][1]
                newcube[0][1][2] = cube[0][1][2]
                newcube[0][2][0] = cube[0][2][0]
                newcube[0][2][1] = cube[0][2][1]
                newcube[0][2][2] = cube[0][2][2]

                newcube[1][0][0] = cube[0][0][2] #
                newcube[1][0][1] = cube[1][0][1]
                newcube[1][0][2] = cube[1][0][2]
                newcube[1][1][0] = cube[0][0][1] #
                newcube[1][1][1] = cube[1][1][1]
                newcube[1][1][2] = cube[1][1][2]
                newcube[1][2][0] = cube[0][0][0] #
                newcube[1][2][1] = cube[1][2][1]
                newcube[1][2][2] = cube[1][2][2]

                newcube[2] = cube[2]

                newcube[3][0][0] = cube[3][0][0]
                newcube[3][0][1] = cube[3][0][1]
                newcube[3][0][2] = cube[5][2][2] #
                newcube[3][1][0] = cube[3][1][0]
                newcube[3][1][1] = cube[3][1][1]
                newcube[3][1][2] = cube[5][2][1] #
                newcube[3][2][0] = cube[3][2][0]
                newcube[3][2][1] = cube[3][2][1]
                newcube[3][2][2] = cube[5][2][0] #

                newcube[4][0][0] = cube[4][2][0] #
                newcube[4][0][1] = cube[4][1][0] #
                newcube[4][0][2] = cube[4][0][0] #
                newcube[4][1][0] = cube[4][2][1] #
                newcube[4][1][1] = cube[4][1][1]
                newcube[4][1][2] = cube[4][0][1] #
                newcube[4][2][0] = cube[4][2][2] #
                newcube[4][2][1] = cube[4][1][2] #
                newcube[4][2][2] = cube[4][0][2] #

                newcube[5][0][0] = cube[5][0][0]
                newcube[5][0][1] = cube[5][0][1]
                newcube[5][0][2] = cube[5][0][2]
                newcube[5][1][0] = cube[5][1][0]
                newcube[5][1][1] = cube[5][1][1]
                newcube[5][1][2] = cube[5][1][2]
                newcube[5][2][0] = cube[1][0][0] #
                newcube[5][2][1] = cube[1][1][0] #
                newcube[5][2][2] = cube[1][2][0] #

                cube = newcube

        if face == 5: # D working
            for i in range(amount):
                newcube = [[['', '', ''],['', '', ''],['', '', '']] for x in range(6)]
                newcube[0] = cube[0]

                newcube[1][0][0] = cube[1][0][0]
                newcube[1][0][1] = cube[1][0][1]
                newcube[1][0][2] = cube[1][0][2]
                newcube[1][1][0] = cube[1][1][0]
                newcube[1][1][1] = cube[1][1][1]
                newcube[1][1][2] = cube[1][1][2]
                newcube[1][2][0] = cube[4][2][0] #
                newcube[1][2][1] = cube[4][2][1] #
                newcube[1][2][2] = cube[4][2][2] #

                newcube[2][0][0] = cube[2][0][0]
                newcube[2][0][1] = cube[2][0][1]
                newcube[2][0][2] = cube[2][0][2]
                newcube[2][1][0] = cube[2][1][0]
                newcube[2][1][1] = cube[2][1][1]
                newcube[2][1][2] = cube[2][1][2]
                newcube[2][2][0] = cube[1][2][0] #
                newcube[2][2][1] = cube[1][2][1] #
                newcube[2][2][2] = cube[1][2][2] #

                newcube[3][0][0] = cube[3][0][0]
                newcube[3][0][1] = cube[3][0][1]
                newcube[3][0][2] = cube[3][0][2]
                newcube[3][1][0] = cube[3][1][0]
                newcube[3][1][1] = cube[3][1][1]
                newcube[3][1][2] = cube[3][1][2]
                newcube[3][2][0] = cube[2][2][0] #
                newcube[3][2][1] = cube[2][2][1] #
                newcube[3][2][2] = cube[2][2][2] #

                newcube[4][0][0] = cube[4][0][0]
                newcube[4][0][1] = cube[4][0][1]
                newcube[4][0][2] = cube[4][0][2]
                newcube[4][1][0] = cube[4][1][0]
                newcube[4][1][1] = cube[4][1][1]
                newcube[4][1][2] = cube[4][1][2]
                newcube[4][2][0] = cube[3][2][0] #
                newcube[4][2][1] = cube[3][2][1] #
                newcube[4][2][2] = cube[3][2][2] #

                newcube[5][0][0] = cube[5][2][0] #
                newcube[5][0][1] = cube[5][1][0] #
                newcube[5][0][2] = cube[5][0][0] #
                newcube[5][1][0] = cube[5][2][1] #
                newcube[5][1][1] = cube[5][1][1]
                newcube[5][1][2] = cube[5][0][1] #
                newcube[5][2][0] = cube[5][2][2] #
                newcube[5][2][1] = cube[5][1][2] #
                newcube[5][2][2] = cube[5][0][2] #

                cube = newcube

        return newcube

    # transform the array to represent the scramble, returns self
    def scramble(self, scramble):
        for x in scramble:
            for y in moves3x3:
                try:
                    amount = y.index(x) + 1 
                    f = moves3x3.index(y) 
                    self.cube = self._move_face(f, amount)
                except ValueError: 
                    pass

        return self.cube

    # draw an image and save it to 'path' then return the path to the image
    def draw(self):
        squareSize = 25 # size of each square
        gap = 2 # gap between each square
        spread = 3 * (squareSize + gap) # for simplicity in calculation of coords
        # creates image with size based on square sizes
        imgw = 12 * (squareSize + gap)
        imgh = 9 * (squareSize + gap)
        img = Image.new('RGB', (imgw, imgh), (54, 57, 63))
        # points for the top right hand corner of each face
        frontx = spread
        fronty = spread
        leftx = frontx - spread
        lefty = fronty
        downx = frontx
        downy = fronty + spread
        upx = frontx
        upy = fronty - spread
        rightx = frontx + spread
        righty = fronty
        backx = rightx + spread
        backy = righty

        d = ImageDraw.Draw(img) # ImageDraw object

        # draws each quadrant of a face in the correct position where xy is the top left corner of the face
        # and face is an integer representing the face of the cube
        def drawface(x, y, face):
            cube = self.cube
            d.rectangle([x, y, x + squareSize, y + squareSize], fill=cube[face][0][0])
            d.rectangle([x + squareSize + gap, y, x + 2 * squareSize + gap, y + squareSize], fill=cube[face][0][1])
            d.rectangle([x + 2 * squareSize +  2 * gap, y, x + 3 * squareSize + 2 * gap, y + squareSize], fill=cube[face][0][2])

            d.rectangle([x, y + squareSize + gap, x + squareSize, y + 2 * squareSize + gap], fill=cube[face][1][0])
            d.rectangle([x + squareSize + gap, y + squareSize + gap, x + 2 * squareSize + gap, y + 2 * squareSize + gap], fill=cube[face][1][1])
            d.rectangle([x + 2 * squareSize +  2 * gap, y + squareSize + gap, x + 3 * squareSize + 2 * gap, y + 2 * squareSize + gap], fill=cube[face][1][2])

            d.rectangle([x, y + 2 * (squareSize + gap), x + squareSize, y + 3 * squareSize + 2 * gap], fill = cube[face][2][0])
            d.rectangle([x + squareSize + gap, y + 2 * (squareSize + gap), x + 2 * squareSize + gap, y + 3 * squareSize + 2 * gap], fill = cube[face][2][1])
            d.rectangle([x + 2 * (squareSize + gap), y + 2 * (squareSize + gap), x + 3 * squareSize + 2 * gap, y + 3 * squareSize + 2 * gap], fill = cube[face][2][2])
        # calls the draw face function for each face
        drawface(upx, upy, 0)
        drawface(leftx, lefty, 1)
        drawface(frontx, fronty, 2)
        drawface(rightx, righty, 3)
        drawface(backx, backy, 4)
        drawface(downx, downy, 5)

        # saves the image in the specified directory with a uui filename then returns the path to the image
        path = IMAGEPATH % str(uuid.uuid4().hex)
        img.save(path)
        return(path)

# 3x3 cube object
class Cube2x2:
    def __init__(self):
        self.cube = [
        [['yellow', 'yellow'],
        ['yellow', 'yellow']],  # up 0
        [['limegreen', 'limegreen'],
        ['limegreen', 'limegreen']],    # left 1
        [['darkorange', 'darkorange'],
        ['darkorange', 'darkorange']],  # front 2
        [['deepskyblue', 'deepskyblue'],
        ['deepskyblue', 'deepskyblue']],      # right 3
        [['red', 'red'],
        ['red', 'red']],        # back 4
        [['white', 'white'],
        ['white', 'white']],    # down 5
        ]


    def move_face(self, face, amount):
        cube = self.cube
        if face == 0: # U
            for i in range(amount):
                newcube = [[['', ''],['', '']] for x in range(6)]
                # up
                newcube[0][0][0] = cube[0][1][0]
                newcube[0][0][1] = cube[0][0][0]
                newcube[0][1][0] = cube[0][1][1]
                newcube[0][1][1] = cube[0][0][1]
                # left
                newcube[1][0][0] = cube[2][0][0]
                newcube[1][0][1] = cube[2][0][1]
                newcube[1][1][0] = cube[1][1][0]
                newcube[1][1][1] = cube[1][1][1]
                # front
                newcube[2][0][0] = cube[3][0][0]
                newcube[2][0][1] = cube[3][0][1]
                newcube[2][1][0] = cube[2][1][0]
                newcube[2][1][1] = cube[2][1][1]
                # right
                newcube[3][0][0] = cube[4][0][0]
                newcube[3][0][1] = cube[4][0][1]
                newcube[3][1][0] = cube[3][1][0]
                newcube[3][1][1] = cube[3][1][1]
                # back
                newcube[4][0][0] = cube[1][0][0]
                newcube[4][0][1] = cube[1][0][1]
                newcube[4][1][0] = cube[4][1][0]
                newcube[4][1][1] = cube[4][1][1]
                # down face
                newcube[5] = cube[5]
                cube = newcube # U
        if face == 1: # R
            for i in range(amount):
                newcube = [[['', ''],['', '']], [['', ''],['', '']],[['', ''],['', '']],[['', ''],['', '']],[['', ''],['', '']],[['', ''],['', '']],]
                # up
                newcube[0][0][0] = cube[0][0][0]
                newcube[0][0][1] = cube[2][0][1]
                newcube[0][1][0] = cube[0][1][0]
                newcube[0][1][1] = cube[2][1][1]
                # left
                newcube[1] = cube[1]
                # front
                newcube[2][0][0] = cube[2][0][0]
                newcube[2][0][1] = cube[5][0][1]
                newcube[2][1][0] = cube[2][1][0]
                newcube[2][1][1] = cube[5][1][1]
                # right
                newcube[3][0][0] = cube[3][1][0]
                newcube[3][0][1] = cube[3][0][0]
                newcube[3][1][0] = cube[3][1][1]
                newcube[3][1][1] = cube[3][0][1]
                # back
                newcube[4][0][0] = cube[0][1][1] #
                newcube[4][0][1] = cube[4][0][1]
                newcube[4][1][0] = cube[0][0][1] #
                newcube[4][1][1] = cube[4][1][1]
                # down face
                newcube[5][0][0] = cube[5][0][0]
                newcube[5][0][1] = cube[4][1][0] #
                newcube[5][1][0] = cube[5][1][0]
                newcube[5][1][1] = cube[4][0][0] #

                cube = newcube
        if face == 2: # F
            for i in range(amount):
                newcube = [[['', ''],['', '']], [['', ''],['', '']],[['', ''],['', '']],[['', ''],['', '']],[['', ''],['', '']],[['', ''],['', '']],]
                # up face
                newcube[0][0][0] = cube[0][0][0]
                newcube[0][0][1] = cube[0][0][1]
                newcube[0][1][0] = cube[1][1][1] #
                newcube[0][1][1] = cube[1][0][1] #
                # left face
                newcube[1][0][0] = cube[1][0][0]
                newcube[1][0][1] = cube[5][0][0] #
                newcube[1][1][0] = cube[1][1][0]
                newcube[1][1][1] = cube[5][0][1] #
                # front face
                newcube[2][0][0] = cube[2][1][0]
                newcube[2][0][1] = cube[2][0][0]
                newcube[2][1][0] = cube[2][1][1]
                newcube[2][1][1] = cube[2][0][1]
                # right face
                newcube[3][0][0] = cube[0][1][0] #
                newcube[3][0][1] = cube[3][0][1]
                newcube[3][1][0] = cube[0][1][1] #
                newcube[3][1][1] = cube[3][1][1]
                # back face
                newcube[4] = cube[4]
                # down face, amount
                newcube[5][0][0] = cube[3][1][0] #
                newcube[5][0][1] = cube[3][0][0] #
                newcube[5][1][0] = cube[5][1][0]
                newcube[5][1][1] = cube[5][1][1]
                cube = newcube

        return newcube


    def scramble(self, scramble):
        for x in scramble:
            for y in moves2x2:
                try:
                    amount = y.index(x) + 1 # number of times to move the face
                    f = moves2x2.index(y) # which face to move
                    self.cube = self.move_face(f, amount)
                except ValueError: # catches list.index() ValueError
                    pass

        return self.cube


    def draw(self):
        squareSize = 20 # size of each square
        gap = 2 # gap between each square
        spread = 2 * (squareSize + gap) # for simplicity in calculation of coords
        # creates image with size based on square sizes
        imgw = 8 * (squareSize + gap)
        imgh = 6 * (squareSize + gap)
        img = Image.new('RGB', (imgw, imgh), (54, 57, 63))
        # points for the top right hand corner of each face
        frontx = 2 * (squareSize + gap)
        fronty = 2 * (squareSize + gap)
        leftx = frontx - spread
        lefty = fronty
        downx = frontx
        downy = fronty + spread
        upx = frontx
        upy = fronty - spread
        rightx = frontx + spread
        righty = fronty
        backx = rightx + spread
        backy = righty

        d = ImageDraw.Draw(img) # ImageDraw object

        # draws each quadrant of a face in the correct position where xy is the top left corner of the face
        # and face is an integer representing the face of the cube
        def drawface(x, y, face):
            cube = self.cube
            d.rectangle([x, y, x + squareSize, y + squareSize], fill=cube[face][0][0])
            d.rectangle([x + squareSize + gap, y, x + 2 * squareSize + gap, y + squareSize], fill=cube[face][0][1])
            d.rectangle([x, y + squareSize + gap, x + squareSize, y + 2 * squareSize + gap], fill=cube[face][1][0])
            d.rectangle([x + squareSize + gap, y + squareSize + gap, x + 2 * squareSize + gap, y + 2 * squareSize + gap], fill=cube[face][1][1])

        # calls the draw face function for each face
        drawface(upx, upy, 0)
        drawface(leftx, lefty, 1)
        drawface(frontx, fronty, 2)
        drawface(rightx, righty, 3)
        drawface(backx, backy, 4)
        drawface(downx, downy, 5)

        # saves the image in the temp directory with a uuid filename then returns the path to the image
        path = IMAGEPATH % str(uuid.uuid4().hex)
        img.save(path)
        return(path)


@bot.command()
async def scramble(ctx, *args):
    cube = args[0]
    if cube in validcubes:
        if cube == '2x2':
            scramble = generate_2x2_scramble()
            scramble_text = EMOJI + ' **' + '  '.join(scramble) + '** ' + EMOJI
            cube = Cube2x2()
            cube.scramble(scramble)
            
            image = cube.draw()
            await ctx.send(scramble_text, file=discord.File(image))
            os.remove(image)

        if cube == '3x3':
            scramble = generate_3x3_scramble()
            scramble_text = EMOJI + ' **' + '  '.join(scramble) + '** ' + EMOJI
            cube = Cube3x3()
            cube.scramble(scramble)
            image = cube.draw()

            await ctx.send(scramble_text, file=discord.File(image))
            os.remove(image)
    else:
        await ctx.send('Please specify a valid cube to scramble, see help for more info')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------')

bot.run(TOKEN)
