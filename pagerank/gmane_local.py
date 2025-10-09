import sqlite3
import re

# --------------------------------------------------
# CONFIGURAÇÃO INICIAL DO BANCO DE DADOS
# --------------------------------------------------
conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Messages')
cur.execute('DROP TABLE IF EXISTS Senders')
cur.execute('DROP TABLE IF EXISTS Subjects')

cur.execute('''
CREATE TABLE Messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    subject TEXT,
    sent_at TEXT
)
''')

print("Banco de dados 'content.sqlite' criado e limpo com sucesso.")

# --------------------------------------------------
# LEITURA DO ARQUIVO MBOX LOCAL
# --------------------------------------------------
fname = input('Digite o nome do arquivo mbox (default: mbox.txt): ')
if len(fname) < 1:
    fname = 'mbox.txt'

try:
    fhand = open(fname)
except:
    print('Erro: arquivo não encontrado ->', fname)
    quit()

count = 0
for line in fhand:
    line = line.strip()

    # Extrair remetente
    if line.startswith('From: '):
        email_match = re.findall(r'From: (.+)', line)
        if len(email_match) > 0:
            email = email_match[0].strip()
        else:
            email = None

    # Extrair assunto
    if line.startswith('Subject: '):
        subject_match = re.findall(r'Subject: (.+)', line)
        if len(subject_match) > 0:
            subject = subject_match[0].strip()
        else:
            subject = None

    # Extrair data
    if line.startswith('Date: '):
        date_match = re.findall(r'Date: (.+)', line)
        if len(date_match) > 0:
            sent_at = date_match[0].strip()
        else:
            sent_at = None

    # Registrar no banco se tiver remetente e data
    if line.startswith('X-FileName:'):
        if email and sent_at:
            cur.execute('''
                INSERT INTO Messages (email, subject, sent_at)
                VALUES (?, ?, ?)
            ''', (email, subject, sent_at))
            count += 1
            if count % 50 == 0:
                print(f'{count} mensagens processadas...')

conn.commit()
cur.close()
print(f'\n✅ Concluído! {count} mensagens gravadas em "content.sqlite".')
