def eh_digito(c):
    return "0" <= c <= "9"


def eh_maiuscula(c):
    return "A" <= c <= "Z"


def _pode_ser_numero_negativo(tokens):
    if not tokens:
        return True
    
    ultimo = tokens[-1]
    
    if ultimo in ("(", "+", "-", "*", "/", "//", "%", "^"):
        return True
    
    try:
        float(ultimo)
        return True
    except ValueError:
        pass
    
    if ultimo and all(c.isupper() for c in ultimo):
        return True
    
    return False


def validarParenteses(tokens):
    contador = 0
    for token in tokens:
        if token == "(":
            contador += 1
        elif token == ")":
            contador -= 1
            if contador < 0:
                raise ValueError("Erro léxico: parêntese fechado sem abertura")
    
    if contador != 0:
        raise ValueError("Erro léxico: parênteses desbalanceados")


def parseExpressao(linha):
    tokens = []
    i = 0

    # percorre a linha chamando estados
    while i < len(linha):
        i = estado_inicial(linha, i, tokens)

    validarParenteses(tokens)
    
    return tokens


def estado_inicial(linha, i, tokens):
    # ignora espaços
    while i < len(linha) and linha[i].isspace():
        i += 1

    if i >= len(linha):
        return i

    c = linha[i]

    # parênteses
    if c == "(":
        tokens.append("(")
        return i + 1

    if c == ")":
        tokens.append(")")
        return i + 1

    if eh_digito(c):
        return estado_numero(linha, i, tokens)

    if c == "-" and _pode_ser_numero_negativo(tokens):
        if i + 1 < len(linha) and eh_digito(linha[i + 1]):
            return estado_numero(linha, i, tokens)
        if i + 1 < len(linha) and linha[i + 1] == ".":
            if i + 2 < len(linha) and eh_digito(linha[i + 2]):
                return estado_numero(linha, i, tokens)
        tokens.append("-")
        return i + 1

    # identificador (RES, MEM, etc.)
    if eh_maiuscula(c):
        return estado_identificador(linha, i, tokens)

    # operadores simples
    if c == "+":
        tokens.append("+")
        return i + 1

    if c == "-":
        tokens.append("-")
        return i + 1

    if c == "*":
        tokens.append("*")
        return i + 1

    if c == "%":
        tokens.append("%")
        return i + 1

    if c == "^":
        tokens.append("^")
        return i + 1

    # / ou //
    if c == "/":
        return estado_barra(linha, i, tokens)

    raise ValueError(f"Erro léxico: '{c}'")


def estado_numero(linha, i, tokens):
    inicio = i
    tem_ponto = False

    if i < len(linha) and linha[i] == "-":
        i += 1

    # lê número com possível ponto
    while i < len(linha):
        c = linha[i]

        if eh_digito(c):
            i += 1
            continue

        if c == ".":
            if tem_ponto:
                raise ValueError("Erro léxico: número inválido (múltiplos pontos decimais)")
            tem_ponto = True
            i += 1
            if i >= len(linha) or not eh_digito(linha[i]):
                raise ValueError("Erro léxico: número inválido (ponto sem dígito após)")
            continue

        break

    tokens.append(linha[inicio:i])
    return i


def estado_identificador(linha, i, tokens):
    inicio = i

    # lê sequência de letras maiúsculas
    while i < len(linha) and eh_maiuscula(linha[i]):
        i += 1

    tokens.append(linha[inicio:i])
    return i


def estado_barra(linha, i, tokens):
    # distingue / de //
    if i + 1 < len(linha) and linha[i + 1] == "/":
        tokens.append("//")
        return i + 2

    tokens.append("/")
    return i + 1