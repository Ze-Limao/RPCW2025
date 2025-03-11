from SPARQLWrapper import SPARQLWrapper, JSON
import random

prefixes = """
        PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        """

sparql = SPARQLWrapper("http://localhost:7200/repositories/historiaPT")


def execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


# Escolha multipla
def fetch_question_king_birth():
    results = execute_query(
        prefixes
        + """
        select ?nome ?dataNascimento where {
            ?s rdf:type :Rei .
            ?s :nome ?nome .
            ?s :nascimento ?dataNascimento .
        } 
    """
    )

    random_binding = random.choice(results["results"]["bindings"])
    person = random_binding["nome"]["value"]
    date = random_binding["dataNascimento"]["value"]
    question_text = f"What is the date of birth of {person}?"
    options = [date]
    while len(options) < 4:
        random_date = random.choice(results["results"]["bindings"])["dataNascimento"][
            "value"
        ]
        if random_date not in options:
            options.append(random_date)
    random.shuffle(options)

    question = {"question": question_text, "options": options, "answer": date, "type": 'select'}

    return question


def fetch_question_dinasty():
    results = execute_query(
        prefixes
        + """
        select ?nome ?nomeDinastia where {
            ?s rdf:type :Rei .
            ?s :nome ?nome .
            ?s :temReinado ?reinado .
            ?reinado :dinastia ?dinastia .
            ?dinastia :nome ?nomeDinastia . 
        } 
    """
    )

    random_binding = random.choice(results["results"]["bindings"])
    person = random_binding["nome"]["value"]
    dinasty = random_binding["nomeDinastia"]["value"]
    question_text = f"What is the dinasty of {person}?"
    options = [dinasty]
    while len(options) < 4:
        random_dinasty = random.choice(results["results"]["bindings"])["nomeDinastia"][
            "value"
        ]
        if random_dinasty not in options:
            options.append(random_dinasty)
    random.shuffle(options)

    question = {"question": question_text, "options": options, "answer": dinasty, "type": 'select'}

    return question


# V/F
def fetch_question_kings_per_dinasty():
    results = execute_query(
        prefixes
        + """
        select ?nomeDinastia (COUNT(?rei) AS ?quantidadeReis) where {
        ?rei rdf:type :Rei .
        ?rei :temReinado ?reinado .
        ?reinado :dinastia ?dinastia .
    	?dinastia :nome ?nomeDinastia .
        }
        GROUP BY ?nomeDinastia
    """
    )

    random_binding = random.choice(results["results"]["bindings"])
    dinasty = random_binding["nomeDinastia"]["value"]
    quantity = random_binding["quantidadeReis"]["value"]

    answer = random.choice([True, False])

    if answer:
        question_text = f"The dinasty {dinasty} had {quantity} kings. True or False?"
        answer = "True"
        options = ["True", "False"]
    else:
        random_quantity = random.choice(results["results"]["bindings"])[
            "quantidadeReis"
        ]["value"]
        while random_quantity == dinasty:
            random_quantity = random.choice(results["results"]["bindings"])[
                "quantidadeReis"
            ]["value"]
        question_text = (
            f"The dinasty {dinasty} had {random_quantity} kings. True or False?"
        )
        answer = "False"
        options = ["True", "False"]

    question = {"question": question_text, "options": options, "answer": answer, "type": 'select'}

    return question


def fetch_question_surname():
    results = execute_query(
        prefixes
        + """
        select ?nome ?cognome where {
            ?s rdf:type :Rei .
            ?s :nome ?nome .
            ?s :cognomes ?cognome .
        } 
    """
    )

    random_binding = random.choice(results["results"]["bindings"])
    person = random_binding["nome"]["value"]
    cognome = random_binding["cognome"]["value"]
    answer = random.choice([True, False])

    if answer:
        question_text = f"The cognome of {person} is {cognome}. True or False?"
        answer = "True"
        options = ["True", "False"]
    else:
        random_cognome = random.choice(results["results"]["bindings"])["cognome"][
            "value"
        ]
        while random_cognome == cognome:
            random_cognome = random.choice(results["results"]["bindings"])["cognome"][
                "value"
            ]

        question_text = f"The cognome of {person} is {random_cognome}. True or False?"
        answer = "False"
        options = ["True", "False"]

    question = {"question": question_text, "options": options, "answer": answer, "type": 'select'}

    return question


# Write Question
def fetch_question_kings_conquests():
    results = execute_query(
        prefixes
        + """
        select ?nome ?data ?nomeMonarca where {
            ?conquista a historia:Conquista .
            ?conquista historia:nome ?nome .
            ?conquista historia:data ?data .
            ?conquista historia:temReinado ?reinado .
            ?reinado historia:temMonarca ?monarca .
            ?monarca historia:nome ?nomeMonarca .
        } order by ?data
    """
    )
    random_binding = random.choice(results["results"]["bindings"])
    conquest_name = random_binding["nome"]["value"]
    king = random_binding["nomeMonarca"]["value"]

    question_text = f"Which king led the conquest of {conquest_name}?"
    options = [king]

    question = {"question": question_text, "options": options, "answer": king, "type": 'write'}

    return question


def fetch_questions_from_dbpedia():
    questions = []
    questions.append(fetch_question_king_birth())
    questions.append(fetch_question_dinasty())
    questions.append(fetch_question_kings_per_dinasty())
    questions.append(fetch_question_surname())
    questions.append(fetch_question_kings_conquests())

    print(questions)
    return questions
