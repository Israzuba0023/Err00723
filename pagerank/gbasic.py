import sqlite3

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

print("Gerando estatísticas básicas...")

cur.execute('''
SELECT Senders.sender, COUNT(Messages.id) as total
FROM Messages 
JOIN Senders ON Messages.sender_id = Senders.id
GROUP BY Senders.sender
ORDER BY total DESC
LIMIT 25
''')

results = cur.fetchall()
print("\nTop 25 remetentes com mais mensagens:\n")
for row in results:
    print(f"{row[0]:40s} {row[1]}")

print("\n✅ Estatísticas concluídas.\n")
conn.close()
