from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.template import Template
import json
import time

class MainAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dicionário para armazenar carros em diferentes direções
        self.cars = {
            'left': [],
            'right': [],
            'up': [],
            'down': [],
        }
        # Lista para armazenar sinais de trânsito
        self.signals = []
        # Flag para controlar bloqueio
        self.block = False

    class ReceiveBehaviour (OneShotBehaviour):
        async def run (self):
            # Recebe uma mensagem com timeout de 10 segundos
            msg = await self.receive(timeout=10)
            if msg:
                # Analisa os dados da mensagem JSON
                data = json.loads(msg.body)

                # Remove um carro ou adiciona um novo, dependendo dos dados da mensagem
                if (data['remove'] == True):
                    self.agent.cars[data['direction']].pop()
                else:
                    self.agent.cars[data['direction']].append('normal')

                # Verifica se o bloqueio está desativado e faz gerencia dos sinais
                if (self.agent.block == False):
                    self.agent.block = True
                    await self.manager_signal()
                    self.agent.block = False

        async def manager_signal (self):
            # Obtém a direção com mais carros
            max_direction = max(self.agent.cars, key=lambda direction: len(self.agent.cars[direction]))
            tmp_sg = None
            # Itera sobre os sinais de trânsito
            for signal in self.agent.signals:
                if (max_direction == signal.direction):
                    tmp_sg = signal
                else:
                    if (signal.current_green == True):
                        signal.current_yellow = True
                        signal.current_green = False
                        signal.red_turn()
                    else:
                        signal.current_yellow = False

                    signal.current_green = False
            # Ativa o sinal verde para a direção com mais carros
            tmp_sg.green_turn()

            # Calcula o tempo de espera com base no número de carros
            seconds = len(self.agent.cars[max_direction]) * 5
            if (seconds >= 10):
                seconds = 10
            time.sleep(seconds)

    async def active (self):
        self.b = self.ReceiveBehaviour()
        self.template = Template()
        self.template.set_metadata("performative", "inform")
        self.add_behaviour(self.b, self.template)