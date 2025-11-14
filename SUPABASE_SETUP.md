# Configuração do Supabase

Este guia explica como conectar o sistema de autenticação ao Supabase.

## Passos para Configuração

### 1. Criar Projeto no Supabase

1. Acesse [https://app.supabase.com](https://app.supabase.com)
2. Crie uma conta ou faça login
3. Crie um novo projeto
4. Anote a **URL do projeto** e a **API Key (anon/public)**

### 2. Criar Tabela de Usuários

1. No painel do Supabase, vá em **SQL Editor**
2. Execute o script SQL do arquivo `supabase_schema.sql`:

```sql
-- Execute o conteúdo do arquivo supabase_schema.sql
```

Isso criará:
- Tabela `users` com os campos necessários
- Índices para performance
- Trigger para atualizar `updated_at` automaticamente

### 3. Configurar Variáveis de Ambiente

1. Copie o arquivo `env.example` para `.env`:

```bash
cp env.example .env
```

2. Edite o arquivo `.env` e preencha com suas credenciais:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publica-anon-key
SECRET_KEY=sua-chave-secreta-aleatoria-aqui
```

**Onde encontrar as credenciais:**
- **SUPABASE_URL**: Em Settings > API > Project URL
- **SUPABASE_KEY**: Em Settings > API > Project API keys > `anon` `public`
- **SECRET_KEY**: Gere uma chave aleatória (pode usar: `openssl rand -hex 32`)

### 4. Instalar Dependências

As dependências já estão no `requirements.txt`. Se ainda não instalou:

```bash
pip install -r requirements.txt
```

### 5. Testar a Conexão

Inicie o servidor:

```bash
uvicorn app.main:app --reload
```

A API agora usará o Supabase automaticamente se as variáveis de ambiente estiverem configuradas.

## Como Funciona

O sistema segue o padrão **Repository Pattern** e **Dependency Inversion Principle**:

- Se `SUPABASE_URL` e `SUPABASE_KEY` estiverem configurados → usa `SupabaseUserRepository`
- Caso contrário → usa `InMemoryUserRepository` (desenvolvimento/testes)

Isso permite:
- ✅ Desenvolvimento local sem banco de dados
- ✅ Produção com Supabase
- ✅ Fácil troca entre implementações
- ✅ Testes com mock repository

## Estrutura da Tabela

A tabela `users` possui:

```sql
- id (BIGSERIAL PRIMARY KEY)
- email (VARCHAR UNIQUE NOT NULL)
- name (VARCHAR NOT NULL)
- hashed_password (TEXT NOT NULL)
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
```

## Troubleshooting

### Erro: "SUPABASE_URL e SUPABASE_KEY devem estar configurados"

- Verifique se o arquivo `.env` existe
- Confirme que as variáveis estão corretas
- Reinicie o servidor após criar/editar o `.env`

### Erro ao conectar com Supabase

- Verifique se a URL está correta
- Confirme que a API Key é a `anon` `public` key
- Verifique se a tabela `users` foi criada

### Usando repositório em memória mesmo com Supabase configurado

- Verifique os logs do servidor para erros
- O sistema faz fallback automático para memória em caso de erro
