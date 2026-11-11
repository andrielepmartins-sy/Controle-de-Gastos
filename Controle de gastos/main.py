
import tkinter
from tkinter import ttk, messagebox
import json
import os
import math
from datetime import datetime
from decimal import Decimal, InvalidOperation

# ------------------------------ JANELA PRINCIPAL ------------------------------

root = tkinter.Tk()
root.title("Andriele | Controle de Gastos")
root.geometry("1000x870")
root.minsize(850, 600)
root.configure(bg="#161228")

# -------------------------- CENTRALIZAR JANELA --------------------------

largura_janela = 1000
altura_janela = 870

largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2

root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")


# ------------------------------ PALETA DE CORES ------------------------------

rosa_claro = "#BEA7B9"
malva = "#975F8F"
roxo = "#48294E"
azul_roxo = "#1F1B3D"
preto = "#161228"
branco = "#FFFFFF"
hover_roxo = "#704A76"

# ------------------------------ ARQUIVO JSON ------------------------------

# O arquivo fica na mesma pasta deste programa.
arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados.json")

# ------------------------------ DADOS DO SISTEMA ------------------------------

movimentacoes = []

# ------------------------------ FUNÇÕES DE ARQUIVO ------------------------------

def carregar_dados():
    global movimentacoes

    if not os.path.exists(arquivo):
        movimentacoes = []
        try:
            salvar_dados()
        except OSError:
            messagebox.showerror(
                "Erro",
                "Não foi possível criar o arquivo dados.json. Verifique a pasta do projeto."
            )
        return

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

    except (json.JSONDecodeError, OSError):
        movimentacoes = []
        messagebox.showwarning(
            "Aviso",
            "Não foi possível ler o dados.json. O programa vai iniciar sem movimentações."
        )
        return

    if not isinstance(dados, list):
        movimentacoes = []
        messagebox.showwarning(
            "Aviso",
            "O conteúdo do dados.json não está no formato esperado."
        )
        return

    # Confere os campos antes de usar os registros carregados.
    dados_validos = []
    ids_utilizados = set()
    registros_invalidos = 0

    for item in dados:
        try:
            identificador = item["id"]
            descricao = item["descricao"]
            valor = Decimal(str(item["valor"]))
            tipo = item["tipo"]
            data = item["data"]

            if not isinstance(identificador, int) or isinstance(identificador, bool):
                raise ValueError
            if identificador <= 0 or identificador in ids_utilizados:
                raise ValueError
            if not isinstance(descricao, str) or descricao.strip() == "":
                raise ValueError
            if not isinstance(tipo, str) or tipo not in ("Receita", "Despesa"):
                raise ValueError
            if not isinstance(data, str) or data.strip() == "":
                raise ValueError
            if not valor.is_finite() or valor <= 0:
                raise ValueError
            if valor != valor.quantize(Decimal("0.01")):
                raise ValueError

            dados_validos.append({
                "id": identificador,
                "descricao": descricao.strip(),
                "valor": float(valor),
                "tipo": tipo,
                "data": data
            })
            ids_utilizados.add(identificador)

        except (KeyError, TypeError, ValueError, InvalidOperation):
            registros_invalidos += 1

    movimentacoes = dados_validos

    if registros_invalidos > 0:
        messagebox.showwarning(
            "Aviso",
            f"{registros_invalidos} registro(s) inválido(s) foram ignorados ao carregar os dados."
        )


def salvar_dados():
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(movimentacoes, f, indent=4, ensure_ascii=False, allow_nan=False)


# ------------------------------ FUNÇÕES FINANCEIRAS ------------------------------

def calcular_totais():
    total_receitas = Decimal("0.00")
    total_despesas = Decimal("0.00")

    for item in movimentacoes:
        valor = Decimal(str(item["valor"]))

        if item["tipo"] == "Receita":
            total_receitas += valor
        elif item["tipo"] == "Despesa":
            total_despesas += valor

    saldo = total_receitas - total_despesas
    return total_receitas, total_despesas, saldo


def formatar_valor(valor):
    valor = Decimal(str(valor))
    valor_formatado = f"{valor:,.2f}"
    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")
    return f"R$ {valor_formatado}"


def converter_valor(texto):
    # Aceita, por exemplo, 1500,50; 1500.50 ou 1.500,50.
    texto = texto.strip().replace("R$", "").strip()

    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif texto.count(".") > 1:
        texto = texto.replace(".", "")
    elif texto.count(".") == 1 and len(texto.rsplit(".", 1)[1]) == 3:
        # Sem vírgula, um grupo de três dígitos depois do ponto é milhar.
        texto = texto.replace(".", "")

    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError("Digite um valor numérico válido.")

    if not valor.is_finite():
        raise ValueError("Digite um valor numérico válido.")

    if valor <= 0:
        raise ValueError("O valor precisa ser maior que zero.")

    try:
        valor = valor.quantize(Decimal("0.01"))
        valor_float = float(valor)
    except (InvalidOperation, OverflowError):
        raise ValueError("O valor informado é muito alto.")

    if not math.isfinite(valor_float):
        raise ValueError("O valor informado é muito alto.")

    # Não aceita casas decimais extras; não arredonda silenciosamente.
    if Decimal(texto) != valor:
        raise ValueError("Informe no máximo duas casas decimais.")

    return valor


def proximo_id():
    if len(movimentacoes) == 0:
        return 1

    maior_id = max(item["id"] for item in movimentacoes)
    return maior_id + 1


# ------------------------------ ATUALIZAR INTERFACE ------------------------------

def atualizar_dashboard():
    receitas, despesas, saldo = calcular_totais()

    valor_saldo.config(text=formatar_valor(saldo))
    valor_receitas.config(text=formatar_valor(receitas))
    valor_despesas.config(text=formatar_valor(despesas))

    # Mostra as cinco movimentações mais recentes na tela inicial.
    for item in tabela_principal.get_children():
        tabela_principal.delete(item)

    recentes = sorted(
        movimentacoes,
        key=lambda item: item["id"],
        reverse=True
    )

    for item in recentes[:5]:
        tabela_principal.insert(
            "",
            "end",
            values=(
                item["id"],
                item["data"],
                item["descricao"],
                item["tipo"],
                formatar_valor(item["valor"])
            )
        )


# ------------------------------ CADASTRO DE RECEITAS E DESPESAS ------------------------------

def adicionar_movimentacao(tipo):
    janela = tkinter.Toplevel(root)
    janela.title(f"Adicionar {tipo}")
    janela.geometry("430x370")
    janela.configure(bg=preto)
    janela.resizable(False, False)
    janela.transient(root)
    janela.grab_set()

    titulo = tkinter.Label(
        janela,
        text=f"CADASTRAR {tipo.upper()}",
        bg=preto,
        fg=rosa_claro,
        font=("Arial", 17, "bold")
    )
    titulo.pack(pady=25)

    # Campo de descrição.
    label_descricao = tkinter.Label(
        janela,
        text="Descrição:",
        bg=preto,
        fg=branco,
        font=("Arial", 11)
    )
    label_descricao.pack(anchor="w", padx=45)

    campo_descricao = tkinter.Entry(
        janela,
        font=("Arial", 12),
        bg=azul_roxo,
        fg=branco,
        insertbackground=branco,
        relief="flat"
    )
    campo_descricao.pack(fill="x", padx=45, ipady=8, pady=(5, 15))

    # Campo de valor.
    label_valor = tkinter.Label(
        janela,
        text="Valor (R$):",
        bg=preto,
        fg=branco,
        font=("Arial", 11)
    )
    label_valor.pack(anchor="w", padx=45)

    campo_valor = tkinter.Entry(
        janela,
        font=("Arial", 12),
        bg=azul_roxo,
        fg=branco,
        insertbackground=branco,
        relief="flat"
    )
    campo_valor.pack(fill="x", padx=45, ipady=8, pady=(5, 20))

    def salvar_movimentacao():
        descricao = campo_descricao.get().strip()
        valor_texto = campo_valor.get().strip()

        if descricao == "":
            messagebox.showerror(
                "Erro",
                "Informe a descrição da movimentação.",
                parent=janela
            )
            campo_descricao.focus()
            return

        try:
            valor = converter_valor(valor_texto)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro), parent=janela)
            campo_valor.focus()
            return

        nova_movimentacao = {
            "id": proximo_id(),
            "descricao": descricao,
            "valor": float(valor),
            "tipo": tipo,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        movimentacoes.append(nova_movimentacao)

        try:
            salvar_dados()
        except OSError:
            # Se não conseguiu gravar, desfaz a inclusão na lista.
            movimentacoes.pop()
            messagebox.showerror(
                "Erro",
                "Não foi possível salvar os dados no arquivo JSON.",
                parent=janela
            )
            return

        atualizar_dashboard()
        messagebox.showinfo(
            "Sucesso",
            f"{tipo} cadastrada com sucesso!",
            parent=janela
        )
        janela.destroy()

    botao_salvar = tkinter.Button(
        janela,
        text=f"Salvar {tipo}",
        bg=malva,
        fg=branco,
        activebackground=hover_roxo,
        activeforeground=branco,
        font=("Arial", 11, "bold"),
        relief="flat",
        cursor="hand2",
        command=salvar_movimentacao
    )
    botao_salvar.pack(fill="x", padx=45, ipady=8)

    campo_descricao.focus()


def adicionar_receita():
    adicionar_movimentacao("Receita")


def adicionar_despesa():
    adicionar_movimentacao("Despesa")


# ------------------------------ ESTILO DAS TABELAS ------------------------------

def configurar_tabela():
    estilo = ttk.Style()
    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background=azul_roxo,
        foreground=branco,
        fieldbackground=azul_roxo,
        rowheight=30,
        font=("Arial", 10)
    )

    estilo.configure(
        "Treeview.Heading",
        background=roxo,
        foreground=branco,
        font=("Arial", 10, "bold")
    )

    estilo.map(
        "Treeview",
        background=[("selected", malva)],
        foreground=[("selected", branco)]
    )


# ------------------------------ LISTAR MOVIMENTAÇÕES ------------------------------

def listar_movimentacoes():
    janela = tkinter.Toplevel(root)
    janela.title("Movimentações")
    janela.geometry("850x450")
    janela.configure(bg=preto)

    titulo = tkinter.Label(
        janela,
        text="HISTÓRICO DE MOVIMENTAÇÕES",
        bg=preto,
        fg=rosa_claro,
        font=("Arial", 17, "bold")
    )
    titulo.pack(pady=20)

    if len(movimentacoes) == 0:
        tkinter.Label(
            janela,
            text="Nenhuma movimentação cadastrada.",
            bg=preto,
            fg=rosa_claro,
            font=("Arial", 11)
        ).pack(pady=40)
        return

    tabela = ttk.Treeview(
        janela,
        columns=("id", "data", "descricao", "tipo", "valor"),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("data", text="Data")
    tabela.heading("descricao", text="Descrição")
    tabela.heading("tipo", text="Tipo")
    tabela.heading("valor", text="Valor")

    tabela.column("id", width=50, anchor="center")
    tabela.column("data", width=150, anchor="center")
    tabela.column("descricao", width=230)
    tabela.column("tipo", width=100, anchor="center")
    tabela.column("valor", width=130, anchor="center")

    tabela.pack(fill="both", expand=True, padx=20, pady=10)

    recentes = sorted(movimentacoes, key=lambda item: item["id"], reverse=True)

    for item in recentes:
        tabela.insert(
            "",
            "end",
            values=(
                item["id"],
                item["data"],
                item["descricao"],
                item["tipo"],
                formatar_valor(item["valor"])
            )
        )


# ------------------------------ CONSULTAR SALDO ------------------------------

def adicionar_saldo():
    receitas, despesas, saldo = calcular_totais()

    mensagem = (
        f"Total de receitas: {formatar_valor(receitas)}\n\n"
        f"Total de despesas: {formatar_valor(despesas)}\n\n"
        f"Saldo atual: {formatar_valor(saldo)}"
    )

    messagebox.showinfo("Consulta de Saldo", mensagem, parent=root)


# ------------------------------ EXCLUIR MOVIMENTAÇÃO ------------------------------

def adicionar_excluir():
    janela = tkinter.Toplevel(root)
    janela.title("Excluir Movimentação")
    janela.geometry("850x550")
    janela.configure(bg=preto)

    titulo = tkinter.Label(
        janela,
        text="EXCLUIR MOVIMENTAÇÃO",
        bg=preto,
        fg=rosa_claro,
        font=("Arial", 17, "bold")
    )
    titulo.pack(pady=15)

    texto = tkinter.Label(
        janela,
        text="Selecione uma movimentação e clique em excluir.",
        bg=preto,
        fg=rosa_claro,
        font=("Arial", 10)
    )
    texto.pack(pady=5)

    tabela = ttk.Treeview(
        janela,
        columns=("id", "descricao", "tipo", "valor"),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("descricao", text="Descrição")
    tabela.heading("tipo", text="Tipo")
    tabela.heading("valor", text="Valor")

    tabela.column("id", width=60, anchor="center")
    tabela.column("descricao", width=280)
    tabela.column("tipo", width=130, anchor="center")
    tabela.column("valor", width=150, anchor="center")

    tabela.pack(fill="both", expand=True, padx=20, pady=10)

    def atualizar_lista():
        for item_tabela in tabela.get_children():
            tabela.delete(item_tabela)

        for item in movimentacoes:
            tabela.insert(
                "",
                "end",
                values=(
                    item["id"],
                    item["descricao"],
                    item["tipo"],
                    formatar_valor(item["valor"])
                )
            )

    def excluir_selecionada():
        selecionado = tabela.selection()

        if not selecionado:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma movimentação para excluir.",
                parent=janela
            )
            return

        dados = tabela.item(selecionado[0], "values")
        identificador = int(dados[0])

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir esta movimentação?",
            parent=janela
        )

        if not confirmar:
            return

        # Localiza o registro pelo ID para não depender da posição na tabela.
        indice = None
        for posicao, item in enumerate(movimentacoes):
            if item["id"] == identificador:
                indice = posicao
                break

        if indice is None:
            messagebox.showerror(
                "Erro",
                "Essa movimentação não foi encontrada.",
                parent=janela
            )
            atualizar_lista()
            return

        removida = movimentacoes.pop(indice)

        try:
            salvar_dados()
        except OSError:
            # Se não conseguiu gravar, coloca a movimentação de volta.
            movimentacoes.insert(indice, removida)
            messagebox.showerror(
                "Erro",
                "Não foi possível salvar a exclusão no arquivo JSON.",
                parent=janela
            )
            atualizar_lista()
            return

        atualizar_lista()
        atualizar_dashboard()
        messagebox.showinfo(
            "Sucesso",
            "Movimentação excluída!",
            parent=janela
        )

    atualizar_lista()

    botao_excluir = tkinter.Button(
        janela,
        text="Excluir selecionada",
        bg=malva,
        fg=branco,
        activebackground=hover_roxo,
        activeforeground=branco,
        font=("Arial", 11, "bold"),
        relief="flat",
        cursor="hand2",
        command=excluir_selecionada
    )
    botao_excluir.pack(pady=10, ipadx=15, ipady=5)


# ------------------------------ GERAR RELATÓRIO ------------------------------

def adicionar_relatorio():
    receitas, despesas, saldo = calcular_totais()
    quantidade = len(movimentacoes)

    mensagem = (
        "RELATÓRIO FINANCEIRO\n\n"
        f"Total de receitas: {formatar_valor(receitas)}\n\n"
        f"Total de despesas: {formatar_valor(despesas)}\n\n"
        f"Saldo atual: {formatar_valor(saldo)}\n\n"
        f"Quantidade de movimentações: {quantidade}"
    )

    messagebox.showinfo("Relatório Financeiro", mensagem, parent=root)


# ------------------------------ BOTÕES DO MENU ------------------------------

def criar_botao(parent, texto, comando, cor):
    botao = tkinter.Button(
        parent,
        text=texto,
        bg=cor,
        fg=branco,
        activebackground=hover_roxo,
        activeforeground=branco,
        font=("Arial", 11, "bold"),
        relief="flat",
        cursor="hand2",
        command=comando
    )

    # Deixa o hover em um roxo mais discreto.
    botao.bind("<Enter>", lambda evento: botao.configure(bg=hover_roxo))
    botao.bind("<Leave>", lambda evento: botao.configure(bg=cor))
    return botao


def sair():
    confirmar = messagebox.askyesno(
        "Sair",
        "Deseja encerrar o Controle de Gastos?",
        parent=root
    )

    if confirmar:
        root.destroy()


# ------------------------------ CABEÇALHO ------------------------------

cabecalho = tkinter.Frame(root, bg=preto)
cabecalho.pack(fill="x", padx=30, pady=20)

titulo = tkinter.Label(
    cabecalho,
    text="Andriele | Controle de Gastos",
    bg=preto,
    fg=branco,
    font=("Arial", 23, "bold")
)
titulo.pack(side="left")

subtitulo = tkinter.Label(
    cabecalho,
    text="CONTROLE FINANCEIRO PESSOAL",
    bg=preto,
    fg=rosa_claro,
    font=("Arial", 9, "bold")
)
subtitulo.pack(side="right", pady=10)


# ------------------------------ PAINEL DE SALDO ------------------------------

painel = tkinter.Frame(root, bg=roxo)
painel.pack(fill="x", padx=30, pady=10)

label_saldo = tkinter.Label(
    painel,
    text="SALDO DISPONÍVEL",
    bg=roxo,
    fg=rosa_claro,
    font=("Arial", 11, "bold")
)
label_saldo.pack(anchor="w", padx=20, pady=(15, 5))

valor_saldo = tkinter.Label(
    painel,
    text="R$ 0,00",
    bg=roxo,
    fg=branco,
    font=("Arial", 27, "bold")
)
valor_saldo.pack(anchor="w", padx=20, pady=(0, 15))


# ------------------------------ RESUMO FINANCEIRO ------------------------------

resumo = tkinter.Frame(root, bg=preto)
resumo.pack(fill="x", padx=30, pady=10)

card_receitas = tkinter.Frame(resumo, bg=azul_roxo)
card_receitas.pack(side="left", fill="both", expand=True, padx=(0, 8))

card_despesas = tkinter.Frame(resumo, bg=azul_roxo)
card_despesas.pack(side="left", fill="both", expand=True, padx=(8, 0))

tkinter.Label(
    card_receitas,
    text="TOTAL DE RECEITAS",
    bg=azul_roxo,
    fg=rosa_claro,
    font=("Arial", 10, "bold")
).pack(pady=(12, 5))

valor_receitas = tkinter.Label(
    card_receitas,
    text="R$ 0,00",
    bg=azul_roxo,
    fg=branco,
    font=("Arial", 16, "bold")
)
valor_receitas.pack(pady=(0, 12))

tkinter.Label(
    card_despesas,
    text="TOTAL DE DESPESAS",
    bg=azul_roxo,
    fg=rosa_claro,
    font=("Arial", 10, "bold")
).pack(pady=(12, 5))

valor_despesas = tkinter.Label(
    card_despesas,
    text="R$ 0,00",
    bg=azul_roxo,
    fg=branco,
    font=("Arial", 16, "bold")
)
valor_despesas.pack(pady=(0, 12))


# ------------------------------ MENU DE FUNCIONALIDADES ------------------------------

titulo_menu = tkinter.Label(
    root,
    text="FUNCIONALIDADES",
    bg=preto,
    fg=rosa_claro,
    font=("Arial", 11, "bold")
)
titulo_menu.pack(anchor="w", padx=30, pady=(15, 5))

menu = tkinter.Frame(root, bg=preto)
menu.pack(fill="x", padx=25)

botoes = [
    ("Adicionar Receita", adicionar_receita, roxo),
    ("Adicionar Despesa", adicionar_despesa, roxo),
    ("Listar Movimentações", listar_movimentacoes, azul_roxo),
    ("Consultar Saldo", adicionar_saldo, azul_roxo),
    ("Excluir Movimentação", adicionar_excluir, azul_roxo),
    ("Gerar Relatório", adicionar_relatorio, roxo)
]

for indice, (texto, comando, cor) in enumerate(botoes):
    botao = criar_botao(menu, texto, comando, cor)
    botao.grid(
        row=indice // 2,
        column=indice % 2,
        padx=5,
        pady=5,
        sticky="nsew",
        ipady=8
    )

menu.grid_columnconfigure(0, weight=1)
menu.grid_columnconfigure(1, weight=1)

botao_sair = criar_botao(root, "Sair", sair, azul_roxo)
botao_sair.pack(pady=(8, 0), ipadx=30, ipady=4)


# ------------------------------ MOVIMENTAÇÕES RECENTES ------------------------------

titulo_historico = tkinter.Label(
    root,
    text="MOVIMENTAÇÕES RECENTES",
    bg=preto,
    fg=rosa_claro,
    font=("Arial", 11, "bold")
)
titulo_historico.pack(anchor="w", padx=30, pady=(15, 5))

configurar_tabela()

tabela_principal = ttk.Treeview(
    root,
    columns=("id", "data", "descricao", "tipo", "valor"),
    show="headings",
    height=5
)

tabela_principal.heading("id", text="ID")
tabela_principal.heading("data", text="Data")
tabela_principal.heading("descricao", text="Descrição")
tabela_principal.heading("tipo", text="Tipo")
tabela_principal.heading("valor", text="Valor")

tabela_principal.column("id", width=45, anchor="center")
tabela_principal.column("data", width=140, anchor="center")
tabela_principal.column("descricao", width=220)
tabela_principal.column("tipo", width=100, anchor="center")
tabela_principal.column("valor", width=120, anchor="center")

tabela_principal.pack(fill="x", padx=30, pady=5)


# ------------------------------ RODAPÉ ------------------------------

rodape = tkinter.Label(
    root,
    text="CONTROLE DE GASTOS | GERENCIAMENTO FINANCEIRO",
    bg=preto,
    fg=rosa_claro,
    font=("Arial", 9)
)
rodape.pack(side="bottom", pady=12)


# ------------------------------ INICIAR SISTEMA ------------------------------

carregar_dados()
atualizar_dashboard()

root.protocol("WM_DELETE_WINDOW", sair)
root.mainloop()
