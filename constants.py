import pygame

# Lista para armazenar os sinais de trânsito
signals = []

# Velocidades dos diferentes tipos de veículos
speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5}

# Coordenadas iniciais dos veículos nas diferentes direções
x = {'right': [0, 0, 0], 'down': [755, 727, 697], 'left': [1400, 1400, 1400], 'up': [602, 627, 657]}
y = {'right': [348, 370, 398], 'down': [0, 0, 0], 'left': [498, 466, 436], 'up': [800, 800, 800]}

# Dicionário para armazenar informações sobre os veículos em cada direção
vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
            'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}

# Dicionário para associar números aos tipos de veículos
vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}

# Dicionário para associar números às direções
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# Coordenadas das imagens dos semáforos
signalCoods = [(790, 529, 'left'),  # direita
               (555, 245, 'right'),  # esquerda
               (790, 245, 'down'),   # cima
               (555, 529, 'up')]     # baixo

# Coordenadas da linha de paragem
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

# Espaço entre os veículos
stoppingGap = 15    # espaço ao parar
movingGap = 15       # espaço ao mover

# Inicialização do Pygame
pygame.init()

# Criação de grupos de sprites para os veículos, sinais e o relógio
simulation = pygame.sprite.Group()
group_signals = pygame.sprite.Group()
clock = pygame.time.Clock()
