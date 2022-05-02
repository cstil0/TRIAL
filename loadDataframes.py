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

        self.firstRow_finalPlayers = 0

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

    def create_finalPlayers(self, col_names, cols_num, row_num):
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
        # S'ha de mirar els punts que hi ha a la secció i repartir-los per les portes,
        # per què si s'ha carregat una secció no buida, com que les portes no tenen punts es reseteja -- apaño

        # Creem un nou dataframe a partir dels noms dels jugadors i anem afegint les portes per secció
        data = [self.finalPlayers['SORTIDA'], self.finalPlayers['NOM'], self.finalPlayers['ABR']]
        headers = ['SORTIDA', 'NOM', 'ABR']
        self.puntsPortes = pd.concat(data, axis=1, keys=headers)

        # Recorrem cada secció i mirem quants punts té
        for player_i in range (6):
            for section in range (1, 6):
                section_points = self.finalPlayers.iloc[player_i]['SECCIÓ ' + str(section)]
                num_points = section_points/10
                # Ho emplenem segons els punts que hi ha
                fill = '0'
                for porta in range (1,7):
                    # Si estem dins el numero de punts, posem +10, sino espai buit
                    if (porta <= num_points):
                        fill = 10
                    else:
                        fill = '-'
                    # Recorrem el dataframe per seccions i portes respectivament i ho omplim tot
                    # Sumem la fila on comença el dataset de finalplayers per què l'index es guarda a partir de 16
                    curr_row = player_i + self.firstRow_finalPlayers + 1
                    self.puntsPortes.loc[curr_row, 'P' + str(porta) + '_S' + str(section)] = fill

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
        # Eliminem la columna que s'afegeix al principi al guardar l'excel
        if 'Unnamed: 0.1' in self.dataRaw:
            del self.dataRaw['Unnamed: 0.1']
        if 'Unnamed: 0' in self.vmixRaw:
            del self.vmixRaw['Unnamed: 0']
        if 'Unnamed: 0.1' in self.trialRaw:
            del self.trialRaw['Unnamed: 0.1']
        if 'Unnamed: 0.1' in self.playerRaw:
            del self.playerRaw['Unnamed: 0.1']

        col_names_qual = self.getColNames(cols_num, row_num)

        self.create_qualifyingPlayers(col_names_qual, cols_num, row_num, qualifying_players_num)
        # Sumem set al número de columnes per què ara volem agafar també els possibles punts (0-60)
        self.firstRow_finalPlayers = 2*row_num + qualifying_players_num + 3
        col_names_final = self.getColNames(cols_num + 7, self.firstRow_finalPlayers)
        self.create_finalPlayers(col_names_final, cols_num + 7, self.firstRow_finalPlayers)
        print(self.finalPlayers)

        self.create_PuntsPortes()

        # Això realment no és necessari ja que ho guarda l'excel original al lloc que toca
        # Per tant no s'exporta cada cop que es fa un save però ho guardo per si de cas
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
        # Resetejem index per què comenci a 0 a la columna row_num que és la que guarda aquest nou index
        self.finalPlayers['row_num'] = self.finalPlayers.reset_index().index
        print(self.finalPlayers)

    def saveExcel(self):
        path_export = 'TRIAL_VMIX.xlsx'
        with pd.ExcelWriter(path_export) as writer:
            self.vmixRaw.to_excel(writer, sheet_name='VMIX')
            self.dataRaw.to_excel(writer, sheet_name='DADES')
            self.trialRaw.to_excel(writer, sheet_name='TRIAL')
            self.playerRaw.to_excel(writer, sheet_name='PLAYER1')

    def exportVMIXDataframe(self, section_num, player_name):
        # Agafem l'index del player sabent que estan ordenats al row_num (ho necessitem per saber exactament la posició del player i saber on guardar-lo al excel final)
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

            # Recorrem els punts de cada secció
            for section in range(1, 6):
                self.vmixRaw.loc[0, 'F_S' + str(section) + '_' + str(player_i)] = row['SECCIÓ ' + str(section)]
                self.vmixRaw.loc[0, str(player_i) + '_PUNTS_SECCIO'] = row['SECCIÓ ' + str(section_num)]

            player_i+=1

        # Recorrem les portes del player sol ja que només es mostra per un
        player_i = self.puntsPortes.index[self.puntsPortes['NOM'] == player_name].tolist()[0]
        for porta in range(1, 7):
            self.vmixRaw.loc[0, 'C_PUNTS_P' + str(porta)] = self.puntsPortes.loc[player_i, 'P' + str(porta) + '_S' + str(section_num)]
        print(self.puntsPortes)

    def exportTRIALDataframe(self):
        player_i = 1
        curr_row = self.firstRow_finalPlayers + 1
        for index, row in self.finalPlayers.iterrows():
            self.trialRaw.loc[curr_row, 'Unnamed: 0'] = row['SORTIDA']
            self.trialRaw.loc[curr_row, 'Unnamed: 1'] = row['NUMERO']
            self.trialRaw.loc[curr_row, 'Unnamed: 2'] = row['NOM']
            self.trialRaw.loc[curr_row, 'Unnamed: 3'] = row['ABR']
            self.trialRaw.loc[curr_row, 'Unnamed: 4'] = row['PAIS']
            self.trialRaw.loc[curr_row, 'Unnamed: 5'] = row['BANDERA']
            self.trialRaw.loc[curr_row, 'Unnamed: 6'] = row['SECCIÓ 1']
            self.trialRaw.loc[curr_row, 'Unnamed: 7'] = row['SECCIÓ 2']
            self.trialRaw.loc[curr_row, 'Unnamed: 8'] = row['SECCIÓ 3']
            self.trialRaw.loc[curr_row, 'Unnamed: 9'] = row['SECCIÓ 4']
            self.trialRaw.loc[curr_row, 'Unnamed: 10'] = row['SECCIÓ 5']
            self.trialRaw.loc[curr_row, 'Unnamed: 11'] = row['TOTAL']
            self.trialRaw.loc[curr_row, 'Unnamed: 12'] = row[60.0]
            self.trialRaw.loc[curr_row, 'Unnamed: 13'] = row[50]
            self.trialRaw.loc[curr_row, 'Unnamed: 14'] = row[40.0]
            self.trialRaw.loc[curr_row, 'Unnamed: 15'] = row[30.0]
            self.trialRaw.loc[curr_row, 'Unnamed: 16'] = row[20.0]
            self.trialRaw.loc[curr_row, 'Unnamed: 17'] = row[10.0]
            self.trialRaw.loc[curr_row, 'Unnamed: 18'] = row[0.0]

            curr_row += 1

    def exportDataframe(self, section_num, player_name):
        # Actualitzem tant l'excel que llegeix l'VMIX com "llegible"
        self.exportVMIXDataframe(section_num, player_name)
        self.exportTRIALDataframe()

    # -- Update selections --
    def updateSection(self, section_num, player_name=None):
        # Actualitzem només la cel·la que es mostra amb la info del player
        self.vmixRaw.loc[0, 'SECCIO'] = 'SECTION ' + str(section_num)
        self.saveExcel()

    def updatePlayer(self, player_name, section_num):
        # Agafem index player
        row_index = self.finalPlayers.index[self.finalPlayers['NOM'] == player_name].tolist()[0]

        # Update
        self.vmixRaw.loc[0, 'C_PAIS'] = self.finalPlayers.loc[row_index]['PAIS']
        self.vmixRaw.loc[0, 'C_PLAYER'] = player_name
        self.vmixRaw.loc[0, 'C_BANDERA'] = self.finalPlayers.loc[row_index]['BANDERA']

        # Recorrem les portes del player per tal que es netegi el marcador petit
        # Tornem a agafar l'index per què el punts portes no està ordenat
        row_index_porta = self.puntsPortes.index[self.puntsPortes['NOM'] == player_name].tolist()[0]
        for porta in range(1, 7):
            self.vmixRaw.loc[0, 'C_PUNTS_P' + str(porta)] = self.puntsPortes.loc[row_index_porta]['P' + str(porta) + '_S' + str(section_num)]
            print(self.vmixRaw.loc[0, 'C_PUNTS_P' + str(porta)])

        # Actualitzem també els punts de la secció que es mostren al marcador petit
        self.vmixRaw.loc[0, 'C_PUNTS_SECCIO'] = self.finalPlayers.loc[row_index]['SECCIÓ ' + str(section_num)]

        self.saveExcel()

    def updateData(self, point, porta_num, section_num, player_name):
        section_total = 0
        # Primer busquem a quina fila està el nom del player seleccionat --> estarà al [0] de la llista que retorna la funció index
        row_index = self.puntsPortes.index[self.puntsPortes['NOM'] == player_name].tolist()[0]

        # Actualitzem només els punts de la porta introduida
        # Try/except per si és '-' ja que no ho podrà convertir a int
        try:
            self.puntsPortes.loc[row_index, 'P' + porta_num + '_S' + str(section_num)] = int(point)
        except:
            self.puntsPortes.loc[row_index, 'P' + porta_num + '_S' + str(section_num)] = point

        # Recorrem totes les portes de la secció i sumem els punts
        # Així és més fàcil si es canvia de 10 a 0 per exemple i coses així
        for point_i in range (1, 7):
            curr_point = self.puntsPortes.loc[row_index, 'P' + str(point_i) + '_S' + str(section_num)]
            # Sumem només si és 10 (podria ser '-')
            if curr_point == 10:
                section_total += int(curr_point)

        # Actualitzem quants punts 60-0 s'han fet per secció

        # Mirem el total de punts anterior de la secció per saber d'on hem de restar un punt a les columnes de punts 60-0 i així sumar-lo on toqui
        # Primer busquem a quina fila està el nom del player seleccionat --> estarà al [0] de la llista que retorna la funció index (que és diferent a la de les portes per què s'ordena)
        row_index = self.finalPlayers.index[self.finalPlayers['NOM'] == player_name].tolist()[0]
        # Busquem el total que hi ha en aquella secció per aquell player
        last_total_section = self.finalPlayers.loc[row_index, 'SECCIÓ ' + section_num]
        # Total general
        last_total = self.finalPlayers.loc[row_index, 'TOTAL']

        # Necessitem saber quina diferència hi ha entre el total actual i l'anterior, i això serà el que sumarem -- crec que és més eficient que fer un for i recorre-ho tot de nou
        # Si és negatiu significa que s'han equivocat i han passat de 0 a 10 -->funciona per què com que està sumant, li resta 10 al total ja que l'added és negatiu
        added_total = section_total - last_total_section
        #curr_total_section = added_total + last_total_section

        # Ho sumem tant a la secció com al total general
        #self.finalPlayers.loc[row_index, 'SECCIÓ ' + section_num] = curr_total_section
        self.finalPlayers.loc[row_index, 'SECCIÓ ' + section_num] = section_total
        self.finalPlayers.loc[row_index, 'TOTAL'] = last_total + added_total


        # Actualitzem els totals de la classificació 60-0 -- crec que és més eficient fer-ho així que recorre-ho tot i anar comptant
        # Convertim el total a float per què així es guarda el nom de la columna
        self.finalPlayers.loc[row_index, float(section_total)] = self.finalPlayers.loc[row_index, section_total] + 1
        self.finalPlayers.loc[row_index, float(last_total_section)] = self.finalPlayers.loc[row_index, last_total_section] - 1

        self.sortPlayers()
        self.exportDataframe(section_num, player_name)
        self.saveExcel()