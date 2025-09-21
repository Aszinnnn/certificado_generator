import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class EmailConfigWindow:
    def __init__(self, parent, log_callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Configuração de E-mail")
        self.top.geometry("600x500")
        self.top.configure(bg="#f0f0f0")
        self.top.grab_set()  # Modal window
        
        self.log_callback = log_callback
        
        # Frame principal
        main_frame = ttk.Frame(self.top)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(main_frame, text="Configuração do Servidor de E-mail", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Formulário
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Campos de configuração
        fields = [
            ("server", "Servidor SMTP (ex: smtp.gmail.com):", "O servidor de saída do seu provedor de e-mail"),
            ("port", "Porta (ex: 587):", "A porta para conexão SMTP (587 para TLS, 465 para SSL)"),
            ("email", "Seu E-mail:", "Seu endereço de e-mail completo"),
            ("password", "Senha/App Password:", "Sua senha ou senha de aplicativo"),
            ("subject", "Assunto do E-mail:", "Assunto que aparecerá no e-mail enviado")
        ]
        
        self.entries = {}
        
        for i, (field, label, hint) in enumerate(fields):
            row_frame = ttk.Frame(form_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(row_frame, text=label, width=25).pack(side=tk.LEFT)
            entry = ttk.Entry(row_frame, width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # Tooltip
            def make_tooltip(hint_text, event):
                tooltip = tk.Toplevel(self.top)
                tooltip.wm_overrideredirect(True)
                tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                label = ttk.Label(tooltip, text=hint_text, background="yellow", relief="solid", borderwidth=1)
                label.pack()
                tooltip.after(5000, tooltip.destroy)
            
            hint_label = ttk.Label(row_frame, text="(?)", foreground="blue", cursor="hand2")
            hint_label.pack(side=tk.RIGHT, padx=5)
            hint_label.bind("<Enter>", lambda e, h=hint: make_tooltip(h, e))
            
            self.entries[field] = entry
        
        # Área de mensagem
        ttk.Label(main_frame, text="Mensagem do E-mail:").pack(anchor=tk.W, pady=(20, 5))
        
        self.message_text = tk.Text(main_frame, height=8, width=50)
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Texto padrão
        default_message = """Prezado(a) {nome},

É com grande prazer que entregamos seu certificado de participação no curso.

Agradecemos sua dedicação e empenho.

Atenciosamente,
Equipe do Curso
"""
        self.message_text.insert("1.0", default_message)
        
        # Botões
        btn_frame = tk.Frame(form_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=20)
        
        # Frame para botões da esquerda
        left_btn_frame = tk.Frame(btn_frame, bg="#f0f0f0")
        left_btn_frame.pack(side=tk.LEFT)
        
        tk.Button(left_btn_frame, text="💾 Salvar", command=self.save_config, 
                 bg="#4caf50", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(left_btn_frame, text="❌ Cancelar", command=self.top.destroy,
                 bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        
        # Frame para botões da direita
        right_btn_frame = tk.Frame(btn_frame, bg="#f0f0f0")
        right_btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(right_btn_frame, text="🆘 Ajuda", command=self.show_password_help,
                 bg="#2196F3", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        # Carregar configuração existente se disponível
        self.load_existing_config()
    
    def load_existing_config(self):
        config_path = "data/email_config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                
                for key, entry in self.entries.items():
                    if key in config:
                        entry.delete(0, tk.END)
                        entry.insert(0, config[key])
                
                if "message" in config:
                    self.message_text.delete("1.0", tk.END)
                    self.message_text.insert("1.0", config["message"])
                    
            except Exception as e:
                self.log_callback(f"Erro ao carregar configuração: {str(e)}")
    
    def save_config(self):
        try:
            config = {
                "server": self.entries["server"].get(),
                "port": self.entries["port"].get(),
                "email": self.entries["email"].get(),
                "password": self.entries["password"].get(),
                "subject": self.entries["subject"].get(),
                "message": self.message_text.get("1.0", tk.END).strip()
            }
            
            # Validação básica
            if not all([config["server"], config["port"], config["email"], config["password"]]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            # Criar diretório se não existir
            os.makedirs("data", exist_ok=True)
            
            # Salvar configuração
            with open("data/email_config.json", "w") as f:
                json.dump(config, f, indent=4)
            
            self.log_callback("Configuração de e-mail salva com sucesso!")
            self.top.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar configuração: {str(e)}")