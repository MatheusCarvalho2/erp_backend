# Guia de Deploy no Render

Este guia explica como fazer deploy da aplicação no Render (plano gratuito).

## Variáveis de Ambiente Necessárias

No painel do Render, vá em **Environment** e adicione as seguintes variáveis:

### ✅ Obrigatórias

| Variável | Descrição | Onde Obter |
|----------|-----------|------------|
| `SUPABASE_URL` | URL do seu projeto Supabase | Supabase Dashboard > Settings > API > Project URL |
| `SUPABASE_KEY` | Chave pública anon do Supabase | Supabase Dashboard > Settings > API > Project API keys > `anon` `public` |
| `SECRET_KEY` | Chave secreta para JWT (segurança crítica!) | Gere com: `openssl rand -hex 32` ou use um gerador online |

### ⚙️ Opcionais (com valores padrão)

| Variável | Valor Padrão | Descrição |
|----------|--------------|-----------|
| `ALGORITHM` | `HS256` | Algoritmo de assinatura JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Tempo de expiração do token em minutos |
| `SUPABASE_SERVICE_KEY` | - | Chave de serviço do Supabase (opcional, para operações administrativas) |

## Passos para Deploy

### 1. Preparar o Repositório

Certifique-se de que seu código está no GitHub/GitLab/Bitbucket.

### 2. Criar Novo Web Service no Render

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **New +** > **Web Service**
3. Conecte seu repositório
4. Configure:
   - **Name**: Nome do seu serviço (ex: `erp-backend`)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Configurar Variáveis de Ambiente

1. No painel do serviço, vá em **Environment**
2. Adicione todas as variáveis obrigatórias listadas acima
3. Clique em **Save Changes**

### 4. Deploy

O Render fará o deploy automaticamente após salvar as configurações.

## ⚠️ Importante

- **SECRET_KEY**: Use uma chave aleatória forte e única. **NUNCA** compartilhe ou commite no Git!
- **SUPABASE_URL e SUPABASE_KEY**: Essas são necessárias para a aplicação funcionar corretamente
- O Render usa a porta definida pela variável `$PORT` automaticamente

## Verificação

Após o deploy, acesse:
- `https://seu-servico.onrender.com/` - Deve retornar `{"message": "ERP Backend API", "version": "1.0.0"}`
- `https://seu-servico.onrender.com/docs` - Documentação automática do FastAPI (Swagger UI)

## Troubleshooting

Se a aplicação não iniciar:
1. Verifique os logs no Render Dashboard
2. Confirme que todas as variáveis de ambiente obrigatórias estão configuradas
3. Verifique se o `requirements.txt` está atualizado
4. Confirme que o `Start Command` está correto
