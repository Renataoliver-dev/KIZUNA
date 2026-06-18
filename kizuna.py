import sqlite3
import tkinter as tk
from tkinter import messagebox
import random


DB_NAME = "kizuna.db"


class Banco:
    def __init__(self):
        self.con = sqlite3.connect(DB_NAME)
        self.criar_tabelas()

    def criar_tabelas(self):
        cur = self.con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS amizades (
                usuario1 INTEGER NOT NULL,
                usuario2 INTEGER NOT NULL,
                PRIMARY KEY (usuario1, usuario2),
                FOREIGN KEY (usuario1) REFERENCES usuarios(id),
                FOREIGN KEY (usuario2) REFERENCES usuarios(id)
            )
        """)

        self.con.commit()

    def cadastrar_usuario(self, nome, idade):
        cur = self.con.cursor()

        for _ in range(9000):
            novo_id = random.randint(1000, 9999)

            if not self.buscar_usuario(novo_id):
                cur.execute(
                    "INSERT INTO usuarios (id, nome, idade) VALUES (?, ?, ?)",
                    (novo_id, nome, idade)
                )
                self.con.commit()
                return novo_id

        raise ValueError("Nao foi possivel gerar um ID disponivel.")

    def buscar_usuario(self, user_id):
        cur = self.con.cursor()
        cur.execute("SELECT id, nome, idade FROM usuarios WHERE id = ?", (user_id,))
        return cur.fetchone()

    def listar_usuarios(self, termo=""):
        cur = self.con.cursor()

        if termo:
            cur.execute("""
                SELECT id, nome, idade
                FROM usuarios
                WHERE nome LIKE ? OR CAST(id AS TEXT) LIKE ?
                ORDER BY nome
            """, (f"%{termo}%", f"%{termo}%"))
        else:
            cur.execute("""
                SELECT id, nome, idade
                FROM usuarios
                ORDER BY nome
            """)

        return cur.fetchall()

    def contar_amigos(self, user_id):
        cur = self.con.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM amizades
            WHERE usuario1 = ? OR usuario2 = ?
        """, (user_id, user_id))
        return cur.fetchone()[0]

    def sao_amigos(self, id1, id2):
        a, b = sorted([id1, id2])
        cur = self.con.cursor()
        cur.execute("""
            SELECT 1 FROM amizades
            WHERE usuario1 = ? AND usuario2 = ?
        """, (a, b))
        return cur.fetchone() is not None

    def criar_amizade(self, id1, id2):
        if id1 == id2:
            raise ValueError("Voce nao pode adicionar voce mesmo.")

        if not self.buscar_usuario(id2):
            raise ValueError("Usuario nao encontrado.")

        if self.sao_amigos(id1, id2):
            raise ValueError("Essa amizade ja existe.")

        a, b = sorted([id1, id2])

        cur = self.con.cursor()
        cur.execute(
            "INSERT INTO amizades (usuario1, usuario2) VALUES (?, ?)",
            (a, b)
        )
        self.con.commit()

    def remover_amizade(self, id1, id2):
        if not self.sao_amigos(id1, id2):
            raise ValueError("Essa amizade nao existe.")

        a, b = sorted([id1, id2])

        cur = self.con.cursor()
        cur.execute(
            "DELETE FROM amizades WHERE usuario1 = ? AND usuario2 = ?",
            (a, b)
        )
        self.con.commit()

    def listar_amigos(self, user_id):
        cur = self.con.cursor()
        cur.execute("""
            SELECT u.id, u.nome, u.idade
            FROM usuarios u
            JOIN amizades a
            ON (
                (a.usuario1 = ? AND a.usuario2 = u.id)
                OR
                (a.usuario2 = ? AND a.usuario1 = u.id)
            )
            ORDER BY u.nome
        """, (user_id, user_id))
        return cur.fetchall()

    def remover_usuario(self, user_id):
        cur = self.con.cursor()
        cur.execute(
            "DELETE FROM amizades WHERE usuario1 = ? OR usuario2 = ?",
            (user_id, user_id)
        )
        cur.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        self.con.commit()


class KizunaApp:
    def __init__(self):
        self.banco = Banco()
        self.usuario_logado = None

        self.root = tk.Tk()
        self.root.title("Kizuna")
        self.root.geometry("370x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#202124")

        self.phone = tk.Frame(
            self.root,
            bg="#f4f7fb",
            width=335,
            height=610,
            highlightbackground="#111",
            highlightthickness=4
        )
        self.phone.pack(pady=16)
        self.phone.pack_propagate(False)

        self.tela_login()

    def limpar(self):
        for widget in self.phone.winfo_children():
            widget.destroy()

    def titulo(self, texto, subtitulo=None):
        tk.Label(
            self.phone,
            text=texto,
            bg="#f4f7fb",
            fg="#1d3557",
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(22, 4))

        if subtitulo:
            tk.Label(
                self.phone,
                text=subtitulo,
                bg="#f4f7fb",
                fg="#617083",
                font=("Segoe UI", 9)
            ).pack(pady=(0, 14))

    def botao(self, parent, texto, comando, cor="#2563eb"):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=cor,
            fg="white",
            activebackground=cor,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            height=2
        )

    def entrada(self, parent, placeholder=""):
        entrada = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="flat",
            bg="white",
            fg="#111827",
            insertbackground="#111827"
        )
        entrada.insert(0, placeholder)

        def foco_in(event):
            if entrada.get() == placeholder:
                entrada.delete(0, tk.END)

        def foco_out(event):
            if not entrada.get():
                entrada.insert(0, placeholder)

        entrada.bind("<FocusIn>", foco_in)
        entrada.bind("<FocusOut>", foco_out)
        return entrada

    def tela_login(self):
        self.limpar()
        self.titulo("Kizuna", " mini rede social")

        card = tk.Frame(self.phone, bg="white")
        card.pack(padx=22, pady=8, fill="x")

        tk.Label(
            card,
            text="Login",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=(14, 6))

        id_login = self.entrada(card, "Digite seu ID")
        id_login.pack(padx=16, pady=7, fill="x", ipady=9)

        def entrar():
            try:
                user_id = int(id_login.get())
                usuario = self.banco.buscar_usuario(user_id)

                if not usuario:
                    messagebox.showerror("Erro", "ID nao encontrado.")
                    return

                self.usuario_logado = usuario
                self.tela_principal()

            except ValueError:
                messagebox.showerror("Erro", "Digite um ID valido.")

        self.botao(card, "Entrar", entrar).pack(padx=16, pady=12, fill="x")

        tk.Label(
            self.phone,
            text="Ainda nao tem conta?",
            bg="#f4f7fb",
            fg="#617083",
            font=("Segoe UI", 9)
        ).pack(pady=(22, 6))

        self.botao(
            self.phone,
            "Criar cadastro",
            self.tela_cadastro,
            "#10b981"
        ).pack(padx=38, fill="x")

    def tela_cadastro(self):
        self.limpar()
        self.titulo("Cadastro", "crie sua conta no Kizuna")

        card = tk.Frame(self.phone, bg="white")
        card.pack(padx=22, pady=12, fill="x")

        nome = self.entrada(card, "Nome completo")
        nome.pack(padx=16, pady=(20, 7), fill="x", ipady=9)

        idade = self.entrada(card, "Idade")
        idade.pack(padx=16, pady=7, fill="x", ipady=9)

        def cadastrar():
            nome_valor = nome.get().strip()

            try:
                idade_valor = int(idade.get())
            except ValueError:
                messagebox.showerror("Erro", "Digite uma idade valida.")
                return

            if not nome_valor or nome_valor == "Nome completo":
                messagebox.showerror("Erro", "Digite seu nome.")
                return

            if idade_valor <= 0:
                messagebox.showerror("Erro", "A idade deve ser maior que zero.")
                return

            novo_id = self.banco.cadastrar_usuario(nome_valor, idade_valor)

            messagebox.showinfo(
                "Cadastro feito",
                f"Seu ID de login e: {novo_id}\n\nGuarde esse numero para entrar depois."
            )

            self.tela_login()

        self.botao(card, "Cadastrar", cadastrar, "#10b981").pack(
            padx=16,
            pady=16,
            fill="x"
        )

        self.botao(
            self.phone,
            "Voltar ao login",
            self.tela_login,
            "#6b7280"
        ).pack(padx=38, pady=10, fill="x")

    def barra_superior(self):
        user_id, nome, idade = self.usuario_logado

        topo = tk.Frame(self.phone, bg="#2563eb", height=78)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        tk.Label(
            topo,
            text=f"Ola, {nome.split()[0]}",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=18, pady=(12, 0))

        tk.Label(
            topo,
            text=f"ID: {user_id} | {idade} anos",
            bg="#2563eb",
            fg="#dbeafe",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=18)

    def menu_inferior(self):
        menu = tk.Frame(self.phone, bg="white", height=56)
        menu.pack(side="bottom", fill="x")
        menu.pack_propagate(False)

        self.botao(menu, "Perfis", self.tela_principal, "#2563eb").pack(
            side="left", expand=True, fill="both", padx=3, pady=7
        )
        self.botao(menu, "Amigos", self.tela_amigos, "#7c3aed").pack(
            side="left", expand=True, fill="both", padx=3, pady=7
        )
        self.botao(menu, "Conta", self.tela_conta, "#374151").pack(
            side="left", expand=True, fill="both", padx=3, pady=7
        )

    def area_rolavel(self):
        container = tk.Frame(self.phone, bg="#f4f7fb")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#f4f7fb", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

        conteudo = tk.Frame(canvas, bg="#f4f7fb")
        conteudo.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=conteudo, anchor="nw", width=315)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return conteudo

    def card_usuario(self, parent, usuario):
        id_user, nome, idade = usuario
        meu_id = self.usuario_logado[0]

        card = tk.Frame(parent, bg="white")
        card.pack(padx=12, pady=6, fill="x")

        amigos = self.banco.contar_amigos(id_user)

        tk.Label(
            card,
            text=nome,
            bg="white",
            fg="#111827",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 0))

        tk.Label(
            card,
            text=f"ID: {id_user} | {idade} anos | {amigos} amigos",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=12, pady=(2, 8))

        if id_user != meu_id:
            if self.banco.sao_amigos(meu_id, id_user):
                texto = "Remover amizade"
                cor = "#ef4444"
                comando = lambda: self.remover_amizade(id_user)
            else:
                texto = "Adicionar amigo"
                cor = "#10b981"
                comando = lambda: self.adicionar_amizade(id_user)

            self.botao(card, texto, comando, cor).pack(
                padx=12,
                pady=(0, 10),
                fill="x"
            )

    def tela_principal(self):
        self.limpar()
        self.barra_superior()

        busca_frame = tk.Frame(self.phone, bg="#f4f7fb")
        busca_frame.pack(fill="x", padx=14, pady=10)

        busca = self.entrada(busca_frame, "Pesquisar por nome ou ID")
        busca.pack(fill="x", ipady=9)

        conteudo = self.area_rolavel()

        def carregar():
            for widget in conteudo.winfo_children():
                widget.destroy()

            termo = busca.get().strip()
            if termo == "Pesquisar por nome ou ID":
                termo = ""

            usuarios = self.banco.listar_usuarios(termo)

            if not usuarios:
                tk.Label(
                    conteudo,
                    text="Nenhum usuario encontrado.",
                    bg="#f4f7fb",
                    fg="#6b7280",
                    font=("Segoe UI", 10)
                ).pack(pady=24)
                return

            for usuario in usuarios:
                self.card_usuario(conteudo, usuario)

        busca.bind("<KeyRelease>", lambda e: carregar())

        carregar()
        self.menu_inferior()

    def adicionar_amizade(self, id_amigo):
        try:
            self.banco.criar_amizade(self.usuario_logado[0], id_amigo)
            messagebox.showinfo("Sucesso", "Amizade criada com sucesso.")
            self.tela_principal()
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def remover_amizade(self, id_amigo):
        try:
            self.banco.remover_amizade(self.usuario_logado[0], id_amigo)
            messagebox.showinfo("Sucesso", "Amizade removida com sucesso.")
            self.tela_principal()
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def tela_amigos(self):
        self.limpar()
        self.barra_superior()

        tk.Label(
            self.phone,
            text="Meus amigos",
            bg="#f4f7fb",
            fg="#1d3557",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=18, pady=12)

        conteudo = self.area_rolavel()
        amigos = self.banco.listar_amigos(self.usuario_logado[0])

        if not amigos:
            tk.Label(
                conteudo,
                text="Voce ainda nao adicionou amigos.",
                bg="#f4f7fb",
                fg="#6b7280",
                font=("Segoe UI", 10)
            ).pack(pady=24)
        else:
            for amigo in amigos:
                self.card_usuario(conteudo, amigo)

        self.menu_inferior()

    def tela_conta(self):
        self.limpar()
        self.barra_superior()

        user_id, nome, idade = self.usuario_logado
        total_amigos = self.banco.contar_amigos(user_id)

        card = tk.Frame(self.phone, bg="white")
        card.pack(padx=22, pady=22, fill="x")

        tk.Label(
            card,
            text=nome,
            bg="white",
            fg="#111827",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(20, 4))

        tk.Label(
            card,
            text=f"ID de login: {user_id}",
            bg="white",
            fg="#2563eb",
            font=("Segoe UI", 12, "bold")
        ).pack()

        tk.Label(
            card,
            text=f"Idade: {idade} anos\nAmigos: {total_amigos}",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 10)
        ).pack(pady=12)

        def sair():
            self.usuario_logado = None
            self.tela_login()

        def excluir():
            confirmar = messagebox.askyesno(
                "Excluir conta",
                "Tem certeza que deseja excluir sua conta?"
            )

            if confirmar:
                self.banco.remover_usuario(user_id)
                self.usuario_logado = None
                messagebox.showinfo("Conta excluida", "Sua conta foi removida.")
                self.tela_login()

        self.botao(card, "Sair da conta", sair, "#6b7280").pack(
            padx=16,
            pady=(6, 8),
            fill="x"
        )

        self.botao(card, "Excluir minha conta", excluir, "#ef4444").pack(
            padx=16,
            pady=(0, 18),
            fill="x"
        )

        self.menu_inferior()

    def iniciar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = KizunaApp()
    app.iniciar()


        



