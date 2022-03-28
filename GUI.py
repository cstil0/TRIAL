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
    option_points = (0, 10)
    # S'HA DE PENSAR COM GUARDAR-HO BÉ..
    peus = 0
    # -- GUI definition --
    window_name = 'Secció ' + section_num + '- ' + player_name
    layout = [
        [sg.Text(window_name, font=('Calibri', 15), text_color='White')],
        [sg.Text('Porta 1: ', font=('Calibri', 15)), sg.InputOptionMenu(option_points)],
        [sg.Text('Porta 2: ', font=('Calibri', 15)), sg.InputOptionMenu(option_points)],
        [sg.Text('Porta 3: ', font=('Calibri', 15)), sg.InputOptionMenu(option_points)],
        [sg.Text('Porta 4: ', font=('Calibri', 15)), sg.InputOptionMenu(option_points)],
        [sg.Text('Porta 5: ', font=('Calibri', 15)), sg.InputOptionMenu(option_points)],
        [sg.Text('Peus: ' + str(peus), font=('Calibri', 15), key='peus_output'), sg.Button('+1', key='peus+', font=('Calibri', 15)), sg.Button('-1', key='peus-', font=('Calibri', 15))],
        [sg.Button('Actualitzar', key = 'update', font=('Calibri', 15))]
    ]

    window = sg.Window(window_name, layout)
    # -- Loop & Process menu choices --
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'peus+':
            peus += 1
            window['peus_output'].update('Peus: ' + str(peus))
            Dataframes.changePeus(dataframes, peus, '+')
        if event == 'peus-':
            peus -= 1
            window['peus_output'].update('Peus: ' + str(peus))
            Dataframes.changePeus(dataframes, peus, '-')
        if event == 'update':
            Dataframes.updateData(dataframes, values, peus, section_num, player_name)

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
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'section1':
            section_window(dataframes, '1')
        if event == 'section2':
            section_window(dataframes, '2')
        if event == 'section3':
            section_window(dataframes, '3')
        if event == 'section4':
            section_window(dataframes, '4')
        if event == 'section5':
            section_window(dataframes, '5')

    window.close()