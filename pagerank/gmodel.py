import sqlite3

# --------------------------------------------------
# ABRIR O BANCO DE DADOS COM AS MENSAGENS
# --------------------------------------------------
conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('SELECT email, subject, sent_at FROM Messages')

senders = dict()
subjects = dict()
messages = list()

print('Processando mensagens...')
count = 0

for row in cur:
    email = row[0]
    subject = row[1]
    sent_at = row[2]

    if email is None or subject is None:
        continue

    if email not in senders:
        senders[email] = len(senders)
    if subject not in subjects:
        subjects[subject] = len(subjects)

    messages.append((email, subject, sent_at))
    count += 1

print(f'{count} mensagens carregadas.')
conn.close()

# --------------------------------------------------
# CRIAR O BANCO index.sqlite
# --------------------------------------------------
conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Messages;
DROP TABLE IF EXISTS Senders;
DROP TABLE IF EXISTS Subjects;

CREATE TABLE Messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    subject_id INTEGER,
    sent_at TEXT
);

CREATE TABLE Senders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT UNIQUE
);

CREATE TABLE Subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT UNIQUE
);
''')

print('Criando tabelas no index.sqlite...')

# Inserir dados
for email, sid in senders.items():
    cur.execute('INSERT OR IGNORE INTO Senders (id, sender) VALUES (?, ?)', (sid, email))

for subject, sid in subjects.items():
    cur.execute('INSERT OR IGNORE INTO Subjects (id, subject) VALUES (?, ?)', (sid, subject))

for msg in messages:
    email, subject, sent_at = msg
    cur.execute('''
        INSERT INTO Messages (sender_id, subject_id, sent_at)
        VALUES (?, ?, ?)
    ''', (senders[email], subjects[subject], sent_at))

conn.commit()
print('✅ Banco index.sqlite criado com sucesso.')
conn.close()
