-- Script SQL para criar a tabela de usuários no Supabase
-- Execute este script no SQL Editor do Supabase

-- Cria a tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cria índice para busca rápida por email
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Cria função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Cria trigger para atualizar updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Opcional: Configurar Row Level Security (RLS)
-- Descomente as linhas abaixo se quiser habilitar RLS
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Política para permitir leitura apenas para usuários autenticados
-- CREATE POLICY "Users can read own data" ON users
--     FOR SELECT
--     USING (auth.uid() = id);

-- Política para permitir inserção apenas via service key (backend)
-- CREATE POLICY "Service can insert users" ON users
--     FOR INSERT
--     WITH CHECK (true);
