# Controle de Gastos Pessoais

Sistema de controle financeiro pessoal desenvolvido em Python, com interface gráfica utilizando Tkinter e armazenamento de dados em JSON.

O projeto tem como objetivo facilitar o gerenciamento financeiro, permitindo registrar receitas e despesas, acompanhar o saldo disponível e consultar o histórico de movimentações.

## Funcionalidades

- **Adicionar Receita:** registra entradas financeiras.
- **Adicionar Despesa:** registra saídas financeiras.
- **Listar Movimentações:** apresenta o histórico de registros.
- **Consultar Saldo:** calcula automaticamente o saldo disponível.
- **Excluir Movimentação:** permite remover registros existentes.
- **Gerar Relatório:** apresenta o resumo financeiro, incluindo receitas, despesas, saldo e quantidade de movimentações.

## Tecnologias Utilizadas

- Python
- Tkinter – desenvolvimento da interface gráfica.
- JSON – armazenamento e persistência dos dados.
- Decimal – precisão nos cálculos financeiros.
- Datetime – registro automático de data e hora.

## Interface

O sistema possui uma interface gráfica com:

- Painel de saldo disponível.
- Resumo de receitas e despesas.
- Histórico das movimentações recentes.
- Janelas específicas para cadastro e exclusão de registros.

## Armazenamento de Dados

As movimentações são armazenadas no arquivo `dados.json`.

O sistema realiza automaticamente:

- Criação do arquivo caso ele não exista.
- Carregamento dos registros ao iniciar.
- Salvamento após inclusões e exclusões.
- Verificação dos dados carregados.

Dessa forma, as informações permanecem disponíveis mesmo após o encerramento do programa.

## Validações

O sistema possui mecanismos para evitar registros inválidos:

- Não permite valores iguais ou inferiores a zero.
- Não permite descrições vazias.
- Verifica se o valor informado é numérico.
- Aceita valores com até duas casas decimais.
- Apresenta mensagens de erro e confirmação durante as operações.

## Como Executar

**1.** Certifique-se de ter o Python instalado.

**2.** Clone este repositório:

```bash
git clone URL_DO_REPOSITORIO
```

**3.** Entre na pasta do projeto:

```bash
cd nome-do-projeto
```

**4.** Execute o programa:

```bash
python main.py
```

O arquivo `dados.json` será criado automaticamente na pasta do programa caso ainda não exista.

## Objetivo Educacional

Este projeto foi desenvolvido como atividade prática para aplicar conhecimentos de programação, incluindo:

- Variáveis e tipos de dados.
- Estruturas condicionais.
- Laços de repetição.
- Listas e dicionários.
- Funções e modularização.
- Manipulação de arquivos.
- Persistência de dados em JSON.
- Validação e tratamento de erros.

---

**Projeto:** Controle de Gastos Pessoais  
**Linguagem:** Python  
**Interface gráfica:** Tkinter  
**Armazenamento:** JSON
