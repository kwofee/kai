import PySimpleGUI as sg
from pygame import *

sg.theme('DarkTeal5')

import PySimpleGUI as sg

import sys, smtplib, ssl, random
import mysql.connector

con = mysql.connector.connect(
host = 'localhost',
user = "root",
password='ROOT',
database='kai')

cur = con.cursor()

if con.is_connected():

    print("connected successfully")

else:

    print("error while connecting")

sg.theme('DarkTeal5')   # Add a touch of color

# All the stuff inside your window.

layout = [ [sg.Text('  Kai  ',font='8514oem 50 bold',pad=(50,20))],

            [sg.Button('  Log In  ', button_color="#3b8e91", font='8514oem 12 bold', pad=(20,10))],

            [sg.Button('  Sign Up  ', button_color="#3b8e91", font='8514oem 12 bold', pad=(20,10))]]

# Create the Main Window

window = sg.Window('Kai', layout, resizable=True, element_justification='c')

# Login Window

def win_login(og_win=window):

    og_win.close()

    try:

        Left_Column = [[sg.Text('Or are you a new user?', font='8514oem 8'), sg.Text(' ' * 10)],

                       [sg.Text('Then', font='8514oem 8'), sg.Button(' Sign Up ', font='8514oem 8')]]



        layout = [[sg.Text('Email : ', font='8514oem 8'), sg.InputText(key='in1', do_not_clear=False)],

                  [sg.Text('Password : ', font='8514oem 8'), sg.InputText(key='in2', do_not_clear=False)],

                  [sg.Button(' Log In ', font='8514oem 8')],

                  [sg.Text('_' * 60, font='8514oem 8')],

                  [sg.Column(Left_Column)]]


        window = sg.Window('Login', layout, margins=(20, 40))

        while True:

            event, values = window.Read()
            if event == ' Log In ':

                email = str(values['in1'])

                Is_space = email.isspace()
                if not email:

                    sg.Popup('No Input Data!!')

                    window.close()

                    win_login()

                elif Is_space == True:

                    sg.popup('Email Cannot contain Spaces!!')

                    window.close()

                    win_login()

                elif Is_space == False:

                    if email.endswith('@gmail.com') == False:

                        sg.Popup('Invalid Email!!')

                        window.close()

                        win_login()

                    else:
                        query = ("SELECT password, emailid from users where emailid = '%s';"%(email))

                        cur.execute(query)

                        user1 = cur.fetchone()

                        cr_pass = user1[0]
                        gemail = user1[1]

                        if (email != gemail):

                            sg.Popup('Incorrect Email!!')

                            window.close()
                        elif (email == gemail):

                            passwd = str(values['in2'])

                            if (passwd.isspace() == True):

                                sg.Popup('Password cannot contain Spaces!!')

                                window.close()

                                win_login()

                            elif passwd == cr_pass:

                                window.close()

                                global login

                                login = True

                            else:

                                win_Invalid_Input()

                                window.close()

                                win_login()
                        else:

                            window.close()

                            win_login()
                else:

                    sg.Popup('Something Went Wrong!!')

                    window.close()

                    win_login()

            elif event == sg.WIN_CLOSED:

                window.close()

                i = False

                return i

            elif (event == ' Sign Up '):

                window.close()

                win_Signup()

            elif (event == " Forget Email? "):

                window.close()

            else:

                window.close()

                win_login()

    except Exception as err:

        sg.Popup(err)

        win_Invalid_Input()

        window.close()

        win_login()



def win_Signup():

    try:

        layout = [[sg.Text('Enter Email : ', font='8514oem 8'), sg.InputText(key='in1', do_not_clear=False)],

                  [sg.Text('Enter Username : ', font='8514oem 8'), sg.InputText(key='in2', do_not_clear=False)],

                  [sg.Text('Create Password : ', font='8514oem 8'), sg.InputText(key='in3', do_not_clear=False)],

                  [sg.Text('Re-enter Password : ', font='8514oem 8'), sg.InputText(key='in4', do_not_clear=False)],

                  [sg.Text(' ')],

                  [sg.Button(' Sign Up ', font='8514oem 8')]]



        window = sg.Window('Sign Up', layout, margins=(30, 50))



        event, values = window.Read()

        if event == ' Sign Up ':

            global email

            email = str(values['in1'])

            uname = str(values['in2'])

            email = email.lower()

            passwd = str(values['in3'])

            rpasswd = str(values['in4'])

            print(passwd)
            print(rpasswd)

            if not passwd or not email:

                sg.Popup('Please fill up all required details')

                window.close()

                win_Signup()

            elif (email.isspace() == True) or (passwd.isspace() == True):

                sg.Popup('Space is not valid')

                window.close()

                win_Signup()

            elif email.endswith('@gmail.com') == False:

                sg.Popup('Invalid Email!')

                window.close()

                win_Signup()

            elif (len(passwd) < 8):

                sg.Popup('Password length must be of minimum 8 characters')

                window.close()

                win_Signup()

            elif (passwd == rpasswd):

                # last_step(True, email, passd)
                print('before lv')
                lv = last_value()
                print(lv)
                lv+=1
                z = 0
                print('before query')
                query = ("insert into users values(%s,'%s','%s',%s,%s,%s,'%s')" % (lv, uname, passwd, z, z, z, email))

                cur.execute(query)

                con.commit()
                print('query committed')
            else:

                win_Error()

                window.close()

                win_Signup()

        elif event == sg.WIN_CLOSED:

            window.close()

            i = False

            return i

        else:

            window.close()

            win_Signup()

    except Exception as err:

        window.close()

def win_Error():

    text = 'Password is not Matching! Please retry!'

    sg.Popup(text)

def win_Invalid_Input():

    text = 'Incorrect Password or Email'

    sg.Popup(text)


def win_successful_signup():

    text = 'Signed Up Successfully'

    sg.Popup(text)

def win_UserAvailable():

    text = "Can't Sign Up Again. User Already Existed"

    sg.Popup(text)


def last_value():

    query = "SELECT userid FROM users ORDER BY USERID DESC LIMIT 1;"

    cur.execute(query)
    a = cur.fetchone()
    a = a[0]

    return a

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':

        break

    print(event)

    if event == '  Log In  ':

        win_login(window)

    if event == '  Sign Up  ':

        win_Signup()


def bg_main_music():
    song = 'kaihmpgmusic.mp3'
    mixer.init()
    mixer.music.load(song)
    mixer.music.play(10)
    mixer.music.set_volume(0.5)

def win_homepage():
        layout = [[sg.Text('Kai', font='8514oem 50 bold', pad=(50, 10))],
                  [sg.Text('Welcome User', font='8514oem 20', pad=(30, 10))],
                  [sg.Button('Play!!', font='8514oem 12', pad=(20, 10))],
                  [sg.Button('How to play?', font='8514oem 12', pad=(20, 10))],
                  [sg.Button('Leaderboard', font='8514oem 12', pad=(20, 10))],
                  [sg.Button('Credits', font='8514oem 12', pad=(20, 10))],
                  [sg.Button('Log Out', font='8514oem 12', pad=(20, 10))],
                  [sg.Text('© 2022 kai. All rights reserved.', font='8514oem 10', pad=(50, 10))]
                  ]
        window = sg.Window('Kai', layout, resizable=True, element_justification='c')
        bg_main_music()

        def win_howtoplay(og_win=window):
            og_win.close()
            layout = [[sg.Text('                                      How to play?', font='8514oem 20 bold',
                               pad=(30, 10), justification="center")],
                      [sg.Text(
                          '1. Cap\'n Kai needs your help! They need you to protect their food(fishies) from the stingy seagulls.',
                          font='8514oem 12 ')],
                      [sg.Text(
                          'Your only weapon is aÖ beach ball!', font='8514oem 12')],
                      [sg.Text(
                          '2. The objective of the game is to hit the seagulls who are here to steal Capín Kaiís fishies!',
                          font='8514oem 12')],
                      [sg.Text(
                          '3. To move the seal, press D to move right, A to move left.', font='8514oem 12')],
                      [sg.Text(
                          '4. The game has two modes ñ Classic and Arcade.', font='8514oem 12')],
                      [sg.Text(
                          '5. In the classic mode you have 3 lives to survive', font='8514oem 12')],
                      [sg.Text(
                          '6. In the arcade mode, there are no lives and the difficulty is set at random',
                          font='8514oem 12')],
                      [sg.Text('                                    Go help Cap\'n Kai now!!', font='8514oem 12 bold',
                               justification="center")],
                      [sg.Button('Back to Home', font='8514oem 12', pad=(20, 10))]
                      ]
            window = sg.Window('How to play?', layout, resizable=True)

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                print(event)
                if event == 'Back to Home':
                    window.close()
                    win_homepage()

        def win_main_play(og_win=window):
            og_win.close()
            song2 = 'aesthetic music full.mp3'
            mixer.init()
            mixer.music.load(song2)
            mixer.music.play()
            mixer.music.set_volume(0.5)

            layout = [[sg.Text('Choose a mode', font='8514oem 15 bold', pad=(50, 10))],
                      [sg.Button('Classic', font='8514oem 12 bold', pad=(20, 10))],
                      [sg.Button('Arcade', font='8514oem 12 bold', pad=(20, 10))],
                      [sg.Button('Back to Home', font='8514oem 12 bold', pad=(20, 10))]]

            window = sg.Window('game modes', layout, resizable=True, element_justification='c')

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                print(event)
                if event == 'Classic':
                    window.close()
                    classic_mode(window)
                if event == 'Arcade':
                    window.close()
                    arcade_mode(window)
                if event == 'Back to Home':
                    window.close()
                    mixer.music.stop()
                    bg_main_music()
                    win_homepage()

        def win_Score(window, ball):
            og_win = window
            ball_score = ball.score
            layout = [[sg.Text('Well Done: ', font='8514oem 16 bold', pad=(30, 10))],  # <after colon put username>
                      [sg.Text('You scored %s' % (ball_score), font='8514oem 15 bold', pad=(30, 10))],
                      [sg.Button('Back to levels', font='8514oem 12 bold', pad=(20, 10))]
                      ]

            window = sg.Window('Game Over!', layout, resizable=True, element_justification='c')
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                print(event)
                if event == 'Back to levels':
                    win_main_play(window)

        def classic_mode(window):
            og_win = window

            layout = [[sg.Text('Levels', font='8514oem 15 bold', pad=(50, 10))],
                      [sg.Button('level 1', font='8514oem 12 bold', pad=(20, 10))],
                      [sg.Button('level 2', font='8514oem 12 bold', pad=(20, 10))],
                      [sg.Button('level 3', font='8514oem 12 bold', pad=(20, 10))],
                      [sg.Button('level 4', font='8514oem 12 bold', pad=(20, 10))],
                      [sg.Button('game modes', font='8514oem 12', pad=(20, 10))]]

            window = sg.Window('Classic Mode', layout, resizable=True, element_justification='c')

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                print(event)
                if event == 'level 1':
                    window.close()
                    mixer.music.stop()
                    mixer.music.stop()
                    song2 = 'aesthetic music full.mp3'
                    level_1(window)
                    # win_Score(window)

                if event == 'level 2':
                    window.close()
                    mixer.music.stop()
                    level_2(window)

                if event == 'level 3':
                    window.close()
                    mixer.music.stop()
                    level_3(window)

                if event == 'level 4':
                    window.close()
                    mixer.music.stop()
                    level_4(window)

                if event == 'game modes':
                    window.close()
                    win_main_play(window)

        def level_1(window):
            og_win = window
            import random
            import math
            import pygame
            bg_main_music()

            WIDTH, HEIGHT = 956, 546

            DEFAULT_IMAGE_SIZE = (100, 100)

            NUM_OF_GULLS = 3

            IMGS = [

                pygame.transform.rotate(pygame.transform.scale(pygame.image.load('seal.png'), DEFAULT_IMAGE_SIZE), 45),

                pygame.transform.scale(pygame.image.load('seagull.png'), DEFAULT_IMAGE_SIZE),

                pygame.transform.scale(pygame.image.load('beach-ball.png'), (50, 50))

            ]

            BG_IMG = pygame.image.load('kai-bg2.png')

            BALL_WIDTH = IMGS[2].get_width()

            BALL_HEIGHT = IMGS[2].get_height()

            win = pygame.display.set_mode((WIDTH, HEIGHT))

            pygame.display.set_caption("Kai")

            def blit_rotate_center(win, image, top_left, angle):

                rotated_image = pygame.transform.rotate(image, angle)

                new_rect = rotated_image.get_rect(

                    center=image.get_rect(topleft=top_left).center)

                win.blit(rotated_image, new_rect.topleft)

            FPS = 120

            PADDLE_HEIGHT = 40

            PADDLE_WIDTH = 10

            MAX_VEL = 50

            class AbstractSeal:

                def __init__(self, max_vel, rotation_vel):

                    self.img = self.IMG

                    self.max_vel = max_vel

                    self.vel = 0

                    self.angle = 0

                    self.rotation_vel = rotation_vel

                    self.x, self.y = self.START_POS

                    self.acceleration = 40

                    self.width = IMGS[0].get_width()

                    self.height = IMGS[0].get_height()

                    self.mask = pygame.mask.from_surface(self.img)

                def rotate(self, left=False, right=False):

                    if left:

                        self.angle += self.rotation_vel

                    elif right:

                        self.angle -= self.rotation_vel

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                def move_left(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.move()

                def move_right(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.x -= self.vel

                def move(self):

                    self.x += self.vel

                    self.collide_edge()

                def collide_edge(self):

                    if self.x <= 0:
                        self.x = IMGS[0].get_width() + WIDTH

                    if self.x + IMGS[0].get_width() >= WIDTH:
                        self.x = 0

            class PlayerSeal(AbstractSeal):

                IMG = IMGS[0]

                START_POS = (WIDTH / 2 - 50, HEIGHT - 150)

            class Gull():

                def __init__(self):
                    self.img = IMGS[1]

                    self.num = NUM_OF_GULLS

                    # self.x = random.randrange(self.img.get_width(), WIDTH-self.img.get_width())

                    self.rect = self.img.get_rect()

                    self.y = random.randrange(self.img.get_height(), HEIGHT - 400)

                    self.x = 0

                    self.mask = pygame.mask.from_surface(self.img)

                def draw(self, win):
                    win.blit(self.img, (self.x, self.y))

            class Ball:

                VEL = 5

                def __init__(self):

                    self.img = IMGS[2]

                    self.x, self.y = WIDTH / 2, HEIGHT / 2

                    self.angle = 0

                    self.x_vel = 0

                    self.y_vel = -5

                    self.mask = pygame.mask.from_surface(self.img)

                    self.score = 0

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                    self.x += self.x_vel

                    self.y += self.y_vel

                    if self.x <= 0 or self.x >= WIDTH - self.img.get_width():
                        self.x -= self.x_vel

                    if self.y <= 0 or self.y >= HEIGHT - self.img.get_height():
                        self.y -= self.y_vel

                def set_vel(self, x_vel, y_vel):

                    self.x_vel = x_vel

                    self.y_vel = y_vel

            def gull_generator(gulls=[]):

                d = [(159, 318), (318, 477), (477, 636)]

                for i, j in d:
                    gull = Gull()

                    gull.x = random.randrange(i, j)

                    gulls.append(gull)

                return gulls

            def ball_collision(ball):

                if ball.x - BALL_WIDTH <= 0 or ball.x + BALL_WIDTH >= WIDTH:
                    ball.set_vel(ball.x_vel * -1, ball.y_vel)

                if ball.y - BALL_HEIGHT / 2 <= 0 or ball.y + BALL_HEIGHT >= HEIGHT:
                    ball.set_vel(ball.x_vel, ball.y_vel * -1)

            def ball_seal_collision(ball, seal):

                if not (ball.x <= seal.x + seal.width and ball.x >= seal.x):
                    return

                if not (ball.y + BALL_WIDTH >= seal.y):
                    return

                seal_center = seal.x + seal.width / 2

                distance_to_center = ball.x - seal_center

                percent_width = distance_to_center / seal.width

                angle = percent_width * 90

                angle_radians = math.radians(angle)

                x_vel = math.sin(angle_radians) * ball.VEL

                y_vel = math.cos(angle_radians) * ball.VEL * -1

                ball.set_vel(x_vel, y_vel)

            def ball_gull_collision(ball, gulls, x=0, y=0):

                gull_masks = {}

                ball_mask = ball.mask

                score_checker = False

                for i in gulls:
                    gull_masks[i] = pygame.mask.from_surface(i.img)

                for k in gull_masks:

                    offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                    if ball_mask.overlap(gull_masks[k], offset) is not None:

                        k.x = 10000

                        ball.score += 100

                    else:

                        pass

                # for i in gulls:

                #     gull_masks.append(i.mask)a

                # for k in gull_masks:

                #     offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                #     if ball_mask.overlap(k.mask, offset) != None:

                #         k.img.fill((0,0,0,0))

                #     else:

                #         pass

            def draw(win, player_seal, gulls, ball, score):

                player_seal.draw(win)

                for i in gulls:
                    i.draw(win)

                ball.draw(win)

                pygame.display.update()

            def main():

                clock = pygame.time.Clock()

                player_seal = PlayerSeal(4, 4)

                ball = Ball()

                gulls = gull_generator()

                score = str(ball.score)

                run = True

                while run:

                    win.blit(BG_IMG, (0, 0))

                    clock.tick(FPS)

                    draw(win, player_seal, gulls, ball, score)

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            run = False

                            break

                    keys = pygame.key.get_pressed()

                    moved = False

                    if keys[pygame.K_d]:
                        moved = True

                        player_seal.move_left()

                    if keys[pygame.K_a]:
                        moved = True

                        player_seal.move_right()

                    ball_collision(ball)

                    ball_seal_collision(ball, player_seal)

                    ball_gull_collision(ball, gulls)

                    print(ball.score)

                    if math.ceil(ball.y) in [488, 489, 490, 491, 492, 493, 494, 495]:
                        pygame.time.wait(1000)
                        pygame.quit()
                        quit()
                        win_Score(window, ball)

                    draw(win, player_seal, gulls, ball, score)

                pygame.quit()

                quit()

            if __name__ == "__main__":
                main()

        def level_2(window):
            og_win = window
            import math

            import random

            import math

            import pygame

            bg_main_music()

            WIDTH, HEIGHT = 956, 546

            DEFAULT_IMAGE_SIZE = (100, 100)

            NUM_OF_GULLS = 5

            IMGS = [

                pygame.transform.rotate(pygame.transform.scale(pygame.image.load('seal.png'), DEFAULT_IMAGE_SIZE), 45),

                pygame.transform.scale(pygame.image.load('seagull.png'), DEFAULT_IMAGE_SIZE),

                pygame.transform.scale(pygame.image.load('beach-ball.png'), (50, 50))

            ]

            BG_IMG = pygame.image.load('kai-bg2.png')

            BALL_WIDTH = IMGS[2].get_width()

            BALL_HEIGHT = IMGS[2].get_height()

            win = pygame.display.set_mode((WIDTH, HEIGHT))

            pygame.display.set_caption("Kai")

            def blit_rotate_center(win, image, top_left, angle):

                rotated_image = pygame.transform.rotate(image, angle)

                new_rect = rotated_image.get_rect(

                    center=image.get_rect(topleft=top_left).center)

                win.blit(rotated_image, new_rect.topleft)

            FPS = 120

            PADDLE_HEIGHT = 40

            PADDLE_WIDTH = 10

            MAX_VEL = 70

            class AbstractSeal:

                def __init__(self, max_vel, rotation_vel):

                    self.img = self.IMG

                    self.max_vel = max_vel

                    self.vel = 0

                    self.angle = 0

                    self.rotation_vel = rotation_vel

                    self.x, self.y = self.START_POS

                    self.acceleration = 50

                    self.width = IMGS[0].get_width()

                    self.height = IMGS[0].get_height()

                    self.mask = pygame.mask.from_surface(self.img)

                def rotate(self, left=False, right=False):

                    if left:

                        self.angle += self.rotation_vel

                    elif right:

                        self.angle -= self.rotation_vel

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                def move_left(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.move()

                def move_right(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.x -= self.vel

                def move(self):

                    self.x += self.vel

                    self.collide_edge()

                def collide_edge(self):

                    if self.x <= 0:
                        self.x = IMGS[0].get_width() + WIDTH

                    if self.x + IMGS[0].get_width() >= WIDTH:
                        self.x = 0

            class PlayerSeal(AbstractSeal):

                IMG = IMGS[0]

                START_POS = (WIDTH / 2 - 50, HEIGHT - 150)

            class Gull():

                def __init__(self):
                    self.img = IMGS[1]

                    self.num = NUM_OF_GULLS

                    # self.x = random.randrange(self.img.get_width(), WIDTH-self.img.get_width())

                    self.rect = self.img.get_rect()

                    self.y = random.randrange(self.img.get_height(), HEIGHT - 400)

                    self.x = 0

                    self.mask = pygame.mask.from_surface(self.img)

                def draw(self, win):
                    win.blit(self.img, (self.x, self.y))

            class Ball:

                VEL = 5

                def __init__(self):

                    self.img = IMGS[2]

                    self.x, self.y = WIDTH / 2, HEIGHT / 2

                    self.angle = 0

                    self.x_vel = 0

                    self.y_vel = -5

                    self.mask = pygame.mask.from_surface(self.img)

                    self.score = 0

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                    self.x += self.x_vel

                    self.y += self.y_vel

                    if self.x <= 0 or self.x >= WIDTH - self.img.get_width():
                        self.x -= self.x_vel

                    if self.y <= 0 or self.y >= HEIGHT - self.img.get_height():
                        self.y -= self.y_vel

                def set_vel(self, x_vel, y_vel):

                    self.x_vel = x_vel

                    self.y_vel = y_vel

            def gull_generator(gulls=[]):

                d = [(159, 318), (318, 477), (477, 636), (636, 956)]

                for i, j in d:
                    gull = Gull()

                    gull.x = random.randrange(i, j)

                    gulls.append(gull)

                return gulls

            def ball_collision(ball):

                if ball.x - BALL_WIDTH <= 0 or ball.x + BALL_WIDTH >= WIDTH:
                    ball.set_vel(ball.x_vel * -1, ball.y_vel)

                if ball.y - BALL_HEIGHT / 2 <= 0 or ball.y + BALL_HEIGHT >= HEIGHT:
                    ball.set_vel(ball.x_vel, ball.y_vel * -1)

            def ball_seal_collision(ball, seal):

                if not (ball.x <= seal.x + seal.width and ball.x >= seal.x):
                    return

                if not (ball.y + BALL_WIDTH >= seal.y):
                    return

                seal_center = seal.x + seal.width / 2

                distance_to_center = ball.x - seal_center

                percent_width = distance_to_center / seal.width

                angle = percent_width * 90

                angle_radians = math.radians(angle)

                x_vel = math.sin(angle_radians) * ball.VEL

                y_vel = math.cos(angle_radians) * ball.VEL * -1

                ball.set_vel(x_vel, y_vel)

            def ball_gull_collision(ball, gulls, x=0, y=0):

                gull_masks = {}

                ball_mask = ball.mask

                score_checker = False

                for i in gulls:
                    gull_masks[i] = pygame.mask.from_surface(i.img)

                for k in gull_masks:

                    offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                    if ball_mask.overlap(gull_masks[k], offset) is not None:

                        k.x = 10000

                        ball.score += 100

                    else:

                        pass

                # for i in gulls:

                #     gull_masks.append(i.mask)a

                # for k in gull_masks:

                #     offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                #     if ball_mask.overlap(k.mask, offset) != None:

                #         k.img.fill((0,0,0,0))

                #     else:

                #         pass

            def draw(win, player_seal, gulls, ball, score):

                player_seal.draw(win)

                for i in gulls:
                    i.draw(win)

                ball.draw(win)

                pygame.display.update()

            def main():

                clock = pygame.time.Clock()

                player_seal = PlayerSeal(4, 4)

                ball = Ball()

                gulls = gull_generator()

                score = str(ball.score)

                run = True

                while run:

                    win.blit(BG_IMG, (0, 0))

                    clock.tick(FPS)

                    draw(win, player_seal, gulls, ball, score)

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            run = False

                            break

                    keys = pygame.key.get_pressed()

                    moved = False

                    if keys[pygame.K_d]:
                        moved = True

                        player_seal.move_left()

                    if keys[pygame.K_a]:
                        moved = True

                        player_seal.move_right()

                    ball_collision(ball)

                    ball_seal_collision(ball, player_seal)

                    ball_gull_collision(ball, gulls)

                    print(ball.score)

                    if math.ceil(ball.y) in [490, 491, 492, 493, 494]:
                        pygame.time.wait(1000)

                        pygame.quit()
                        win_Score(window, ball)
                        quit()

                    draw(win, player_seal, gulls, ball, score)

                pygame.quit()

                quit()

            if __name__ == "__main__":
                main()

        def level_3(window):
            og_win = window
            import math

            import random

            import math

            import pygame

            bg_main_music()

            WIDTH, HEIGHT = 956, 546

            DEFAULT_IMAGE_SIZE = (100, 100)

            NUM_OF_GULLS = 5

            IMGS = [

                pygame.transform.rotate(pygame.transform.scale(pygame.image.load('seal.png'), DEFAULT_IMAGE_SIZE), 45),

                pygame.transform.scale(pygame.image.load('seagull.png'), DEFAULT_IMAGE_SIZE),

                pygame.transform.scale(pygame.image.load('beach-ball.png'), (50, 50))

            ]

            BG_IMG = pygame.image.load('kai-bg2.png')

            BALL_WIDTH = IMGS[2].get_width()

            BALL_HEIGHT = IMGS[2].get_height()

            win = pygame.display.set_mode((WIDTH, HEIGHT))

            pygame.display.set_caption("Kai")

            def blit_rotate_center(win, image, top_left, angle):

                rotated_image = pygame.transform.rotate(image, angle)

                new_rect = rotated_image.get_rect(

                    center=image.get_rect(topleft=top_left).center)

                win.blit(rotated_image, new_rect.topleft)

            FPS = 120

            PADDLE_HEIGHT = 40

            PADDLE_WIDTH = 10

            MAX_VEL = 200

            class AbstractSeal:

                def __init__(self, max_vel, rotation_vel):

                    self.img = self.IMG

                    self.max_vel = max_vel

                    self.vel = 0

                    self.angle = 0

                    self.rotation_vel = rotation_vel

                    self.x, self.y = self.START_POS

                    self.acceleration = 70

                    self.width = IMGS[0].get_width()

                    self.height = IMGS[0].get_height()

                    self.mask = pygame.mask.from_surface(self.img)

                def rotate(self, left=False, right=False):

                    if left:

                        self.angle += self.rotation_vel

                    elif right:

                        self.angle -= self.rotation_vel

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                def move_left(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.move()

                def move_right(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.x -= self.vel

                def move(self):

                    self.x += self.vel

                    self.collide_edge()

                def collide_edge(self):

                    if self.x <= 0:
                        self.x = IMGS[0].get_width() + WIDTH

                    if self.x + IMGS[0].get_width() >= WIDTH:
                        self.x = 0

            class PlayerSeal(AbstractSeal):

                IMG = IMGS[0]

                START_POS = (WIDTH / 2 - 50, HEIGHT - 150)

            class Gull():

                def __init__(self):
                    self.img = IMGS[1]

                    self.num = NUM_OF_GULLS

                    # self.x = random.randrange(self.img.get_width(), WIDTH-self.img.get_width())

                    self.rect = self.img.get_rect()

                    self.y = random.randrange(self.img.get_height(), HEIGHT - 400)

                    self.x = 0

                    self.mask = pygame.mask.from_surface(self.img)

                def draw(self, win):
                    win.blit(self.img, (self.x, self.y))

            class Ball:

                VEL = 5

                def __init__(self):

                    self.img = IMGS[2]

                    self.x, self.y = WIDTH / 2, HEIGHT / 2

                    self.angle = 0

                    self.x_vel = 0

                    self.y_vel = -5

                    self.mask = pygame.mask.from_surface(self.img)

                    self.score = 0

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                    self.x += self.x_vel

                    self.y += self.y_vel

                    if self.x <= 0 or self.x >= WIDTH - self.img.get_width():
                        self.x -= self.x_vel

                    if self.y <= 0 or self.y >= HEIGHT - self.img.get_height():
                        self.y -= self.y_vel

                def set_vel(self, x_vel, y_vel):

                    self.x_vel = x_vel

                    self.y_vel = y_vel

            def gull_generator(gulls=[]):

                d = [(0, 159), (159, 318), (318, 477), (477, 636), (636, 956)]

                for i, j in d:
                    gull = Gull()

                    gull.x = random.randrange(i, j)

                    gulls.append(gull)

                return gulls

            def ball_collision(ball):

                if ball.x - BALL_WIDTH <= 0 or ball.x + BALL_WIDTH >= WIDTH:
                    ball.set_vel(ball.x_vel * -1, ball.y_vel)

                if ball.y - BALL_HEIGHT / 2 <= 0 or ball.y + BALL_HEIGHT >= HEIGHT:
                    ball.set_vel(ball.x_vel, ball.y_vel * -1)

            def ball_seal_collision(ball, seal):

                if not (ball.x <= seal.x + seal.width and ball.x >= seal.x):
                    return

                if not (ball.y + BALL_WIDTH >= seal.y):
                    return

                seal_center = seal.x + seal.width / 2

                distance_to_center = ball.x - seal_center

                percent_width = distance_to_center / seal.width

                angle = percent_width * 90

                angle_radians = math.radians(angle)

                x_vel = math.sin(angle_radians) * ball.VEL

                y_vel = math.cos(angle_radians) * ball.VEL * -1

                ball.set_vel(x_vel, y_vel)

            def ball_gull_collision(ball, gulls, x=0, y=0):

                gull_masks = {}

                ball_mask = ball.mask

                score_checker = False

                for i in gulls:
                    gull_masks[i] = pygame.mask.from_surface(i.img)

                for k in gull_masks:

                    offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                    if ball_mask.overlap(gull_masks[k], offset) is not None:

                        k.x = 10000

                        ball.score += 100

                    else:

                        pass

                # for i in gulls:

                #     gull_masks.append(i.mask)a

                # for k in gull_masks:

                #     offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                #     if ball_mask.overlap(k.mask, offset) != None:

                #         k.img.fill((0,0,0,0))

                #     else:

                #         pass

            def draw(win, player_seal, gulls, ball, score):

                player_seal.draw(win)

                for i in gulls:
                    i.draw(win)

                ball.draw(win)

                pygame.display.update()

            def main():

                clock = pygame.time.Clock()

                player_seal = PlayerSeal(4, 4)

                ball = Ball()

                gulls = gull_generator()

                score = str(ball.score)

                run = True

                while run:

                    win.blit(BG_IMG, (0, 0))

                    clock.tick(FPS)

                    draw(win, player_seal, gulls, ball, score)

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            run = False

                            break

                    keys = pygame.key.get_pressed()

                    moved = False

                    if keys[pygame.K_d]:
                        moved = True

                        player_seal.move_left()

                    if keys[pygame.K_a]:
                        moved = True

                        player_seal.move_right()

                    ball_collision(ball)

                    ball_seal_collision(ball, player_seal)

                    ball_gull_collision(ball, gulls)

                    print(ball.score)

                    if math.ceil(ball.y) in [490, 491, 492, 493, 494]:
                        pygame.time.wait(1000)

                        pygame.quit()
                        win_Score(window, ball)
                        quit()

                    draw(win, player_seal, gulls, ball, score)

                pygame.quit()

                quit()

            if __name__ == "__main__":
                main()

            # class Seal:

            #     VEL = 5

            #

            #     def __init__(self, x, y, width, height, color):

            #         self.img = None

            #         self.x = x

            #         self.y = y

            #         self.width = width

            #         self.height = height

            #         self.color = color

            #         self.vel = 0

            #         self.max_vel = MAX_VEL

            #         self.acceleration = 0.1

            #

            #     def draw(self, win):

            #         #self.img = pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

            #         self.img = pygame.transform.rotate(pygame.transform.scale(IMGS[0], DEFAULT_IMAGE_SIZE), 45)

            #         win.blit(self.img, (WIDTH/2-50, HEIGHT-200))

            #

            #     def move_forward(self):

            #         self.vel = min(self.vel + self.acceleration, self.max_vel)

            #         self.move()

            #

            #

            #     def move(self):

            #         self.x += self.vel

        def level_4(window):
            og_win = window
            import math

            import random

            import math

            import pygame

            bg_main_music()

            WIDTH, HEIGHT = 956, 546

            DEFAULT_IMAGE_SIZE = (100, 100)

            NUM_OF_GULLS = 5

            IMGS = [

                pygame.transform.rotate(pygame.transform.scale(pygame.image.load('seal.png'), DEFAULT_IMAGE_SIZE), 45),

                pygame.transform.scale(pygame.image.load('seagull.png'), DEFAULT_IMAGE_SIZE),

                pygame.transform.scale(pygame.image.load('beach-ball.png'), (50, 50))

            ]

            BG_IMG = pygame.image.load('kai-bg2.png')

            BALL_WIDTH = IMGS[2].get_width()

            BALL_HEIGHT = IMGS[2].get_height()

            win = pygame.display.set_mode((WIDTH, HEIGHT))

            pygame.display.set_caption("Kai")

            def blit_rotate_center(win, image, top_left, angle):

                rotated_image = pygame.transform.rotate(image, angle)

                new_rect = rotated_image.get_rect(

                    center=image.get_rect(topleft=top_left).center)

                win.blit(rotated_image, new_rect.topleft)

            FPS = 120

            PADDLE_HEIGHT = 40

            PADDLE_WIDTH = 10

            MAX_VEL = 200

            class AbstractSeal:

                def __init__(self, max_vel, rotation_vel):

                    self.img = self.IMG

                    self.max_vel = max_vel

                    self.vel = 0

                    self.angle = 0

                    self.rotation_vel = rotation_vel

                    self.x, self.y = self.START_POS

                    self.acceleration = 70

                    self.width = IMGS[0].get_width()

                    self.height = IMGS[0].get_height()

                    self.mask = pygame.mask.from_surface(self.img)

                def rotate(self, left=False, right=False):

                    if left:

                        self.angle += self.rotation_vel

                    elif right:

                        self.angle -= self.rotation_vel

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                def move_left(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.move()

                def move_right(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.x -= self.vel

                def move(self):

                    self.x += self.vel

                    self.collide_edge()

                def collide_edge(self):

                    if self.x <= 0:
                        self.x = IMGS[0].get_width() + WIDTH

                    if self.x + IMGS[0].get_width() >= WIDTH:
                        self.x = 0

            class PlayerSeal(AbstractSeal):

                IMG = IMGS[0]

                START_POS = (WIDTH / 2 - 50, HEIGHT - 150)

            class Gull():

                def __init__(self):
                    self.img = IMGS[1]

                    self.num = NUM_OF_GULLS

                    # self.x = random.randrange(self.img.get_width(), WIDTH-self.img.get_width())

                    self.rect = self.img.get_rect()

                    self.y = random.randrange(self.img.get_height(), HEIGHT - 400)

                    self.x = 0

                    self.mask = pygame.mask.from_surface(self.img)

                def draw(self, win):
                    win.blit(self.img, (self.x, self.y))

            class Ball:

                VEL = 5

                def __init__(self):

                    self.img = IMGS[2]

                    self.x, self.y = WIDTH / 2, HEIGHT / 2

                    self.angle = 0

                    self.x_vel = 0

                    self.y_vel = -5

                    self.mask = pygame.mask.from_surface(self.img)

                    self.score = 0

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                    self.x += self.x_vel

                    self.y += self.y_vel

                    if self.x <= 0 or self.x >= WIDTH - self.img.get_width():
                        self.x -= self.x_vel

                    if self.y <= 0 or self.y >= HEIGHT - self.img.get_height():
                        self.y -= self.y_vel

                def set_vel(self, x_vel, y_vel):

                    self.x_vel = x_vel

                    self.y_vel = y_vel

            def gull_generator(gulls=[]):

                d = [(0, 159), (159, 318), (159, 318), (318, 477), (477, 636), (477, 636), (636, 956)]

                for i, j in d:
                    gull = Gull()

                    gull.x = random.randrange(i, j)

                    gulls.append(gull)

                return gulls

            def ball_collision(ball):

                if ball.x - BALL_WIDTH <= 0 or ball.x + BALL_WIDTH >= WIDTH:
                    ball.set_vel(ball.x_vel * -1, ball.y_vel)

                if ball.y - BALL_HEIGHT / 2 <= 0 or ball.y + BALL_HEIGHT >= HEIGHT:
                    ball.set_vel(ball.x_vel, ball.y_vel * -1)

            def ball_seal_collision(ball, seal):

                if not (ball.x <= seal.x + seal.width and ball.x >= seal.x):
                    return

                if not (ball.y + BALL_WIDTH >= seal.y):
                    return

                seal_center = seal.x + seal.width / 2

                distance_to_center = ball.x - seal_center

                percent_width = distance_to_center / seal.width

                angle = percent_width * 90

                angle_radians = math.radians(angle)

                x_vel = math.sin(angle_radians) * ball.VEL

                y_vel = math.cos(angle_radians) * ball.VEL * -1

                ball.set_vel(x_vel, y_vel)

            def ball_gull_collision(ball, gulls, x=0, y=0):

                gull_masks = {}

                ball_mask = ball.mask

                for i in gulls:
                    gull_masks[i] = pygame.mask.from_surface(i.img)

                for k in gull_masks:

                    offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                    if ball_mask.overlap(gull_masks[k], offset) is not None:

                        k.x = 10000

                        ball.score += 100

                    else:

                        pass

                # for i in gulls:

                #     gull_masks.append(i.mask)a

                # for k in gull_masks:

                #     offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                #     if ball_mask.overlap(k.mask, offset) != None:

                #         k.img.fill((0,0,0,0))

                #     else:

                #         pass

            def draw(win, player_seal, gulls, ball, score):

                player_seal.draw(win)

                for i in gulls:
                    i.draw(win)

                ball.draw(win)

                pygame.display.update()

            def main():

                clock = pygame.time.Clock()

                player_seal = PlayerSeal(4, 4)

                ball = Ball()

                gulls = gull_generator()

                score = str(ball.score)

                run = True

                while run:

                    win.blit(BG_IMG, (0, 0))

                    clock.tick(FPS)

                    draw(win, player_seal, gulls, ball, score)

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            run = False

                            break

                    keys = pygame.key.get_pressed()

                    moved = False

                    if keys[pygame.K_d]:
                        moved = True

                        player_seal.move_left()

                    if keys[pygame.K_a]:
                        moved = True

                        player_seal.move_right()

                    ball_collision(ball)

                    ball_seal_collision(ball, player_seal)

                    ball_gull_collision(ball, gulls)

                    print(ball.score)

                    if math.ceil(ball.y) in [490, 491, 492, 493, 494]:
                        pygame.time.wait(1000)

                        pygame.quit()
                        win_Score(window, ball)
                        quit()

                    draw(win, player_seal, gulls, ball, score)

                pygame.quit()

                quit()

            if __name__ == "__main__":
                main()

        def arcade_mode(window):
            og_win = window
            import random

            import math

            import pygame

            bg_main_music()

            pygame.init()
            WIDTH, HEIGHT = 956, 546

            DEFAULT_IMAGE_SIZE = (100, 100)

            NUM_OF_GULLS = 5

            FONT = pygame.font.SysFont('Courier', 20, bold=True)

            IMGS = [

                pygame.transform.rotate(pygame.transform.scale(pygame.image.load('seal.png'), DEFAULT_IMAGE_SIZE), 45),

                pygame.transform.scale(pygame.image.load('seagull.png'), DEFAULT_IMAGE_SIZE),

                pygame.transform.scale(pygame.image.load('beach-ball.png'), (50, 50))

            ]

            BG_IMG = pygame.image.load('kai-bg2.png')

            BALL_WIDTH = IMGS[2].get_width()

            BALL_HEIGHT = IMGS[2].get_height()

            win = pygame.display.set_mode((WIDTH, HEIGHT))

            pygame.display.set_caption("Kai")

            def blit_rotate_center(win, image, top_left, angle):

                rotated_image = pygame.transform.rotate(image, angle)

                new_rect = rotated_image.get_rect(

                    center=image.get_rect(topleft=top_left).center)

                win.blit(rotated_image, new_rect.topleft)

            FPS = 120

            PADDLE_HEIGHT = 40

            PADDLE_WIDTH = 10

            MAX_VEL = 50

            ARCADE_TIME = 10

            class AbstractSeal:

                def __init__(self, max_vel, rotation_vel):

                    self.img = self.IMG

                    self.max_vel = max_vel

                    self.vel = 0

                    self.angle = 0

                    self.rotation_vel = rotation_vel

                    self.x, self.y = self.START_POS

                    self.acceleration = 40

                    self.width = IMGS[0].get_width()

                    self.height = IMGS[0].get_height()

                    self.mask = pygame.mask.from_surface(self.img)

                def rotate(self, left=False, right=False):

                    if left:

                        self.angle += self.rotation_vel

                    elif right:

                        self.angle -= self.rotation_vel

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                def move_left(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.move()

                def move_right(self):

                    self.vel = min(self.vel + self.acceleration, self.max_vel)

                    self.x -= self.vel

                def move(self):

                    self.x += self.vel

                    self.collide_edge()

                def collide_edge(self):

                    if self.x <= 0:
                        self.x = IMGS[0].get_width() + WIDTH

                    if self.x + IMGS[0].get_width() >= WIDTH:
                        self.x = 0

            class PlayerSeal(AbstractSeal):

                IMG = IMGS[0]

                START_POS = (WIDTH / 2 - 50, HEIGHT - 150)

            class Gull():

                def __init__(self):
                    self.img = IMGS[1]

                    self.num = NUM_OF_GULLS

                    # self.x = random.randrange(self.img.get_width(), WIDTH-self.img.get_width())

                    self.rect = self.img.get_rect()

                    self.y = random.randrange(self.img.get_height(), HEIGHT - 400)

                    self.x = 0

                    self.mask = pygame.mask.from_surface(self.img)

                def draw(self, win):
                    win.blit(self.img, (self.x, self.y))

            class Ball:

                VEL = 5

                def __init__(self):

                    self.img = IMGS[2]

                    self.x, self.y = WIDTH / 2, HEIGHT / 2

                    self.angle = 0

                    self.x_vel = 0

                    self.y_vel = -5

                    self.mask = pygame.mask.from_surface(self.img)

                    self.score = 0

                def draw(self, win):

                    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

                    self.x += self.x_vel

                    self.y += self.y_vel

                    if self.x <= 0 or self.x >= WIDTH - self.img.get_width():
                        self.x -= self.x_vel

                    if self.y <= 0 or self.y >= HEIGHT - self.img.get_height():
                        self.y -= self.y_vel

                def set_vel(self, x_vel, y_vel):

                    self.x_vel = x_vel

                    self.y_vel = y_vel

            class Timer:

                def __init__(self):
                    self.current_time = pygame.time.get_ticks()

                    self.time_left = str(ARCADE_TIME - (self.current_time - 600) // 1000)

                    self.timer_text = 'Time left: ' + self.time_left

                    self.x, self.y = WIDTH - 200, 30

                    self.angle = 0

                    self.text = FONT.render(self.timer_text, False, (0, 0, 0))

                def draw(self, win):
                    blit_rotate_center(win, self.text, (self.x, self.y), self.angle)

            def gull_generator(gulls=[]):

                d = [(0, 159), (159, 318), (159, 318), (318, 477), (477, 636), (477, 636), (636, 956)]

                for i, j in d:
                    gull = Gull()

                    gull.x = random.randrange(i, j)

                    gulls.append(gull)

                return gulls

            def ball_collision(ball):

                if ball.x - BALL_WIDTH <= 0 or ball.x + BALL_WIDTH >= WIDTH:
                    ball.set_vel(ball.x_vel * -1, ball.y_vel)

                if ball.y - BALL_HEIGHT / 2 <= 0 or ball.y + BALL_HEIGHT >= HEIGHT:
                    ball.set_vel(ball.x_vel, ball.y_vel * -1)

            def ball_seal_collision(ball, seal):

                if not (ball.x <= seal.x + seal.width and ball.x >= seal.x):
                    return

                if not (ball.y + BALL_WIDTH >= seal.y):
                    return

                seal_center = seal.x + seal.width / 2

                distance_to_center = ball.x - seal_center

                percent_width = distance_to_center / seal.width

                angle = percent_width * 90

                angle_radians = math.radians(angle)

                x_vel = math.sin(angle_radians) * ball.VEL

                y_vel = math.cos(angle_radians) * ball.VEL * -1

                ball.set_vel(x_vel, y_vel)

            def ball_gull_collision(ball, gulls, x=0, y=0):

                gull_masks = {}

                ball_mask = ball.mask

                score_checker = False

                for i in gulls:
                    gull_masks[i] = pygame.mask.from_surface(i.img)

                for k in gull_masks:

                    offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                    if ball_mask.overlap(gull_masks[k], offset) is not None:

                        k.x = 10000

                        ball.score += 100

                    else:

                        pass

                # for i in gulls:

                #     gull_masks.append(i.mask)a

                # for k in gull_masks:

                #     offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))

                #     if ball_mask.overlap(k.mask, offset) != None:

                #         k.img.fill((0,0,0,0))

                #     else:

                #         pass

            def draw(win, player_seal, gulls, ball, timer):

                player_seal.draw(win)

                for i in gulls:
                    i.draw(win)

                ball.draw(win)

                timer.draw(win)

                pygame.display.update()

            def main():

                player_seal = PlayerSeal(4, 4)

                ball = Ball()

                gulls = gull_generator()

                score = str(ball.score)

                clock = pygame.time.Clock()

                run = True

                while run:

                    win.blit(BG_IMG, (0, 0))

                    # clock.tick(FPS)

                    score_time = Timer()

                    print(score_time.current_time)

                    draw(win, player_seal, gulls, ball, score_time)

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            run = False

                            break

                        # if event.type == pygame.USEREVENT:

                        #     if event.type == tick:

                        #         ## do whatever you want when the tick happens

                        #         print('My tick happened')

                    keys = pygame.key.get_pressed()

                    moved = False

                    if keys[pygame.K_d]:
                        moved = True

                        player_seal.move_left()

                    if keys[pygame.K_a]:
                        moved = True

                        player_seal.move_right()

                    ball_collision(ball)

                    ball_seal_collision(ball, player_seal)

                    ball_gull_collision(ball, gulls)

                    if math.ceil(ball.y) in [490, 491, 492, 493, 494]:
                        pygame.time.wait(1000)

                        pygame.quit()
                        win_Score(window, ball)
                        quit()

                    draw(win, player_seal, gulls, ball, score_time)

                    if int(score_time.time_left) < 0:
                        pygame.quit()
                        win_Score(window, ball)
                pygame.quit()

                quit()

            if __name__ == "__main__":
                main()

        def win_leaderboard(og_win=window):
            og_win.close()
            import PySimpleGUI as sg
            import mysql.connector

            sg.theme('DarkTeal5')
            sqc = mysql.connector.connect(host="localhost", user="root", password="ROOT", database="kai")
            cur = sqc.cursor()

            L = []
            cur.execute('select Player_Name,score from leaderboard order by score desc')
            result = cur.fetchall()
            for item in result:
                a, b = item
                L.append([a, b])

            heading = ['         Name         ', '      Score      ']

            lbd_layout = [
                [sg.Table(values=L,
                          headings=heading,
                          max_col_width=1000,
                          # auto_size_columns=(True),
                          justification='centre',
                          num_rows=10,
                          key='-LEADERBOARD-',
                          font=('8514oem', 10),
                          row_height=35,
                          text_color='#464159'), [sg.Button('Back to Home', font='8514oem 12 bold', pad=(10, 20))]]
            ]

            window = sg.Window("kai leaderboard", lbd_layout, resizable=True, element_justification='c')

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                print(event)
                if event == 'Back to Home':
                    window.close()
                    win_homepage()

        def win_Credits(og_win=window):
            og_win.close()
            credits_layout = [[sg.Text('Credits', font='8514oem 16 bold', pad=(30, 10))],
                              [sg.Text(
                                  'All the youtube tutorials, stack overflow programs and all sites that helped us make this game possible',
                                  font='8514oem 15', pad=(30, 10))],
                              [sg.Text('Creators: Isha, Laalenthika and Tanishaa', font='8514oem 15', pad=(30, 10))],
                              [sg.Button('Back to Home', font='8514oem 12 bold', pad=(20, 10))]
                              ]

            window = sg.Window("credits", credits_layout, resizable=True, element_justification='c')

            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                print(event)
                if event == 'Back to Home':
                    window.close()
                    win_homepage()

        def win_Logout(og_win=window):
            og_win.close()
            layout = [[sg.Text('Logging out will close the game.', font='8514oem 16 bold', pad=(30, 10))],
                      [sg.Text('Are you sure you want to logout?', font='8514oem 15 bold', pad=(30, 10))],
                      [sg.Button('Yes', font='8514oem 12 bold', pad=(20, 10))],
                      [sg.Button('No', font='8514oem 12 bold', pad=(20, 10))]

                      ]

            window = sg.Window('Log Out', layout, resizable=True, element_justification='c')
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                print(event)
                if event == 'Yes':
                    login = False
                    window.close()
                    break
                elif event == 'No':
                    window.close()
                    win_homepage()

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            print(event)
            if event == 'Play!!':
                win_main_play(window)
            if event == 'How to play?':
                window.close()
                win_howtoplay(window)
            if event == 'Leaderboard':
                window.close()
                win_leaderboard(window)
            if event == 'Credits':
                win_Credits(window)
            if event == 'Log Out':
                win_Logout(window)
                break

if login == True:
    win_homepage()


