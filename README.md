# 📧 GERADOR DE CERTIFICADOS COM ENVIO AUTOMÁTICO POR E-MAIL
###
## 🚀 COMEÇAR RÁPIDO

### 📦 PRÉ-REQUISITOS 
```bash
# Verificar Python
python --version  # Python 3.8+

# Instalar dependências
pip install -r requirements.txt
```
###
# Clone e execute
git clone https://github.com/Aszinnnn/certificado_generator.git <br>
cd certificado_generator<br>
python src/main.py
##
# 🎯 FUNCIONALIDADES
✅ GERAÇÃO DE CERTIFICADOS <br>
- Certificados HTML modernos e profissionais

- Design responsivo com animações CSS

- Códigos de verificação únicos

- Template personalizável

##
# 📧 ENVIO AUTOMÁTICO
- Envio em massa para múltiplos participantes

- Suporte a Gmail, Outlook, Yahoo, UOL

- Anexo automático de certificados

- Configuração de SMTP intuitiva

  ##
  # 👥 GERENCIAMENTO
- Interface gráfica para participantes

- Importação em massa via CSV

- Validação de e-mails

- Remoção e edição de participantes

  ##
  # 📁 ESTRUTURA DO PROJETO

```bash gerador-certificados/
├── src/
│   ├── main.py                 # Aplicação principal
│   ├── email_config.py         # Configuração de e-mail
│   ├── participants_manager.py # Gerenciador de participantes
│   ├── certificate_generator.py # Gerador de certificados
│   └── email_sender.py         # Envio de e-mails
├── data/
│   ├── participants.csv        # Lista de participantes
│   └── email_config.json       # Configurações de e-mail
├── output/
│   ├── certificates/           # Certificados gerados
│   └── sent/                   # Certificados enviados
├── templates/                  # Templates de certificado
└── requirements.txt            # Dependências
```
  ##
  # ⚙️ CONFIGURAÇÃO
🔧 CONFIGURAR E-MAIL
Execute o programa: python src/main.py

Clique em "Configurar E-mail"

Preencha os dados do servidor SMTP:

Servidor: smtp.gmail.com (Gmail)

Porta: 587

E-mail: seu_email@gmail.com

Senha: SENHA DE APP (16 caracteres)
