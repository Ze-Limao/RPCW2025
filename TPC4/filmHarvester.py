import json, requests
from urllib.parse import urlparse

endpoint = "https://dbpedia.org/sparql"
dataset = []

def query_graphdb(sparql_query):
    headers = {'Accept': 'application/json'}
    
    response = requests.get(endpoint, headers=headers, params={'query': sparql_query})
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: HTTP {response.status_code} - {response.text}")
    
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        raise Exception(f"Failed to decode JSON: {e}. Response text: {response.text}")


def extract_name_from_url(url):
    return urlparse(url).path.split('/')[-1].replace('_', ' ')


def get_filmes():
    movies_query = """
    SELECT DISTINCT ?id ?title ?country ?releaseDate ?director ?abstract
	WHERE {{
        ?id a dbo:Film .
		?id rdfs:label ?title .
		?id dbo:abstract ?abstract .
		OPTIONAL {{ ?id dbo:country ?country . }}
		OPTIONAL {{ ?id dbo:releaseDate ?releaseDate . }}
		OPTIONAL {{ ?id dbo:director ?director . }}
		FILTER (lang(?abstract) = "en") .
		FILTER (lang(?title) = "en") .
	}} LIMIT 1
    """

    films = query_graphdb(movies_query)

    for film in films.get('results', {}).get('bindings', []):
        film_id = film["id"]["value"]
        title = film.get("title", {}).get("value", "")
        country = film.get("country", {}).get("value", "")
        release_date = film.get("releaseDate", {}).get("value", "")
        director = film.get("director", {}).get("value", "")
        abstract = film.get("abstract", {}).get("value", "")

        cast_query = f"""
        SELECT DISTINCT ?actor ?name ?birthDate ?nationality WHERE {{
            <{film_id}> dbo:starring ?actor .
            OPTIONAL {{ ?actor rdfs:label ?name . FILTER (lang(?name) = "en") . }}
            OPTIONAL {{ ?actor dbo:birthDate ?birthDate . }}
            OPTIONAL {{ ?actor dbo:nationality ?nationality . }}
        }} LIMIT 5
        """

        result = query_graphdb(cast_query)
        cast = [
            {
                "id": extract_name_from_url(actor.get("actor", {}).get("value", "")),
                "nome": actor.get("name", {}).get("value", ""),
                "dataNasc": actor.get("birthDate", {}).get("value", ""),
                "origem": extract_name_from_url(actor.get("nationality", {}).get("value", ""))
            }
            for actor in result.get("results", {}).get("bindings", [])
        ]

        genres_query = f"""
        SELECT DISTINCT ?genreLabel WHERE {{
            <{film_id}> dbo:genre ?genre .
            ?genre rdfs:label ?genreLabel .
            FILTER (lang(?genreLabel) = "en") .
        }} LIMIT 5
        """
        result3 = query_graphdb(genres_query)
        genres = [genre.get("genreLabel", {}).get("value", "") for genre in result3.get("results", {}).get("bindings", [])]

        dataset.append(
            {
                "id": extract_name_from_url(film_id),
                "titulo": title,
                "pais": extract_name_from_url(country),
                "data": release_date,
                "diretor": extract_name_from_url(director),
                "elenco": cast,
                "genero": genres,
                "sinopse": abstract
            }
        )


def main():
    get_filmes()
    with open('dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()