import sys
import os

from loadDataframes import Dataframes
import GUI
import streamdeckControl

if __name__ == '__main__':
    excel_path = 'TRIAL.xlsx'
    dataframes = Dataframes(excel_path)

    # -- Define variables --
    # Number of players
    qualifying_players_num, final_players_num = (8, 6)
    # Number of columns info players
    cols_num = 12
    # Row number for column names
    row_num = 2
    dataframes = Dataframes.createDataframes(dataframes, qualifying_players_num, final_players_num, cols_num, row_num)

    # Initialize streamdeck
    streamdeckControl.initiate_streamdeck(dataframes)

    # Open window GUI
    GUI.selectSection_window(dataframes)


