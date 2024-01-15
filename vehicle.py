import asyncio
import threading
import pygame
import spade
import constants
from carAgent import CarAgent
from mainAgent import MainAgent

trafficLightAgent = None

# Inicializar o agente de semáforo global
async def inicialize_trafficLight ():
    global trafficLightAgent
    trafficLightAgent = MainAgent("trafficlight@localhost", "password")
    await trafficLightAgent.start(auto_register=True)
    trafficLightAgent.signals = constants.group_signals

# Classe que representa um veículo no simulador
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = constants.speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = constants.x[direction][lane]
        self.y = constants.y[direction][lane]
        self.crossed = 0
        constants.vehicles[direction][lane].append(self)
        self.index = len(constants.vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)
        self.message_sended = False

        if(len(constants.vehicles[direction][lane])>1 and constants.vehicles[direction][lane][self.index-1].crossed==0):    # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
            if(direction=='right'):
                self.stop = constants.vehicles[direction][lane][self.index-1].stop - constants.vehicles[direction][lane][self.index-1].image.get_rect().width - constants.stoppingGap         # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            elif(direction=='left'):
                self.stop = constants.vehicles[direction][lane][self.index-1].stop + constants.vehicles[direction][lane][self.index-1].image.get_rect().width + constants.stoppingGap 
            elif(direction=='down'):
                self.stop = constants.vehicles[direction][lane][self.index-1].stop - constants.vehicles[direction][lane][self.index-1].image.get_rect().height - constants.stoppingGap 
            elif(direction=='up'):
                self.stop = constants.vehicles[direction][lane][self.index-1].stop + constants.vehicles[direction][lane][self.index-1].image.get_rect().height + constants.stoppingGap 
        else:
            self.stop = constants.defaultStop[direction]

        # Set new starting and stopping coordinate
        if(direction=='right'):
            temp = self.image.get_rect().width + constants.stoppingGap
            constants.x[direction][lane] -= temp
        elif(direction=='left'):
            temp = self.image.get_rect().width + constants.stoppingGap
            constants.x[direction][lane] += temp
        elif(direction=='down'):
            temp = self.image.get_rect().height + constants.stoppingGap
            constants.y[direction][lane] -= temp
        elif(direction=='up'):
            temp = self.image.get_rect().height + constants.stoppingGap
            constants.y[direction][lane] += temp

    # Método para renderizar o veículo na tela
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    # Método para movimentar o veículo
    def move(self):
        # Get current green and current yellow
        currentGreen = -1
        currentYellow = 0
        stop = True
        crossed = self.crossed
        for signal in constants.group_signals:
            if (self.direction == signal.direction):
                if (signal.current_yellow == True):
                    currentYellow = 1
                if (signal.current_green == True):
                    match self.direction:
                        case 'right':
                            currentGreen = 0
                        case 'left':
                            currentGreen = 2
                        case 'down':
                            currentGreen = 1
                        case 'up':
                            currentGreen = 3

        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.image.get_rect().width>constants.stopLines[self.direction]):   # if the image has crossed stop line now
                self.crossed = 1
            if((self.x+self.image.get_rect().width<=self.stop or self.crossed == 1 or (currentGreen==0 and currentYellow==0)) and (self.index==0 or self.x+self.image.get_rect().width<(constants.vehicles[self.direction][self.lane][self.index-1].x - constants.movingGap))):
            # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                self.x += self.speed  # move the vehicle
                stop = False
        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.image.get_rect().height>constants.stopLines[self.direction]):
                self.crossed = 1
            if((self.y+self.image.get_rect().height<=self.stop or self.crossed == 1 or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.image.get_rect().height<(constants.vehicles[self.direction][self.lane][self.index-1].y - constants.movingGap))):
                self.y += self.speed
                stop = False
        elif(self.direction=='left'):
            if(self.crossed==0 and self.x<constants.stopLines[self.direction]):
                self.crossed = 1
            if((self.x>=self.stop or self.crossed == 1 or (currentGreen==2 and currentYellow==0)) and (self.index==0 or self.x>(constants.vehicles[self.direction][self.lane][self.index-1].x + constants.vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + constants.movingGap))):
                self.x -= self.speed
                stop = False
        elif(self.direction=='up'):
            if(self.crossed==0 and self.y<constants.stopLines[self.direction]):
                self.crossed = 1
            if((self.y>=self.stop or self.crossed == 1 or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(constants.vehicles[self.direction][self.lane][self.index-1].y + constants.vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + constants.movingGap))):
                self.y -= self.speed
                stop = False

        if (stop and self.message_sended == False):
            message_thread = threading.Thread(name="inicialize_message",target=self.inicialize_message, args=(), kwargs={'remove': False})    # Generating vehicles
            message_thread.daemon = True
            message_thread.start()
            self.message_sended = True
        elif (crossed != self.crossed and self.message_sended == True):
            message_thread = threading.Thread(name="inicialize_message",target=self.inicialize_message, args=(), kwargs={'remove': True})    # Generating vehicles
            message_thread.daemon = True
            message_thread.start()

    # Método assíncrono para gerar o agente do veículo
    async def generate_agent(self):
        self.agent = CarAgent("car@localhost", "123")
        await self.agent.start(auto_register=True)
        await self.agent.setup_car(self.direction)
        constants.simulation.add(self)

    # Método para inicializar o envio de mensagens
    def inicialize_message (self, remove):
        asyncio.run(self.send_message(remove))

    # Método assíncrono para enviar uma mensagem ao agente de semáforo
    async def send_message (self, remove):
        await trafficLightAgent.active()
        await self.agent.send(remove)
        await spade.wait_until_finished(trafficLightAgent)