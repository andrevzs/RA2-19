from ler_tokens import lerTokens, imprimirTokens


def main():
    caminho = "teste_parte3.txt"
    tokens = lerTokens(caminho)
    imprimirTokens(tokens)


if __name__ == "__main__":
    main()