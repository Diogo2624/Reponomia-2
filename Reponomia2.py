import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import os

# Funções para salvar e carregar o jogo

def salvar_jogo(jogadores, nome_save, level):
    with open(f"{nome_save}.txt", "w") as arquivo:
        arquivo.write(f"LEVEL:{level}\n")
        for nome, valor in jogadores.items():
            arquivo.write(f"{nome}: {valor}K\n")

def carregar_jogo(nome_save):
    jogadores = {}
    level = 1
    try:
        with open(f"{nome_save}.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            if linhas[0].startswith("LEVEL:"):
                level = int(linhas[0].strip().split(":")[1])
                linhas = linhas[1:]
            for linha in linhas:
                nome, valor = linha.strip().split(": ")
                jogadores[nome] = float(valor[:-1])
    except FileNotFoundError:
            messagebox.showerror("Erro", f"Arquivo {nome_save}.txt não encontrado.")
    return jogadores, level
    
def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()
    x = int((screen_width / 2) - (largura / 2))
    y = int((screen_height / 2) - (altura / 2))
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def iniciar_interface():
    jogadores = {}
    nome_save = ""
    level = 1

    def mostrar_botoes_jogo():
        btn_novo_jogo.pack_forget()
        btn_carregar_jogo.pack_forget()
        btn_novo_level.pack(pady=10)
        btn_encerrar_salvar.pack(pady=10)

    def iniciar_novo_jogo():
        nonlocal jogadores, nome_save, level
        nome_save = simpledialog.askstring("Novo Jogo", "Digite um nome para o save:")
        jogadores = {}
        level = int(simpledialog.askstring("Fase", "Digite a fase inicial:"))
        janela_jogadores = tk.Toplevel(root)
        janela_jogadores.title("Adicionar Jogadores")
        centralizar_janela(janela_jogadores, 650, 250)
        janela_jogadores.grab_set()
        janela_jogadores.focus_force()

        label_instrucao = tk.Label(janela_jogadores, text="Digite o nome dos jogadores e clique em 'OK'. Quando terminar, clique em 'Pronto'.")
        label_instrucao.pack(pady=10)

        entrada_nome = tk.Entry(janela_jogadores, width=40)
        entrada_nome.pack(pady=5)

        def adicionar_jogador():
            nome = entrada_nome.get()
            if nome:
                jogadores[nome] = 0
                entrada_nome.delete(0, tk.END)

        def finalizar_adicao():
            janela_jogadores.destroy()
            if not jogadores:
                messagebox.showinfo("Aviso", "Nenhum jogador adicionado. Encerrando o programa.")
                root.destroy()
            atualizar_saldos()

        botao_ok = tk.Button(janela_jogadores, text="OK", command=adicionar_jogador, width=30, height=3, font=("Arial", 10, "bold"))
        botao_ok.pack(pady=5)

        botao_pronto = tk.Button(janela_jogadores, text="Pronto", command=finalizar_adicao, width=30, height=3, font=("Arial", 10, "bold"))
        botao_pronto.pack(pady=5)

        entrada_nome.focus_set()


        
