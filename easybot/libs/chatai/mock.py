class MockChatAi:
    def __init__(self, botname):
        print("Mock: {}".format(botname))

    def get_intent(self, msg):
        print('get intent!: {}'.format(msg))

    def get_entity(self, msg, entity_type):
        pass

    def create_intent(self, intent_name):
        pass

    def create_entity(self, entity_name):
        pass



    

