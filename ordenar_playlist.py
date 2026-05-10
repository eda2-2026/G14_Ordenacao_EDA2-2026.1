import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ==================================================
# FUNÇÃO MERGE
# ==================================================

def merge(esquerda, direita, chave):

    resultado = []

    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):

        valor_esq = esquerda[i][chave].lower()
        valor_dir = direita[j][chave].lower()

        if valor_esq <= valor_dir:
            resultado.append(esquerda[i])
            i += 1

        else:
            resultado.append(direita[j])
            j += 1

    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado


# ==================================================
# MERGE SORT
# ==================================================

def merge_sort(lista, chave):

    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2

    esquerda = merge_sort(lista[:meio], chave)
    direita = merge_sort(lista[meio:], chave)

    return merge(esquerda, direita, chave)


# ==================================================
# CARREGAR MÚSICAS
# ==================================================

def carregar_musicas(caminho):

    musicas = []

    try:

        with open(caminho, encoding='utf-8') as arquivo:

            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                musicas.append(linha)

    except FileNotFoundError:

        messagebox.showerror(
            'Erro',
            'Arquivo musicas.csv não encontrado.'
        )

    return musicas


# ==================================================
# EXPORTAR CSV
# ==================================================

def exportar_csv(lista):

    with open(
        'playlist_exportada.csv',
        'w',
        newline='',
        encoding='utf-8'
    ) as arquivo:

        campos = [
            'nome',
            'album',
            'artista',
            'genero',
            'ano',
            'duracao'
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()

        for musica in lista:
            escritor.writerow(musica)

    messagebox.showinfo(
        'Sucesso',
        'Playlist exportada com sucesso!'
    )


# ==================================================
# INTERFACE
# ==================================================

class App:

    def __init__(self, root):

        self.root = root

        self.root.title('🎵 Ordenador de Playlist')
        self.root.geometry('1200x600')
        self.root.configure(bg='#1e1e1e')

        self.musicas = carregar_musicas('musicas.csv')

        self.criar_widgets()
        self.exibir_musicas(self.musicas)

    # ==================================================
    # CRIAR WIDGETS
    # ==================================================

    def criar_widgets(self):

        titulo = tk.Label(
            self.root,
            text='🎵 Ordenador de Playlist com Merge Sort',
            font=('Arial', 20, 'bold'),
            bg='#1e1e1e',
            fg='white'
        )

        titulo.pack(pady=10)

        frame_topo = tk.Frame(
            self.root,
            bg='#1e1e1e'
        )

        frame_topo.pack(pady=10)

        # ==============================================
        # TEXTO ORDENAR
        # ==============================================

        label_ordenar = tk.Label(
            frame_topo,
            text='Ordenar por:',
            bg='#1e1e1e',
            fg='white'
        )

        label_ordenar.pack(
            side=tk.LEFT,
            padx=5
        )

        # ==============================================
        # COMBOBOX
        # ==============================================

        self.combo = ttk.Combobox(
            frame_topo,
            values=[
                'nome',
                'album',
                'artista',
                'genero',
                'ano',
                'duracao'
            ],
            state='readonly',
            width=15
        )

        self.combo.current(0)

        self.combo.pack(
            side=tk.LEFT,
            padx=5
        )

        # ==============================================
        # BOTÃO ORDENAR
        # ==============================================

        btn_ordenar = tk.Button(
            frame_topo,
            text='Ordenar',
            command=self.ordenar,
            bg='#4CAF50',
            fg='white',
            width=12
        )

        btn_ordenar.pack(
            side=tk.LEFT,
            padx=5
        )

        # ==============================================
        # BUSCA
        # ==============================================

        self.busca = tk.Entry(
            frame_topo,
            width=30
        )

        self.busca.pack(
            side=tk.LEFT,
            padx=10
        )

        btn_busca = tk.Button(
            frame_topo,
            text='Buscar',
            command=self.buscar,
            bg='#2196F3',
            fg='white'
        )

        btn_busca.pack(side=tk.LEFT)

        # ==============================================
        # EXPORTAR CSV
        # ==============================================

        btn_exportar = tk.Button(
            frame_topo,
            text='Exportar CSV',
            command=lambda: exportar_csv(self.musicas),
            bg='#FF9800',
            fg='white'
        )

        btn_exportar.pack(
            side=tk.LEFT,
            padx=10
        )

        # ==============================================
        # TABELA
        # ==============================================

        colunas = (
            'nome',
            'album',
            'artista',
            'genero',
            'ano',
            'duracao'
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=colunas,
            show='headings'
        )

        for coluna in colunas:

            self.tree.heading(
                coluna,
                text=coluna.capitalize()
            )

            self.tree.column(
                coluna,
                width=180
            )

        self.tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # ==============================================
        # STATUS
        # ==============================================

        self.status = tk.Label(
            self.root,
            text='',
            bg='#1e1e1e',
            fg='white'
        )

        self.status.pack(pady=5)

        self.atualizar_status(self.musicas)

    # ==================================================
    # STATUS
    # ==================================================

    def atualizar_status(self, lista):

        total = len(lista)

        artistas = set()

        for musica in lista:
            artistas.add(musica['artista'])

        self.status.config(
            text=f'Total de músicas: {total} | Artistas únicos: {len(artistas)}'
        )

    # ==================================================
    # EXIBIR MÚSICAS
    # ==================================================

    def exibir_musicas(self, lista):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for musica in lista:

            self.tree.insert(
                '',
                tk.END,
                values=(
                    musica['nome'],
                    musica['album'],
                    musica['artista'],
                    musica['genero'],
                    musica['ano'],
                    musica['duracao']
                )
            )

        self.atualizar_status(lista)

    # ==================================================
    # ORDENAR
    # ==================================================

    def ordenar(self):

        chave = self.combo.get()

        self.musicas = merge_sort(
            self.musicas,
            chave
        )

        self.exibir_musicas(self.musicas)

    # ==================================================
    # BUSCAR
    # ==================================================

    def buscar(self):

        termo = self.busca.get().lower()

        filtradas = []

        for musica in self.musicas:

            if (
                termo in musica['nome'].lower()
                or termo in musica['artista'].lower()
                or termo in musica['album'].lower()
            ):

                filtradas.append(musica)

        self.exibir_musicas(filtradas)


# ==================================================
# MAIN
# ==================================================

if __name__ == '__main__':

    root = tk.Tk()

    app = App(root)

    root.mainloop()