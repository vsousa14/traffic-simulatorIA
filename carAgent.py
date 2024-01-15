from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import json

class CarAgent(Agent):
    class MessageBehaviour(OneShotBehaviour):
        async def run(self):
            # Criação de uma mensagem direcionada ao agente "trafficlight@localhost"
            msg = Message(to="trafficlight@localhost")
            
            # Definição do tipo de interação da mensagem como "inform"
            msg.set_metadata("performative", "inform")
            
            # Construção do corpo da mensagem em JSON com informações do carro
            msg.body = json.dumps({
                'direction': self.agent.direction,
                'message': 'Informação do Carro',
                'remove': self.agent.remove
            })

            # Envio da mensagem ao agente de semáforo
            await self.send(msg)

    async def setup_car(self, direction):
        # Método para configurar a direção do carro
        self.direction = direction

    async def send(self, remove):
        # Método para enviar a mensagem com informações do carro
        self.remove = remove
        b = self.MessageBehaviour()
        
        # Adição do comportamento de envio da mensagem ao agente de carro
        self.add_behaviour(b)
