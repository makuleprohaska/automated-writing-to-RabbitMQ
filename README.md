# Rekursiver Datei-Publisher nach RabbitMQ (Python)

In dieser README beschreibe ich meine Umsetzung der Aufgabe, inklusive Setup, Ausführung und Test über die **RabbitMQ-Weboberfläche**. Alles ist so aufgebaut, dass ich diese Datei und eine einzige Python-Datei (`file_publisher.py`) verwenden kann.

---

## 1. Aufgabe & Ansatz

**Aufgabe:**  
Ich soll ein Programm entwickeln, das ein lokales Dateisystem rekursiv durchsucht und für jede gefundene Datei eine Nachricht in eine RabbitMQ-Queue sendet.

**Mein Ansatz:**

- Programmiersprache: **Python 3**
- Messaging-System: **RabbitMQ**
- Python-Bibliothek: **`pika`**
- Nachrichtenformat: **JSON** pro Datei
- Rekursive Verzeichnissuche mit `os.walk`
- Fokus auf:
  - robuste Fehlerbehandlung (z. B. fehlende Rechte),
  - klare Struktur,
  - einfache Erweiterbarkeit (weitere Metadaten, Filter, andere Queue etc.).

---

## 2. Dateien in meinem Repo

Mein Repository besteht aus:

- `README.md` (diese Datei)
- `file_publisher.py` (das eigentliche Programm)

Optional kann ich später noch eine Consumer-Datei hinzufügen, ist aber für den Test über die RabbitMQ-Oberfläche nicht zwingend nötig.

---

## 3. Voraussetzungen (lokal)

Alles läuft lokal auf meinem Rechner. Ich brauche:

1. **Python 3.8, Docker, +**

   Prüfung:
   ```bash
   python --version
   docker --version

2. **Pika**
   pip install pika

3. **Rabbit MQ Starten**

  docker run -d --name some-rabbit \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3-management

  Optional können Umgebungsvariablen genutzt werden:

    RABBITMQ_QUEUE
    RABBITMQ_HOST
    RABBITMQ_PORT
    RABBITMQ_USER
    RABBITMQ_PASSWORD


4. **Beispiel**

  *Wenn nicht bereits vorhanden:*
  mkdir -p test_data/subdir
  echo "hello" > test_data/file1.txt
  echo "world" > test_data/subdir/file2.txt

  python file_publisher.py test_data \
  --queue files_queue \
  --host localhost \
  --port 5672 \
  --user guest \
  --password guest

5. **Gesendete Nachrichten Überprüfen**

  1. Browser öffnen → http://localhost:15672

  2. Einloggen → guest / guest

  3. Queues → meine Queue auswählen (z. B. files_queue)

  4. Nachrichtenanzahl ansehen

  5. Mit Get Message(s) JSON-Payload anzeigen

6. **RabbitMQ Stoppen**

  docker stop some-rabbit
  docker rm some-rabbit




