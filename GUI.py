import sys
import PySimpleGUI as sg

from loadDataframes import Dataframes

def section_window(dataframes, section_num):
    # Load players
    players = dataframes.finalPlayers['NOM'].values.tolist()
    # -- GUI definition --
    window_name = 'Secció' + section_num
    layout = [
        [sg.Text('Selecció de player:', font=('Calibri', 15), text_color='White')],
        [sg.Button(players[0], key='player1', font=('Calibri', 15)), sg.Button(players[1], key='player2', font=('Calibri', 15))],
        [sg.Button(players[2], key='player3', font=('Calibri', 15)),sg.Button(players[3], key='player4', font=('Calibri', 15))],
        [sg.Button(players[4], key='player5', font=('Calibri', 15)), sg.Button(players[5], key='player6', font=('Calibri', 15))]
    ]

    window = sg.Window(window_name, layout)
    # -- Loop & Process menu choices --
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'player1':
            player_window(dataframes, players[0], section_num)
        if event == 'player2':
            player_window(dataframes, players[1], section_num)
        if event == 'player3':
            player_window(dataframes, players[2], section_num)
        if event == 'player4':
            player_window(dataframes, players[3], section_num)
        if event == 'player5':
            player_window(dataframes, players[4], section_num)
        if event == 'player6':
            player_window(dataframes, players[5], section_num)

    window.close()

def player_window(dataframes, player_name, section_num):
    # -- GUI definition --
    window_name = 'Secció ' + section_num + '- ' + player_name
    layout = [
        [sg.Text(window_name, font=('Calibri', 15), text_color='White')],
        [sg.Text('Porta 1: ', font=('Calibri', 15)), sg.Button('0', key='zero1', font=('Calibri', 15)), sg.Button('10', key='ten1', font=('Calibri', 15)), sg.Button('-', key='empty1', font=('Calibri', 15))],
        [sg.Text('Porta 2: ', font=('Calibri', 15)), sg.Button('0', key='zero2', font=('Calibri', 15)), sg.Button('10', key='ten2', font=('Calibri', 15)), sg.Button('-', key='empty2', font=('Calibri', 15))],
        [sg.Text('Porta 3: ', font=('Calibri', 15)), sg.Button('0', key='zero3', font=('Calibri', 15)), sg.Button('10', key='ten3', font=('Calibri', 15)), sg.Button('-', key='empty3', font=('Calibri', 15))],
        [sg.Text('Porta 4: ', font=('Calibri', 15)), sg.Button('0', key='zero4', font=('Calibri', 15)), sg.Button('10', key='ten4', font=('Calibri', 15)), sg.Button('-', key='empty4', font=('Calibri', 15))],
        [sg.Text('Porta 5: ', font=('Calibri', 15)), sg.Button('0', key='zero5', font=('Calibri', 15)), sg.Button('10', key='ten5', font=('Calibri', 15)), sg.Button('-', key='empty5', font=('Calibri', 15))]
        #[sg.Button('Actualitzar', key = 'update', font=('Calibri', 15))]
    ]

    window = sg.Window(window_name, layout)
    # -- Loop & Process menu choices --
    while True:
        event, values = window.read()
        # Try/except per què quan es tanca la pestanya no és un string
        try:
            # Per no fer tants ifs
            point = event[:-1]
            porta = event[-1]
        except:
            pass

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        #if event == 'update':
            #Dataframes.updateData(dataframes, values, porta, section_num, player_name)
        if point == 'zero':
            Dataframes.updateData(dataframes, '0', porta, section_num, player_name)
        if point == 'ten':
            Dataframes.updateData(dataframes, '10', porta, section_num, player_name)
        if point == 'empty':
            Dataframes.updateData(dataframes, '-', porta, section_num, player_name)

    window.close()

def selectSection_window(dataframes):
    # -- GUI definition --
    sg.theme('DarkBlue8')
    layout = [
        [sg.Text('Selecció de secció:', font=('Calibri', 15), text_color='White')],
        [sg.Button('Secció 1', key='section1', font=('Calibri', 15)), sg.Button('Secció 2', key='section2', font=('Calibri', 15))],
        [sg.Button('Secció 3', key='section3', font=('Calibri', 15)),sg.Button('Secció 4', key='section4', font=('Calibri', 15))],
        [sg.Button('Secció 5', key='section5', font=('Calibri', 15))]
    ]

    window = sg.Window('Selecció de secció', layout)
    # -- Loop & Process menu choices --
    while True:
        event, values = window.read()
        # Try/except per què quan es tanca la pestanya no és un string
        try:
            # Per no fer tants ifs
            event_clean = event[:-1]
            section = event[-1]
        except:
            pass

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event_clean == 'section':
            Dataframes.updateSection(dataframes, section)
            section_window(dataframes, section)

    window.close()