from libs.chatai.chatai import ChatAi

chatai = ChatAi('wit', '1584Bot')
resp = chatai.get_intent('hello world')
print(str(resp))


