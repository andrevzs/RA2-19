# Integrantes do grupo:
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Nome do grupo no Canvas: RA2 19

EPSILON = "ε"
EOF = "$"


def construirGramatica():
    return {
        "simbolo_inicial": "programa",

        "terminais": {
            "START_CMD", "END_CMD", "EOL",
            "LPAREN", "RPAREN",
            "RES", "SET", "GET",
            "IF", "IFELSE", "WHILE", "BLOCK",
            "INT", "REAL", "ID",
            "+", "-", "*", "|", "/", "%", "^",
            EOF
        },

        "nao_terminais": {
            "programa",
            "listalinhas",
            "linha",
            "comando",
            "corpocomando",
            "corpoaposvalor",
            "valor",
            "operador",
            "listacomando"
        },

        "producoes": {
            "programa": [
                ["START_CMD", "EOL", "listalinhas", "END_CMD", "EOL", EOF]
            ],

            "listalinhas": [
                ["linha", "listalinhas"],
                [EPSILON]
            ],

            "linha": [
                ["comando", "EOL"]
            ],

            "comando": [
                ["LPAREN", "corpocomando", "RPAREN"]
            ],

            "corpocomando": [
                ["RES", "valor"],
                ["SET", "valor", "ID"],
                ["GET", "ID"],
                ["IF", "valor", "comando"],
                ["IFELSE", "valor", "comando", "comando"],
                ["WHILE", "valor", "comando"],
                ["BLOCK", "listacomando"],
                ["valor", "corpoaposvalor"]
            ],

            "corpoaposvalor": [
                ["valor", "operador"],
                [EPSILON]
            ],

            "listacomando": [
                ["linha", "listacomando"],
                [EPSILON]
            ],

            "valor": [
                ["INT"],
                ["REAL"],
                ["ID"],
                ["comando"]
            ],

            "operador": [
                ["+"],
                ["-"],
                ["*"],
                ["|"],
                ["/"],
                ["%"],
                ["^"]
            ]
        }
    }


def calcularFirst(gramatica):
    producoes = gramatica["producoes"]
    terminais = gramatica["terminais"]
    nao_terminais = gramatica["nao_terminais"]

    first = {nt: set() for nt in nao_terminais}

    mudou = True
    while mudou:
        mudou = False

        for nt, regras in producoes.items():
            for regra in regras:
                if regra == [EPSILON]:
                    if EPSILON not in first[nt]:
                        first[nt].add(EPSILON)
                        mudou = True
                    continue

                todos_derivam_epsilon = True

                for simbolo in regra:
                    if simbolo in terminais:
                        if simbolo not in first[nt]:
                            first[nt].add(simbolo)
                            mudou = True
                        todos_derivam_epsilon = False
                        break

                    elif simbolo in nao_terminais:
                        antes = len(first[nt])
                        first[nt] |= (first[simbolo] - {EPSILON})
                        if len(first[nt]) > antes:
                            mudou = True

                        if EPSILON not in first[simbolo]:
                            todos_derivam_epsilon = False
                            break

                if todos_derivam_epsilon:
                    if EPSILON not in first[nt]:
                        first[nt].add(EPSILON)
                        mudou = True

    return first


def calcularFollow(gramatica, first):
    producoes = gramatica["producoes"]
    nao_terminais = gramatica["nao_terminais"]
    simbolo_inicial = gramatica["simbolo_inicial"]

    follow = {nt: set() for nt in nao_terminais}
    follow[simbolo_inicial].add(EOF)

    mudou = True
    while mudou:
        mudou = False

        for A, regras in producoes.items():
            for regra in regras:
                trailer = follow[A].copy()

                for simbolo in reversed(regra):
                    if simbolo in nao_terminais:
                        antes = len(follow[simbolo])
                        follow[simbolo] |= trailer
                        if len(follow[simbolo]) > antes:
                            mudou = True

                        if EPSILON in first[simbolo]:
                            trailer |= (first[simbolo] - {EPSILON})
                        else:
                            trailer = first[simbolo] - {EPSILON}

                    elif simbolo != EPSILON:
                        trailer = {simbolo}

    return follow


def firstDeSequencia(sequencia, first, terminais, nao_terminais):
    resultado = set()

    if not sequencia:
        resultado.add(EPSILON)
        return resultado

    for simbolo in sequencia:
        if simbolo in terminais:
            resultado.add(simbolo)
            return resultado

        elif simbolo in nao_terminais:
            resultado |= (first[simbolo] - {EPSILON})
            if EPSILON not in first[simbolo]:
                return resultado

        elif simbolo == EPSILON:
            resultado.add(EPSILON)
            return resultado

    resultado.add(EPSILON)
    return resultado


def construirTabelaLL1(gramatica, first, follow):
    producoes = gramatica["producoes"]
    terminais = gramatica["terminais"]
    nao_terminais = gramatica["nao_terminais"]

    tabela = {nt: {} for nt in nao_terminais}
    conflitos = []

    for A, regras in producoes.items():
        for regra in regras:
            first_regra = firstDeSequencia(regra, first, terminais, nao_terminais)

            for terminal in (first_regra - {EPSILON}):
                if terminal in tabela[A]:
                    conflitos.append((A, terminal, tabela[A][terminal], regra))
                tabela[A][terminal] = regra

            if EPSILON in first_regra:
                for terminal in follow[A]:
                    if terminal in tabela[A]:
                        conflitos.append((A, terminal, tabela[A][terminal], regra))
                    tabela[A][terminal] = regra

    return tabela, conflitos


def analisarLL1(gramatica):
    first = calcularFirst(gramatica)
    follow = calcularFollow(gramatica, first)
    tabela, conflitos = construirTabelaLL1(gramatica, first, follow)

    return {
        "first": first,
        "follow": follow,
        "tabela": tabela,
        "conflitos": conflitos,
        "eh_ll1": len(conflitos) == 0
    }


def imprimirAnalise(analise):
    print("=== FIRST ===")
    for nt in sorted(analise["first"]):
        print(f"{nt} = {sorted(analise['first'][nt])}")

    print("\n=== FOLLOW ===")
    for nt in sorted(analise["follow"]):
        print(f"{nt} = {sorted(analise['follow'][nt])}")

    print("\n=== CONFLITOS ===")
    if not analise["conflitos"]:
        print("Nenhum conflito encontrado.")
    else:
        for conflito in analise["conflitos"]:
            A, terminal, antiga, nova = conflito
            print(f"Conflito em ({A}, {terminal}): {antiga} <-> {nova}")

    print(f"\nGramática é LL(1)? {analise['eh_ll1']}")


def gerarMarkdownGramatica(gramatica):
    producoes = gramatica["producoes"]
    terminais = gramatica["terminais"]
    nao_terminais = gramatica["nao_terminais"]
    
    linhas = [
        "# Gramática LL(1)",
        "",
        "## Símbolo Inicial",
        gramatica["simbolo_inicial"],
        "",
        "## Terminais",
    ]
    
    # Separar terminais em categorias
    t_sorted = sorted([t for t in terminais if t != EOF and t != EPSILON])
    operadores = [t for t in t_sorted if t in ["+", "-", "*", "/", "%", "^", "|"]]
    keywords = [t for t in t_sorted if t in ["START_CMD", "END_CMD", "RES", "SET", "GET", "IF", "IFELSE", "WHILE", "BLOCK"]]
    tipos = [t for t in t_sorted if t in ["INT", "REAL", "ID", "EOL"]]
    delim = [t for t in t_sorted if t in ["LPAREN", "RPAREN"]]
    
    partes = []
    if delim:
        partes.append(", ".join(delim))
    if tipos:
        partes.append(", ".join(tipos))
    if keywords:
        partes.append(", ".join(keywords))
    if operadores:
        partes.append(", ".join(operadores))
    
    linhas.append(", ".join(partes))
    linhas.append("")
    linhas.append("## Não-Terminais")
    linhas.append(", ".join(sorted(nao_terminais)))
    linhas.append("")
    linhas.append("---")
    linhas.append("")
    linhas.append("## Produções")
    linhas.append("")
    
    for nt in sorted(producoes.keys()):
        linhas.append(nt + " →")
        regras = producoes[nt]
        for i, regra in enumerate(regras):
            if regra == [EPSILON]:
                linhas.append("  | ε")
            else:
                regra_str = " ".join(regra)
                if i == 0:
                    linhas.append("  " + regra_str)
                else:
                    linhas.append("  | " + regra_str)
        linhas.append("")
    
    conteudo = "\n".join(linhas)
    with open("GRAMATICA_LL1.md", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("✓ Arquivo GRAMATICA_LL1.md gerado")


def gerarMarkdownFirstFollow(analise):
    first = analise["first"]
    follow = analise["follow"]
    
    linhas = [
        "# FIRST e FOLLOW",
        "",
        "## FIRST",
        ""
    ]
    
    for nt in sorted(first.keys()):
        conj = first[nt]
        conj_str = ", ".join(sorted([str(x) for x in conj]))
        linhas.append("FIRST(" + nt + ") = { " + conj_str + " }")
        linhas.append("")
    
    linhas.append("---")
    linhas.append("")
    linhas.append("## FOLLOW")
    linhas.append("")
    
    for nt in sorted(follow.keys()):
        conj = follow[nt]
        conj_str = ", ".join(sorted([str(x) for x in conj]))
        linhas.append("FOLLOW(" + nt + ") = { " + conj_str + " }")
        linhas.append("")
    
    conteudo = "\n".join(linhas)
    with open("FIRST_FOLLOW_LL1.md", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("✓ Arquivo FIRST_FOLLOW_LL1.md gerado")


def gerarMarkdownTabela(gramatica, analise):
    tabela = analise["tabela"]
    
    linhas = [
        "# Tabela LL(1)",
        "",
        "## Entradas da Tabela de Parsing",
        "",
    ]
    
    for nt in sorted(tabela.keys()):
        linhas.append("### " + nt)
        linhas.append("")
        
        entradas = tabela[nt]
        if not entradas:
            linhas.append("(nenhuma entrada)")
        else:
            for terminal in sorted(entradas.keys(), key=str):
                regra = entradas[terminal]
                regra_str = " ".join(str(r) for r in regra)
                linhas.append("M[" + nt + ", " + str(terminal) + "] = " + nt + " → " + regra_str)
        
        linhas.append("")
    
    conteudo = "\n".join(linhas)
    with open("TABELA_LL1.md", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("✓ Arquivo TABELA_LL1.md gerado")


if __name__ == "__main__":
    print("Gerando análise LL(1)...\n")
    
    gramatica = construirGramatica()
    analise = analisarLL1(gramatica)
    
    print("\n" + "="*50)
    imprimirAnalise(analise)
    print("="*50 + "\n")
    
    print("Gerando arquivos markdown...\n")
    gerarMarkdownGramatica(gramatica)
    gerarMarkdownFirstFollow(analise)
    gerarMarkdownTabela(gramatica, analise)
    
    print("\n✓ Análise LL(1) concluída com sucesso!")