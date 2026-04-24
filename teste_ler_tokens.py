from ler_tokens import lerTokens, imprimirTokens


def main():
    print("[1] Teste com arquivo-fonte")
    tokens_fonte = lerTokens("teste_parte3.txt")
    imprimirTokens(tokens_fonte)

    print("\n[2] Teste com formato da Fase 1 (tokens salvos)")
    tokens_fase1 = lerTokens("tokens_fase1_exemplo.txt")
    imprimirTokens(tokens_fase1)

    if ("OPERADOR", ">") not in tokens_fase1:
        raise ValueError("Falha: operador relacional '>' nao foi reconhecido.")

    print("\nTeste concluido: leitura de tokens em ambos os formatos OK.")


if __name__ == "__main__":
    main()