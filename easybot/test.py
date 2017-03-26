import sys
import csv
from libs.chatai.chatai import ChatAi

if __name__ == "__main__":
    chatai = ChatAi('wit', '1584Bot')
    filename = sys.argv[1]

    # resp = chatai.get_entity('this is bangkok', 'location')
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        resp = {}
        for fi in reader.fieldnames:
            resp[fi] = []

        for i, row in enumerate(reader):
            for fi in reader.fieldnames:
                if fi in row:
                    resp[fi].append(row[fi])

        print(resp)

        for intent in resp:
            examples = [x.strip() for x in resp[intent] if x]
            chatai.create_intent(intent.strip(), examples=examples)


