import random
import time
import threading
import pygame
import sys
import asyncio
import constants
from trafficSignal import TrafficSignal
from vehicle import Vehicle, inicialize_trafficLight

def generate_car():
    # Cria um tipo de veículo aleatório
    vehicle_type = random.randint(0, 3)
    
    # Cria um número de via aleatório
    lane_number = random.randint(1, 2)
    
    # Gera um número aleatório para determinar a direção do veículo
    temp = random.randint(0, 99)
    direction_number = 0
    dist = [25, 50, 75, 100]
    
    # Determina a direção com base na distribuição
    if temp < dist[0]:
        direction_number = 0
    elif temp < dist[1]:
        direction_number = 1
    elif temp < dist[2]:
        direction_number = 2
    elif temp < dist[3]:
        direction_number = 3
    
    # Cria um veículo com os parâmetros gerados
    car = Vehicle(lane_number, constants.vehicleTypes[vehicle_type], direction_number, constants.directionNumbers[direction_number])
    
    # Executa a geração do agente do veículo de forma assíncrona
    asyncio.run(car.generate_agent())
    
    # Aguarda um curto intervalo de tempo antes de gerar outro veículo
    time.sleep(1)

def generateVehicles():
    generate = True
    while generate:
        generate_car()

def generate_traffic_light():
    # Gera sinais de trânsito para as coordenadas especificadas
    for cord in constants.signalCoods:
        TrafficSignal(cord)

# Classe principal
class Main:
    def __init__(self):
        # Tamanho da tela
        screenWidth = 1400
        screenHeight = 800
        screenSize = (screenWidth, screenHeight)

        # Carrega a imagem de fundo
        background = pygame.image.load('images/intersection.png')

        screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption("Smart Traffic Lights")

        # Inicia a thread para gerar sinais de trânsito
        thread1 = threading.Thread(name="generate_traffic_light", target=generate_traffic_light, args=(), kwargs={})
        thread1.daemon = True
        thread1.start()

        # Inicia a thread para gerar veículos
        thread2 = threading.Thread(name="generateVehicles", target=generateVehicles, args=(), kwargs={})
        thread2.daemon = True
        thread2.start()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.blit(background, (0, 0))

            # Exibe os sinais de trânsito no ecra
            for signal in constants.group_signals:
                screen.blit(signal.redSignal, [signal.x, signal.y])
                if signal.current_green:
                    screen.blit(signal.greenSignal, [signal.x, signal.y])
                else:
                    if signal.current_yellow:
                        screen.blit(signal.yellowSignal, [signal.x, signal.y])
                    else:
                        screen.blit(signal.redSignal, [signal.x, signal.y])

            # Exibe os veículos no ecra e move-os
            for vehicle in constants.simulation:
                screen.blit(vehicle.image, [vehicle.x, vehicle.y])
                vehicle.move()

            pygame.display.update()
            constants.clock.tick(30)

# Inicializa as luzes de trânsito de forma assíncrona
asyncio.run(inicialize_trafficLight())

# Cria uma instância da classe principal
Main()