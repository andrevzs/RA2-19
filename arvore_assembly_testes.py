# Integrantes do grupo:
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Nome do grupo no Canvas: RA2 19

from ler_tokens import lerTokens
from gramatica_ll1 import construirGramatica, analisarLL1
from parser import parsear
from arvore_assembly import gerarArvore, gerarAssembly


ARQUIVOS = ["teste1.txt", "teste2.txt", "teste3.txt"]


def executar_teste_arquivo(caminho):
    tokens = lerTokens(caminho)
    analise = analisarLL1(construirGramatica())
    resultado = parsear(tokens, analise)

    if not resultado["sucesso"]:
        raise AssertionError(f"Parsing falhou em {caminho}: {resultado['erro']}")

    derivacao = resultado.get("derivacao", resultado.get("arvore"))
    arvore = gerarArvore(derivacao)
    codigo = gerarAssembly(arvore, tokens)

    if not codigo or "_start:" not in codigo:
        raise AssertionError(f"Assembly inválido para {caminho}")

    print(f"[OK] {caminho} -> parsing e assembly gerados")


def main():
    for arquivo in ARQUIVOS:
        executar_teste_arquivo(arquivo)

    print("\nTodos os testes end-to-end do Aluno 4 passaram.")


if __name__ == "__main__":
    main()
