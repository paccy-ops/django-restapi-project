from pymongo import MongoClient

client = MongoClient(
    'mongodb://divisor:0l6YIeoLMjL4yEpQ@104.40.187.114:27017/divisor?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
db = client['divisor']
client = db.get_collection('clients')
post = client.find()
#
seen = set()
new_l = []

for x in post:
    t = tuple(dict(x).items())
    if t not in seen:
        seen.add(dict(x).get('company'))
        seen.add(dict(x).get('cvr'))
        new_l.append(t)

listna = []
data = {}
n = 1
for i in new_l:
    data[n] = f'{i[1][1]};{i[2][1]}'
    listna.append(data[n])
    n += 1


def get_all_data(listna):
    for b in listna:
        yield b


dat_client = get_all_data(listna)
listpa = []


def list_generator():
    for s in dat_client:
        b = s.split(';')
        listpa.append(b)
    return listpa


def cassa():
    pass
