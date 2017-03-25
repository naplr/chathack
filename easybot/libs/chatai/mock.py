class MockChatAi:
    def __init__(self, botname):
        print("Mock: {}".format(botname))

    def get_intent(self, msg):
        print('get intent!: {}'.format(msg))
        return('report_taxi', 20.8)

    def get_entity(self, msg, entity_name, mock):
        print('get entity: {}'.format(entity_name))
        if mock:
            return('2345-23334', 78.9)

        if entity_name == 'location':
            return('Siam Square', 87.3)
        else:
            return None

    def create_intent(self, intent_name):
        pass

    def create_entity(self, entity_name):
        pass



    

