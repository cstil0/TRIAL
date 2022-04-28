import sys
import PySimpleGUI as sg

from loadDataframes import Dataframes

def selectPlayer_window(dataframes, section_num):
    # Load players --> ho agafem del dataframe de portes per què l'altre es va ordenant i llavors els botons es canvien de lloc
    players = dataframes.puntsPortes['NOM'].values.tolist()
    # -- GUI definition --
    window_name = 'Secció' + section_num
    layout = [
        [sg.Text('Selecció de player:', font=('Calibri', 17))],
        [sg.Button(players[0], key='player0', font=('Calibri', 20), size=(15,3)), sg.Button(players[1], key='player1', font=('Calibri', 20), size=(15,3))],
        [sg.Button(players[2], key='player2', font=('Calibri', 20), size=(15,3)), sg.Button(players[3], key='player3', font=('Calibri', 20), size=(15,3))],
        [sg.Button(players[4], key='player4', font=('Calibri', 20), size=(15,3)), sg.Button(players[5], key='player5', font=('Calibri', 20), size=(15,3))]
    ]

    window = sg.Window(window_name, layout, grab_anywhere=True)
    # -- Loop & Process menu choices --

    while True:
        event, values = window.read()
        # Try/except per què quan es tanca la pestanya no és un string
        try:
            # Per no fer tants ifs
            event_clean = event[:-1]
            player = event[-1]
        except:
            pass

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event_clean == 'player':
            player_name = players[int(player)]
            Dataframes.updatePlayer(dataframes, player_name, section_num)
            points_window(dataframes, player_name, section_num)

    window.close()

def points_window(dataframes, player_name, section_num):
    # -- GUI definition --
    window_name = 'Secció ' + section_num + '- ' + player_name
    layout = [
        [sg.Text(window_name, font=('Calibri', 17))],
        [sg.Text('Porta 1: ', font=('Calibri', 20)), sg.Button('0', key='zero1', font=('Calibri', 20), size=(10,3), button_color = '#36914d'), sg.Button('10', key='ten1', font=('Calibri', 20), size=(10,3), button_color = '#e44949'), sg.Button('-', key='empty1', font=('Calibri', 20), size=(10,3), button_color = '#d1bd57')],
        [sg.Text('Porta 2: ', font=('Calibri', 20)), sg.Button('0', key='zero2', font=('Calibri', 20), size=(10,3), button_color = '#36914d'), sg.Button('10', key='ten2', font=('Calibri', 20), size=(10,3), button_color = '#e44949'), sg.Button('-', key='empty2', font=('Calibri', 20), size=(10,3), button_color = '#d1bd57')],
        [sg.Text('Porta 3: ', font=('Calibri', 20)), sg.Button('0', key='zero3', font=('Calibri', 20), size=(10,3), button_color = '#36914d'), sg.Button('10', key='ten3', font=('Calibri', 20), size=(10,3), button_color = '#e44949'), sg.Button('-', key='empty3', font=('Calibri', 20), size=(10,3), button_color = '#d1bd57')],
        [sg.Text('Porta 4: ', font=('Calibri', 20)), sg.Button('0', key='zero4', font=('Calibri', 20), size=(10,3), button_color = '#36914d'), sg.Button('10', key='ten4', font=('Calibri', 20), size=(10,3), button_color = '#e44949'), sg.Button('-', key='empty4', font=('Calibri', 20), size=(10,3), button_color = '#d1bd57')],
        [sg.Text('Porta 5: ', font=('Calibri', 20)), sg.Button('0', key='zero5', font=('Calibri', 20), size=(10,3), button_color = '#36914d'), sg.Button('10', key='ten5', font=('Calibri', 20), size=(10,3), button_color = '#e44949'), sg.Button('-', key='empty5', font=('Calibri', 20), size=(10,3), button_color = '#d1bd57')],
        [sg.Text('Porta 6: ', font=('Calibri', 20)), sg.Button('0', key='zero6', font=('Calibri', 20), size=(10,3), button_color = '#36914d'), sg.Button('10', key='ten6', font=('Calibri', 20), size=(10,3), button_color = '#e44949'), sg.Button('-', key='empty6', font=('Calibri', 20), size=(10,3), button_color = '#d1bd57')]

        #[sg.Button('Actualitzar', key = 'update', font=('Calibri', 15))]
    ]

    window = sg.Window(window_name, layout, grab_anywhere=True)
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
    trial_theme = {'BACKGROUND': '#1c272b',
                    'TEXT': '#c4e5db',
                    'INPUT': '#c4e5db',
                    'TEXT_INPUT': '#000000',
                    'SCROLL': '#c4e5db',
                    'BUTTON': ('#c4e5db', '#d3ab7b'),
                    'PROGRESS': ('#c4e5db', '#d3ab7b'),
                    'BORDER': 0,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH': 0}

    sg.theme_add_new('TrialTheme', trial_theme)

    # -- GUI definition --
    sg.theme('TrialTheme')
    layout = [
        [sg.Text('Selecció de secció:', font=('Calibri', 17))],
        [sg.Button('Secció 1', key='section1', font=('Calibri', 20), size=(10,3)), sg.Button('Secció 2', key='section2', font=('Calibri', 20), size=(10,3))],
        [sg.Button('Secció 3', key='section3', font=('Calibri', 20), size=(10,3)),sg.Button('Secció 4', key='section4', font=('Calibri', 20), size=(10,3))],
        [sg.Button('Secció 5', key='section5', font=('Calibri', 20), size=(10,3))]
    ]

    window = sg.Window('Selecció de secció', layout, grab_anywhere=True)
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
            selectPlayer_window(dataframes, section)

    window.close()