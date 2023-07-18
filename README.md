<h1 align="center">Django Recipes</h1>
<p align="center">Neste projeto, foi desenvolvida uma aplicação full stack de um site de receitas utilizando Django
  e uma API utilizando Rest Framework separada da aplicação mas que alimenta o mesmo banco de dados.</p>

---

<br>

<h2 align="center">📃 Sobre o Projeto</h2>

<p align="center">Foi desenvolvida uma aplicação em Python Django que permite fazer um CRUD para um banco de dados. Esse CRUD possibilita
  tanto a criação quanto o login de usuários, assim como criação edição e deleção de receitas, tudo isso atravez de forms.
  Também foi disponibilizado uma API construida em Rest Framework, que possibilita também um CRUD na aplicação atravez de métodos HTTP, 
  possibilitando também a adição e login de usuários, tendo sua validação através de Jwt validators, possibilitando também a criação edição
  e deleção de receitas.
</p>

<br>

<h2 align="center">Rotas utilizáveis na API</h2>

<details>
  <summary><strong>Ver rotas</strong></summary><br />

  <details>
    <summary>POST</summary>
  
  - POST `http://localhost:8001/authors/api/v2/` para cadastrar novo usuario. Utilize um body nesse formato:
    
    ```jsx
      {
      	"first_name": "SeuNome",
      	"last_name": "SeuSobrenome",
      	"username": "SeuUsername",
      	"password": "SeuPassword1.",
      	"email": "algo2@email.com"
      }
    ```

  ---
    
  - POST `http://localhost:8001/recipes/api/token/` para fazer login e receber um token. Utilize um body nesse formato:
    
    ```jsx
      {
      	"username": "SeuUsername",
      	"password": "SeuPassword1.",
      }
    ```
      
  ---

- POST `http://localhost:8001/recipes/api/token/refresh/` para atualizar o token. Utilize um body nesse formato:
  
  ```jsx
    {
	    "refresh": "<O "refresh" token que foi recebido ao fazer login>"
    }
  ```
    
---

- POST `http://localhost:8001/recipes/api/token/verify/` para validar o token. Utilize um body nesse formato:
  
  ```jsx
    {
	    "token": "<O "access" token que foi recebido ao fazer login>"
    }
  ```
    
---
  
- POST `http://localhost:8001/recipes/api/v2/` para criar uma nova receita. Utilize um body nesse formato:
  <br>
  Para essa ação, o usuário deve enviar o "access" token no Header da requisição.
  `Authorization`  `Bearer <access token>`

  ```jsx
    {
    	"title": "Minha receita",
    	"description": "Uma receita deliciosa",
    	"preparation_time":10,
    	"preparation_time_unit": "minute",
    	"servings": 10,
    	"servings_unit": "portion",
    	"preparation_steps": "Descrição dos passos necessários para a criação bem sucedida da receita."
    }
  ```
    ps: Para enviar a imagem, os mesmos dados devem ser enviados por multipart form com a inclusão do campo "cover".

</details>

---

<details>
  <summary>GET</summary>

- GET `http://localhost:8001/authors/api/v2/<id>` exibe os dados do próprioe só o mesmo pode acessar.
	  <br>
	  Para essa ação, o usuário deve enviar o "access" token no Header da requisição.
	  `Authorization`  `Bearer <access token>`
	
	---
	
- GET `http://localhost:8001/authors/api/v2/me` exibe os dados do usuário autenticado.
  <br>
  Para essa ação, o usuário deve enviar o "access" token no Header da requisição.
  `Authorization`  `Bearer <access token>`
	
---
	  
- GET `http://localhost:8001/authors/api/v2/` exibe todas as receitas publicadas.
	  
---
  
- GET `http://localhost:8001/authors/api/v2/<id>` uma receita publicada de acordo com o id.
	  
---
	  
- GET `http://localhost:8001/authors/api/v2/?category_id=<id>` busca receitas publicada de acordo com a categoria.
	
---
	  
- GET `http://localhost:8001/authors/api/v2/?q=<search>` busca receitas de acordo com a palavra passada "<search>".
	
</details>

---

<details>
  <summary>PATCH</summary>

  Para todos os métodos PATCH, o usuário devera enviar o "access" token no Header da requisição.
  `Authorization`  `Bearer <access token>`
	
  - PATCH `http://localhost:8001/authors/api/v2/<id>/` para atualizar dados do usuário. Utilize um body nesse formato:
	
	```jsx
	  {
	    "last_name": "Cruz"
	  }
	```
	
	---
	
  - PATCH `http://localhost:8001/recipes/api/v2/<id>/` para atualizar a receita. Utilize um body nesse formato:
	
	```jsx
	    {
	      "title": "Novo titulo",
	      "description": "Nova descrição",
	    }
	```

</details>

---

<details>
  <summary>DELETE</summary>

  Para todos os métodos DELETE, o usuário devera enviar o "access" token no Header da requisição.
  `Authorization`  `Bearer <access token>`
  
- DELETE `http://localhost:8001/authors/api/v2/<id>` deleta o usuário.
  
---
  
- DELETE `http://localhost:8001/recipes/api/v2/<id>` deleta a receita se a mesma pertencer ao usuário.

</details>

<br>

---
