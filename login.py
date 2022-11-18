import PySimpleGUI as sg
import sys, smtplib, ssl, random
import mysql.connector

#

# sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '#3b8e91',
#                                             'TEXT': '#99d98c',
#                                             'INPUT': '#339966',
#                                             'TEXT_INPUT': '#000000',
#                                             'SCROLL': '#99CC99',
#                                             'BUTTON': ('#3b8e91', '#99d98c'),
#                                             'PROGRESS': ('#D1826B', '#CC8019'),
#                                             'BORDER': 1, 'SLIDER_DEPTH': 0,
#                                             'PROGRESS_DEPTH': 0, }
sg.theme('DarkTeal5')   # Add a touch of color

# All the stuff inside your window.
layout = [ [sg.Text('  Kai  ',font='8514oem 50 bold',pad=(50,20))],
            [sg.Button('  Log In  ', button_color="#3b8e91", font='8514oem 12 bold', pad=(20,10))],
            [sg.Button('  Sign Up  ', button_color="#3b8e91", font='8514oem 12 bold', pad=(20,10))]]

# Create the Window
window = sg.Window('Kai', layout, resizable=True, element_justification='c')
# Event Loop to process "events" and get the "values" of the inputs



# window.close()
def win_login(og_win=window):
    og_win.close()
    try:
        Left_Column = [[sg.Text('Or are you a new user?', font='8514oem 8'), sg.Text(' ' * 10)],
                       [sg.Text('Then', font='8514oem 8'), sg.Button(' Sign Up ', font='8514oem 8')]]

        Right_Column = [[sg.Text(' ' * 3), sg.Button(' Forgot Password? ', font='8514oem 8')]]

        layout = [[sg.Text('Email : ', font='8514oem 8'), sg.InputText(key='in1', do_not_clear=False)],
                  [sg.Text('Password : ', font='8514oem 8'), sg.InputText(key='in2', do_not_clear=False, password_char='*')],
                  [sg.Button(' Log In ', font='8514oem 8')],
                  [sg.Text('_' * 60, font='8514oem 8')],
                  [sg.Column(Left_Column), sg.VSeperator(), sg.Column(Right_Column)]]

        window = sg.Window('Login', layout, margins=(20, 40))
        while True:
            event, values = window.Read()

            if (event == 'Log In'):
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
                        with open('datafile.py', 'r') as f:
                            dic = json.load(f)
                        gemail = list(dic.keys())[0]

                        if (email != gemail):
                            sg.Popup('Incorrect Email!!')
                            window.close()

                        elif (email == gemail):
                            passwd = str(values['in2'])
                            evalue = dic[email]
                            cr_pass = pass_decoder(evalue)


                            if (passwd.isspace() == True):
                                sg.Popup('Password cannot contain Spaces!!')
                                window.close()
                                win_login()

                            elif passwd == cr_pass:
                                window.close()
                                sg.Popup('Incorrect Password!!')
                                window.close()
                                win_login()

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
                  [sg.Text('Create Password : ', font='8514oem 8'), sg.InputText(key='in2', password_char='*', do_not_clear=False)],
                  [sg.Text('Re-enter Password : ', font='8514oem 8'), sg.InputText(key='in3', password_char='*', do_not_clear=False)],
                  [sg.Text(' ')],
                  [sg.Button(' Sign Up ', font='8514oem 8')]]

        window = sg.Window('Sign Up', layout, margins=(30, 50))

        event, values = window.Read()
        if (event == ' Sign Up '):
            global email
            email = str(values['in1'])
            email = email.lower()
            passwd = str(values['in2'])
            rpasswd = str(values['in3'])
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
                global passd
                passd = pass_encoder(passwd)
                window.close()
                last_step(True, email, passd)
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
    text = 'Password is not Matching.. Please retry!'
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

def pass_decoder(evalue):
    pss = ''
    for val in evalue:
        pss = pss + chr(val)
    return str(pss)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    print(event)
    if event == '  Log In  ':
        win_login(window)
    if event == '  Sign Up  ':
        win_Signup()

