import wit

ACCESS_TOKEN = 'NL4Y24EMPAVTPLCQJKRRWKOJ54AAZ4QG'


class WitChatAi:
    def __init__(self, botname):
        print("Wit: {}".format(botname))
        self.client = wit.Wit(access_token=ACCESS_TOKEN)
        self.req = lambda method, path, params, data: wit.req(self.client.logger, self.client.access_token, method, path, params, **{'data': data})

        # (self.logger, self.access_token, 'GET', '/message', params)
        # params['context'] = json.dumps(context)

    def get_intent(self, msg):
        print('get intent!: {}'.format(msg))
        params = {}
        data = {'id': 'hello'}
        resp = self.req('POST', '/entities', params, data)
        print('result: {}'.format(str(resp)))

    def get_entity(self, msg, entity_type):
        pass

    def create_intent(self, intent_name):
        pass

    def create_entity(self, entity_name):
        pass

    def add_entity_to_intent(self, entity_name, intent_name):
        pass

