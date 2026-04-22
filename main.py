# Integrantes do grupo (ordem alfabética):
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Grupo no Canvas:
# RA1 19

import sys
from lexer import parseExpressao
from executor import executarExpressao
from assembler import GeradorAssembly


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
        for numero_linha, tokens in todos_tokens:
            arquivo.write(f"Linha {numero_linha}: {tokens}\n")


def salvarAssembly(codigo):
    with open("output.asm", "w", encoding="utf-8") as arquivo:
        arquivo.write(codigo)


def processarLinhas(linhas):
    memoria = {}
    resultados = []
    todos_tokens = []
    gerador = GeradorAssembly()

    gerador.iniciar_programa()

    for numero_linha, conteudo in linhas:
        tokens = parseExpressao(conteudo)
        resultado = executarExpressao(tokens, memoria, resultados)

        print(f"Linha {numero_linha}: {tokens}")
        print(f"  Executor: {resultado}")

        todos_tokens.append((numero_linha, tokens))
        resultados.append(resultado)

        gerador.adicionar_linha(numero_linha, resultado)

    gerador.finalizar_programa()

    salvarTokens(todos_tokens)
    salvarAssembly(gerador.obter_codigo())

    return todos_tokens


def main():
    if len(sys.argv) != 2:
        print("Uso: python[3] main.py <arquivo_teste.txt>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    linhas = lerArquivoTeste(nome_arquivo)
    processarLinhas(linhas)


if __name__ == "__main__":
    main()