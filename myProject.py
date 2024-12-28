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
game_state = "MENU"  # States: "MENU", "PLAYING", "GAME_OVER"
current_level = None  # Will store the currently selected level
global stickman_crouching
stickman_crouching = False
global bird_obstacle
bird_obstacle = []  
bird_wait_time = 0.005


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
    global stickman_crouching
    
    if stickman_crouching:
        # Crouching position - draw shorter stickman
        # Head (lower position)
        circledrawingAlgo(stickman_x, stickman_y - 10 + jump_height, stickman_head_radius)

        glColor3f(0.2, 0.6, 0.85)
        glPointSize(2)
        glBegin(GL_POINTS)

        # Body (shorter)
        linedrawingalgo(stickman_x, stickman_y - 20 + jump_height, stickman_x, stickman_y - 30 + jump_height)
        # Arms (lower position)
        linedrawingalgo(stickman_x + 8, stickman_y - 30 + jump_height, stickman_x, stickman_y - 25 + jump_height)
        linedrawingalgo(stickman_x - 8, stickman_y - 30 + jump_height, stickman_x, stickman_y - 25 + jump_height)
        # Legs (bent position)
        linedrawingalgo(stickman_x + 6, stickman_y - 40 + jump_height, stickman_x, stickman_y - 30 + jump_height)
        linedrawingalgo(stickman_x - 6, stickman_y - 40 + jump_height, stickman_x, stickman_y - 30 + jump_height)
        
    else:
        # Normal standing position (existing code)
        circledrawingAlgo(stickman_x, stickman_y + jump_height, stickman_head_radius)

        glColor3f(0.2, 0.6, 0.85)
        glPointSize(2)
        glBegin(GL_POINTS)

        # Body
        linedrawingalgo(stickman_x, stickman_y - 10 + jump_height, stickman_x, stickman_y - 30 + jump_height)
        # Arms
        linedrawingalgo(stickman_x + 10, stickman_y - 26 + jump_height, stickman_x, stickman_y - 20 + jump_height)
        linedrawingalgo(stickman_x - 10, stickman_y - 26 + jump_height, stickman_x, stickman_y - 20 + jump_height)
        # Legs
        linedrawingalgo(stickman_x - 4, stickman_y - 50 + jump_height, stickman_x, stickman_y - 30 + jump_height)
        linedrawingalgo(stickman_x + 4, stickman_y - 50 + jump_height, stickman_x, stickman_y - 30 + jump_height)
    
    glEnd()

def draw_text(text, x, y):
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))

def draw_bird(x, y):
    # Draw body
    glColor3f(0.6, 0.3, 0.1)  # Brown color
    circledrawingAlgo(x, y, 15)  # Body
    
    # Draw wings using lines
    glColor3f(0.4, 0.2, 0.1)  # Darker brown
    # Left wing
    linedrawingalgo(x-15, y, x-5, y+15)
    linedrawingalgo(x-5, y+15, x, y)
    # Right wing
    linedrawingalgo(x+15, y, x+5, y+15)
    linedrawingalgo(x+5, y+15, x, y)
    
    # Draw head
    glColor3f(0.6, 0.3, 0.1)
    circledrawingAlgo(x+15, y+5, 8)
    
    # Draw beak
    glColor3f(1.0, 0.7, 0.0)  # Orange
    linedrawingalgo(x+20, y+5, x+28, y+5)

# def draw_bird(x, y):
#     glPushMatrix()
#     glTranslatef(x, y, 0)  # Move the bird to the specified position

#     # Set the color for the bird
#     glColor3f(1.0, 0.5, 0.0)  # Example color: orange

#     # Draw the bird's body using a triangle
#     glBegin(GL_TRIANGLES)
#     glVertex2f(-0.1, 0.0)  # Left vertex
#     glVertex2f(0.1, 0.0)   # Right vertex
#     glVertex2f(0.0, 0.2)   # Top vertex
#     glEnd()

#     # Draw the bird's wings using lines
#     glBegin(GL_LINES)
#     glVertex2f(-0.1, 0.0)
#     glVertex2f(-0.2, 0.1)
#     glVertex2f(0.1, 0.0)
#     glVertex2f(0.2, 0.1)
#     glEnd()

#     glPopMatrix()

def animate():
    global game_over, paused, game_state
    glClear(GL_COLOR_BUFFER_BIT)
    
    if game_state == "MENU":
        # Draw title
        glColor3f(1.0, 1.0, 1.0)  # White color for title
        draw_text("Stickman Obstacle Jumping Game", window_width//2 - 150, window_height-300)
        # title_text = "Stickman Obstacle Jumping Game"
        # x = window_width//2 - (len(title_text) * 4)
        # y = window_height - 100
        # draw_text(title_text, x, y)
        # Draw level selection buttons and labels
        draw_easy_button()
        glColor3f(0.0, 1.0, 0.0)  # Green color for Easy text
        draw_text("Easy", 35, 550)
        
        draw_medium_button()
        glColor3f(1.0, 1.0, 0.0)  # Yellow color for Medium text
        draw_text("Medium", 270, 550)
        
        draw_hard_button()
        glColor3f(1.0, 0.0, 0.0)  # Red color for Hard text
        draw_text("Hard", 510, 550)
        
    elif game_state == "PLAYING":
        # Draw game elements
        draw_platform()
        draw_stickman()

        # Draw control buttons
        draw_left_arrow()
        if paused:
            draw_play_icon()
        else:
            draw_pause_icon()
        draw_cross()
        
        # Draw obstacles
        for thorn_ in thorn_obstacle:
            draw_obsticle_thorn(thorn_[0], thorn_[1])
        
        glColor3f(1, 1, 1)
        for halfCircle in halfCircle_obstacle:
            circledrawingAlgo_half(halfCircle[0], halfCircle[1], 30)

        for bird in bird_obstacle:
            draw_bird(bird[0], bird[1])
        
        # Draw score
        glColor3f(1.0, 1.0, 1.0)
        draw_text(f"Score: {score}", 10, 500)
        
    if game_over:
        # Game Over Screen
        glColor3f(1.0, 0.0, 0.0)  # Red color for game over
        draw_text("GAME OVER", window_width//2 - 50, window_height//2)
        draw_text(f"Final Score: {score}", window_width//2 - 60, window_height//2 - 30)
        draw_text("Click anywhere to continue", window_width//2 - 100, window_height//2 - 60)
        
        # Don't immediately restart - wait for mouse click
        game_state = "GAME_OVER"

    glutSwapBuffers()

# Timer Function
def timer(value):
    global thorn_obstacle, halfCircle_obstacle, bird_obstacle, score, game_over, stickman_y, stickman_x, jump, jump_height, jump_limit, jump_speed, game_state

    # Only update game logic if we're in PLAYING state
    if game_state == "PLAYING" and not game_over and not paused:
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

        # Check for collisions
        # For thorns
        for thorn_ in thorn_obstacle:
            if math.sqrt((thorn_[0] - stickman_x)** 2) <= (10 + 10) and math.sqrt((thorn_[1] - (stickman_y+jump_height)) ** 2) <= (50 + 30):
                game_over = True
                break

        #For half circles
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
            
        # Update jumping
        if jump:
            jump_height += jump_speed
            if jump_height > jump_limit:
                jump_height = jump_limit
                jump = False
        else:
            if jump_height > 0:
                jump_height -= jump_speed

        # Only increment score while playing
        score += 1

        # Update bird positions
        for bird in bird_obstacle:
            if bird[0] > 5:
                bird[0] = bird[0] - speed
            else:
                bird_obstacle.remove(bird)
        
        # Check bird collisions
        for bird in bird_obstacle:
            if math.sqrt((bird[0] - stickman_x)**2) <= (10 + 8) and \
               math.sqrt((bird[1] - (stickman_y+jump_height))**2) <= (10 + 10):
                game_over = True
                break
        
        # Spawn birds
        if random.random() < bird_wait_time:
            # Bird spawns at stickman's head height (stickman_y + jump_height)
            bird_obstacle.append([
                random.randint(620, 720),  # Random x position only
                stickman_y +22
            ])

    glutTimerFunc(24, timer, 0)
    glutPostRedisplay()


# Keyboard Function
def keyboard(key, x, y):
    global jump_height, jumping, stickman_crouching, game_over, paused, jump
    if key == b'x':  
        stickman_crouching = True
    elif key == b' ' and not game_over and not paused and not jump:
        jump = True
    else:
        stickman_crouching = False   
    glutPostRedisplay()

def keyboard_up(key, x, y):
    global stickman_crouching
    if key == b'x':  
        stickman_crouching = False
    
    glutPostRedisplay()
        

# Restart Game
def restart_game():
    global thorn_obstacle, halfCircle_obstacle, bird_obstacle, score, game_over, stickman_crouching
    thorn_obstacle = []
    halfCircle_obstacle = []
    bird_obstacle = []
    score = 0
    game_over = False
    stickman_crouching = False

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
    global paused, game_over, game_state, current_level
    if state == GLUT_DOWN:
        y = 600 - y
        
        if game_state == "GAME_OVER":
            # Any click during game over screen returns to menu
            game_state = "MENU"
            restart_game()
            return
            
        if game_state == "MENU":
            # Level selection only works in menu state
            if 25 <= x <= 85 and 510 <= y <= 530:
                current_level = "EASY"
                easy_mode()
                game_state = "PLAYING"
                print("Playing in easy mode")
            elif 260 <= x <= 320 and 510 <= y <= 530:
                current_level = "MEDIUM"
                medium_mode()
                game_state = "PLAYING"
                print("Playing in medium mode")
            elif 495 <= x <= 555 and 510 <= y <= 530:
                current_level = "HARD"
                hard_mode()
                game_state = "PLAYING"
                print("Playing in hard mode")

        if game_state == "PLAYING":
            if 25 <= x <= 75 and 550 <= y <= 600:
                game_state = "MENU"
                restart_game()
                print("Starting Over")
            elif 275 <= x <= 325 and 550 <= y <= 600:
                if game_state == "PLAYING":
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
glutKeyboardUpFunc(keyboard_up)
glutMouseFunc(mouse_click)
glutTimerFunc(0, timer, 0)
initialize()
glutMainLoop()