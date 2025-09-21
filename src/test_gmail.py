import smtplib

def test_gmail():
    print("🧪 Testando conexão com Gmail...")
    
    email = input("Seu email Gmail: ")
    password = input("Senha de App (16 caracteres): ")
    
    # Testar porta 587 (TLS)
    try:
        print("\n🔧 Testando porta 587 (TLS)...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        print("✅ PORTA 587 FUNCIONOU!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Porta 587 falhou: {e}")
    
    # Testar porta 465 (SSL)
    try:
        print("\n🔧 Testando porta 465 (SSL)...")
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(email, password)
        print("✅ PORTA 465 FUNCIONOU!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Porta 465 falhou: {e}")
    
    return False

if __name__ == "__main__":
    if test_gmail():
        print("\n🎉 Conexão bem-sucedida! Use essas configurações no programa.")
    else:
        print("\n😥 Não foi possível conectar. Verifique:")
        print("1. ✅ Verificação em 2 etapas está ATIVADA")
        print("2. ✅ Você gerou uma SENHA DE APP (não senha normal)")
        print("3. ✅ Copiou os 16 caracteres corretamente")