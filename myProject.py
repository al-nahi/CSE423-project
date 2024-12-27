import OpenGL.GLUT as glu
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


# Global Variables
window_width = 600
window_height = 600
stickman_x = 100
stickman_y = 60
stickman_head_radius = 10 
thorn_obstacle = []
halfCircle_obstacle = []
thorn_wait_time = 0.01
halfCircle_wait_time = 0.001
speed = 5
score = 0
game_over = False
paused = False
jump = False
jump_height = 0
jump_limit = 70
jump_speed = 5


def circledrawingAlgo(x_center, y_center, radius):
    x = 0
    y = radius
    d = 1 - radius
    plot_circle_points(x_center, y_center, x, y)

    while x < y:
        if d < 0:
            d = d + (2 * x + 3)
        else:
            y = y - 1
            d = d + (2 * x - 2 * y + 5)
        x = x + 1
        plot_circle_points(x_center, y_center, x, y)

def plot_circle_points(x_center, y_center, x, y):
    glBegin(GL_POINTS)
    glVertex2f(x_center + x, y_center + y)
    glVertex2f(x_center - x, y_center + y)
    glVertex2f(x_center + x, y_center - y)
    glVertex2f(x_center - x, y_center - y)
    glVertex2f(x_center + y, y_center + x)
    glVertex2f(x_center - y, y_center + x)
    glVertex2f(x_center + y, y_center - x)
    glVertex2f(x_center - y, y_center - x)
    glEnd()


def circledrawingAlgo_half(x_center, y_center, radius):
    x = 0
    y = radius
    d = 1 - radius
    plot_circle_points_half(x_center, y_center, x, y)

    while x < y:
        if d < 0:
            d = d + (2 * x + 3)
        else:
            y = y - 1
            d = d + (2 * x - 2 * y + 5)
        x = x + 1
        plot_circle_points_half(x_center, y_center, x, y)

def plot_circle_points_half(x_center, y_center, x, y):
    glBegin(GL_POINTS)
    glVertex2f(x_center + x, y_center + y)   #zone 1
    glVertex2f(x_center - x, y_center + y)   #zone 2
    glVertex2f(x_center + y, y_center + x)   #zone 0
    glVertex2f(x_center - y, y_center + x)   #zone 3
    glEnd()


def drawPoints(x, y, zone):
    if zone == 0:
        glVertex2f(x, y)
    elif zone == 1:
        glVertex2f(y, x)
    elif zone == 2:
        glVertex2f(-y, x)
    elif zone == 3:
        glVertex2f(-x, y)
    elif zone == 4:
        glVertex2f(-x, -y)
    elif zone == 5:
        glVertex2f(-y, -x)
    elif zone == 6:
        glVertex2f(y, -x)
    elif zone == 7:
        glVertex2f(x, -y)


def midpointLine(x1, y1, x2, y2, zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x1
    y = y1

    drawPoints(x, y, zone)

    while x < x2:
        
        if d < 0:
            d = d + dE
            x = x + 1
        else:
            d = d + dNE
            x = x + 1
            y = y + 1
        drawPoints(x, y, zone)

def convertToZoneZero(x1, y1, x2, y2, zone):
    if zone == 0:
        return x1, y1, x2, y2
    elif zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2


def getZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx > 0:
            if dy >= 0:
                return 0
            else:
                return 7
        else:
            if dy >= 0:
                return 3
            else:
                return 4
    else:
        if dx > 0:
            if dy >= 0:
                return 1
            else:
                return 6
        else:
            if dy >= 0:
                return 2
            else:
                return 5


def linedrawingalgo(x1, y1, x2, y2):
    zone = getZone(x1, y1, x2, y2)

    x1, y1, x2, y2 = convertToZoneZero(x1, y1, x2, y2, zone)
    midpointLine(x1, y1, x2, y2, zone)

def draw_left_arrow():
    glColor3f(0, 1, 1)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(25, 575, 50, 590)
    linedrawingalgo(25, 575, 70, 575)
    linedrawingalgo(25, 575, 50, 560)
    glEnd()


def draw_pause_icon():
    glColor3f(1, 0.647, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(288, 555, 288, 595)
    linedrawingalgo(312, 555, 312, 595)
    glEnd()    

def draw_play_icon():
    glColor3f(1, 0.647, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(280, 555, 320, 575)
    linedrawingalgo(280, 595, 320, 575)
    linedrawingalgo(280, 555, 280, 595)
    glEnd()

def draw_cross():
    glColor3f(1, 0, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(505, 555, 545, 595)
    linedrawingalgo(545, 555, 505, 595)
    glEnd()

def draw_easy_button():
    glColor3f(0, 1, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(25, 510, 25, 530)
    linedrawingalgo(85, 510, 85, 530)
    linedrawingalgo(25, 510, 85, 510)
    linedrawingalgo(25, 530, 85, 530)
    glEnd()

def draw_medium_button():
    glColor3f(1, 1, 0.199)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(260, 510, 260, 530)
    linedrawingalgo(320, 510, 320, 530)
    linedrawingalgo(260, 510, 320, 510)
    linedrawingalgo(260, 530, 320, 530)
    glEnd()

def draw_hard_button():
    glColor3f(1, 0, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(495, 510, 495, 530)
    linedrawingalgo(555, 510, 555, 530)
    linedrawingalgo(495, 510, 555, 510)
    linedrawingalgo(495, 530, 555, 530)
    glEnd()

def draw_platform():
    glColor3f(1, 0, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(0, 10, 600, 10)
    glEnd()


def draw_obsticle_thorn(x,y):
    glColor3f(0, 1, 0)
    glPointSize(2)
    glBegin(GL_POINTS)
    linedrawingalgo(x-10, y, x, y+30)
    linedrawingalgo(x+10, y, x, y+30)
    glEnd()

def draw_stickman():
    # Head
    circledrawingAlgo(stickman_x, stickman_y + jump_height, stickman_head_radius)

    glColor3f(0.2, 0.6, 0.85)
    glPointSize(2)
    glBegin(GL_POINTS)

    # Body
    linedrawingalgo(stickman_x, stickman_y - 10 + jump_height, stickman_x, stickman_y - 30 + jump_height)
    # Arms
    linedrawingalgo(stickman_x + 10, stickman_y - 26 + jump_height, stickman_x, stickman_y - 20 + jump_height)
    linedrawingalgo(stickman_x + 10, stickman_y - 20 + jump_height, stickman_x, stickman_y - 20 + jump_height)
    # Legs
    linedrawingalgo(stickman_x - 4, stickman_y - 50 + jump_height, stickman_x, stickman_y - 30 + jump_height)
    linedrawingalgo(stickman_x + 4, stickman_y - 50 + jump_height, stickman_x, stickman_y - 30 + jump_height)
    glEnd()



def animate():
    global thorn_obstacle, halfCircle_obstacle, game_over

    glClear(GL_COLOR_BUFFER_BIT)

    draw_left_arrow()
    if not paused:
        draw_pause_icon()
    else: 
        draw_play_icon()
    draw_cross()

    draw_platform()

    draw_easy_button()

    draw_medium_button()

    draw_hard_button()

    
    if not game_over:
        # Draw Stickman
        draw_stickman()

        # Draw thorn obstacles
        glColor3f(1, 1, 1)
        for thorn_ in thorn_obstacle:
             draw_obsticle_thorn(thorn_[0], thorn_[1])

        # Draw half circle obstacles
        glColor3f(1, 1, 1)
        for halfCircle in halfCircle_obstacle:
             circledrawingAlgo_half(halfCircle[0], halfCircle[1], 30)
        
        # animate Score
        glColor3f(0, 1, 0)
        glRasterPos2f(10, window_height - 130)
        for ch in f'Score: {score}':
            glutBitmapCharacter(glu.GLUT_BITMAP_HELVETICA_18, ord(ch))


    else:
        # Game Over Screen
        draw_stickman()
        glColor3f(0.0, 1.0, 0.0)

        glRasterPos2f(window_width // 2 - 50, window_height // 2)
        for ch in 'Game Over':
            glutBitmapCharacter(glu.GLUT_BITMAP_HELVETICA_18, ord(ch))
            
        glRasterPos2f(window_width // 2 - 70, window_height // 2 - 20)
        for ch in f'Final Score: {score}':
            glutBitmapCharacter(glu.GLUT_BITMAP_HELVETICA_18, ord(ch))
    

    glutSwapBuffers()
    glutPostRedisplay()

# Timer Function
def timer(value):
    global thorn_obstacle, halfCircle_obstacle, score, game_over, stickman_y, stickman_x, jump, jump_height, jump_limit, jump_speed

    if not game_over and not paused:

        # Update thorns
        for thorn_ in thorn_obstacle:
            if thorn_[0] > 5:
                thorn_[0] = thorn_[0] - speed
            else:
                thorn_obstacle.remove(thorn_)



        # Update half circles
        for halfCircle in halfCircle_obstacle:
            if halfCircle[0] - 10 > 0:
                halfCircle[0] = halfCircle[0] - speed
            else:
                halfCircle_obstacle.remove(halfCircle)
         
        

        #  Check for any collison
         # Checking for thorns
        for thorn_ in thorn_obstacle:
            if  math.sqrt((thorn_[0] - stickman_x)** 2) <= (10 + 10) and math.sqrt((thorn_[1] - (stickman_y+jump_height)) ** 2) <= (50 + 30):
                game_over = True  
                break

         # Checking for half circles 
        for halfCircle in halfCircle_obstacle:
            if  math.sqrt((halfCircle[0] - stickman_x)** 2) <= (10 + 20) and math.sqrt((halfCircle[1] - (stickman_y+jump_height)) ** 2) <= (50 + 20):
                game_over = True  
                break

        # Spawn thorns
        if random.random() < thorn_wait_time:
            thorn_obstacle.append([random.randint(620, 720), 10])

        # Spawn half circles
        if random.random() < halfCircle_wait_time:
            halfCircle_obstacle.append([random.randint(650, 750), 10])

        if jump == True:
            jump_height += jump_speed
            if jump_height > jump_limit:
                jump = False
        else:
            if jump_height > 0:
                jump_height -= jump_speed
        score += 1
    glutTimerFunc(24, timer, 0)
    glutPostRedisplay()


# Keyboard Function
def keyboard(key, x, y):
    global game_over, paused, jump

    if key == b' ' and not game_over and not paused and not jump:
        jump = True
        
    glutPostRedisplay()
        

# Restart Game
def restart_game():
    global thorn_obstacle, halfCircle_obstacle, score, game_over
    thorn_obstacle = []
    halfCircle_obstacle = []
    score = 0
    game_over = False

# Easy mode
def easy_mode():
    global thorn_wait_time, halfCircle_wait_time, speed
    thorn_wait_time = 0.01
    halfCircle_wait_time = 0.001
    speed = 5
    restart_game()


# Medium mode
def medium_mode():
    global thorn_wait_time, halfCircle_wait_time, speed
    thorn_wait_time = 0.02
    halfCircle_wait_time = 0.002
    speed = 8
    restart_game()


# Hard mode
def hard_mode():
    global thorn_wait_time, halfCircle_wait_time, speed
    thorn_wait_time = 0.03
    halfCircle_wait_time = 0.003
    speed = 10
    restart_game()


def mouse_click(button, state, x, y):
    global paused, game_over
    if state == GLUT_DOWN:
        y = 600 - y 
        if 25 <= x <= 85 and 520 <= y <= 530:
            easy_mode()
            print("Playing in easy mode")

        elif 260 <= x <= 320 and 520 <= y <= 530:
            medium_mode()
            print("Playing in medium mode")

        elif 495 <= x <= 555 and 520 <= y <= 530:
            hard_mode()
            print("Playing in hard mode")

        elif 25 <= x <= 75 and 550 <= y <= 600:
            restart_game()
            print("Starting Over")

        elif 275 <= x <= 325 and 550 <= y <= 600:
            paused = not paused

        elif 500 <= x <= 550 and 550 <= y <= 600:
            game_over = True
            print(f"Goodbye. Final Score: {score}")
            glutLeaveMainLoop()

    glutPostRedisplay()


# Initialize OpenGL
def initialize():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, 0, 1)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b'Stickman Obstacle Jumping')
glutDisplayFunc(animate)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_click)
glutTimerFunc(0, timer, 0)
initialize()
glutMainLoop()