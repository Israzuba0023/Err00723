import sqlite3
import json

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

print('Gerando gword.js a partir do banco de dados...')

# Obter os assuntos e a contagem de mensagens por assunto
cur.execute('''
SELECT Subjects.subject, COUNT(Messages.id) as count
FROM Messages
JOIN Subjects ON Messages.subject_id = Subjects.id
GROUP BY Subjects.subject
ORDER BY count DESC
LIMIT 50
''')

data = []
for row in cur:
    subject = row[0]
    count = row[1]
    data.append({'text': subject, 'size': count})

# Gerar o arquivo gword.js
fhand = open('gword.js', 'w')
fhand.write("gword = ")
fhand.write(json.dumps(data, indent=2))
fhand.close()

print('✅ Arquivo gword.js criado com sucesso — abra gword.htm no navegador.')
