rutor = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
speltur = 'X'
spelet_spelas = True

def rita_bräde():
# Ritar upp bräde med innehållet i listan "rutor"
    print (' ', rutor[0], '|', rutor[1], '|', rutor[2])
    print ('-------------')
    print (' ', rutor[3], '|', rutor[4], '|', rutor[5])
    print ('-------------')
    print (' ', rutor[6], '|', rutor[7], '|', rutor[8])
 
def byta_spelare():
# Variablen "speltur" växlas mellan 'X' och 'O'
    global speltur
    if speltur == 'X':
        speltur = 'O'
    elif speltur == 'O':
        speltur = 'X'

def vinst():
# Tre for loopar som checkar alla horisontella, 
# vertikala respektive diagonala vinstmöjligheter.
# En if sats som förklarar spelet oavgjort om lediga
# rutor på spelbrädan tar slut utan vinst.
    global spelet_spelas
    for x in range (0, 7, 3):
        if rutor[x] == rutor[x + 1] == rutor[x + 2] and rutor[x] != ' ':
            spelet_spelas = False
            rita_bräde()
            print('Tre i rad!', speltur, 'vinner!')

    for x in range (0, 3):
            if rutor[x] == rutor[x + 3] == rutor[x + 6] and rutor[x] != ' ':
                spelet_spelas = False
                rita_bräde()
                print('Tre i rad!', speltur, 'vinner!')

    for x in range (2, 5, 2):
            if rutor[4 - x] == rutor[4] == rutor[4 + x] and rutor[4] != ' ':
                spelet_spelas = False
                rita_bräde()
                print('Tre i rad!', speltur, 'vinner!')

    if ' ' not in rutor and spelet_spelas:
        spelet_spelas = False
        rita_bräde()
        print('Oavgjort!')

def spel_omgång():
# Användar input kontrolleras så det är en siffra 1-9,
# samt att rutan är ledig. 
# Vald ruta byts ut mot symbol som returnerata från 
# "byta_spelare" och vinst kollas med "vinst" funktionen.
    rita_bräde()
    print('Välj en ruta. 1-9')
    while True:
        try:
            val = int(input(' '))
            break
        except:
            print("Det måste vara ett tal")
    if val < 1 or val > 9:
        print('Talet måste vara mellan 1-9')
    elif rutor[val - 1] != ' ':
        print(f'Ruta {val} är redan tagen')
    else:
        rutor[val-1] = speltur
        vinst()
        byta_spelare()

while spelet_spelas:
# While loop som loopar spelet till vinst eller lika ändrar "spelet_spelas" till false
    spel_omgång()