EPSILON = "ε"
EOF = "$"


def construirGramatica():
    return {
        "simbolo_inicial": "Programa",

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
            "Programa",
            "ListaLinhas",
            "Linha",
            "Comando",
            "CorpoComando",
            "CorpoAposValor",
            "Valor",
            "Operador",
            "ListaComandosBloco"
        },

        "producoes": {
            "Programa": [
                ["START_CMD", "EOL", "ListaLinhas", "END_CMD", "EOL", EOF]
            ],

            "ListaLinhas": [
                ["Linha", "ListaLinhas"],
                [EPSILON]
            ],

            "Linha": [
                ["Comando", "EOL"]
            ],

            "Comando": [
                ["LPAREN", "CorpoComando", "RPAREN"]
            ],

            "CorpoComando": [
                ["RES", "INT"],
                ["SET", "Valor", "ID"],
                ["GET", "ID"],
                ["IF", "Valor", "Comando"],
                ["IFELSE", "Valor", "Comando", "Comando"],
                ["WHILE", "Valor", "Comando"],
                ["BLOCK", "ListaComandosBloco"],
                ["Valor", "CorpoAposValor"]
            ],

            "CorpoAposValor": [
                ["Valor", "Operador"]
            ],

            "ListaComandosBloco": [
                ["Linha", "ListaComandosBloco"],
                [EPSILON]
            ],

            "Valor": [
                ["INT"],
                ["REAL"],
                ["ID"],
                ["Comando"]
            ],

            "Operador": [
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


if __name__ == "__main__":
    gramatica = construirGramatica()
    analise = analisarLL1(gramatica)
    imprimirAnalise(analise)