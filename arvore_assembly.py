# Integrantes do grupo:
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Nome do grupo no Canvas: RA2 19

import json

from assembler import GeradorAssembly
from executor import executarExpressao


CONTROLES = {"IF", "IFELSE", "WHILE", "BLOCK"}


def gerarArvore(derivacao):
    """
    A derivação já está materializada em uma árvore de nós do parser.
    Esta função preserva a interface pedida na especificação.
    """
    if derivacao is None:
        raise ValueError("Derivação inválida: valor None")
    return derivacao


def salvarArvore(arvore, arquivo_json="arvore_sintatica.json", arquivo_txt="arvore_sintatica.txt"):
    """Salva a árvore em JSON e em formato texto."""
    with open(arquivo_json, "w", encoding="utf-8") as f_json:
        json.dump(arvore.para_dict(), f_json, ensure_ascii=False, indent=2)

    with open(arquivo_txt, "w", encoding="utf-8") as f_txt:
        f_txt.write(str(arvore))


def gerarAssembly(arvore, tokens_programa=None):
    """
    Gera assembly a partir da árvore sintática.

    Estratégia:
    - Extrai cada linha/comando da árvore
    - Usa executor + gerador assembly para expressões/memória/RES
    - Representa controles como no-op (linha válida + resultado 0.0)
    """
    linhas_tokens = _extrair_linhas_tokens_de_programa(tokens_programa) if tokens_programa else _extrair_linhas_tokens(arvore)
    gerador = GeradorAssembly()
    memoria = {}
    resultados = []
    contexto = {"linha": 0}

    gerador.iniciar_programa()

    for tokens_linha in linhas_tokens:
        _gerar_comando_tokens(tokens_linha, gerador, memoria, resultados, contexto)

    gerador.finalizar_programa()
    return gerador.obter_codigo()


def _tipo_controle(tokens_linha):
    if len(tokens_linha) >= 2 and tokens_linha[0] == "(":
        cabecalho = str(tokens_linha[1])
        if cabecalho in CONTROLES:
            return cabecalho
    return None


def _extrair_linhas_tokens(arvore):
    """Extrai a lista de comandos da árvore como listas de tokens com parênteses."""
    linhas = []
    _coletar_linhas(arvore, linhas)
    return linhas


def _coletar_linhas(nodo, linhas):
    if nodo is None:
        return

    tipo_nodo = getattr(nodo, "tipo", None)
    valor_nodo = getattr(nodo, "valor", None)

    if valor_nodo == "linha" or tipo_nodo == "linha":
        for filho in getattr(nodo, "filhos", []):
            if getattr(filho, "valor", None) == "comando" or getattr(filho, "tipo", None) == "comando":
                tokens_comando = _tokens_terminais(filho)
                if tokens_comando:
                    linhas.append(tokens_comando)
                break

    for filho in getattr(nodo, "filhos", []):
        _coletar_linhas(filho, linhas)


def _tokens_terminais(nodo):
    tokens = []

    def visitar(atual):
        if getattr(atual, "tipo", None) == "terminal":
            lexema = getattr(atual, "lexema", None)
            valor = getattr(atual, "valor", None)
            token = lexema if lexema is not None else valor
            if token == "LPAREN":
                token = "("
            elif token == "RPAREN":
                token = ")"

            if token is not None and valor != "EOL":
                tokens.append(token)
            return

        for filho in getattr(atual, "filhos", []):
            visitar(filho)

    visitar(nodo)
    return tokens


def _extrair_linhas_tokens_de_programa(tokens_programa):
    """Converte o vetor de tokens estruturado em linhas de comando com parênteses."""
    if not tokens_programa:
        return []

    linhas = []
    atual = []

    for tipo, valor in tokens_programa:
        if tipo == "START_CMD" or tipo == "END_CMD":
            continue

        if tipo == "EOL":
            if atual:
                linhas.append(atual)
                atual = []
            continue

        if tipo == "LPAREN":
            atual.append("(")
        elif tipo == "RPAREN":
            atual.append(")")
        elif tipo == "OPERADOR":
            atual.append(valor)
        elif tipo in {"INT", "REAL", "ID", "RES", "SET", "GET", "IF", "IFELSE", "WHILE", "BLOCK"}:
            atual.append(valor if valor is not None else tipo)

    if atual:
        linhas.append(atual)

    return linhas


def _normalizar_para_executor(tokens_linha):
    """
    Adapta comandos da sintaxe atual para o formato do executor legado:
    - (RES N) -> (N RES)
    - (SET V MEM) -> (V MEM)
    - (GET MEM) -> (MEM)
    """
    if len(tokens_linha) >= 4 and tokens_linha[0] == "(" and tokens_linha[-1] == ")":
        cabecalho = str(tokens_linha[1])

        if cabecalho == "RES" and len(tokens_linha) == 4:
            return ["(", str(tokens_linha[2]), "RES", ")"]

        if cabecalho == "SET" and len(tokens_linha) == 5:
            return ["(", str(tokens_linha[2]), str(tokens_linha[3]), ")"]

        if cabecalho == "GET" and len(tokens_linha) == 4:
            return ["(", str(tokens_linha[2]), ")"]

    return [str(tok) for tok in tokens_linha]


def _proxima_linha(contexto):
    contexto["linha"] += 1
    return contexto["linha"]


def _gerar_comando_tokens(tokens_linha, gerador, memoria, resultados, contexto):
    tipo_controle = _tipo_controle(tokens_linha)

    if tipo_controle is None:
        numero_linha = _proxima_linha(contexto)
        tokens_executor = _normalizar_para_executor(tokens_linha)
        resultado_executor = executarExpressao(tokens_executor, memoria, resultados)
        resultados.append(resultado_executor)
        gerador.adicionar_linha(numero_linha, resultado_executor)
        return

    if tipo_controle == "IF":
        _gerar_if(tokens_linha, gerador, memoria, resultados, contexto)
        return

    if tipo_controle == "IFELSE":
        _gerar_ifelse(tokens_linha, gerador, memoria, resultados, contexto)
        return

    if tipo_controle == "WHILE":
        _gerar_while(tokens_linha, gerador, memoria, resultados, contexto)
        return

    if tipo_controle == "BLOCK":
        _gerar_block(tokens_linha, gerador, memoria, resultados, contexto)
        return


def _gerar_if(tokens_linha, gerador, memoria, resultados, contexto):
    args = _extrair_argumentos(tokens_linha)
    if len(args) != 2:
        raise ValueError(f"IF inválido: esperado 2 argumentos, encontrado {len(args)}")

    cond_tokens = _normalizar_valor_para_comando(args[0])
    corpo_tokens = args[1]

    _gerar_comando_tokens(cond_tokens, gerador, memoria, resultados, contexto)

    label_fim = gerador._novo_label()
    _emit_branch_if_zero(gerador, label_fim)
    _gerar_comando_tokens(corpo_tokens, gerador, memoria, resultados, contexto)
    gerador._emit(f"{label_fim}:")


def _gerar_ifelse(tokens_linha, gerador, memoria, resultados, contexto):
    args = _extrair_argumentos(tokens_linha)
    if len(args) != 3:
        raise ValueError(f"IFELSE inválido: esperado 3 argumentos, encontrado {len(args)}")

    cond_tokens = _normalizar_valor_para_comando(args[0])
    corpo_true = args[1]
    corpo_false = args[2]

    _gerar_comando_tokens(cond_tokens, gerador, memoria, resultados, contexto)

    label_else = gerador._novo_label()
    label_fim = gerador._novo_label()

    _emit_branch_if_zero(gerador, label_else)
    _gerar_comando_tokens(corpo_true, gerador, memoria, resultados, contexto)
    gerador._emit(f"    B {label_fim}")
    gerador._emit(f"{label_else}:")
    _gerar_comando_tokens(corpo_false, gerador, memoria, resultados, contexto)
    gerador._emit(f"{label_fim}:")


def _gerar_while(tokens_linha, gerador, memoria, resultados, contexto):
    args = _extrair_argumentos(tokens_linha)
    if len(args) != 2:
        raise ValueError(f"WHILE inválido: esperado 2 argumentos, encontrado {len(args)}")

    cond_tokens = _normalizar_valor_para_comando(args[0])
    corpo_tokens = args[1]

    label_inicio = gerador._novo_label()
    label_fim = gerador._novo_label()

    gerador._emit(f"{label_inicio}:")
    _gerar_comando_tokens(cond_tokens, gerador, memoria, resultados, contexto)
    _emit_branch_if_zero(gerador, label_fim)
    _gerar_comando_tokens(corpo_tokens, gerador, memoria, resultados, contexto)
    gerador._emit(f"    B {label_inicio}")
    gerador._emit(f"{label_fim}:")


def _gerar_block(tokens_linha, gerador, memoria, resultados, contexto):
    args = _extrair_argumentos(tokens_linha)
    for comando in args:
        _gerar_comando_tokens(comando, gerador, memoria, resultados, contexto)


def _emit_branch_if_zero(gerador, label_destino):
    gerador._carrega_constante_float("0.0", "d7")
    gerador._emit("    VCMP.F64 d0, d7")
    gerador._emit("    VMRS APSR_nzcv, FPSCR")
    gerador._emit(f"    BEQ {label_destino}")


def _normalizar_valor_para_comando(valor_tokens):
    # valor já no formato de comando parentetizado
    if valor_tokens and valor_tokens[0] == "(" and valor_tokens[-1] == ")":
        return valor_tokens

    # valor atômico vira comando de um único valor para avaliação
    if len(valor_tokens) == 1:
        return ["(", str(valor_tokens[0]), ")"]

    raise ValueError(f"Valor inválido em estrutura de controle: {valor_tokens}")


def _extrair_argumentos(tokens_comando):
    """
    Recebe um comando completo '(CMD ...)' e retorna os argumentos de nível superior.
    """
    if len(tokens_comando) < 3 or tokens_comando[0] != "(" or tokens_comando[-1] != ")":
        raise ValueError(f"Comando inválido: {tokens_comando}")

    internos = [str(t) for t in tokens_comando[2:-1]]
    args = []
    i = 0

    while i < len(internos):
        token = internos[i]

        if token == "(":
            inicio = i
            nivel = 1
            i += 1
            while i < len(internos) and nivel > 0:
                if internos[i] == "(":
                    nivel += 1
                elif internos[i] == ")":
                    nivel -= 1
                i += 1

            if nivel != 0:
                raise ValueError(f"Parênteses desbalanceados em comando: {tokens_comando}")

            args.append(internos[inicio:i])
            continue

        args.append([token])
        i += 1

    return args
