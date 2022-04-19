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

# Returns styling information for a key based on its position and state.
def get_key_style(deck, key, state):
    ten_keys = (16, 24, 19, 27, 6, 7)
    zero_keys = (17, 20, 25, 28, 14, 15)
    empty_keys = (18, 21, 26, 29, 22, 23)

    # Last button in the example application is the exit button.
    exit_key_index = deck.key_count() - 1
    font = "verdana-bold.ttf"

    if key >= 0 and key <= 4:
        name = "section"
        icon = "{}.png".format("green") if state else "{}.png".format("purple")
        label = "SEC {}".format(key + 1)

    elif key >= 8 and key <= 13:
        name = "player"
        icon = "{}.png".format("green") if state else "{}.png".format("blue")
        abreviations = list(players.keys())
        label = "{}".format(abreviations[key-8])

    elif key == 5:
        name = "exit"
        icon = "{}.png".format("Exit")
        label = ""

    # Només creem els diferents diccionaris en el cas que estiguem en els punts corresponents (així no cal guardar també el color del botó
    elif key in ten_keys:
        # Creem un diccionari per no haver de fer un if per cada tecla
        stdeck_keys = {ten_keys[0]: ('110', 'P1\n+10'), ten_keys[1]: ('210', 'P2\n+10'), ten_keys[2]: ('310', 'P3\n+10'),
                       ten_keys[3]: ('410', 'P4\n+10'), ten_keys[4]: ('510', 'P5\n+10'), ten_keys[5]: ('610', 'P6\n+10')}

        icon = "{}.png".format("green_door")
        name = stdeck_keys[key][0]
        label = stdeck_keys[key][1]

    elif key in zero_keys:
        stdeck_keys = {zero_keys[0]: ('10', 'P1\n+0'), zero_keys[1]: ('20', 'P2\n+0'), zero_keys[2]: ('30', 'P3\n+0'),
                       zero_keys[3]: ('40', 'P4\n+0'), zero_keys[4]: ('50', 'P5\n+0'), zero_keys[5]: ('60', 'P6\n+0')}

        icon = "{}.png".format("red")
        name = stdeck_keys[key][0]
        label = stdeck_keys[key][1]

    elif key in empty_keys:
        stdeck_keys = {empty_keys[0]: ('110', 'P1\n+10'), empty_keys[1]: ('210', 'P2\n+10'), empty_keys[2]: ('310', 'P3\n+10'),
                       empty_keys[3]: ('410', 'P4\n+10'), empty_keys[4]: ('510', 'P5\n+10'), empty_keys[5]: ('610', 'P6\n+10')}

        icon = "{}.png".format("yellow")
        name = stdeck_keys[key][0]
        label = stdeck_keys[key][1]

    else:
        name = "empty"
        icon = "black.png"
        label = ""

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
                global curr_section, curr_player
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
        if style_name == "player":
            player_abr = key_style['label']
            name = players[player_abr]
            section_num = curr_section[-1]
            Dataframes.updatePlayer(dataframes, players[player_abr], section_num)

        elif style_name == "section":
            section_num = key_style['label'][-1]
            Dataframes.updateSection(dataframes, section_num)

        # Comprovem si es tracta d'alguna porta
        elif key_style['label'][0] == 'P':
            porta_num = style_name[0]
            porta_punts = style_name[1:]
            Dataframes.updateData(dataframes, porta_punts, porta_num, curr_section[-1], players[curr_player])

        elif style_name == "exit":
            # Use a scoped-with on the deck to ensure we're the only thread
            # using it right now.
            with deck:
                # Reset deck, clearing all button images.
                deck.reset()

                # Close deck handle, terminating internal worker threads.
                deck.close()

# Per trobar la key del diccionari donat el valor
def get_key(val):
    for key, value in players.items():
        if val == value:
            return key

    return

def initiate_streamdeck(data):
    # Creem variables globals per què no podem passar-ho per paràmetre al key_change_callback
    global dataframes, players, curr_player, curr_section
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
    curr_section_name = dataframes.vmixRaw.loc[0, 'SECCIO']
    curr_section = 'SEC {}'.format(curr_section_name[-1])

    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        deck.open()
    deck.reset()

    print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))

    # Set initial screen brightness to 100%.
    deck.set_brightness(100)

    # Set initial key images.
    for key in range(deck.key_count()):
        key_style = get_key_style(deck, key, False)
        # Posem en verd els que coincideixen amb el current
        if key_style['label'] == curr_section or key_style['label'] == curr_player:
            update_key_image(deck, key, True)
        else:
            update_key_image(deck, key, False)

    # Register callback function for when a key state changes.
    deck.set_key_callback(key_change_callback)

    # Wait until all application threads have terminated (for this example,
    # this is when all deck handles are closed).
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            pass