import os
import sys
import json
import argparse
import datetime
import pika


def publish_files(root_dir, host, port, user, password, queue_name):
    credentials = pika.PlainCredentials(user, password)
    params = pika.ConnectionParameters(host=host, port=port, credentials=credentials)

    try:
        connection = pika.BlockingConnection(params)
    except Exception as e:
        print(f"ERROR: RabbitMQ Verbindung fehlgeschlagen: {e}", file=sys.stderr)
        return False

    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        files_published = 0
        print(f"Scanne '{root_dir}' und sende Dateiinformationen an Queue '{queue_name}'...")

        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                full_path = os.path.abspath(os.path.join(dirpath, filename))

                try:
                    stat = os.stat(full_path)
                except Exception:
                    continue

                message = {
                    "path": full_path,
                    "size_bytes": stat.st_size,
                    "modified_iso": datetime.datetime.fromtimestamp(
                        stat.st_mtime
                    ).isoformat(),
                }

                try:
                    channel.basic_publish(
                        exchange="",
                        routing_key=queue_name,
                        body=json.dumps(message).encode("utf-8"),
                        properties=pika.BasicProperties(delivery_mode=2),
                    )
                    files_published += 1
                except Exception as e:
                    print(f"Warnung: Nachricht fehlgeschlagen: {e}", file=sys.stderr)

        print(f"Fertig. {files_published} Nachrichten gesendet.")
    finally:
        try:
            connection.close()
        except:
            pass

    return True


def parse_args():
    parser = argparse.ArgumentParser(description="Rekursiver Datei-Scanner → RabbitMQ")
    parser.add_argument("directory", nargs="?", default=".", help="Startverzeichnis")
    parser.add_argument("--queue", "-q", required=not bool(os.getenv("RABBITMQ_QUEUE")),
                        default=os.getenv("RABBITMQ_QUEUE"))
    parser.add_argument("--host", "-H", default=os.getenv("RABBITMQ_HOST", "localhost"))
    parser.add_argument("--port", "-P", type=int, default=int(os.getenv("RABBITMQ_PORT", "5672")))
    parser.add_argument("--user", "-u", default=os.getenv("RABBITMQ_USER", "guest"))
    parser.add_argument("--password", "-p", default=os.getenv("RABBITMQ_PASSWORD", "guest"))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ok = publish_files(args.directory, args.host, args.port, args.user, args.password, args.queue)
    sys.exit(0 if ok else 1)
