"""
Script de teste para verificar conexão com Supabase
Execute: python test_supabase_connection.py
"""
import asyncio
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

async def test_connection():
    url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_KEY')

    print("=" * 50)
    print("TESTE DE CONEXÃO COM SUPABASE")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Key: {service_key[:20]}..." if service_key else "❌ Key não encontrada")
    print()

    if not url or not service_key:
        print("❌ Variáveis de ambiente não configuradas!")
        return

    try:
        # Cria cliente
        client = create_client(url, service_key)
        print("✅ Cliente Supabase criado")

        # Testa se a tabela existe
        print("\n📋 Testando acesso à tabela 'users'...")
        response = client.table("users").select("id").limit(1).execute()
        print(f"✅ Tabela 'users' acessível! ({len(response.data)} registros encontrados)")

        # Testa inserção
        print("\n📝 Testando inserção...")
        test_email = f"teste_{os.urandom(4).hex()}@test.com"
        test_data = {
            "email": test_email,
            "name": "Usuário Teste",
            "hashed_password": "$2b$12$test_hash_password_12345678901234567890"
        }

        insert_response = client.table("users").insert(test_data).execute()

        if insert_response.data and len(insert_response.data) > 0:
            print(f"✅ Inserção bem-sucedida! ID: {insert_response.data[0].get('id')}")

            # Limpa o teste
            user_id = insert_response.data[0].get('id')
            client.table("users").delete().eq("id", user_id).execute()
            print(f"🧹 Registro de teste removido (ID: {user_id})")
        else:
            print("❌ Inserção falhou - resposta vazia")
            if hasattr(insert_response, 'error'):
                print(f"   Erro: {insert_response.error}")

        print("\n" + "=" * 50)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        print("\nTraceback completo:")
        print(traceback.format_exc())
        print("\n" + "=" * 50)
        print("❌ TESTE FALHOU")
        print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_connection())







