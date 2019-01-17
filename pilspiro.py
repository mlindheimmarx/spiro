from PIL import Image, ImageDraw
import aggdraw
import math

# set the speeds of yellow, blue, and turntable
speed1 = - (500) / 5
speed2 = - (505) / 5
speed3 =   (-100) / 50

# set the lengths of the rods
length1 = 18.3
length2 = 18.3

# set the radius that the rod bases travel around on their wheels in
radius1 = 3
radius2 = 3

# set the initial rotation of the wheels
initial_theta1 = math.pi / 2
initial_theta2 =  math.pi / 2

def lcm(a, b):
    # simple function, calculates least common multiple
    a, b = abs(a), abs(b)
    c = 1
    while c * a / b != int (c * a / b):
        c += 1
    return c * a

class Wheel():
    # the class defining the rods attacted to the blue or yellow wheels, with all necessary information about it
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

# I create two wheels at the inch locations of the two wheels with respect to horizontal and vertical axes going through the center of the white turntable
wheel1 = Wheel([-13.375, -13.375], length1, radius1, initial_theta1, speed1)
wheel2 = Wheel([13.375, -13.375], length2, radius2, initial_theta2, speed2)

head_loc = [0.0, 0.0]
base_distance = ((wheel1.loc[0] - wheel2.loc[0]) ** 2 + (wheel1.loc[1] - wheel2.loc[1]) ** 2) ** (1 / 2)

# I set the resolution of the image
res = 720

# I initialize my blank image and collect all of its pixels
im = Image.new('RGB', (res, res), color = (255, 255, 255))
pixels = im.load()

# I calculate the number of rotations that the turntable will need to turn. Currently intentionally erroneous
rotations = int(lcm(abs(speed1), abs(speed2)))

# I calculate the number of pixels per "petal" or single rotation of the turntable
num_pixels = 10000

# I start ImageDraw
draw = ImageDraw.Draw(im)
last_coord = (0, 0)

def rotate(x, y, theta):
    # simple function, given x and y, returns them rotated about (res / 2, res / 2)
    old_x = x - res / 2
    old_y = y - res / 2
    x = old_x * math.cos(theta) - old_y * math.sin(theta) + res / 2
    y = old_x * math.sin(theta) + old_y * math.cos(theta) + res / 2
    return [x, y]

for n in range(0, int(num_pixels) + 2):
    # main stuff: gets the current location of the head (pen)
    old_x = head_loc[0]
    old_y = head_loc[1]
    # calculates the movement of the wheels
    theta = (n / num_pixels) * 2 * math.pi * rotations
    wheel1.theta = theta / speed2
    wheel2.theta = theta / speed1
    theta = theta / speed1 / speed2 * speed3
    # moves the wheels
    wheel1.recalculate_loc()
    wheel2.recalculate_loc()
    # calculates the location of the head
    base_distance = ((wheel1.loc[0] - wheel2.loc[0]) ** 2 + (wheel1.loc[1] - wheel2.loc[1]) ** 2) ** (1 / 2)
    base_angle = math.atan((wheel2.loc[1] - wheel1.loc[1]) / (wheel2.loc[0] - wheel1.loc[0]))
    angle = math.acos((base_distance ** 2 + wheel1.length ** 2 - wheel2.length ** 2) / (2 * base_distance * wheel1.length))
    head_loc[0] = (wheel1.loc[0] + wheel1.length * math.cos(angle + base_angle)) * 100
    head_loc[1] = (wheel1.loc[1] + wheel1.length * math.sin(angle + base_angle)) * 100
    # rotates that by the amount by which the turntable has moved (to simulate the paper turning)
    x = old_x * math.cos(theta) - old_y * math.sin(theta) + (res / 2)
    y = old_x * math.sin(theta) + old_y * math.cos(theta) + (res / 2)
    try:
        if n > 1:
            points = points + [x, y]
            # draws all the petals of this that are necessary
            for k in range(0, int(math.ceil(abs((speed1 - speed2) / speed3)))):
                r_xy = rotate(x, y, k * 2 * rotations * math.pi * speed3 / speed2 / speed1)
                r_last_coord = rotate(last_coord[0], last_coord[1], k * 2 * rotations * math.pi * speed3 / speed2 / speed1)
                # draws the line between the old position and new position
                draw.line((r_xy[0], r_xy[1], r_last_coord[0], r_last_coord[1]), fill=(0, 0, 0, 255))
        last_coord = (x, y)
    except KeyboardInterrupt:
        quit()        

# the image is flipped from how I normally see the spirograph, so I flip it (technically unneccessary)
im.transpose(Image.FLIP_TOP_BOTTOM).save('pattern.png')
im.show()
