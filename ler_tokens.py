# Integrantes do grupo:
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Nome do grupo no Canvas: RA2 19

import re
import ast


PALAVRAS_RESERVADAS = {
    "START": "START_CMD",
    "END": "END_CMD",
    "RES": "RES",
    "SET": "SET",
    "GET": "GET",
    "IF": "IF",
    "IFELSE": "IFELSE",
    "WHILE": "WHILE",
    "BLOCK": "BLOCK",
}

OPERADORES = {"+", "-", "*", "/", "//", "%", "^", "|"}
OPERADORES_RELACIONAIS = {">", "<", ">=", "<=", "==", "!="}


def eh_inteiro(token):
    """Retorna True se o token for um inteiro válido."""
    return re.fullmatch(r"-?\d+", token) is not None


def eh_real(token):
    """Retorna True se o token for um real válido."""
    return re.fullmatch(r"-?\d+\.\d+", token) is not None


def eh_identificador(token):
    """Retorna True se o token for um identificador válido (maiúsculas)."""
    return re.fullmatch(r"[A-Z]+", token) is not None


def quebrar_tokens_linha(linha):
    """
    Quebra uma linha em tokens básicos, separando parênteses.
    Exemplo:
        "(SET 42 X)" -> ["(", "SET", "42", "X", ")"]
    """
    linha = linha.strip()
    if not linha:
        return []

    linha = linha.replace("(", " ( ").replace(")", " ) ")
    return linha.split()


def converter_token(token):
    """
    Converte um token bruto para o formato esperado pelo parser:
    (tipo, valor)
    """
    if token == "(":
        return ("LPAREN", "(")

    if token == ")":
        return ("RPAREN", ")")

    if token in OPERADORES or token in OPERADORES_RELACIONAIS:
        return ("OPERADOR", token)

    if token in PALAVRAS_RESERVADAS:
        tipo = PALAVRAS_RESERVADAS[token]
        return (tipo, tipo)

    if eh_real(token):
        return ("REAL", float(token))

    if eh_inteiro(token):
        return ("INT", int(token))

    if eh_identificador(token):
        return ("ID", token)

    raise ValueError(f"Token inválido: {token}")


def normalizar_linha(tokens_brutos):
    """
    Trata casos especiais de linha completa:
    (START) -> [("START_CMD", "START_CMD")]
    (END)   -> [("END_CMD", "END_CMD")]

    As demais linhas são convertidas token a token.
    """
    if tokens_brutos == ["(", "START", ")"]:
        return [("START_CMD", "START_CMD")]

    if tokens_brutos == ["(", "END", ")"]:
        return [("END_CMD", "END_CMD")]

    return [converter_token(tok) for tok in tokens_brutos]


def lerTokens(caminho_arquivo):
    """
    Lê um arquivo fonte da linguagem e retorna a lista de tokens
    no formato esperado pelo parser.
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    if not linhas:
        return []

    # Formato já estruturado: uma tupla por linha, ex. ('INT', 3)
    estruturado = _tentar_ler_tokens_estruturados(linhas)
    if estruturado is not None:
        return estruturado

    # Formato da Fase 1: "Linha N: ['(', '3', '2', '+', ')']"
    if _eh_formato_fase1(linhas):
        return _ler_formato_fase1(linhas)

    # Formato alternativo da Fase 1: lista Python por linha
    if _eh_formato_lista_por_linha(linhas):
        return _ler_formato_lista_por_linha(linhas)

    # Fallback: arquivo-fonte da linguagem
    return _ler_formato_fonte(linhas)


def _tentar_ler_tokens_estruturados(linhas):
    tokens = []

    try:
        for linha in linhas:
            item = ast.literal_eval(linha)
            if not isinstance(item, tuple) or len(item) != 2:
                return None
            tokens.append(item)
    except (ValueError, SyntaxError):
        return None

    return tokens


def _eh_formato_fase1(linhas):
    return all(linha.startswith("Linha ") and ":" in linha for linha in linhas)


def _eh_formato_lista_por_linha(linhas):
    return all(linha.startswith("[") and linha.endswith("]") for linha in linhas)


def _converter_linha_bruta(tokens_brutos, numero_linha):
    try:
        tokens_convertidos = normalizar_linha(tokens_brutos)
    except ValueError as e:
        raise ValueError(f"Linha {numero_linha}: {e}")

    return tokens_convertidos


def _ler_formato_fase1(linhas):
    tokens_finais = []

    for numero_linha, linha in enumerate(linhas, start=1):
        trecho_tokens = linha.split(":", 1)[1].strip()

        try:
            tokens_brutos = ast.literal_eval(trecho_tokens)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Linha {numero_linha}: formato inválido de lista de tokens ({e})")

        if not isinstance(tokens_brutos, list):
            raise ValueError(f"Linha {numero_linha}: esperado lista de tokens")

        tokens_convertidos = _converter_linha_bruta(tokens_brutos, numero_linha)
        tokens_finais.extend(tokens_convertidos)
        tokens_finais.append(("EOL", None))

    return tokens_finais


def _ler_formato_lista_por_linha(linhas):
    tokens_finais = []

    for numero_linha, linha in enumerate(linhas, start=1):
        try:
            tokens_brutos = ast.literal_eval(linha)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Linha {numero_linha}: formato inválido de lista de tokens ({e})")

        if not isinstance(tokens_brutos, list):
            raise ValueError(f"Linha {numero_linha}: esperado lista de tokens")

        tokens_convertidos = _converter_linha_bruta(tokens_brutos, numero_linha)
        tokens_finais.extend(tokens_convertidos)
        tokens_finais.append(("EOL", None))

    return tokens_finais


def _ler_formato_fonte(linhas):
    tokens_finais = []

    for numero_linha, linha in enumerate(linhas, start=1):
        tokens_brutos = quebrar_tokens_linha(linha)
        tokens_convertidos = _converter_linha_bruta(tokens_brutos, numero_linha)
        tokens_finais.extend(tokens_convertidos)
        tokens_finais.append(("EOL", None))

    return tokens_finais


def imprimirTokens(tokens):
    """Imprime os tokens gerados de forma legível."""
    print("=" * 60)
    print("TOKENS GERADOS")
    print("=" * 60)
    for token in tokens:
        print(token)
    print("=" * 60)


if __name__ == "__main__":
    caminho = "teste1.txt"
    tokens = lerTokens(caminho)
    imprimirTokens(tokens)