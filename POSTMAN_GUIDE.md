# Guia de Testes no Postman

Este guia mostra como testar todos os endpoints da API de autenticação no Postman.

## Configuração Inicial

1. **Certifique-se de que o servidor está rodando:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **URL Base:** `http://127.0.0.1:8000`

---

## Endpoint 1: Registrar Usuário

### Configuração da Requisição

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/auth/register`
- **Headers:**
  - `Content-Type: application/json`

### Body (JSON)

```json
{
  "email": "usuario@example.com",
  "name": "João Silva",
  "password": "senha123"
}
```

### Exemplo Completo no Postman:

1. Crie uma nova requisição
2. Selecione método **POST**
3. URL: `http://127.0.0.1:8000/auth/register`
4. Vá em **Headers** e adicione:
   - Key: `Content-Type`
   - Value: `application/json`
5. Vá em **Body** → selecione **raw** → escolha **JSON**
6. Cole o JSON acima
7. Clique em **Send**

### Resposta Esperada (201 Created):

```json
{
  "id": 1,
  "email": "usuario@example.com",
  "name": "João Silva"
}
```

---

## Endpoint 2: Login

### Configuração da Requisição

- **Método:** `POST`
- **URL:** `http://127.0.0.1:8000/auth/login`
- **Headers:**
  - `Content-Type: application/json`

### Body (JSON)

```json
{
  "email": "usuario@example.com",
  "password": "senha123"
}
```

### Exemplo Completo no Postman:

1. Crie uma nova requisição
2. Selecione método **POST**
3. URL: `http://127.0.0.1:8000/auth/login`
4. Vá em **Headers** e adicione:
   - Key: `Content-Type`
   - Value: `application/json`
5. Vá em **Body** → selecione **raw** → escolha **JSON**
6. Cole o JSON acima
7. Clique em **Send**

### Resposta Esperada (200 OK):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**⚠️ IMPORTANTE:** Copie o `access_token` da resposta! Você precisará dele para o próximo endpoint.

---

## Endpoint 3: Obter Dados do Usuário (Protegido)

### Configuração da Requisição

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/auth/me`
- **Headers:**
  - `Authorization: Bearer <seu-token-aqui>`

### Exemplo Completo no Postman:

1. Crie uma nova requisição
2. Selecione método **GET**
3. URL: `http://127.0.0.1:8000/auth/me`
4. Vá em **Headers** e adicione:
   - Key: `Authorization`
   - Value: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (cole o token completo)
5. Clique em **Send**

### Resposta Esperada (200 OK):

```json
{
  "id": 1,
  "email": "usuario@example.com",
  "name": "João Silva"
}
```

### Alternativa: Usar a Aba Authorization

No Postman, você também pode usar a aba **Authorization**:

1. Selecione **Type:** `Bearer Token`
2. Cole o token no campo **Token**
3. O Postman adiciona automaticamente o header `Authorization: Bearer <token>`

---

## Fluxo Completo de Teste

### Passo 1: Registrar um usuário
```
POST http://127.0.0.1:8000/auth/register
Body: {
  "email": "teste@example.com",
  "name": "Usuário Teste",
  "password": "senha123"
}
```

### Passo 2: Fazer login
```
POST http://127.0.0.1:8000/auth/login
Body: {
  "email": "teste@example.com",
  "password": "senha123"
}
```
**Copie o `access_token` da resposta!**

### Passo 3: Acessar endpoint protegido
```
GET http://127.0.0.1:8000/auth/me
Headers: Authorization: Bearer <token-copiado>
```

---

## Erros Comuns

### 400 Bad Request - Registro
```json
{
  "detail": "Email já está cadastrado"
}
```
**Solução:** Use um email diferente ou delete o usuário do banco.

### 401 Unauthorized - Login
```json
{
  "detail": "Email ou senha incorretos"
}
```
**Solução:** Verifique se o email e senha estão corretos.

### 401 Unauthorized - /auth/me
```json
{
  "detail": "Token inválido ou expirado"
}
```
**Solução:**
- Verifique se o token está completo
- Verifique se está usando `Bearer ` antes do token
- Faça login novamente para obter um novo token

---

## Dica: Usar Variáveis no Postman

Para facilitar, você pode criar variáveis no Postman:

1. Vá em **Environments** → **Create Environment**
2. Adicione variável `base_url` = `http://127.0.0.1:8000`
3. Adicione variável `token` = (deixe vazio inicialmente)
4. Use `{{base_url}}/auth/login` nas URLs
5. Após login, salve o token na variável `{{token}}`
6. Use `{{token}}` no header Authorization

---

## Testando com a Documentação Interativa

Você também pode testar diretamente no navegador:

1. Acesse: `http://127.0.0.1:8000/docs`
2. Teste os endpoints diretamente na interface Swagger
3. Clique em "Try it out" em cada endpoint
4. Preencha os dados e clique em "Execute"
