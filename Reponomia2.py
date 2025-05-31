import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from PIL import Image, ImageTk

def salvar_jogo(jogadores, nome_save, level):
    with open(f"{nome_save}.txt", "w") as arquivo:
        arquivo.write(f"LEVEL:{level}\n")
        for nome, valor in jogadores.items():
            arquivo.write(f"{nome}: {int(valor)}K\n")

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

    def iniciar_novo_jogo():
        nonlocal jogadores, nome_save, level
        label_imagem.pack_forget()
        nome_save = simpledialog.askstring("Novo Jogo", "Digite um nome para o save:")
        jogadores = {}
        level = int(simpledialog.askstring("Fase", "Digite a fase inicial:"))
        adicionar_jogadores()
        mostrar_botoes_jogo()

    def carregar_jogo_existente():
        nonlocal jogadores, nome_save, level
        nome_save = simpledialog.askstring("Carregar Jogo", "Digite o nome do save:")
        jogadores, level = carregar_jogo(nome_save)
        label_imagem.pack_forget()
        if not jogadores:
            messagebox.showinfo("Aviso", "Nenhum jogador encontrado no save.")
            root.destroy()
        else:
            atualizar_saldos()
            mostrar_botoes_jogo()

    def adicionar_jogadores():
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

        tk.Button(janela_jogadores, text="OK", command=adicionar_jogador, width=30, height=3, font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(janela_jogadores, text="Pronto", command=finalizar_adicao, width=30, height=3, font=("Arial", 10, "bold")).pack(pady=5)
        entrada_nome.focus_set()

    def realizar_round():
        nonlocal level

        def escolher_acao(resposta):
            janela_acao.destroy()
            if resposta == "sair":
                remover_jogador()
            elif resposta == "entrar":
                adicionar_novo_jogador()
            processar_level()

        janela_acao = tk.Toplevel(root)
        janela_acao.title("Mudanças de Jogador")
        centralizar_janela(janela_acao, 400, 200)
        janela_acao.grab_set()
        janela_acao.focus_force()

        tk.Label(janela_acao, text="Entrou ou saiu algum jogador?", font=("Arial", 12)).pack(pady=10)

        tk.Button(janela_acao, text="Entrou", command=lambda: escolher_acao("entrar"), width=20, height=2).pack(pady=5)
        tk.Button(janela_acao, text="Saiu", command=lambda: escolher_acao("sair"), width=20, height=2).pack(pady=5)
        tk.Button(janela_acao, text="Não mudou", command=lambda: escolher_acao("nao"), width=20, height=2).pack(pady=5)

    def remover_jogador():
        janela_saida = tk.Toplevel(root)
        janela_saida.title("Jogador Saiu")
        centralizar_janela(janela_saida, 400, 200)
        janela_saida.grab_set()
        janela_saida.focus_force()

        tk.Label(janela_saida, text="Nome do jogador que saiu:", font=("Arial", 12)).pack(pady=10)
        entrada_saida = tk.Entry(janela_saida, font=("Arial", 12), width=30)
        entrada_saida.pack(pady=10)

        def confirmar_saida():
            nome_saida = entrada_saida.get()
            if nome_saida in jogadores:
                valor_sair = jogadores.pop(nome_saida)
                if jogadores:
                    valor_extra = valor_sair / len(jogadores)
                    for nome in jogadores:
                        jogadores[nome] += valor_extra
            janela_saida.destroy()

        tk.Button(janela_saida, text="Confirmar", command=confirmar_saida, width=20, height=2).pack(pady=10)
        janela_saida.wait_window()

    def adicionar_novo_jogador():
        janela_entrada = tk.Toplevel(root)
        janela_entrada.title("Novo Jogador")
        centralizar_janela(janela_entrada, 400, 200)
        janela_entrada.grab_set()
        janela_entrada.focus_force()

        tk.Label(janela_entrada, text="Nome do novo jogador:", font=("Arial", 12)).pack(pady=10)
        entrada_entrada = tk.Entry(janela_entrada, font=("Arial", 12), width=30)
        entrada_entrada.pack(pady=10)

        def confirmar_entrada():
            nome_entrada = entrada_entrada.get()
            if nome_entrada:
                jogadores[nome_entrada] = 0
            janela_entrada.destroy()

        tk.Button(janela_entrada, text="Confirmar", command=confirmar_entrada, width=20, height=2).pack(pady=10)
        janela_entrada.wait_window()

    def processar_level():
        nonlocal level
        try:
            valor_round = float(simpledialog.askstring("Valor do Level", f"Level {level}\nDigite o valor total ganho neste level:"))
            valor_jogador = valor_round / len(jogadores)
            for nome in jogadores:
                jogadores[nome] += valor_jogador

            atualizar_saldos()

            for nome in jogadores:
                janela_gasto = tk.Toplevel(root)
                janela_gasto.title("Gasto do Jogador")
                centralizar_janela(janela_gasto, 400, 150)
                janela_gasto.grab_set()
                janela_gasto.focus_force()

                tk.Label(janela_gasto, text=f"{nome} possui {int(jogadores[nome])}K\nQuanto ele gastou?", font=("Arial", 12)).pack(pady=10)
                entrada = tk.Entry(janela_gasto)
                entrada.pack(pady=5)

                def confirmar(nome=nome):
                    try:
                        gasto = float(entrada.get())
                        jogadores[nome] -= gasto
                        janela_gasto.destroy()
                        atualizar_saldos()
                    except ValueError:
                        messagebox.showerror("Erro", "Digite um valor válido.")

                tk.Button(janela_gasto, text="Confirmar", command=confirmar, width=30, height=3).pack(pady=10)
                janela_gasto.wait_window()

            atualizar_saldos()
            level += 1
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def encerrar_jogo():
        salvar_jogo(jogadores, nome_save, level)
        messagebox.showinfo("Fim de jogo", "Jogo salvo com sucesso. Encerrando.")
        root.destroy()

    def atualizar_saldos():
        for widget in frame_saldos.winfo_children():
            widget.destroy()
        tk.Label(frame_saldos, text=f"LEVEL: {level}", font=("Arial", 16, "bold")).pack(pady=5)
        for nome, saldo in jogadores.items():
            tk.Label(frame_saldos, text=f"{nome}: {int(saldo)}K", font=("Arial", 14)).pack(anchor='w')

    def mostrar_botoes_jogo():
        frame_top.pack_forget()
        btn_round.pack(side="left", padx=10)
        btn_sair.pack(side="left", padx=10)
        frame_botoes.pack(pady=20)

    root = tk.Tk()
    root.title("Reponomia")
    root.geometry("1000x700")
    root.configure(bg="#000000")

    titulo = tk.Label(root, text="REPONOMIA", font=("Segoe UI", 32, "bold"), bg="#000000", fg="#FFFFFF", justify="center")
    titulo.config(anchor='center')
    titulo.pack(pady=30)

    imagem_logo = Image.open("logo.png")
    imagem_logo = imagem_logo.resize((330, 245))
    imagem_logo = ImageTk.PhotoImage(imagem_logo)


    label_imagem = tk.Label(root, image=imagem_logo, bg="#000000")
    label_imagem.pack(pady=0)

    frame_top = tk.Frame(root, bg="#000000")
    frame_top.pack(pady=10)

    btn_novo = tk.Button(frame_top, text="Novo Jogo", command=iniciar_novo_jogo, width=40, height=4, font=("Segoe UI", 14, "bold"), bg="#1E1E1E", fg="#FFFFFF")
    btn_novo.pack(side="left", padx=10)

    btn_carregar = tk.Button(frame_top, text="Carregar Jogo", command=carregar_jogo_existente, width=40, height=4, font=("Segoe UI", 14, "bold"), bg="#1E1E1E", fg="#FFFFFF")
    btn_carregar.pack(side="left", padx=10)

    frame_saldos = tk.Frame(root, bg="#000000")
    frame_saldos.pack(pady=20)

    frame_botoes = tk.Frame(root, bg="#000000")

    btn_round = tk.Button(frame_botoes, text="Novo Level", command=realizar_round, width=40, height=4, font=("Segoe UI", 14, "bold"), bg="#1E1E1E", fg="#FFFFFF")
    btn_sair = tk.Button(frame_botoes, text="Encerrar e Salvar", command=encerrar_jogo, width=40, height=4, font=("Segoe UI", 14, "bold"), bg="#1E1E1E", fg="#FFFFFF")

    root.mainloop()

iniciar_interface()
