
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import csv
from email_config import EmailConfigWindow
from certificate_generator import generate_certificate
from email_sender import send_certificate_email
from participants_manager import ParticipantsManager

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Certificados")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Cabeçalho
        header_frame = tk.Frame(root, bg="#4caf50", height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Gerador de Certificados com Envio por E-mail", 
                              font=("Arial", 16, "bold"), bg="#4caf50", fg="white")
        title_label.pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Botões de ação
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(button_frame, text="📧 Configurar E-mail", command=self.open_email_config, 
             bg="#2196F3", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="👥 Gerenciar Participantes", command=self.open_participants_manager, 
            bg="#2196F3", fg="white", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="📄 Gerar Certificados", command=self.generate_certificates, 
            bg="#4caf50", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="✉️ Enviar Certificados", command=self.send_certificates, 
            bg="#4caf50", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        # Status frame
        status_frame = tk.LabelFrame(main_frame, text="Status e Logs", bg="#f0f0f0", padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_text = tk.Text(status_frame, height=15, width=85, font=("Consolas", 10))
        scrollbar = tk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Verificar se a configuração de e-mail já existe
        self.check_email_config()
        
        # Verificar se existem participantes
        self.check_participants()
        
        self.log_status("✅ Sistema iniciado. Use os botões acima para começar.")
    
    def check_email_config(self):
        config_path = "data/email_config.json"
        if os.path.exists(config_path):
            self.log_status("✅ Configuração de e-mail encontrada")
        else:
            self.log_status("⚠️ Configure o e-mail primeiro (Botão 'Configurar E-mail')")
    
    def check_participants(self):
        csv_path = "data/participants.csv"
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    participants = list(reader)
                    self.log_status(f"✅ {len(participants)} participantes carregados")
                    print(f"DEBUG: Participantes carregados: {participants}")
            except Exception as e:
                self.log_status(f"⚠️ Erro ao carregar participantes: {str(e)}")
                print(f"DEBUG: Erro ao carregar CSV: {str(e)}")
        else:
            self.log_status("⚠️ Adicione participantes primeiro (Botão 'Gerenciar Participantes')")
    
    def open_email_config(self):
        EmailConfigWindow(self.root, self.log_status)
        self.check_email_config()
    
    def open_participants_manager(self):
        manager = ParticipantsManager(self.root, self.log_status)
        # Configurar callback para quando fechar
        self.root.wait_window(manager.top)
        # Recarregar participantes após fechar
        self.check_participants()
    
    def generate_certificates(self):
        try:
            # Verificar se o arquivo de participantes existe
            if not os.path.exists("data/participants.csv"):
                messagebox.showerror("Erro", "Nenhum participante encontrado.\nUse 'Gerenciar Participantes' para adicionar participantes.")
                return
            
            # Criar pasta de certificados se não existir
            os.makedirs("output/certificates", exist_ok=True)
            
            # Contadores
            success_count = 0
            error_count = 0
            
            # Ler participantes
            with open("data/participants.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                participants = list(reader)
                print(f"DEBUG: Participantes para gerar: {participants}")
            
            if not participants:
                messagebox.showwarning("Aviso", "Nenhum participante encontrado no arquivo CSV!")
                return
            
            # Gerar certificados
            for participant in participants:
                nome = participant['nome']
                email = participant['email']
                try:
                    filename = generate_certificate(nome, email)
                    if filename and os.path.exists(filename):
                        self.log_status(f"✅ Certificado gerado para {nome}")
                        success_count += 1
                    else:
                        self.log_status(f"❌ Falha ao gerar certificado para {nome}")
                        error_count += 1
                except Exception as e:
                    self.log_status(f"❌ Erro ao gerar certificado para {nome}: {str(e)}")
                    error_count += 1
                    print(f"DEBUG: Erro detalhado: {str(e)}")
            
            messagebox.showinfo("Geração Concluída", 
                               f"Certificados gerados:\n✅ {success_count} com sucesso\n❌ {error_count} com erro")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar certificados: {str(e)}")
            print(f"DEBUG: Erro geral: {str(e)}")
    
    def send_certificates(self):
        try:
            # Verificar configuração de e-mail
            if not os.path.exists("data/email_config.json"):
                messagebox.showerror("Erro", "Configure o e-mail primeiro!")
                return
            
            # Verificar participantes
            if not os.path.exists("data/participants.csv"):
                messagebox.showerror("Erro", "Nenhum participante encontrado!")
                return
            
            # Carregar configuração
            with open("data/email_config.json", "r") as f:
                config = json.load(f)
            
            # Contadores
            success_count = 0
            error_count = 0
            
            # Enviar certificados
            with open("data/participants.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    nome = row['nome']
                    email = row['email']
                    certificate_path = f"output/certificates/Certificado_{nome.replace(' ', '_')}.html"
                    
                    if os.path.exists(certificate_path):
                        try:
                            send_certificate_email(config, email, nome, certificate_path)
                            self.log_status(f"✅ E-mail enviado para {nome} ({email})")
                            success_count += 1
                        except Exception as e:
                            self.log_status(f"❌ Erro ao enviar para {nome}: {str(e)}")
                            error_count += 1
                    else:
                        self.log_status(f"⚠️ Certificado não encontrado para {nome}")
                        error_count += 1
            
            messagebox.showinfo("Envio Concluído", 
                               f"E-mails enviados:\n✅ {success_count} com sucesso\n❌ {error_count} com erro")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar e-mails: {str(e)}")
    
    def log_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()