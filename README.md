# 🧾 Sistema de Controle de Caixa - Deise Lanches

Este é um sistema simples de **Controle de Caixa** para gerenciar transações de entrada e saída de valores em um caixa, desenvolvido com **Tkinter** e **SQLite**.

## 📋 Funcionalidades

- Registrar **Entradas** e **Saídas** de valores
- Exibir o saldo atual do caixa
- Gerar relatórios de transações com ou sem exclusão de registros
- Excluir registros de transações com validação de senha


## 🚀 Como Utilizar

1. **Registrar uma transação**:
   - Preencha o valor e a descrição da transação.
   - Clique no botão **Registrar Entrada** para adicionar uma entrada ou **Registrar Saída** para registrar uma saída.

2. **Gerar Relatório**:
   - Clique no botão **Gerar Relatório**.
   - Um modal aparecerá perguntando se você deseja gerar o relatório e **limpar** os registros do banco de dados.
   - **Opções**:
     - **Sim**: Gera o relatório e exclui todos os registros.
     - **Não**: Gera o relatório sem excluir os registros.
     - **Cancelar**: Cancela a operação de gerar o relatório.

3. **Excluir Transações**:
   - Selecione uma transação na lista.
   - Clique no botão **Excluir Registro**.
   - Será solicitada uma **senha** para confirmar a exclusão.


## 🔑 Senha para Excluir Transações

A senha padrão para exclusão de registros ou para a geração de relatórios com exclusão de dados é:

```plaintext
admin

```
## 💡 Dicas de Uso

Certifique-se de preencher todos os campos antes de registrar uma transação.
O saldo é automaticamente atualizado após cada transação registrada ou excluída.
Os relatórios gerados são salvos na pasta relatorios no formato .txt com a data e hora da criação no nome do arquivo.
Se você deseja apenas gerar um relatório sem perder os dados, escolha a opção Não no modal de geração de relatório.


## 🛠️ Tecnologias Utilizadas

Python: Linguagem principal
Tkinter: Interface gráfica
SQLite: Banco de dados local


## 📂 Estrutura de Arquivos

```plaintext
├── deise_lanches.db     # Banco de dados SQLite
├── relatorios/          # Pasta onde os relatórios são gerados
├── main.py              # Código principal do sistema
└── deise_lanches_logo.png  # Logo utilizado na interface
```

## 🎨 Interface

A interface do sistema é simples e funcional, garantindo uma navegação fácil para os usuários.

