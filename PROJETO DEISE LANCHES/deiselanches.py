import tkinter as tk
from tkinter import messagebox, PhotoImage, ttk, simpledialog
import sqlite3
import os
from datetime import datetime

conn = sqlite3.connect('deise_lanches.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS caixa
             (id INTEGER PRIMARY KEY, data TEXT, tipo TEXT, valor REAL, descricao TEXT)''')
conn.commit()

def adicionar_transacao(tipo, valor, descricao):
    if not valor or not descricao:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return
    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        return
    
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        c.execute("INSERT INTO caixa (data, tipo, valor, descricao) VALUES (?, ?, ?, ?)",
                  (data, tipo, valor, descricao))
    atualizar_lista()
    atualizar_saldo()
    entry_valor.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)

def exibir_saldo():
    c.execute("SELECT SUM(valor) FROM caixa WHERE tipo='Entrada'")
    entradas = c.fetchone()[0] or 0
    c.execute("SELECT SUM(valor) FROM caixa WHERE tipo='Saída'")
    saidas = c.fetchone()[0] or 0
    saldo = entradas - saidas
    return saldo

def atualizar_saldo():
    saldo = exibir_saldo()
    label_saldo['text'] = f"Saldo atual: R$ {saldo:.2f}"

def gerar_relatorio():
    resposta = messagebox.askquestion("Gerar Relatório", "Você deseja gerar o relatório e limpar os registros do banco?", icon='question', type="yesnocancel")
    
    if resposta == "yes":
        while True:
            senha = simpledialog.askstring("Autenticação", "Por favor, insira a senha para gerar o relatório e limpar os registros:", show='*')
            if senha is None:
                messagebox.showinfo("Cancelado", "A operação foi cancelada.")
                return
            elif senha == "admin":
                break
            else:
                messagebox.showerror("Erro", "Senha incorreta. Tente novamente.")
        
        c.execute("SELECT * FROM caixa")
        transacoes = c.fetchall()
        relatorio = "\n".join([f"ID: {t[0]}, Data: {t[1]}, Tipo: {t[2]}, Valor: R$ {t[3]:.2f}, Descrição: {t[4]}" for t in transacoes])
        if not relatorio:
            relatorio = "Nenhuma transação registrada."
        saldo_atual = exibir_saldo()
        relatorio += f"\n\nSaldo total em caixa: R$ {saldo_atual:.2f}"

        data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if not os.path.exists('relatorios'):
            os.makedirs('relatorios')
        nome_arquivo = os.path.join('relatorios', f"relatorio_transacoes_{data_atual}.txt")

        with open(nome_arquivo, 'w') as file:
            file.write(relatorio)

        messagebox.showinfo("Relatório de Transações", f"Relatório salvo como {nome_arquivo}")

        with conn:
            c.execute("DELETE FROM caixa")
        atualizar_lista()
        atualizar_saldo()
    
    elif resposta == "no":
        gerar_relatorio_sem_excluir()

    elif resposta == "cancel":
        messagebox.showinfo("Cancelado", "A operação foi cancelada.")
        return

def gerar_relatorio_sem_excluir():
    c.execute("SELECT * FROM caixa")
    transacoes = c.fetchall()
    relatorio = "\n".join([f"ID: {t[0]}, Data: {t[1]}, Tipo: {t[2]}, Valor: R$ {t[3]:.2f}, Descrição: {t[4]}" for t in transacoes])
    if not relatorio:
        relatorio = "Nenhuma transação registrada."
    saldo_atual = exibir_saldo()
    relatorio += f"\n\nSaldo total em caixa: R$ {saldo_atual:.2f}"

    data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists('relatorios'):
        os.makedirs('relatorios')
    nome_arquivo = os.path.join('relatorios', f"relatorio_transacoes_{data_atual}.txt")

    with open(nome_arquivo, 'w') as file:
        file.write(relatorio)

    messagebox.showinfo("Relatório de Transações", f"Relatório salvo como {nome_arquivo}")

def excluir_transacao():
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showerror("Erro", "Por favor, selecione um registro para excluir.")
        return

    while True:
        senha = simpledialog.askstring("Autenticação", "Por favor, insira a senha para excluir o registro:", show='*')
        if senha is None:
            messagebox.showinfo("Cancelado", "A operação foi cancelada.")
            return
        elif senha == "admin":
            break
        else:
            messagebox.showerror("Erro", "Senha incorreta. Tente novamente.")
    
    transacao = tree.item(item_selecionado, 'values')
    data = transacao[0]
    tipo = transacao[1]
    valor = transacao[2].replace("R$ ", "")
    descricao = transacao[3]

    confirmacao = messagebox.askquestion("Excluir Transação", f"Tem certeza de que deseja excluir a transação:\n\nData: {data}\nTipo: {tipo}\nValor: R$ {valor}\nDescrição: {descricao}", icon='question')
    
    if confirmacao == "yes":
        with conn:
            c.execute("DELETE FROM caixa WHERE data=? AND tipo=? AND valor=? AND descricao=?", (data, tipo, valor, descricao))
        atualizar_lista()
        atualizar_saldo()
        messagebox.showinfo("Sucesso", "Transação excluída com sucesso.")

def atualizar_lista():
    for i in tree.get_children():
        tree.delete(i)
    c.execute("SELECT * FROM caixa ORDER BY id DESC")
    transacoes = c.fetchall()
    for transacao in transacoes:
        tree.insert("", "end", values=(transacao[1], transacao[2], f"R$ {transacao[3]:.2f}", transacao[4]))

root = tk.Tk()
root.title("Controle de Caixa")
root.geometry("500x750")
root.resizable(False, False)

logo = PhotoImage(file="deise_lanches_logo.png")
logo = logo.subsample(6)
label_logo = tk.Label(root, image=logo)
label_logo.pack(side='top', anchor='n', pady=10)

label_saldo = tk.Label(root, text="Saldo atual: R$ 0.00", font=("Arial", 16))
label_saldo.pack(pady=5)

frame_lista = tk.Frame(root)
frame_lista.pack(padx=10, pady=10, fill='both', expand=True)

columns = ("Data", "Tipo", "Valor", "Descrição")
tree = ttk.Treeview(frame_lista, columns=columns, show="headings", height=12)
tree.heading("Data", text="Data")
tree.heading("Tipo", text="Tipo")
tree.heading("Valor", text="Valor")
tree.heading("Descrição", text="Descrição")
tree.column("Data", anchor="center", width=100)
tree.column("Tipo", anchor="center", width=80)
tree.column("Valor", anchor="center", width=100)
tree.column("Descrição", anchor="center", width=200)

vsb = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
tree.configure(yscroll=vsb.set)
tree.pack(side="left", fill="both", expand=True)
vsb.pack(side="right", fill="y")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10, padx=10, fill='x')

label_valor = tk.Label(frame_inputs, text="Valor:")
label_valor.pack(anchor='w')
entry_valor = tk.Entry(frame_inputs)
entry_valor.pack(fill='x')

label_descricao = tk.Label(frame_inputs, text="Descrição:")
label_descricao.pack(anchor='w')
entry_descricao = tk.Entry(frame_inputs)
entry_descricao.pack(fill='x')

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

btn_entrada = tk.Button(frame_botoes, text="Registrar Entrada", command=lambda: adicionar_transacao('Entrada', entry_valor.get(), entry_descricao.get()), bg='white', fg='black')
btn_entrada.grid(row=0, column=0, padx=5, pady=5)

btn_saida = tk.Button(frame_botoes, text="Registrar Saída", command=lambda: adicionar_transacao('Saída', entry_valor.get(), entry_descricao.get()), bg='white', fg='black')
btn_saida.grid(row=0, column=1, padx=5, pady=5)

btn_relatorio = tk.Button(frame_botoes, text="Gerar Relatório", command=gerar_relatorio, bg='white', fg='black')
btn_relatorio.grid(row=1, column=0, padx=5, pady=5)

btn_excluir = tk.Button(frame_botoes, text="Excluir Registro", command=excluir_transacao, bg='white', fg='black')
btn_excluir.grid(row=1, column=1, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), root.destroy()))

atualizar_saldo()
atualizar_lista()
root.mainloop()
