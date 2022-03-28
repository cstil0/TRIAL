import sys

import pandas as pd
import numpy as np

class Dataframes:
    def __init__(self, path):
        self.excelPath = path

        self.vmixRaw = None
        self.dataRaw = None
        self.trialRaw = None
        self.playerRaw = None

        self.qualifyingPlayers = None
        self.finalPlayers = None
        self.startTitle = None
        self.midTitle = None
        self.finalTitle = None
        self.finalTitle2 = None
        self.hashtag = None

    # -- Create dataframes --
    def create_qualifyingPlayers(self, col_names, cols_num, row_num, qualifying_players_num):
        # Borrem tot el que hi ha abans i després del que ens interesa
        df_data_clean = self.trialRaw.drop(self.trialRaw.index[:row_num + 1])
        # Sumem 2 al numero de players per què hi ha una fila buida
        df_data_clean = df_data_clean.drop(self.trialRaw.index[row_num + qualifying_players_num + 2:])

        # Agafem les columnes necessaries
        qualifying_players_clean = []
        col_name_raw = 'Unnamed: '
        for i in range (cols_num):
            curr_col_name = col_name_raw + str(i)
            qualifying_players_clean.append(df_data_clean[curr_col_name])

        # Concatenem en un mateix dataframe
        self.qualifyingPlayers = pd.concat(qualifying_players_clean, axis=1, keys=col_names)

    def create_finalPlayers(self, col_names, cols_num, row_num, qualifying_players_num):
        # Borrem tot el que hi ha abans del que ens interesa
        df_data_clean = self.trialRaw.drop(self.trialRaw.index[:row_num + 1])
        print(df_data_clean)

        # Agafem les columnes necessaries
        final_players_clean = []
        col_name_raw = 'Unnamed: '
        for i in range (cols_num):
            curr_col_name = col_name_raw + str(i)
            final_players_clean.append(df_data_clean[curr_col_name])

        # Concatenem en un mateix dataframe
        self.finalPlayers = pd.concat(final_players_clean, axis=1, keys=col_names)

    # -- Load excel --
    def getColNames(self, cols_num, row_num):
        col_names = []
        # Iterate the columns knowing that name is at row_num
        for i in range (cols_num):
            col_names.append(self.trialRaw.iloc[row_num, i])

        return col_names

    def loadExcel(self):
        xls_file = pd.ExcelFile(self.excelPath)
        self.vmixRaw = pd.read_excel(xls_file, 'VMIX')
        self.dataRaw = pd.read_excel(xls_file, 'DADES')
        self.trialRaw = pd.read_excel(xls_file, 'TRIAL')
        self.playerRaw = pd.read_excel(xls_file, 'PLAYER1')

        print(self.trialRaw)

    def createDataframes(self, qualifying_players_num, final_players_num, cols_num, row_num):
        self.loadExcel()

        col_names_qual = self.getColNames(cols_num, row_num)

        self.create_qualifyingPlayers(col_names_qual, cols_num, row_num, qualifying_players_num)
        # Sumem set al número de columnes per què ara volem agafar també els possibles punts (0-60)
        row_num_final = 2*row_num + qualifying_players_num + 3
        col_names_final = self.getColNames(cols_num + 7, row_num_final)
        self.create_finalPlayers(col_names_final, cols_num + 7, row_num_final, qualifying_players_num)
        print(self.finalPlayers)

        # NO SÉ SI AIXÒ FA FALTA, JA QUE REALMENT JA HO GUARDA L'EXCEL ORIGINAL AL LLOC QUE TOCA
        # I TAMPOC TÉ MASSA SENTIT GUARDAR-HO CADA VEGADA A NO SER QUE PUGUI CANVIAR EN ALGUN MOMENT
        self.startTitle = self.trialRaw['Unnamed: 13'][2]
        self.midTitle = self.trialRaw['Unnamed: 13'][5]
        self.finalTitle = self.trialRaw['Unnamed: 13'][8]
        self.finalTitle2 = self.trialRaw['Unnamed: 1'][14]
        self.hashtag = self.trialRaw['Unnamed: 20'][2]

        return self

    # -- Export dataframes --
    def updateData(self, portes, peus_points, section_num, player_name):
        # Sumem els punts de l'input
        curr_total = 0
        portes_points = portes.values()
        for point in portes_points:
            if point == '10':
                curr_total += int(point)
        # Mirem el total de punts anterior per saber d'on hem de restar un punt a les columnes de punts 60-0
        # FALTARIA CONTROLAR QUAN ES CANVII DE 10 A 0 JA QUE PETARIA
        # AQUESTA LÍNEA ESTÀ AGAFANT TOTA LA COLUMNA TOTAL -- NOMÉS VOLEM EL VALOR DE LA FILA DEL PLAYER_NAME
        last_total = self.finalPlayers['TOTAL']
        curr_total += last_total

        # S'HA DE MIRAR DE TREURE EL .0 DEL NOM DE LA COLUMNA
        print(curr_total)
        print(' TOTAL: ' + str(curr_total) + '.0')
        print(self.finalPlayers[str(curr_total) + '.0'])
        #self.finalPlayers[str(curr_total) + '.0'] = self.finalPlayers[str(curr_total) + '.0'] + 1
        #self.finalPlayers[str(last_total) + '.0'] = self.finalPlayers[str(last_total) + '.0'] - 1

        self.finalPlayers['TOTAL'] = curr_total

        # FALTA ORDENAR PER NOMBRE DE PUNTS A CADA COLUMNA 60-0 O PER SORTIDA EN EL CAS QUE HI HAGI EMPAT
        print(self.finalPlayers)

    # NO SÉ SI FA FALTA, POTSER ES POT GUARDAR EN LOCAL A LA GUI
    def changePeus(self, peus_points, add_subs):
        return