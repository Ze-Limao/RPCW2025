=🎬 Movie Data Extractor

This Python script fetches movie data from DBpedia using SPARQL queries, extracting details like title, country, release date, producer, cast, genres, and synopsis. The data is then stored in a structured JSON file.
== 🚀 Features

    Retrieves movie details (title, country, release date, producer, abstract).
    Extracts actors' information (name, birthdate, nationality).
    Fetches movie genres dynamically.
    Saves the dataset in dataset.json.

== ▶️ Usage

Run the script:
```
python main.py  
```

== 📂 Output Format (dataset.json)
[
    {
        "id": "Inception",
        "titulo": "Inception",
        "pais": "United States",
        "data": "2010-07-16",
        "realizador": "Emma Thomas",
        "elenco": [
            {
                "id": "Leonardo_DiCaprio",
                "nome": "Leonardo DiCaprio",
                "dataNasc": "1974-11-11",
                "origem": "United States"
            }
        ],
        "genero": ["Science fiction", "Thriller"],
        "sinopse": "Inception is a 2010 science fiction film directed by Christopher Nolan..."
    }
]
