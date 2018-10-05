from PIL import Image, ImageDraw
import pdb
import math

speed1 = 1
speed2 = math.pi
speed3 = - 1 / 3
length1 = 23.0
length2 = 23.0
radius1 = 3
radius2 = 3
initial_theta1 = 0
initial_theta2 = 0

def lcm(a, b):
    c = 1
    while abs(c * a / b - int (c * a / b)) < 0.001:
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

divisor = 360

head_loc = [0.0, 0.0]
base_distance = ((wheel1.loc[0] - wheel2.loc[0]) ** 2 + (wheel1.loc[1] - wheel2.loc[1]) ** 2) ** (1 / 2)

res = 2160
im = Image.new('RGB', (res, res), color = 'white')
pixels = im.load()
rotations = int(lcm(lcm(abs(speed1), abs(speed2)), abs(speed3)))
num_pixels = divisor * rotations
print(rotations)
draw = ImageDraw.Draw(im)
last_coord = (0, 0)
for n in range(0, num_pixels):
    old_x = head_loc[0]
    old_y = head_loc[1]
    theta = (n / num_pixels) * 2 * math.pi
    wheel1.theta = theta * speed1 / speed3
    wheel2.theta = theta * speed2 / speed3
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
            draw.line((x, y, last_coord[0], last_coord[1]), fill=(0, 0, 0, 255))


        last_coord = (x, y)
    except:
        pass
im.transpose(Image.FLIP_TOP_BOTTOM).save('test.png')
