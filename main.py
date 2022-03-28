import sys
import os

from loadDataframes import Dataframes
import GUI

if __name__ == '__main__':
    excel_path = 'TRIAL.xlsx'
    dataframes = Dataframes(excel_path)

    # -- Define variables --
    # Number of players
    # CREC QUE ELS FINAL PLAYERS NO ELS NECESSITAREM PER QUÈ ÉS EL QUE CALCULA EL PROGRAMA I HO GUARDAREM A UN ALTRE LLOC
    qualifying_players_num, final_players_num = (8, 6)
    # Number of columns info players
    cols_num = 12
    # Row number for column names
    row_num = 2
    dataframes = Dataframes.createDataframes(dataframes, qualifying_players_num, final_players_num, cols_num, row_num)

    # Open window GUI
    GUI.selectSection_window(dataframes)
