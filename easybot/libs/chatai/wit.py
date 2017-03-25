import wit

ACCESS_TOKEN = 'NL4Y24EMPAVTPLCQJKRRWKOJ54AAZ4QG'
_params = {'v': '20160526'}

class WitChatAi:

    def __init__(self, botname):
        print("Wit: {}".format(botname))
        self.client = wit.Wit(access_token=ACCESS_TOKEN)

        self._put = lambda path, data: wit.req(
            self.client.logger, self.client.access_token, 'PUT', path, _params, json=data)
        self._post = lambda path, data: wit.req(
            self.client.logger, self.client.access_token, 'POST', path, _params, json=data)
        self._get = lambda path: wit.req(
            self.client.logger, self.client.access_token, 'GET', path, _params)

        # (self.logger, self.access_token, 'GET', '/message', params)
        # params['context'] = json.dumps(context)


    def _get_with_params(self, path, params):
        params.update(_params)
        return wit.req(self.client.logger, self.client.access_token, 'GET', path, params)


    def _get_wit_intents(self):
        return self._get('/entities/intent')


    def create_intent(self, intent_name, examples=[]):
        data = {
            'value': intent_name,
            'expression': examples
        }

        return self._post('/entities/intents/values', data)


    def create_entity(self, entity_name, values={}):
        data = {
            'id': entity_name,
            'values': values
        }

        return self._post('/entities', data)


    def get_intent(self, msg):
        params = {'q': msg}
        resp = self._get('/entities/intent')
        print(str(resp))

        # return self.client.message(msg, verbose=True)


    def get_entity(self, msg, entity_name):
        pass



        # data = {
            # 'id': 'intent',
            # 'values': [{
                # 'value': 'hello',
                # 'expressions': [
                    # 'Hi',
                    # 'Hi guys!',
                    # 'Hello',
                    # 'Hello mr.',
                    # 'hi people',
                    # 'yo'
                # ]}, {
                # 'value': 'bye',
                # 'expressions': [
                    # 'See you',
                    # 'Bye',
                    # 'Bye Bye',
                    # 'See you later',
                    # 'later',
                    # 'good luck'
                # ]}
            # ]
        # }
