from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal
import csv, json, uuid

# Define Namespace
EX = Namespace("http://www.example.org/disease-ontology#")

# Load Existing Ontology
existing_graph = Graph()
existing_graph.parse("medical.ttl", format="turtle")

# Create a New Graph (this will become the final ontology)
new_graph = Graph()

# Bind Prefixes
new_graph.bind("", EX)
new_graph.bind("owl", OWL)
new_graph.bind("rdf", RDF)
new_graph.bind("rdfs", RDFS)

# Define Ontology Structure
new_graph.add((EX.Ontology, RDF.type, OWL.Ontology))
new_graph.add((EX.Cidade, RDF.type, OWL.Class))
new_graph.add((EX.Distrito, RDF.type, OWL.Class))
new_graph.add((EX.Ligação, RDF.type, OWL.Class))

# Define Properties
new_graph.add((EX.hasSymptom, RDF.type, OWL.ObjectProperty))
new_graph.add((EX.hasSymptom, RDFS.domain, EX.Disease))
new_graph.add((EX.hasSymptom, RDFS.range, EX.Symptom))

new_graph.add((EX.hasTreatment, RDF.type, OWL.ObjectProperty))
new_graph.add((EX.hasTreatment, RDFS.domain, EX.Disease))
new_graph.add((EX.hasTreatment, RDFS.range, EX.Treatment))

new_graph.add((EX.hasDescription, RDF.type, OWL.DatatypeProperty))
new_graph.add((EX.hasDescription, RDFS.domain, EX.Disease))
new_graph.add((EX.hasDescription, RDFS.range, RDFS.Literal))

new_graph.add((EX.hasName, RDF.type, OWL.DatatypeProperty))
new_graph.add((EX.hasName, RDFS.domain, EX.Patient))
new_graph.add((EX.hasName, RDFS.range, RDFS.Literal))

# Transfer existing diseases
for disease_uri in existing_graph.subjects(RDF.type, EX.Disease):
    new_graph.add((disease_uri, RDF.type, EX.Disease))

# Process Symptoms
with open("Disease_Syntoms.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        disease_name = row["Disease"].strip().replace(" ", "_")
        disease_uri = EX[disease_name]

        new_graph.add((disease_uri, RDF.type, EX.Disease))

        symptoms = {
            row[f"Symptom_{i}"].strip().replace(" ", "_")
            for i in range(1, 18)
            if row.get(f"Symptom_{i}") and row[f"Symptom_{i}"].strip()
        }

        for symptom in symptoms:
            symptom_uri = EX[symptom]
            new_graph.add((symptom_uri, RDF.type, EX.Symptom))
            new_graph.add((disease_uri, EX.hasSymptom, symptom_uri))

# Process Disease Descriptions
with open("Disease_Description.csv", "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        disease_name = row["Disease"].strip().replace(" ", "_")
        description = row["Description"].strip()

        disease_uri = EX[disease_name]

        if (disease_uri, RDF.type, EX.Disease) in new_graph:
            new_graph.add((disease_uri, EX.hasDescription, Literal(description)))

with open("Disease_Treatment.csv", "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        disease_name = row["Disease"].strip().replace(" ", "_")
        disease_uri = EX[disease_name]

        new_graph.add((disease_uri, RDF.type, EX.Disease))

        treatments = {
            row[f"Precaution_{i}"].strip().replace(" ", "_")
            for i in range(1, 5)
            if row.get(f"Precaution_{i}") and row[f"Precaution_{i}"].strip()
        }

        for treatment in treatments:
            treatment_uri = EX[treatment]

            new_graph.add((treatment_uri, RDF.type, EX.Treatment))  
            new_graph.add((disease_uri, EX.hasTreatment, treatment_uri))  

# Load Patient Data
with open("doentes.json", "r", encoding="utf-8") as json_file:
    patients_data = json.load(json_file)

# Process Patients
for patient in patients_data:
    patient_id = f"Patient_{uuid.uuid4().hex[:8]}"
    patient_uri = EX[patient_id]
    
    # Add patient instance
    new_graph.add((patient_uri, RDF.type, EX.Patient))
    new_graph.add((patient_uri, EX.hasName, Literal(patient["nome"])))
    
    # Associate symptoms
    for symptom in patient.get("sintomas", []):
        symptom_uri = EX[symptom.replace(" ", "_")]
        new_graph.add((symptom_uri, RDF.type, EX.Symptom))
        new_graph.add((patient_uri, EX.hasSymptom, symptom_uri))

new_graph.serialize(destination="med_doentes.ttl", format="turtle")
