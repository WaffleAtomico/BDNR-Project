"""
Populate each database with sample data for testing purposes.

Must send requests to the backend API endpoints to populate the databases.
The backend API will handle the insertion of data into each database.

Ejecutar desde la carpeta backend:
    python -m app.populate.populate
"""
from app.populate.mongo_populate import populate_mongodb

# TODO: Add explanation about how to populate each database and what kind of data will be inserted.
"""
Cassandra:


"""

"""
MongoDB:
Se hace el populate de mongo leyendo el csv (populate/data/Pinterest-posts.csv), y con eso se pobla
con los datos que tenemos en el csv y se adaptan al formato de colección que definimos previamente,
en la parte de tags se unen dos arreglos ya que en el csv existe una diferencia entre hashtag y
category con el fin de que solo sea tags lo que se use. La lógica está en mongo_populate.py.

pins: salen del csv. size_bytes y save_count no vienen en el csv, se guardan con su valor
por defecto (0).
boards: el csv no los trae, se genera 1 board de prueba por cada autor de pins. Usa lorem ipsum
como descripción y las etiquetas (máximo 5) de los pins de ese autor.
comments: el csv no trae autor ni fecha, se generan 2 comentarios de prueba por pin con lorem ipsum,
un autor al azar entre los autores de pins y una fecha posterior a la del pin.
"""


def main():
    populate_mongodb()


if __name__ == "__main__":
    main()

"""
Dgraph:


"""