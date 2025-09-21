
import os
from datetime import datetime

def generate_certificate(nome, email):
    """Gera um certificado em HTML"""
    
    
    data_emissao = datetime.now().strftime("%d/%m/%Y")
    curso_nome = "Python para Iniciantes"
    carga_horaria = "40 horas"
    assinatura = "Professor João Silva"
    
    # Criar pasta se não existir
    os.makedirs("output/certificates", exist_ok=True)
    
    # Nome do arquivo 
    safe_name = "".join(c for c in nome if c.isalnum() or c in (' ', '_')).rstrip()
    filename = f"output/certificates/Certificado_{safe_name.replace(' ', '_')}.html"
    
    # Conteúdo HTML do certificado
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Certificado - {nome}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 2cm;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .certificate {{
            background: white;
            padding: 3cm;
            border: 2cm solid #4caf50;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 21cm;
        }}
        .title {{
            color: #4caf50;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 1cm;
            text-transform: uppercase;
        }}
        .name {{
            color: #2196F3;
            font-size: 28px;
            font-weight: bold;
            margin: 1cm 0;
            text-transform: uppercase;
        }}
        .text {{
            font-size: 18px;
            margin: 0.5cm 0;
            line-height: 1.6;
        }}
        .signature {{
            margin-top: 2cm;
            border-top: 2px solid #333;
            padding-top: 0.5cm;
            display: inline-block;
        }}
        .footer {{
            margin-top: 1cm;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="certificate">
        <div class="title">🎓 Certificado de Conclusão</div>
        <div class="text">Certificamos que</div>
        <div class="name">{nome.upper()}</div>
        <div class="text">concluiu com sucesso o curso de</div>
        <div class="text" style="font-weight: bold; color: #ff5722;">{curso_nome}</div>
        <div class="text">com carga horária de {carga_horaria}</div>
        <div class="text">Emitido em: {data_emissao}</div>
        
        <div class="signature">
            <div>_________________________</div>
            <div style="font-weight: bold;">{assinatura}</div>
        </div>
        
        <div class="footer">
            Certificado válido e emitido digitalmente | ID: {email.replace('@', '_')}
        </div>
    </div>
</body>
</html>"""
    
    # Salvar arquivo
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"DEBUG: Certificado gerado: {filename}")
        return filename
        
    except Exception as e:
        print(f"ERRO ao gerar certificado: {str(e)}")
        return None