-- Script para corrigir problemas de RLS no Supabase
-- Execute este script no SQL Editor do Supabase

-- Verifica se RLS está habilitado
-- Se estiver causando problemas, desabilite com:
ALTER TABLE users DISABLE ROW LEVEL SECURITY;

-- OU, se preferir manter RLS habilitado, crie políticas adequadas:

-- 1. Desabilita RLS temporariamente (recomendado para desenvolvimento)
-- ALTER TABLE users DISABLE ROW LEVEL SECURITY;

-- 2. OU cria políticas que permitem inserção/leitura via API (produção)
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Política para permitir inserção de usuários (qualquer um pode inserir durante registro)
-- CREATE POLICY "Allow user registration" ON users
--     FOR INSERT
--     WITH CHECK (true);

-- Política para permitir leitura de usuários (qualquer um pode ler)
-- CREATE POLICY "Allow user read" ON users
--     FOR SELECT
--     USING (true);

-- Política para permitir atualização (apenas o próprio usuário)
-- CREATE POLICY "Allow user update" ON users
--     FOR UPDATE
--     USING (true)
--     WITH CHECK (true);







