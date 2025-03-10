# QUIZ HISTÓRIA DE PORTUGAL
Este projeto consiste num quiz sobre a história de Portugal, desenvolvido utilizando Flask para o backend e Jinja templates para o frontend. O quiz obtém perguntas de uma base de dados SPARQL e apresenta-as aos utilizadores, estes podem responder e ver a sua pontuação.

Existem 3 formatos de pergunta: 
- Escolha Múltipla
- Verdadeiro e Falso
- Correspondência 

1. Instalar dependências:
     ```
     pip install Jinja2 click SPARQLWrapper Flask flask-cors certifi
     ```

2. Executar Flask server:
     ```
     python app_hportugal.py
     ```

3. Aceder ao quiz no browser:
    ```
    http://localhost:5000
    ```