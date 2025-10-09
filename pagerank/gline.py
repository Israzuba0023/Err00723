import sqlite3
import json

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

print('Gerando gline.js a partir do banco de dados...')

# Obter a contagem de mensagens por remetente (sender)
cur.execute('''
SELECT Senders.sender, COUNT(Messages.id) as count
FROM Messages
JOIN Senders ON Messages.sender_id = Senders.id
GROUP BY Senders.sender
ORDER BY count DESC
LIMIT 100
''')

data = []
for row in cur:
    sender = row[0]
    count = row[1]
    data.append({'name': sender, 'count': count})

# Gerar o arquivo gline.js
fhand = open('gline.js', 'w')
fhand.write("gline = ")
fhand.write(json.dumps(data, indent=2))
fhand.close()

print('✅ Arquivo gline.js criado com sucesso — abra gline.htm no navegador.')
