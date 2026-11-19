"""
Populate each database with sample data for testing purposes.

Must send requests to the backend API endpoints to populate the databases.
The backend API will handle the insertion of data into each database.

Ejecutar desde la carpeta backend:
    python -m app.populate.populate
"""
import csv
import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import requests

from app.logger.Logger import Logger

logger = Logger()

# El csv se descarga de https://github.com/luminati-io/Pinterest-dataset-samples
# y debe guardarse en la misma carpeta que este archivo (backend/app/populate/).
POSTS_CSV_PATH = Path(__file__).resolve().parent / "Pinterest-posts.csv"

MONGODB_BASE_URL = "http://localhost:8001/mongodb"

LOREM_IPSUM = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa.",
]
COMMENTS_PER_PIN = 2

# TODO: Add explanation about how to populate each database and what kind of data will be inserted.
"""
Cassandra:


"""

"""
MongoDB:
Se hace el populate de mongo leyendo el csv, y con eso se pobla con los datos que tenemos en el csv
y se adaptan al formato de colección que definimos previamente, en la parte de tags se unen dos
arreglos ya que en el csv existe una diferencia entre hashtag y category con el fin de que solo sea
tags lo que se use.

pins: salen del csv. size_bytes y save_count no vienen en el csv, se guardan con su valor
por defecto (0).
boards: el csv no los trae, se genera 1 board de prueba por cada autor de pins. Usa lorem ipsum
como descripción y las etiquetas (máximo 5) de los pins de ese autor.
comments: el csv no trae autor ni fecha, se generan 2 comentarios de prueba por pin con lorem ipsum,
un autor al azar entre los autores de pins y una fecha posterior a la del pin.
"""


def post_to_mongodb(endpoint, document, label):
    response = requests.post(MONGODB_BASE_URL + endpoint, json=document)

    if not response.ok:
        logger.error(
            f"Error al cargar {label}: "
            f"{response.status_code} - {response.text}"
        )


def read_pins():
    with open(POSTS_CSV_PATH, encoding="utf-8-sig", newline="") as fd:
        return [
            {
                "pin_id": post["post_id"],
                "title": post["title"],
                "description": post["content"],
                "url": post["image_video_url"],
                "tags": list(dict.fromkeys(
                    (json.loads(post["hashtags"] or "null") or [])
                    + (json.loads(post["categories"] or "null") or [])
                )),
                "author_id": post["user_id"],
                "created_at": post["date_posted"].strip('"'),
            }
            for post in csv.DictReader(fd)
        ]


def build_boards(pins):
    pins_by_author = {}
    for pin in pins:
        pins_by_author.setdefault(pin["author_id"], []).append(pin)

    boards = []
    for n, (author_id, author_pins) in enumerate(pins_by_author.items(), start=1):
        tags = list(dict.fromkeys(tag for pin in author_pins for tag in pin["tags"]))
        boards.append({
            "board_id": str(uuid.uuid4()),
            "title": f"Tablero de prueba {n}",
            "description": LOREM_IPSUM[n % len(LOREM_IPSUM)],
            "tags": tags[:5],
            "author_id": author_id,
            "created_at": min(pin["created_at"] for pin in author_pins),
        })
    return boards


def build_comments(pins):
    rng = random.Random(42)
    author_ids = sorted({pin["author_id"] for pin in pins})

    comments = []
    for pin in pins:
        pin_date = datetime.fromisoformat(pin["created_at"].replace("Z", "+00:00"))
        for _ in range(COMMENTS_PER_PIN):
            comments.append({
                "comment_id": str(uuid.uuid4()),
                "pin_id": pin["pin_id"],
                "user_id": rng.choice(author_ids),
                "text": rng.choice(LOREM_IPSUM),
                "created_at": (pin_date + timedelta(hours=rng.randint(1, 720))).isoformat(),
            })
    return comments


def populate_mongodb():
    pins = read_pins()

    for pin in pins:
        post_to_mongodb("/pins", pin, f"pin {pin['pin_id']}")

    for board in build_boards(pins):
        post_to_mongodb("/boards", board, f"board {board['board_id']}")

    for comment in build_comments(pins):
        post_to_mongodb("/comments", comment, f"comentario {comment['comment_id']}")


def main():
    populate_mongodb()


if __name__ == "__main__":
    main()

"""
Dgraph:


"""