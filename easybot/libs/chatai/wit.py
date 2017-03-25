from wit import Wit

ACCESS_TOKEN=''

class WitChatAi:
    def __init__(self, botname):
        print("Wit: {}".format(botname))
        self.client = Wit(access_token=ACCESS_TOKEN)

    def get_intent(self, msg):
        print('get intent!: {}'.format(msg))

    def get_entity(self, msg, entity_type):
        pass

    def create_intent(self, intent_name):
        pass

    def create_entity(self, entity_name):
        pass

    def add_entity_to_intent(self, entity_name, intent_name):
        pass
