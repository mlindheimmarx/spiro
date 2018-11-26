from PIL import Image, ImageDraw
import pdb
import aggdraw
import math

speed1 = 35 / 5
speed2 = 30 / 5
speed3 = -10 / 50
length1 = 19.5
length2 = 19.5
radius1 = 3.5
radius2 = 3.5
initial_theta1 = math.pi
initial_theta2 = math.pi

#speed1 = speed1 / 5
#speed2 = speed2 / 5
#speed3 = speed3 / 49

def lcm(a, b):
    a, b = abs(a), abs(b)
    c = 1
    while c * a / b != int (c * a / b):
        c += 1
    return c * a

class Wheel():
    def recalculate_loc(self):
        self.loc = [self.center_loc[0] + self.radius * math.cos(self.theta), self.center_loc[1] + self.radius * math.sin(self.theta)]
    def __init__(self, center_loc, length, radius, theta, speed):
        self.center_loc = center_loc
        self.length = length
        self.radius = radius
        self.theta = theta
        self.speed = speed
        self.recalculate_loc()
    center_loc = [0.0, 0.0]
    length = 0.0
    radius = 0.0
    theta = 0.0
    speed = 0.0
    loc = [0.0, 0.0]

wheel1 = Wheel([-13.5, -13.5], length1, radius1, initial_theta1, speed1)
wheel2 = Wheel([13.5, -13.5], length2, radius2, initial_theta2, speed2)

head_loc = [0.0, 0.0]
base_distance = ((wheel1.loc[0] - wheel2.loc[0]) ** 2 + (wheel1.loc[1] - wheel2.loc[1]) ** 2) ** (1 / 2)

res = 3840
divisor = 100
im = Image.new('RGB', (res, res), color = (255, 255, 255))
pixels = im.load()
rotations = int(lcm(abs(speed1), abs(speed2))) #, abs(speed3)))
num_pixels = 10000
draw = ImageDraw.Draw(im)
last_coord = (0, 0)

def rotate(x, y, theta):
    old_x = x - res / 2
    old_y = y - res / 2
    x = old_x * math.cos(theta) - old_y * math.sin(theta) + res / 2
    y = old_x * math.sin(theta) + old_y * math.cos(theta) + res / 2
    return [x, y]

points = []

print(abs((speed1 - speed2) / speed3))

for n in range(0, int(num_pixels) + 2):
    old_x = head_loc[0]
    old_y = head_loc[1]
    theta = (n / num_pixels) * 2 * math.pi * rotations
    wheel1.theta = theta / speed2
    wheel2.theta = theta / speed1
    theta = theta / speed1 / speed2 * speed3
    wheel1.recalculate_loc()
    wheel2.recalculate_loc()
    base_distance = ((wheel1.loc[0] - wheel2.loc[0]) ** 2 + (wheel1.loc[1] - wheel2.loc[1]) ** 2) ** (1 / 2)
    angle = math.acos(((base_distance ** 2 + wheel1.length ** 2 - wheel2.length ** 2) / (2 * base_distance * wheel1.length)))
    head_loc[0] = (wheel1.loc[0] + wheel1.length * math.cos(angle)) * 100
    head_loc[1] = (wheel1.loc[1] + wheel1.length * math.sin(angle)) * 100
    x = old_x * math.cos(theta) - old_y * math.sin(theta) + (res / 2)
    y = old_x * math.sin(theta) + old_y * math.cos(theta) + (res / 2)
    try:
        if n > 1:
            points = points + [x, y]
            for k in range(0, abs(int((speed1 - speed2) / speed3))):
                r_xy = rotate(x, y, k * 2 * rotations * math.pi * speed3 / speed2 / speed1)
                r_last_coord = rotate(last_coord[0], last_coord[1], k * 2 * rotations * math.pi * speed3 / speed2 / speed1)
                draw.line((r_xy[0], r_xy[1], r_last_coord[0], r_last_coord[1]), fill=(0, 0, 0, 255))
        last_coord = (x, y)
    except:
        pass

im.transpose(Image.FLIP_TOP_BOTTOM).save('pattern.png')
im.show()
