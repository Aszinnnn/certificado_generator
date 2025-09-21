
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import csv
import os

class ParticipantsManager:
    def __init__(self, parent, log_callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Gerenciador de Participantes")
        self.top.geometry("1000x700")  # Aumentado para melhor visualização
        self.top.configure(bg="#f0f0f0")
        self.top.grab_set()
        self.top.focus_set()
        
        self.log_callback = log_callback
        self.participants = []
        self.parent = parent
        
        # Frame principal com scrollbar
        main_frame = tk.Frame(self.top, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#4caf50", height=60)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="👥 Gerenciador de Participantes", 
                              font=("Arial", 16, "bold"), bg="#4caf50", fg="white")
        title_label.pack(expand=True, pady=15)
        
        # Frame de entrada de dados
        input_frame = tk.Frame(main_frame, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Nome
        tk.Label(input_frame, text="Nome:", bg="#f0f0f0", font=("Arial", 10), 
                width=10).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Email
        tk.Label(input_frame, text="E-mail:", bg="#f0f0f0", font=("Arial", 10),
                width=10).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.email_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.email_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)
        
        # Botão Adicionar
        add_btn = tk.Button(input_frame, text="➕ Adicionar", command=self.add_participant, 
                           bg="#4caf50", fg="white", font=("Arial", 10), width=12)
        add_btn.grid(row=0, column=4, padx=10, pady=5)
        
        # Configurar pesos das colunas
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # Área de importação em massa
        bulk_frame = tk.LabelFrame(main_frame, text="📥 Importação em Massa", 
                                  bg="#f0f0f0", padx=10, pady=10, font=("Arial", 10, "bold"))
        bulk_frame.pack(fill=tk.X, pady=(0, 15))
        
        bulk_help = tk.Label(bulk_frame, text="Digite um participante por linha no formato: Nome, E-mail", 
                            bg="#f0f0f0", fg="#666", font=("Arial", 9))
        bulk_help.pack(anchor=tk.W, pady=(0, 5))
        
        self.bulk_text = scrolledtext.ScrolledText(bulk_frame, height=6, font=("Consolas", 10))
        self.bulk_text.pack(fill=tk.X, pady=5)
        
        bulk_button_frame = tk.Frame(bulk_frame, bg="#f0f0f0")
        bulk_button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(bulk_button_frame, text="📤 Importar", command=self.import_bulk, 
                 bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(bulk_button_frame, text="🗑️ Limpar", command=self.clear_bulk, 
                 bg="#ff9800", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        
        # Lista de participantes
        list_frame = tk.LabelFrame(main_frame, text="📋 Lista de Participantes", 
                                  bg="#f0f0f0", padx=10, pady=10, font=("Arial", 10, "bold"))
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Treeview para mostrar participantes
        columns = ("nome", "email")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("nome", text="Nome")
        self.tree.heading("email", text="E-mail")
        
        self.tree.column("nome", width=400, anchor=tk.W)
        self.tree.column("email", width=400, anchor=tk.W)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botões de ação
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Botões da esquerda
        left_btn_frame = tk.Frame(button_frame, bg="#f0f0f0")
        left_btn_frame.pack(side=tk.LEFT)
        
        tk.Button(left_btn_frame, text="❌ Remover Selecionado", command=self.remove_selected, 
                 bg="#f44336", fg="white", width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(left_btn_frame, text="🗑️ Limpar Lista", command=self.clear_list, 
                 bg="#ff9800", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        
        # Botões da direita
        right_btn_frame = tk.Frame(button_frame, bg="#f0f0f0")
        right_btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(right_btn_frame, text="📂 Carregar CSV", command=self.load_from_csv, 
                 bg="#2196F3", fg="white", width=12).pack(side=tk.RIGHT, padx=5)
        tk.Button(right_btn_frame, text="💾 Salvar e Fechar", command=self.save_and_close, 
                 bg="#4caf50", fg="white", width=15).pack(side=tk.RIGHT, padx=5)
        
        # Carregar participantes existentes
        self.load_participants()
        
        # Bind Enter key to add participant
        self.name_entry.bind('<Return>', lambda e: self.add_participant())
        self.email_entry.bind('<Return>', lambda e: self.add_participant())
        
        self.name_entry.focus()
        
        # Configurar protocolo de fechamento
        self.top.protocol("WM_DELETE_WINDOW", self.save_and_close)
    
    def add_participant(self):
        nome = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not nome or not email:
            messagebox.showwarning("Atenção", "Preencha nome e e-mail!")
            return
        
        if not self.is_valid_email(email):
            messagebox.showwarning("Atenção", "Digite um e-mail válido!")
            return
        
        # Verificar se já existe
        for participant in self.participants:
            if participant['email'].lower() == email.lower():
                messagebox.showwarning("Atenção", "Este e-mail já está na lista!")
                return
        
        # Adicionar à lista
        self.participants.append({'nome': nome, 'email': email})
        self.tree.insert("", tk.END, values=(nome, email))
        
        # Limpar campos
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.name_entry.focus()
        
        self.log_callback(f"✅ Participante adicionado: {nome} - {email}")
    
    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um participante para remover!")
            return
        
        for item in selected:
            values = self.tree.item(item, 'values')
            self.participants = [p for p in self.participants if p['email'] != values[1]]
            self.tree.delete(item)
            self.log_callback(f"✅ Participante removido: {values[0]}")
    
    def clear_list(self):
        if not self.participants:
            messagebox.showinfo("Info", "A lista já está vazia!")
            return
            
        if messagebox.askyesno("Confirmar", "Deseja limpar toda a lista de participantes?"):
            self.participants = []
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.log_callback("✅ Lista de participantes limpa!")
    
    def import_bulk(self):
        text = self.bulk_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Atenção", "Digite os participantes para importar!")
            return
            
        lines = text.split('\n')
        added = 0
        errors = 0
        error_messages = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Verificar se a linha tem vírgula
            if ',' not in line:
                errors += 1
                error_messages.append(f"Linha sem vírgula: '{line}'")
                continue
                
            parts = [part.strip() for part in line.split(',', 1)]
            if len(parts) < 2:
                errors += 1
                error_messages.append(f"Formato inválido: '{line}'")
                continue
                
            nome, email = parts[0], parts[1]
            if not nome or not email:
                errors += 1
                error_messages.append(f"Dados incompletos: '{line}'")
                continue
                
            if not self.is_valid_email(email):
                errors += 1
                error_messages.append(f"Email inválido: '{email}'")
                continue
                
            # Verificar duplicata
            if any(p['email'].lower() == email.lower() for p in self.participants):
                errors += 1
                error_messages.append(f"Email duplicado: '{email}'")
                continue
                
            self.participants.append({'nome': nome, 'email': email})
            self.tree.insert("", tk.END, values=(nome, email))
            added += 1
        
        self.bulk_text.delete("1.0", tk.END)
        
        msg = f"✅ Importação concluída: {added} adicionados"
        if errors > 0:
            msg += f", {errors} erros"
            
        messagebox.showinfo("Importação", msg)
        self.log_callback(msg)
        
        # Mostrar erros detalhados se houver
        if errors > 0 and messagebox.askyesno("Ver Erros", "Deseja ver os erros detalhados?"):
            error_window = tk.Toplevel(self.top)
            error_window.title("Erros de Importação")
            error_window.geometry("500x300")
            
            text_area = scrolledtext.ScrolledText(error_window, wrap=tk.WORD)
            text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            for error in error_messages:
                text_area.insert(tk.END, f"• {error}\n")
            
            text_area.config(state=tk.DISABLED)
    
    def clear_bulk(self):
        self.bulk_text.delete("1.0", tk.END)
        self.log_callback("✅ Área de importação limpa!")
    
    def load_from_csv(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo CSV",
            filetypes=[("CSV files", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                loaded = 0
                for row in reader:
                    if 'nome' in row and 'email' in row:
                        nome, email = row['nome'].strip(), row['email'].strip()
                        if nome and email and self.is_valid_email(email):
                            # Verificar duplicata
                            if not any(p['email'].lower() == email.lower() for p in self.participants):
                                self.participants.append({'nome': nome, 'email': email})
                                self.tree.insert("", tk.END, values=(nome, email))
                                loaded += 1
                    elif 'name' in row and 'email' in row:
                        # Tentar com nome em inglês também
                        nome, email = row['name'].strip(), row['email'].strip()
                        if nome and email and self.is_valid_email(email):
                            if not any(p['email'].lower() == email.lower() for p in self.participants):
                                self.participants.append({'nome': nome, 'email': email})
                                self.tree.insert("", tk.END, values=(nome, email))
                                loaded += 1
                
                if loaded > 0:
                    self.log_callback(f"✅ {loaded} participantes carregados de: {file_path}")
                    messagebox.showinfo("Sucesso", f"{loaded} participantes carregados com sucesso!")
                else:
                    messagebox.showinfo("Info", "Nenhum novo participante foi carregado.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar CSV: {str(e)}")
    
    def save_and_close(self):
        try:
            # Criar diretório se não existir
            os.makedirs("data", exist_ok=True)
            
            # Salvar para CSV
            with open("data/participants.csv", "w", encoding="utf-8", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['nome', 'email'])
                writer.writeheader()
                writer.writerows(self.participants)
            
            self.log_callback(f"✅ Lista salva com {len(self.participants)} participantes")
            
            # Fechar a janela
            self.top.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar participantes: {str(e)}")
    
    def load_participants(self):
        csv_path = "data/participants.csv"
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if 'nome' in row and 'email' in row:
                            nome, email = row['nome'].strip(), row['email'].strip()
                            if nome and email:
                                self.participants.append({'nome': nome, 'email': email})
                                self.tree.insert("", tk.END, values=(nome, email))
                
                self.log_callback(f"✅ {len(self.participants)} participantes carregados")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar participantes: {str(e)}")
    
    def is_valid_email(self, email):
        # Validação simples de e-mail
        return '@' in email and '.' in email.split('@')[-1] and len(email) > 5