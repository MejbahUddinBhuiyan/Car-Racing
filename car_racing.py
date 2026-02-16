from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time, sys

# ================= CONFIG =================
WIDTH, HEIGHT = 800, 800
LANES = 3

player_lane = 1
player_z = -6.0

speed = 0.18
score = 0
game_over = False

obstacles = []
last_spawn = time.time()

# ================= ROAD MATH =================
def road_half_width(z):
    near = 2.5
    far = 5.0
    t = min(abs(z) / 50.0, 1.0)
    return near + (far - near) * t

def lane_x(lane, z):
    half = road_half_width(z)
    lane_width = (half * 2) / LANES
    return -half + lane_width/2 + lane * lane_width

# ================= LIGHTING =================
def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    glLightfv(GL_LIGHT0, GL_POSITION, [0, 5, 5, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.3, 0.3, 0.3, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.8, 0.8, 0.8, 1])

# ================= MATERIAL =================
def material(r, g, b):
    glMaterialfv(GL_FRONT, GL_AMBIENT,  [r*0.3, g*0.3, b*0.3, 1])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,  [r, g, b, 1])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1,1,1,1])
    glMaterialf(GL_FRONT, GL_SHININESS, 50)

# ================= BOX =================
def box(w, h, d):
    w, h, d = w/2, h/2, d/2
    glBegin(GL_QUADS)
    faces = [
        ((0,0,1),  [(-w,-h,d),(w,-h,d),(w,h,d),(-w,h,d)]),
        ((0,0,-1), [(-w,-h,-d),(-w,h,-d),(w,h,-d),(w,-h,-d)]),
        ((-1,0,0), [(-w,-h,-d),(-w,-h,d),(-w,h,d),(-w,h,-d)]),
        ((1,0,0),  [(w,-h,-d),(w,h,-d),(w,h,d),(w,-h,d)]),
        ((0,1,0),  [(-w,h,-d),(-w,h,d),(w,h,d),(w,h,-d)]),
        ((0,-1,0), [(-w,-h,-d),(w,-h,-d),(w,-h,d),(-w,-h,d)])
    ]
    for n, verts in faces:
        glNormal3f(*n)
        for v in verts:
            glVertex3f(*v)
    glEnd()

# ================= CAR =================
def draw_car(lane, z, color):
    x = lane_x(lane, z)
    glPushMatrix()
    glTranslatef(x, -0.5, z)

    material(*color)
    box(1.1, 0.5, 2.2)

    glTranslatef(0, 0.45, 0.2)
    material(color[0]*0.8, color[1]*0.8, color[2]*0.8)
    box(0.7, 0.4, 1.2)

    glPopMatrix()

# ================= ROAD =================
def draw_road():
    material(0.05, 0.05, 0.05)  # black road
    glBegin(GL_QUADS)
    glNormal3f(0,1,0)

    far = road_half_width(-50)
    near = road_half_width(5)

    glVertex3f(-far, -1, -50)
    glVertex3f( far, -1, -50)
    glVertex3f( near, -1, 5)
    glVertex3f(-near, -1, 5)
    glEnd()

    # ---- White lane dividers ----
    glDisable(GL_LIGHTING)
    glColor3f(1,1,1)
    glLineWidth(2)

    glBegin(GL_LINES)
    for i in range(1, LANES):
        x_far = -far + (2*far/LANES) * i
        x_near = -near + (2*near/LANES) * i
        glVertex3f(x_far, -0.99, -50)
        glVertex3f(x_near, -0.99, 5)
    glEnd()

    glEnable(GL_LIGHTING)

# ================= COLLISION =================
def collision(a_lane, a_z, b_lane, b_z):
    return a_lane == b_lane and abs(a_z - b_z) < 1.8

# ================= UPDATE =================
def update(v):
    global score, speed, game_over, last_spawn

    if not game_over:
        for o in obstacles:
            o['z'] += speed

        obstacles[:] = [o for o in obstacles if o['z'] < 5]

        if time.time() - last_spawn > 0.9:
            lane = random.randint(0, LANES-1)
            obstacles.append({'lane': lane, 'z': -50})
            last_spawn = time.time()

        score += 1
        speed = 0.18 + score / 2000

        for o in obstacles:
            if collision(player_lane, player_z, o['lane'], o['z']):
                game_over = True

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# ================= INPUT =================
def special(k,x,y):
    global player_lane
    if not game_over:
        if k == GLUT_KEY_LEFT and player_lane > 0:
            player_lane -= 1
        if k == GLUT_KEY_RIGHT and player_lane < LANES-1:
            player_lane += 1

def keyboard(k,x,y):
    global score, speed, obstacles, game_over, player_lane
    if k == b'\x1b':
        sys.exit()
    if game_over and k in [b'r', b'R']:
        obstacles.clear()
        score = 0
        speed = 0.18
        player_lane = 1
        game_over = False

# ================= UI TEXT =================
def draw_text(x,y,text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glColor3f(1,1,1)
    glRasterPos2f(x,y)
    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    glEnable(GL_LIGHTING)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# ================= DISPLAY =================
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0,3,5, 0,0,-15, 0,1,0)

    draw_road()

    draw_car(player_lane, player_z, (0.2,0.4,1.0))  # BLUE PLAYER
    for o in obstacles:
        draw_car(o['lane'], o['z'], (1.0,0.2,0.2))  # RED OBSTACLES

    draw_text(20, HEIGHT-40, f"Score: {score}")

    if game_over:
        draw_text(WIDTH//2-80, HEIGHT//2, "GAME OVER")
        draw_text(WIDTH//2-120, HEIGHT//2-40, "Press R to Restart")

    glutSwapBuffers()

# ================= INIT =================
def init():
    glClearColor(0,0,0,1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, WIDTH/HEIGHT, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    init_lighting()

# ================= MAIN =================
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"3D Car Racing | PyOpenGL")

init()

glutDisplayFunc(display)
glutSpecialFunc(special)
glutKeyboardFunc(keyboard)
glutTimerFunc(0, update, 0)
glutMainLoop()
