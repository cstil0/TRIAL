import os
import threading

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

from loadDataframes import Dataframes

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")
curr_player = None
curr_section = None
dataframes = None
players = None
points = []

# boolan per saber si estem dins la carpeta de punts
is_points = False

# Returns styling information for a key based on its position and state.
def get_key_style(deck, key, state):
    font = "verdana-bold.ttf"
    global is_points
    if is_points:
        # print points folder
        door_keys = (2 ,3, 4, 5, 6, 7)
        ten_keys = (10, 11, 12, 13, 14, 15)
        zero_keys = (18, 19, 20, 21, 22, 23)
        empty_keys = (26, 27, 28, 29, 30, 31)
        # Només creem els diferents diccionaris en el cas que estiguem en els punts corresponents (així no cal guardar també el color del botó)
        if key in ten_keys:
            # Creem un diccionari per no haver de fer un if per cada tecla
            stdeck_keys = {ten_keys[0]: ('110', 'P1\n+10'), ten_keys[1]: ('210', 'P2\n+10'),
                           ten_keys[2]: ('310', 'P3\n+10'),
                           ten_keys[3]: ('410', 'P4\n+10'), ten_keys[4]: ('510', 'P5\n+10'),
                           ten_keys[5]: ('610', 'P6\n+10')}

            icon = "{}.png".format("active_door") if state else "{}.png".format("green_door")
            name = stdeck_keys[key][0]
            label = stdeck_keys[key][1]

        elif key in zero_keys:
            stdeck_keys = {zero_keys[0]: ('10', 'P1\n+0'), zero_keys[1]: ('20', 'P2\n+0'), zero_keys[2]: ('30', 'P3\n+0'),
                           zero_keys[3]: ('40', 'P4\n+0'), zero_keys[4]: ('50', 'P5\n+0'), zero_keys[5]: ('60', 'P6\n+0')}

            icon = "{}.png".format("active_door") if state else "{}.png".format("red")
            name = stdeck_keys[key][0]
            label = stdeck_keys[key][1]

        elif key in empty_keys:
            stdeck_keys = {empty_keys[0]: ('1-', 'P1\n-'), empty_keys[1]: ('2-', 'P2\n-'), empty_keys[2]: ('3-', 'P3\n-'),
                           empty_keys[3]: ('4-', 'P4\n-'), empty_keys[4]: ('5-', 'P5\n-'), empty_keys[5]: ('6-', 'P6\n-')}

            icon = "{}.png".format("active_door") if state else "{}.png".format("yellow")
            name = stdeck_keys[key][0]
            label = stdeck_keys[key][1]

        elif key in door_keys:
            door_num = door_keys.index(key) + 1
            name = "empty_door{}".format(door_num)
            icon = "{}.png".format("active_door") if state else "{}.png".format("black")
            label = " "

        elif key == 0:
            name = "main_app"
            icon = "{}.png".format("up_arrow")
            label = " "

        else:
            name = "empty"
            icon = "black.png"
            label = " "

    # print main application
    else:
        if key >= 0 and key <= 4:
            name = "section"
            icon = "{}.png".format("green") if state else "{}.png".format("purple")
            label = "SEC {}".format(key + 1)

        elif key >= 8 and key <= 13:
            name = "player"
            icon = "{}.png".format("green") if state else "{}.png".format("blue")
            abreviations = list(players.keys())
            label = "{}".format(abreviations[key-8])

        elif key == 16:
            name = "points_folder"
            icon = "{}.png".format("folder_icon")
            label = " "

        else:
            name = "empty"
            icon = "black.png"
            label = " "


    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }

# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, font_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 0, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 28)
    # Si és una porta printem una mica més amunt per que quedi centrat
    # Mirem també que no sigui un string buit per què no peti
    # POTSER ES POT TROBAR UNA MANERA MÉS MACA DE FER AQUEST IF
    if label_text != '' and label_text[0] == 'P' and len(label_text) != 3:
        draw.text((image.width / 2, image.height / 2 - 3), text=label_text, font=font, anchor="ms", fill="white", align='center', stroke_width=1, stroke_fill='black')

    else:
        draw.text((image.width / 2, image.height / 2 + 10), text=label_text, font=font, anchor="ms", fill="white", align='center', stroke_width=1, stroke_fill='black')

    return PILHelper.to_native_format(deck, image)

# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.
def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)

        # Prints key state change information, updates rhe key image and performs any
        # associated actions when a key is pressed.

# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.
def key_change_callback(deck, key, state):
    # Print new key state
    print("Key {} = {}".format(key, state), flush=True)

    # Update the key image based on the new key state.
    # update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        # Primer agafem l'style de la key que s'ha activat
        key_style = get_key_style(deck, key, state)

        # Actualitzem state segons el current player o section
        for curr_key in range(deck.key_count()):
            # Comprovem si el nom de la key coincideix amb el current, i si tant el nou com l'antic son players o seccions per canviar només el que toca
            curr_key_style = get_key_style(deck, curr_key, state)
            if curr_key_style['name'] == key_style['name']:
                # Cridem les variables globals per poder-les modificar
                global curr_section, curr_player, is_points, points
                # Mirem si estem en un player i si aquest coincideix amb el current
                if curr_key_style['label'] == curr_player:
                    # Actualitzem colors
                        update_key_image(deck, curr_key, False)
                        update_key_image(deck, key, True)
                        # Actualitzem el nou current player
                        curr_player = key_style['label']

                elif curr_key_style['label'] == curr_section:
                    # Actualitzem colors
                    update_key_image(deck, curr_key, False)
                    update_key_image(deck, key, True)
                    # Actualitzem secció
                    curr_section = key_style['label']

        # Definim comportament
        style_name = key_style['name']
        style_label = key_style['label']
        if (not is_points) and style_name == "player":
            player_abr = key_style['label']
            name = players[player_abr]
            section_num = curr_section[-1]
            Dataframes.updatePlayer(dataframes, players[player_abr], section_num)

        elif (not is_points) and style_name == "section":
            section_num = key_style['label'][-1]
            Dataframes.updateSection(dataframes, section_num)

        # Comprovem si es tracta d'alguna porta
        elif is_points and style_label[0] == 'P':
            porta_num = style_name[0]
            porta_punts = style_name[1:]
            Dataframes.updateData(dataframes, porta_punts, porta_num, curr_section[-1], players[curr_player])
            # Actualitzem els punts
            porta_i = int(porta_num) - 1
            points[porta_i] = porta_punts
            render_screen(deck, porta_num, porta_punts)

        # print points screen
        elif (not is_points) and style_name == 'points_folder':
            # entrem a la carpeta de punts
            is_points = True
            # actualitzem la llista de punts per portes
            for i in range(1, 7):
                points[i-1] = dataframes.vmixRaw.loc[0, 'C_PUNTS_P' + str(i)]

            render_screen(deck)

        # print main app
        elif is_points and style_name == 'main_app':
            is_points = False
            render_screen(deck)

def render_screen(deck, curr_porta = None, curr_point = None):
    global is_points, points

    if not is_points:
        for key in range(deck.key_count()):
            key_style = get_key_style(deck, key, False)
            # Posem en verd els que coincideixen amb el current
            if key_style['label'] == curr_section or key_style['label'] == curr_player:
                update_key_image(deck, key, True)
            else:
                update_key_image(deck, key, False)

    elif curr_porta and curr_point:
        porta_i = int(curr_porta) - 1
        curr_porta = int(curr_porta)
        # sumem 10 perquè cada fila té 8 keys i comencem a la 2
        key_ten = curr_porta + 8 + 1
        key_zero = curr_porta + 8 * 2 + 1
        key_door = curr_porta + 1

        # si son 10 punts, activem key 10 i la de dalt i desactivem 0
        if curr_point == '10':
            # activem 10
            update_key_image(deck, key_ten, True)
            # desactivem 0
            update_key_image(deck, key_zero, False)
            # activem porta
            update_key_image(deck, key_door, True)

        elif curr_point == '0':
            # activem 0
            update_key_image(deck, key_zero, True)
            # desactivem 10
            update_key_image(deck, key_ten, False)
            # activem porta
            update_key_image(deck, key_door, True)
        else:
            # desactivem 0
            update_key_image(deck, key_zero, False)
            # desactivem 10
            update_key_image(deck, key_ten, False)
            # desactivem porta
            update_key_image(deck, key_door, False)

        """
        for key in range(deck.key_count()):
            key_style = get_key_style(deck, key, False)
            # si la key pertany a la current porta
            if key_style['label'][:2] == 'P' + curr_porta:
                key_point = key_style['name'][1:]
                if curr_point != '-':
                    # Si els punts de la tecla son els mateixos que el current -- activem
                    if key_point == curr_point:
                        update_key_image(deck, key, True)
                    # una altra tecla de la porta -- desactivem
                    else:
                        update_key_image(deck, key, False)

                else:
                    if curr_point == points[porta_i]:
                        update_key_image(deck, key, False)

            # Activem també els botons generals
            elif key_style['name'][-1] == curr_porta:
                if curr_point == '-':
                    update_key_image(deck, key, False)
                else:
                    update_key_image(deck, key, True)
                    """

    # si estem a l'estat inicial dels punts, volem llegir el que hi ha guardat per printar-ho com toca
    else:
        # primer netejem tota la pantalla
        for key in range(deck.key_count()):
            key_style = get_key_style(deck, key, False)
            update_key_image(deck, key, False)

        # Recorrem els punts i pintem de color groc els que coincideixin
        # comencem a la porta 3 per què correspon a la key 3 de la streamdeck
        key_count = 2
        for point in points:
            # si el punt és diferent de empty printem de groc
            if point != '-':
                key = key_count
                update_key_image(deck, key, True)
                # comprovem quin punt és per posar-li també el color groc
                if point == 0:
                    # cada fila té 8 keys
                    key = key_count + 8*2
                    update_key_image(deck, key, True)

                elif point == 10:
                    key = key_count + 8
                    update_key_image(deck, key, True)

            key_count += 1



# Per trobar la key del diccionari donat el valor
def get_key(val):
    for key, value in players.items():
        if val == value:
            return key
    return

def initiate_streamdeck(data):
    # Creem variables globals per què no podem passar-ho per paràmetre al key_change_callback
    global dataframes, players, curr_player, curr_section, points
    dataframes = data
    abreviations = dataframes.puntsPortes['ABR'].values.tolist()
    names = dataframes.puntsPortes['NOM'].values.tolist()
    # Convertim a diccionari per poder agafar tant els noms (passar per paràmetre a dataframes) com les abreviacions (streamdeck) segons us
    players = dict(zip(abreviations, names))

    # Agafem el player que hi ha guardat com a current
    curr_player_name = dataframes.vmixRaw.loc[0, 'C_PLAYER']
    # Trobem l'abreviació del current player -- és més fàcil treballar amb el que es mostra i canviar-ho al que toca quan enviem a dataframes
    curr_player = get_key(curr_player_name)
    # Agafem la secció tal com està guardada
    curr_section_name = dataframes.vmixRaw.loc[0, 'C_SECTION']
    curr_section = 'SEC {}'.format(curr_section_name[-1])

    # agafem la llista de punts per portes
    for i in range(1, 7):
        points.append(dataframes.vmixRaw.loc[0, 'C_PUNTS_P' + str(i)])

    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        if index == 0:
            # Afafem només la primera streamdeck
            deck.open()

    deck.reset()

    print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))

    # Set initial screen brightness to 100%.
    deck.set_brightness(100)

    # Set initial key images.
    render_screen(deck)

    # Register callback function for when a key state changes.
    deck.set_key_callback(key_change_callback)

    # Wait until all application threads have terminated (for this example,
    # this is when all deck handles are closed).
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            pass