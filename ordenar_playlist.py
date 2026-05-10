import csv

# ----------------------------
# Função Merge
# ----------------------------

def merge(esquerda, direita, chave):

    resultado = []

    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):

        valor_esq = (
            esquerda[i][chave].lower(),
            esquerda[i]["nome"].lower()
        )

        valor_dir = (
            direita[j][chave].lower(),
            direita[j]["nome"].lower()
        )

        if valor_esq <= valor_dir:
            resultado.append(esquerda[i])
            i += 1

        else:
            resultado.append(direita[j])
            j += 1

    # adiciona elementos restantes
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado


# ----------------------------
# Merge Sort
# ----------------------------

def merge_sort(lista, chave):

    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2

    esquerda = merge_sort(lista[:meio], chave)
    direita = merge_sort(lista[meio:], chave)

    return merge(esquerda, direita, chave)


# ----------------------------
# Carregar Músicas
# ----------------------------

def carregar_musicas(caminho):
    musicas = []
    
    try:
        with open(caminho, encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=',')
            for linha in leitor:
                musicas.append(linha)
    except FileNotFoundError:
        print("Erro: arquivo musicas.csv não encontrado.")
        return []
    
    return musicas

# ----------------------------
# Main
# ----------------------------

def main():
    musicas = carregar_musicas("musicas.csv")

    if not musicas:
        return

    print("\n=== 🎵 ORDENADOR DE PLAYLISTS ===\n")

    while True:
        print("Organizar músicas por:")
        print("1 - Nome")
        print("2 - Álbum")
        print("3 - Artista")
        print("4 - Gênero")
        print("5 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            chave = "nome"

        elif opcao == "2":
            chave = "album"

        elif opcao == "3":
            chave = "artista"

        elif opcao == "4":
            chave = "genero"
        
        elif opcao == "5":
            print("Encerrando...")
            break

        else:
            print("Opção inválida")
            continue

        playlist_ordenada = merge_sort(musicas, chave)

        print("\n=== PLAYLIST ORDENADA ===\n")

        for i, musica in enumerate(playlist_ordenada, start=1):
            print(
                f'{i}. '
                f'{musica["nome"]} | '
                f'{musica["album"]} | '
                f'{musica["artista"]} | '
                f'{musica["genero"]}'
            )
        
        print("\nGostaria de outra ordenação?")
        resposta = input("(1 - Sim, Qualquer Outro - Não)\n")

        if resposta == '1':
            continue
        else:
            print("Encerrando...")
            break

if __name__ == "__main__":
    main()