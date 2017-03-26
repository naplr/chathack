import wit
from functools import reduce

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

        print(data)

        return self._post('/entities/intent/values', data)

    def create_entity(self, entity_name, values={}):
        data = {
            'id': entity_name,
            'values': values
        }

        return self._post('/entities', data)

    def get_intents(self, msg):
        params = {'q': msg}
        # resp = self._get('/entities/intent')
        # resp = self._get('/entities')
        resp = self.client.message(msg)
        predicted_intent_objs = resp['entities']['intent']

        intents = {}
        for i in predicted_intent_objs:
            intents[i['value']] = i['confidence']

        return intents

    def get_intent(self, msg):
        intents = self.get_intents(msg)
        key, conf = reduce(lambda m, i: [i, intents[i]] if intents[i]>m[1] else m, intents, ['', 0])
        best_intent = (key, conf)

        return best_intent

    def get_entities(self, msg, entity_name):
        resp = self.client.message(msg)
        predicted_entities = resp['entities'][entity_name]

        return map(lambda e: [e['value'], e['confidence']], predicted_entities)

    def get_entity(self, msg, entity_name):
        entities = self.get_entities(msg, entity_name)
        key, conf = reduce(lambda m, e: e if e[1]>m[1] else m, entities, ['', 0])
        best_entity = (key, conf)

        return best_entity
