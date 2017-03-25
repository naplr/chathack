from .mock import MockChatAi
from .wit import WitChatAi

class ChatAi:
    def __init__(self, ainame, botname):
        if ainame == 'wit':
            self.client = WitChatAi(botname)
        elif ainame == 'hippo':
            self.client = HippoChatAi(botname)
        elif ainame == 'mock':
            self.client = MockChatAi(botname)
        else:
            raise Exception('invalid ainame')

    def get_intent(self, msg):
        '''
        return (intent_name, precision)
        '''
        return self.client.get_intent(msg)

    def get_entity(self, msg, entity_name):
        '''
        return (substring_of_entity, precision)
        '''
        return self.client.get_entity(msg, entity_name)

    def create_intent(self, intent_name):
        return self.client.create_intent(intent_name)

    def create_entity(self, entity_name):
        return self.client.create_entity(entity_name)




    

