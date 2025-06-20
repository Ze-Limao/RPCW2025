PREFIX owl: <http://www.w3.org/2002/07/owl#>\
prefix : <http://www.example.org/disease-ontology#>

1.
```
select (count(?disease) as ?nDiseases)
where {
  ?disease a :Disease .
}
```
## R: 41

2.
```
select ?disease
where {
  ?disease a :Disease ;
           :hasSymptom :yellowish_skin .
}
```

:Alcoholic_hepatitis	\
:Chronic_cholestasis	\
:Hepatitis_B	\
:Hepatitis_C\
:Hepatitis_D\
:Hepatitis_E\
:Jaundice\
:hepatitis_A\


3.
```
select ?disease
where {
  ?disease a :Disease ;
           :hasTreatment :exercise .
}
```
:Arthritis\
:Cervical_spondylosis\
:Diabetes\
:GERD\
:Hypothyroidism\
:Paralysis_(brain_hemorrhage)\

4.
```
select ?name
where {
  ?patient a :Patient ;
           :hasName ?name .
}
ORDER BY ASC(?name)
```


13.
```
select ?diseaseY (count(?patientX) as ?numPatients)
where {
    ?patientX a :Patient .
    ?diseaseY a :Disease .
    ?patientX :hasDisease ?diseaseY .
}
group by ?diseaseY
order by desc(?numPatients)
```

14.
```
select ?symptomY (count(?diseaseY) as ?numDiseases)
where {
    ?diseaseY a :Disease .
    ?symptomY a :Symptom .
    ?diseaseY :hasSymptom ?symptomY .
}
group by ?symptomY
order by desc(?numDiseases)
```

15.
```
select ?treatmentY (count(?diseaseY) as ?numDiseases)
where {
    ?diseaseY a :Disease .
    ?treatmentY a :Treatment .
    ?diseaseY :hasTreatment ?treatmentY .
}
group by ?treatmentY
order by desc(?numDiseases)
```