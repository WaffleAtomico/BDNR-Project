"""
Populate each database with sample data for testing purposes.

Must send requests to the backend API endpoints to populate the databases.
The backend API will handle the insertion of data into each database.
"""
import csv
import json
import requests

# TODO: Add explanation about how to populate each database and what kind of data will be inserted.
"""
Cassandra:


"""

"""
MongoDB:
Se hace el populate de mongo leyendo el csv, y con eso se pobla con los datos que tenemos en el csv
y se adaptan al formato de colección que definimos previamnente, en la parte de tags se unen dos 
arreglos ya que en el csv exiaste una diferencia entre hashtag y category con el fin de que solo sea
tags lo que se use.

"""
BASE_URL = "http://localhost:8000/mongodb"
def main():
    with open("Pinterest-posts.csv", encoding="utf-8-sig", newline="") as fd:
        posts_csv = csv.DictReader(fd)

        for post in posts_csv:
            pin = {
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

            response = requests.post(BASE_URL + "/pins", json=pin)

            if not response.ok:
                print(
                    f"Error al cargar pin {pin['pin_id']}: "
                    f"{response.status_code} - {response.text}"
                )


if __name__ == "__main__":
    main()

"""
Dgraph:


"""