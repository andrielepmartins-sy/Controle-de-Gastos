import tkinter
import os
import json 

root = tkinter.Tk()

root.title("Gerenciamento de gastos pessoais")
root.geometry("600x500")
root.configure(bg="black" )

roxo = "#edadfc"
lilas = "#DA8BF1"
preto =  "#000000"
rosa = "#E478BA"
branco = "#FFFFFF"

label = tkinter.Label(root, text="Seja bem-vindo ao sistema de gastos pessoais.",
                      bg= preto,
                      fg= branco,
                      font=("Arial", 16, "bold"))

label.pack(pady=25)

# ------------------------------ FUNÇÕES  --------------------------- 

def adicionar_receita():
    print("Abrir cadastro de receita")

def adicionar_despesa():
    print("Abrir cadastro de despesas")


# ------------------------------ BOTÕES ------------------------------  

botao_receita = tkinter.Button(
    root,
    text="Adicionar Receita",
    font=("Arial", 12, "bold"),
    bg=roxo,
    fg= branco,
    width=20,
    command=adicionar_receita
)

botao_receita.pack(pady=20)

botao_despesa = tkinter.Button(
    root,
    text="Adicionar Despesa",
    font=("Arial", 12, "bold"),
    bg=roxo,
    fg= branco,
    width=20,
    command=adicionar_despesa
)

botao_despesa.pack(pady=10)

botao_listar = tkinter.Button(
    root,
    text="Listar Movimentações",
    font=("Arial", 12, "bold"),
    bg=rosa,
    fg=preto,
    width=20
)

botao_listar.pack(pady=10)


botao_saldo = tkinter.Button(
    root,
    text="Consultar Saldo",
    font=("Arial", 12, "bold"),
    bg=rosa,
    fg=preto,
    width=20
)

botao_saldo.pack(pady=10)

botao_excluir = tkinter.Button(
    root,
    text="Excluir Movimentação",
    font=("Arial", 12, "bold"),
    bg=rosa,
    fg=preto,
    width=20
)

botao_excluir.pack(pady=10)


botao_relatorio = tkinter.Button(
    root,
    text="Gerar Relatório",
    font=("Arial", 12, "bold"),
    bg=rosa,
    fg=preto,
    width=20
)

botao_relatorio.pack(pady=10)


botao_sair = tkinter.Button(
    root,
    text = "Sair",
    bg = lilas,
    fg= preto,
    width= 20,
    command= root.destroy
)

botao_sair.pack(pady=10)



root.mainloop()