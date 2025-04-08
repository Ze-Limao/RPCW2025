from rdflib import Graph, Namespace, RDF, OWL, Literal

g = Graph()
g.parse("med_doentes.ttl")

q = """
    CONSTRUCT {
        ?patientX :hasDisease ?diseaseY .
    }
    WHERE {
        ?patientX a :Patient .
        ?diseaseY a :Disease .
        ?patientX :hasSymptom ?x .
        ?diseaseY :hasSymptom ?x .
        ?patientX :hasSymptom ?y .
        ?diseaseY :hasSymptom ?y .
        ?patientX :hasSymptom ?z .
        ?diseaseY :hasSymptom ?z .
        FILTER(?x != ?y && ?x != ?z && ?y != ?z) 
    } limit 2000
"""

n = Namespace("http://www.example.org/disease-ontology#")

g.add((n.hasDisease, RDF.type, OWL.Ontology))

for r in g.query(q):
    g.add((r[0], n.hasDisease, Literal(r[2].split("#")[1])))
print(g.serialize("med_doentes_.ttl", format="turtle"))

