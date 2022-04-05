import sys

import pandas as pd
import numpy as np

class Dataframes:
    def __init__(self, path):
        self.excelPath = path

        # Raw datasets
        self.vmixRaw = None
        self.dataRaw = None
        self.trialRaw = None
        self.playerRaw = None

        # Clean datasets
        self.puntsPortes = None
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

        # Resetejem index per què comenci a 0
        self.finalPlayers['row_num'] = self.finalPlayers.reset_index().index

    def create_PuntsPortes(self):
        # Creem un nou dataframe a partir dels noms dels jugadors i anem afegint les portes per secció
        data = [self.finalPlayers['SORTIDA'], self.finalPlayers['NOM'], self.finalPlayers['ABR']]
        headers = ['SORTIDA', 'NOM', 'ABR']
        self.puntsPortes = pd.concat(data, axis=1, keys=headers)

        fill = ['-','-','-','-','-', '-']
        for section in range (1, 6):
            for porta in range (1, 7):
                self.puntsPortes['P' + str(porta) + '_S' + str(section)] = fill
        print(self.puntsPortes)

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

        self.create_PuntsPortes()

        # NO SÉ SI AIXÒ FA FALTA, JA QUE REALMENT JA HO GUARDA L'EXCEL ORIGINAL AL LLOC QUE TOCA
        # I TAMPOC TÉ MASSA SENTIT GUARDAR-HO CADA VEGADA A NO SER QUE PUGUI CANVIAR EN ALGUN MOMENT
        self.startTitle = self.trialRaw['Unnamed: 13'][2]
        self.midTitle = self.trialRaw['Unnamed: 13'][5]
        self.finalTitle = self.trialRaw['Unnamed: 13'][8]
        self.finalTitle2 = self.trialRaw['Unnamed: 1'][14]
        self.hashtag = self.trialRaw['Unnamed: 20'][2]

        return self

    # -- Export dataframes --
    def sortPlayers(self):
        # Ordenem en aquest ordre en el cas que hi hagi empats
        self.finalPlayers = self.finalPlayers.sort_values(by=[60.0,50, 40.0, 30.0, 20.0, 10.0, 'SORTIDA'], ascending=[False, False, False, False, False, False, True])
        # Resetejem index per què comenci a 0, però només si no s'ha resetejat encara, ja que sinó peta
        self.finalPlayers['row_num'] = self.finalPlayers.reset_index().index
        print(self.finalPlayers)

    def saveExcel(self):
        path_export = 'TRIAL_VMIX.xlsx'
        with pd.ExcelWriter(path_export) as writer:
            self.vmixRaw.to_excel(writer, sheet_name='VMIX')
            self.dataRaw.to_excel(writer, sheet_name='DADES')
            self.trialRaw.to_excel(writer, sheet_name='TRIAL')
            self.playerRaw.to_excel(writer, sheet_name='PLAYER1')


    def exportDataframe(self, section_num, player_name):
        # Agafem l'index del player sabent que estan ordenats al row_num
        # En aquest cas ho fem així i no amb l'index per què ho necessitem per saber la cel·La a la que s'ha de guardar, i per tant utilitzem iloc que no es fixa en l'index sino en l'ordre de files
        player_i = self.finalPlayers.loc[self.finalPlayers['NOM'] == player_name, 'row_num'].iloc[0]
        # Recorrem dataframe de players i guardem primer les dades que es mostren per un sol player
        self.vmixRaw.loc[0, 'SECCIO'] = 'SECTION ' + str(section_num)
        self.vmixRaw.loc[0, 'C_BANDERA'] = self.finalPlayers.iloc[player_i]['BANDERA']
        self.vmixRaw.loc[0, 'C_PAIS'] = self.finalPlayers.iloc[player_i]['PAIS']
        self.vmixRaw.loc[0, 'C_PLAYER'] = self.finalPlayers.iloc[player_i]['NOM']
        self.vmixRaw.loc[0, 'C_PUNTS_SECCIO'] = self.finalPlayers.iloc[player_i]['SECCIÓ ' + str(section_num)]

        # El resum de resultats es mostra per tots els jugadors per tant ho recorrem tot per si ha canviat l'ordre
        # Iterem cada fila i anem guardant cada valor on toca
        player_i = 1
        for index, row in self.finalPlayers.iterrows():
            self.vmixRaw.loc[0, 'SECCIO'] = 'SECTION ' + str(section_num)

            self.vmixRaw.loc[0, 'F_ABR_' + str(player_i)] = row['ABR']
            self.vmixRaw.loc[0, 'F_BANDERA_' + str(player_i)] = row['BANDERA']
            self.vmixRaw.loc[0, 'F_PAIS_' + str(player_i)] = row['PAIS']
            self.vmixRaw.loc[0, 'F_PLAYER_' + str(player_i)] = row['NOM']
            self.vmixRaw.loc[0, 'F_PUNTS_' + str(player_i)] = row['TOTAL']

            for section in range(1, 6):
                self.vmixRaw.loc[0, 'F_S' + str(section) + '_' + str(player_i)] = row['SECCIÓ ' + str(section)]
                self.vmixRaw.loc[0, str(player_i) + '_PUNTS_SECCIO'] = row['SECCIÓ ' + str(section_num)]

            player_i+=1

        # Recorrem les portes del player sol ja que només es mostra per un
        player_i = self.puntsPortes.index[self.puntsPortes['NOM'] == player_name].tolist()[0]
        for porta in range(1, 7):
            self.vmixRaw.loc[0, 'C_PUNTS_P' + str(porta)] = self.puntsPortes.loc[player_i, 'P' + str(porta) + '_S' + str(section_num)]
        print(self.puntsPortes)

    # -- Update selections --
    def updateSection(self, section_num):
        # Actualitzem només la cel·la que es mostra amb la info del player
        self.vmixRaw.loc[0, 'SECCIO'] = 'SECTION ' + str(section_num)
        self.saveExcel()

    def updatePlayer(self, player_name):
        # Agafem index player
        row_index = self.finalPlayers.index[self.finalPlayers['NOM'] == player_name].tolist()[0]

        # Update
        self.vmixRaw.loc[0, 'C_PAIS'] = self.finalPlayers.loc[row_index]['PAIS']
        self.vmixRaw.loc[0, 'C_PLAYER'] = player_name
        self.vmixRaw.loc[0, 'C_BANDERA'] =  self.finalPlayers.loc[row_index]['BANDERA']

        self.saveExcel()

    def updateData(self, point, porta_num, section_num, player_name):
        #portes_points = portes.values()
        curr_total = 0
        # Primer busquem a quina fila està el nom del player seleccionat --> estarà al [0] de la llista que retorna la funció index
        row_index = self.puntsPortes.index[self.puntsPortes['NOM'] == player_name].tolist()[0]

        # AQUÍ HE FET UNA LIADA, SERIA MOLT MÉS SENCILL GUARDAR ELS PUNTS DE LES PORTES AL DATAFRAME I SUMAR D'ALLÀ
        # Guardem els punts de cada porta al dataframe
        #i = 1
        #for point in portes_points:
        #    if point == '0' or point == '10':
        #        # Actualitzem punts només si s'han introduit
        #        self.puntsPortes.loc[row_index, 'P' + str(i) + '_S' + str(section_num)] = int(point)
        #    i += 1

        # Actualitzem només els punts de la porta introduida
        # Try/except per si és '-' ja que no ho podrà convertir a int
        try:
            self.puntsPortes.loc[row_index, 'P' + porta_num + '_S' + str(section_num)] = int(point)
        except:
            self.puntsPortes.loc[row_index, 'P' + porta_num + '_S' + str(section_num)] = point

        # Recorrem totes les portes de la secció i sumem els punts
        # Així és més fàcil si es canvia de 10 a 0 per exemple i coses així (CREC, PER QUE S'HA DE CONTROLAR AQUEST CAS MÉS AVALL)
        for j in range (1, 7):
            curr_point = self.puntsPortes.loc[row_index, 'P' + str(j) + '_S' + str(section_num)]
            if curr_point == 10:
                curr_total += int(curr_point)

        # Mirem el total de punts anterior de la secció per saber d'on hem de restar un punt a les columnes de punts 60-0
        # FALTARIA CONTROLAR QUAN ES CANVII DE 10 A 0 JA QUE PETARIA
        # Primer busquem a quina fila està el nom del player seleccionat --> estarà al [0] de la llista que retorna la funció index (és diferent a la de les portes per què s'ordena)
        row_index = self.finalPlayers.index[self.finalPlayers['NOM'] == player_name].tolist()[0]
        # Busquem el total que hi ha en aquella secció per aquell player
        last_total_section = self.finalPlayers.loc[row_index, 'SECCIÓ ' + section_num]
        last_total = self.finalPlayers.loc[row_index, 'TOTAL']

        # Necessitem saber quina diferència hi ha entre el total actual i l'anterior, i això serà el que sumarem
        # SI FOS NEGATIU SIGNIFICARIA QUE S'HAN EQUIVOCAT I HAN PASSAT DE 10 A 0 E.G --> CREC QUE HO ARREGLA SOL PER QUÈ COM QUE ESTÀ SUMANT, LI RESTARIA EL 10 AL TOTAL JA QUE ES NEGATIU :)
        added_total = curr_total - last_total_section
        curr_total_section = added_total + last_total_section

        # Ho sumem tant a la secció com al total general
        self.finalPlayers.loc[row_index, 'SECCIÓ ' + section_num] = curr_total_section
        self.finalPlayers.loc[row_index, 'TOTAL'] = last_total + added_total

        # Convertim el total a float per què així es guarda el nom de la columna
        # MOLARIA MÉS POTSER FER-HO COMPTANT QUANTS DE CADA N'HI HA
        self.finalPlayers.loc[row_index, float(curr_total)] = self.finalPlayers.loc[row_index, curr_total] + 1
        self.finalPlayers.loc[row_index, float(last_total_section)] = self.finalPlayers.loc[row_index, last_total_section] - 1

        self.sortPlayers()
        self.exportDataframe(section_num, player_name)
        self.saveExcel()
