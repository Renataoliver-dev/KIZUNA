# Kizuna - Mini Rede Social

**Kizuna** é uma aplicação desktop desenvolvida em Python que simula uma rede social simples.  
O sistema permite cadastrar usuários, realizar login, pesquisar perfis, criar amizades, remover amizades e excluir contas.

A aplicação possui uma interface gráfica feita com **Tkinter**, no estilo de uma tela de celular, e utiliza **SQLite** para armazenar os dados de forma permanente.

---

## Objetivo

O objetivo do projeto é simular as principais funcionalidades de uma rede social, aplicando conceitos de organização de dados, relacionamento entre usuários, validações e persistência em banco de dados.


## Funcionalidades

- Cadastro de usuários com nome completo e idade
- Geração automática de ID único com 4 dígitos
- Login utilizando o ID gerado no cadastro
- Listagem de todos os perfis cadastrados
- Pesquisa de usuários por nome ou ID
- Criação de amizade entre usuários
- Remoção de amizade
- Listagem dos amigos do usuário logado
- Exclusão de conta
- Remoção automática das amizades ao excluir um usuário
- Armazenamento permanente dos dados em banco SQLite
- Interface gráfica em janela própria, sem uso de navegador

---

## Tecnologias Utilizadas

| Tecnologia | Uso no Projeto |
|---|---|
| Python 3 | Linguagem principal do sistema |
| Tkinter | Criação da interface gráfica |
| SQLite | Banco de dados local |
| Random | Geração automática de IDs de 4 dígitos |

---

## Como Executar

### 1. Verificar se o Python está instalado

No terminal, execute:

```bash
python --version
```

Ou, no Windows:

```bash
py --version
```

### 2. Executar o projeto

Na pasta onde está o arquivo `kizuna.py`, execute:

```bash
python kizuna.py
```

Ou:

```bash
py kizuna.py
```

O projeto não precisa de bibliotecas externas, pois utiliza apenas recursos nativos do Python.

---

## Arquivos do Projeto

| Arquivo | Descrição |
|---|---|
| `kizuna.py` | Arquivo principal com todo o código do sistema |
| `kizuna.db` | Banco de dados gerado automaticamente |
| `README.md` | Documentação do projeto |

O arquivo `kizuna.db` é criado automaticamente quando o programa é executado pela primeira vez.

---

## Banco de Dados

O sistema utiliza o banco de dados **SQLite** para guardar as informações dos usuários e das amizades.

O banco é salvo no arquivo:

```text
kizuna.db
```

Dessa forma, mesmo que o programa seja fechado, os dados continuam armazenados. Ao abrir o sistema novamente, o usuário pode fazer login com o mesmo ID gerado anteriormente.

---

## Estrutura do Banco de Dados

O banco possui duas tabelas principais:

- `usuarios`
- `amizades`

---

## Tabela `usuarios`

A tabela `usuarios` armazena os dados principais de cada pessoa cadastrada.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | INTEGER PRIMARY KEY | Sim | Identificador único do usuário |
| `nome` | TEXT | Sim | Nome completo do usuário |
| `idade` | INTEGER | Sim | Idade do usuário |

### Criação da tabela `usuarios`

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL
);
```

O campo `id` é definido como `PRIMARY KEY`, garantindo que não existam dois usuários com o mesmo identificador.

---

## Tabela `amizades`

A tabela `amizades` armazena os relacionamentos entre os usuários.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `usuario1` | INTEGER | Sim | ID de um dos usuários da amizade |
| `usuario2` | INTEGER | Sim | ID do outro usuário da amizade |

### Criação da tabela `amizades`

```sql
CREATE TABLE IF NOT EXISTS amizades (
    usuario1 INTEGER NOT NULL,
    usuario2 INTEGER NOT NULL,
    PRIMARY KEY (usuario1, usuario2),
    FOREIGN KEY (usuario1) REFERENCES usuarios(id),
    FOREIGN KEY (usuario2) REFERENCES usuarios(id)
);
```

A chave primária composta por `usuario1` e `usuario2` impede que a mesma amizade seja cadastrada mais de uma vez.

---

## Como o Sistema Representa as Amizades

As amizades são armazenadas por meio dos IDs dos usuários.

Exemplo:

| usuario1 | usuario2 |
|---|---|
| 1234 | 5678 |

Isso significa que o usuário de ID `1234` é amigo do usuário de ID `5678`.

A amizade é considerada bidirecional. Portanto, se o usuário `1234` é amigo do usuário `5678`, o usuário `5678` também é amigo do usuário `1234`.

Para evitar duplicidade, o sistema organiza os IDs antes de salvar a amizade no banco.

Exemplo:

```python
a, b = sorted([id1, id2])
```

Assim, a amizade entre `1234` e `5678` sempre será salva da mesma forma, independentemente de quem adicionou quem.

---

## Regras de Validação

O sistema possui validações para evitar erros e inconsistências.

| Regra | Como o sistema trata |
|---|---|
| Não permitir IDs duplicados | O ID é chave primária no banco e é verificado antes do cadastro |
| Não permitir amizade consigo mesmo | O sistema compara os dois IDs antes de criar a amizade |
| Não permitir amizade duplicada | O sistema consulta o banco antes de inserir uma nova amizade |
| Não permitir amizade com usuário inexistente | O sistema verifica se o ID informado existe |
| Remover amizades ao excluir usuário | As amizades relacionadas ao usuário são apagadas antes da exclusão da conta |

---

## Requisitos Atendidos

### Adicionar Usuário

Cada usuário cadastrado possui:

- ID único
- Nome completo
- Idade
- Lista de amigos representada pela tabela `amizades`

O cadastro gera automaticamente um ID de 4 dígitos e impede duplicidade.

---

### Remover Usuário

Ao excluir uma conta, o sistema remove primeiro todas as amizades relacionadas ao usuário.

```sql
DELETE FROM amizades
WHERE usuario1 = ? OR usuario2 = ?;
```

Depois, remove o usuário da tabela `usuarios`.

```sql
DELETE FROM usuarios
WHERE id = ?;
```

---

### Criar Amizade

A amizade é criada entre dois usuários cadastrados.

O sistema impede:

- Amizade duplicada
- Amizade com o próprio usuário
- Amizade com usuário inexistente

A relação é salva na tabela `amizades`.

---

### Remover Amizade

O sistema permite remover o vínculo entre dois usuários amigos, apagando o registro correspondente da tabela `amizades`.

---

### Listar Amigos

A tela **Amigos** exibe todos os amigos do usuário logado, mostrando informações como nome, ID e idade.

---

### Listar Perfis

A tela principal lista os usuários cadastrados e exibe:

- Nome
- ID
- Idade
- Número de amigos

---

### Persistência de Dados

Os dados ficam salvos no banco `kizuna.db`.  
Isso permite que os usuários cadastrados continuem existindo mesmo após fechar o programa.

---

### Interface Gráfica

A interface foi desenvolvida com Tkinter e simula uma tela de aplicativo mobile.

O sistema possui as seguintes telas:

| Tela | Função |
|---|---|
| Login | Permite acessar uma conta usando o ID |
| Cadastro | Permite criar uma nova conta |
| Principal | Mostra os perfis cadastrados e a busca |
| Amigos | Mostra os amigos do usuário logado |
| Conta | Mostra dados da conta e opções de sair ou excluir |

---

## Estrutura do Código

O código está concentrado no arquivo `kizuna.py`.

Ele possui duas classes principais:

---

## Classe `Banco`

A classe `Banco` é responsável por toda a parte de armazenamento e manipulação dos dados.

Principais responsabilidades:

- Criar as tabelas do banco
- Cadastrar usuários
- Buscar usuários por ID
- Listar usuários
- Criar amizades
- Remover amizades
- Listar amigos
- Contar amigos
- Remover usuários

---

## Classe `KizunaApp`

A classe `KizunaApp` é responsável pela interface gráfica.

Principais responsabilidades:

- Criar a janela principal
- Exibir a tela de login
- Exibir a tela de cadastro
- Exibir a tela principal
- Exibir a tela de amigos
- Exibir a tela da conta
- Criar botões, campos de entrada e cards de usuários
- Conectar as ações da interface com o banco de dados

---

## Como Usar

### Cadastro

1. Abra o programa.
2. Clique em **Criar cadastro**.
3. Digite seu nome completo.
4. Digite sua idade.
5. Clique em **Cadastrar**.
6. Guarde o ID de 4 dígitos gerado pelo sistema.

---

### Login

1. Na tela inicial, digite o ID gerado no cadastro.
2. Clique em **Entrar**.
3. Se o ID existir, o sistema abrirá a tela principal.

---

### Adicionar Amigo

1. Acesse a tela principal.
2. Procure o usuário desejado.
3. Clique em **Adicionar amigo**.

---

### Remover Amizade

1. Acesse a tela principal ou a tela de amigos.
2. Encontre o usuário já adicionado.
3. Clique em **Remover amizade**.

---

### Excluir Conta

1. Acesse a tela **Conta**.
2. Clique em **Excluir minha conta**.
3. Confirme a exclusão.

Ao excluir a conta, todas as amizades relacionadas a ela também são removidas.

---

## Observação

Caso queira apagar todos os dados cadastrados e começar do zero, exclua o arquivo:

```text
kizuna.db
```

Na próxima execução, o programa criará um novo banco automaticamente.

---

## Autor

<div align="center">

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Renataoliver-dev">
        <img src="https://github.com/Renataoliver-dev.png" width="100px;" alt="Foto de Renata Oliveira"/>
        <br />
        <sub><b>Renata Oliveira</b></sub>
        <br />
        <sub>@Renataoliver-dev</sub>
      </a>
    </td>
  </tr>
</table>

</div>
