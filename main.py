# Integrantes do grupo:
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Nome do grupo no Canvas: RA2 19

import sys
from ler_tokens import lerTokens
from gramatica_ll1 import construirGramatica, analisarLL1
from parser import parsear
from arvore_assembly import gerarArvore, gerarAssembly, salvarArvore


def lerArquivoTeste(nome_arquivo):
    linhas = []

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            for numero_linha, linha in enumerate(arquivo, start=1):
                conteudo = linha.strip()
                if conteudo != "":
                    linhas.append((numero_linha, conteudo))
    except FileNotFoundError:
        print(f"Erro: arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)
    except OSError as erro:
        print(f"Erro ao abrir o arquivo '{nome_arquivo}': {erro}")
        sys.exit(1)

    return linhas


def salvarTokens(todos_tokens):
    with open("tokens.txt", "w", encoding="utf-8") as arquivo:
        for token in todos_tokens:
            arquivo.write(f"{token}\n")


def salvarAssembly(codigo):
    with open("output.asm", "w", encoding="utf-8") as arquivo:
        arquivo.write(codigo)


def processarLinhas(linhas):
    todos_tokens = []

    for numero_linha, conteudo in linhas:
        print(f"Linha {numero_linha}: {conteudo}")

    try:
        todos_tokens = lerTokens(sys.argv[1])
    except ValueError as erro:
        print(f"Erro léxico/sintático na leitura dos tokens: {erro}")
        sys.exit(1)

    print("\nTokens gerados:")
    for token in todos_tokens:
        print(token)

    gramatica = construirGramatica()
    analise = analisarLL1(gramatica)

    print(f"\nGramática é LL(1)? {analise['eh_ll1']}")
    if not analise["eh_ll1"]:
        print("Conflitos encontrados na gramática:")
        for conflito in analise["conflitos"]:
            print(conflito)
        sys.exit(1)

    resultado = parsear(todos_tokens, analise)

    print("\nResultado do parser:")
    if resultado["sucesso"]:
        print("Parsing realizado com sucesso!")
        print("\nÁrvore sintática:")
        derivacao = resultado.get("derivacao", resultado.get("arvore"))
        arvore = gerarArvore(derivacao)
        print(arvore)
    else:
        print("Erro durante o parsing:")
        print(resultado["erro"])
        sys.exit(1)

    salvarTokens(todos_tokens)

    salvarArvore(arvore)
    codigo_asm = gerarAssembly(arvore, todos_tokens)
    salvarAssembly(codigo_asm)

    return {
        "tokens": todos_tokens,
        "arvore": arvore,
        "assembly": codigo_asm,
    }


def main():
    if len(sys.argv) != 2:
        print("Uso: python[3] main.py <arquivo_teste.txt>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    linhas = lerArquivoTeste(nome_arquivo)
    processarLinhas(linhas)


if __name__ == "__main__":
    main()