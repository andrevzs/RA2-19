# Integrantes do grupo:
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Nome do grupo no Canvas: RA2 19

"""
Módulo parser.py - Implementação do Aluno 2

Responsabilidades:
- Validar teoricamente a gramática criada pelo Aluno 1 para garantir que é LL(1)
- Implementar parsear(_tokens_, tabela_ll1) para análise sintática descendente recursiva
- Usar a tabela LL(1) para guiar o processo de parsing
- Implementar a pilha de análise e controle de derivação
- Detectar e reportar erros sintáticos com mensagens claras
- Criar funções de teste para validar o parser
"""

from gramatica_ll1 import EPSILON, EOF


class ErroSintaticoException(Exception):
    """Exceção para erros sintáticos durante o parsing."""
    pass


class NodoArvore:
    """Representa um nó na árvore sintática."""

    def __init__(self, tipo, valor=None):
        """
        Args:
            tipo: 'terminal', 'nao_terminal', ou 'epsilon'
            valor: o token/símbolo representado
        """
        self.tipo = tipo
        self.valor = valor
        self.filhos = []

    def add_filho(self, nodo):
        """Adiciona um nó filho."""
        self.filhos.append(nodo)

    def __repr__(self):
        if self.tipo == "epsilon":
            return "ε"
        return f"{self.valor}"

    def __str__(self):
        return self._string_com_indentacao(0)

    def _string_com_indentacao(self, nivel=0):
        """Retorna representação em árvore com indentação."""
        indent = "  " * nivel

        if not self.filhos:
            return f"{indent}{self.valor}"

        linhas = [f"{indent}{self.valor}"]
        for filho in self.filhos:
            linhas.append(filho._string_com_indentacao(nivel + 1))

        return "\n".join(linhas)

    def para_dict(self):
        """Converte para dicionário JSON."""
        return {
            "tipo": self.tipo,
            "valor": self.valor,
            "filhos": [f.para_dict() for f in self.filhos]
        }


class Parser:
    """Parser descendente recursivo LL(1)."""

    def __init__(self, tokens, gramatica_analise):
        """
        Inicializa o parser.

        Args:
            tokens: Lista de tokens [(tipo, valor), ...]
            gramatica_analise: Resultado de analisarLL1() contendo tabela, first, follow
        """
        self.tokens = tokens
        self.pos = 0
        self.tabela = gramatica_analise["tabela"]
        self.first = gramatica_analise["first"]
        self.follow = gramatica_analise["follow"]
        self.eh_ll1 = gramatica_analise["eh_ll1"]
        self.conflitos = gramatica_analise["conflitos"]
        self.arvore_derivacao = None

        if not self.eh_ll1:
            self._reportar_erro_ll1()

    def _reportar_erro_ll1(self):
        """Reporta conflitos na gramática LL(1)."""
        mensagem = "Erro: A gramática não é LL(1). Conflitos encontrados:\n"
        for conflito in self.conflitos:
            A, terminal, regra1, regra2 = conflito
            r1_str = " ".join(regra1)
            r2_str = " ".join(regra2)
            mensagem += f"  ({A}, {terminal}): {A} → {r1_str} <-> {A} → {r2_str}\n"
        raise ErroSintaticoException(mensagem)

    def _token_atual(self):
        """Retorna o tipo do token atual ou EOF se chegou ao fim."""
        if self.pos < len(self.tokens):
            tipo, valor = self.tokens[self.pos]
            return tipo
        return EOF

    def _valor_token_atual(self):
        """Retorna o valor (parte não-tipo) do token atual."""
        if self.pos < len(self.tokens):
            tipo, valor = self.tokens[self.pos]
            return valor
        return None

    def _avancar(self):
        """Avança para o próximo token."""
        self.pos += 1

    def _tokens_completos_atual(self):
        """Retorna o token completo como tupla (tipo, valor)."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return (EOF, None)

    def _casa_com(self, terminal_esperado):
        """
        Faz match com um terminal esperado (consome o token).
        """
        token_tipo = self._token_atual()
        token_valor = self._valor_token_atual()

        if token_tipo == terminal_esperado:
            nodo = NodoArvore("terminal", terminal_esperado)
            self._avancar()
            return nodo

        if token_valor == terminal_esperado:
            nodo = NodoArvore("terminal", terminal_esperado)
            self._avancar()
            return nodo

        raise ErroSintaticoException(
            f"Erro sintático na posição {self.pos}: "
            f"esperado '{terminal_esperado}', "
            f"encontrado '{token_tipo}'"
        )

    def parsear(self):
        """
        Realiza o parsing da sequência de tokens.
        """
        try:
            self.arvore_derivacao = self._parsear_programa()

            if self._token_atual() != EOF:
                raise ErroSintaticoException(
                    f"Erro sintático: tokens não consumidos após fim esperado. "
                    f"Token restante: {self._token_atual()}"
                )

            return self.arvore_derivacao
        except ErroSintaticoException as e:
            raise e
        except Exception as e:
            raise ErroSintaticoException(f"Erro inesperado durante parsing: {str(e)}")

    def _parsear_programa(self):
        """Parseia: programa → START_CMD EOL listalinhas END_CMD EOL EOF"""
        nodo = NodoArvore("nao_terminal", "programa")

        nodo.add_filho(self._casa_com("START_CMD"))
        nodo.add_filho(self._casa_com("EOL"))
        nodo.add_filho(self._parsear_listalinhas())
        nodo.add_filho(self._casa_com("END_CMD"))
        nodo.add_filho(self._casa_com("EOL"))

        return nodo

    def _parsear_listalinhas(self):
        """
        Parseia: listalinhas → linha listalinhas | ε
        """
        nodo = NodoArvore("nao_terminal", "listalinhas")

        token_tipo = self._token_atual()

        if token_tipo == "LPAREN":
            nodo.add_filho(self._parsear_linha())
            nodo.add_filho(self._parsear_listalinhas())
        else:
            nodo.add_filho(NodoArvore("epsilon"))

        return nodo

    def _parsear_linha(self):
        """Parseia: linha → comando EOL"""
        nodo = NodoArvore("nao_terminal", "linha")

        nodo.add_filho(self._parsear_comando())
        nodo.add_filho(self._casa_com("EOL"))

        return nodo

    def _parsear_comando(self):
        """Parseia: comando → LPAREN corpocomando RPAREN"""
        nodo = NodoArvore("nao_terminal", "comando")

        nodo.add_filho(self._casa_com("LPAREN"))
        nodo.add_filho(self._parsear_corpocomando())
        nodo.add_filho(self._casa_com("RPAREN"))

        return nodo

    def _parsear_corpocomando(self):
        """
        Parseia corpocomando usando a tabela LL(1).

        corpocomando pode ser:
        - RES valor
        - SET valor ID
        - GET ID
        - IF valor comando
        - IFELSE valor comando comando
        - WHILE valor comando
        - BLOCK listacomando
        - valor corpoaposvalor
        """
        nodo = NodoArvore("nao_terminal", "corpocomando")

        token_tipo = self._token_atual()

        if token_tipo == "RES":
            nodo.add_filho(self._casa_com("RES"))
            nodo.add_filho(self._parsear_valor())

        elif token_tipo == "SET":
            nodo.add_filho(self._casa_com("SET"))
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._casa_com("ID"))

        elif token_tipo == "GET":
            nodo.add_filho(self._casa_com("GET"))
            nodo.add_filho(self._casa_com("ID"))

        elif token_tipo == "IF":
            nodo.add_filho(self._casa_com("IF"))
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_comando())

        elif token_tipo == "IFELSE":
            nodo.add_filho(self._casa_com("IFELSE"))
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_comando())
            nodo.add_filho(self._parsear_comando())

        elif token_tipo == "WHILE":
            nodo.add_filho(self._casa_com("WHILE"))
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_comando())

        elif token_tipo == "BLOCK":
            nodo.add_filho(self._casa_com("BLOCK"))
            nodo.add_filho(self._parsear_listacomando())

        elif token_tipo in ["INT", "REAL", "ID", "LPAREN"]:
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_corpoaposvalor())

        else:
            raise ErroSintaticoException(
                f"Erro sintático: token '{token_tipo}' não encontrado "
                f"na tabela para 'corpocomando'"
            )

        return nodo

    def _parsear_corpoaposvalor(self):
        """
        Parseia: corpoaposvalor → valor operador | ε

        Usa tabela LL(1) para decidir.
        """
        nodo = NodoArvore("nao_terminal", "corpoaposvalor")

        token_tipo = self._token_atual()

        if token_tipo in ["INT", "REAL", "ID", "LPAREN"]:
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_operador())
        else:
            nodo.add_filho(NodoArvore("epsilon"))

        return nodo

    def _parsear_valor(self):
        """
        Parseia: valor → INT | REAL | ID | comando
        """
        nodo = NodoArvore("nao_terminal", "valor")

        token_tipo = self._token_atual()

        if token_tipo == "INT":
            nodo.add_filho(self._casa_com("INT"))
        elif token_tipo == "REAL":
            nodo.add_filho(self._casa_com("REAL"))
        elif token_tipo == "ID":
            nodo.add_filho(self._casa_com("ID"))
        elif token_tipo == "LPAREN":
            nodo.add_filho(self._parsear_comando())
        else:
            raise ErroSintaticoException(
                f"Erro sintático: esperado valor (INT, REAL, ID ou comando), "
                f"encontrado '{token_tipo}'"
            )

        return nodo

    def _parsear_operador(self):
        """
        Parseia: operador → + | - | * | | | / | // | % | ^
        """
        nodo = NodoArvore("nao_terminal", "operador")

        token_tipo = self._token_atual()
        token_valor = self._valor_token_atual()

        operadores_validos = {"+", "-", "*", "|", "/", "//", "%", "^"}

        if token_tipo == "OPERADOR" and token_valor in operadores_validos:
            nodo.add_filho(NodoArvore("terminal", token_valor))
            self._avancar()
        elif token_valor in operadores_validos:
            nodo.add_filho(NodoArvore("terminal", token_valor))
            self._avancar()
        else:
            raise ErroSintaticoException(
                f"Erro sintático: operador esperado, encontrado '{token_tipo}' (valor: {token_valor})"
            )

        return nodo

    def _parsear_listacomando(self):
        """
        Parseia: listacomando → linha listacomando | ε
        """
        nodo = NodoArvore("nao_terminal", "listacomando")

        token_tipo = self._token_atual()

        if token_tipo == "LPAREN":
            nodo.add_filho(self._parsear_linha())
            nodo.add_filho(self._parsear_listacomando())
        else:
            nodo.add_filho(NodoArvore("epsilon"))

        return nodo


def validarGramatica(gramatica_analise):
    """
    Valida que a gramática é LL(1).
    """
    return gramatica_analise["eh_ll1"]


def parsear(tokens, gramatica_analise):
    """
    Realiza o parsing de uma lista de tokens usando a tabela LL(1).
    """
    try:
        parser = Parser(tokens, gramatica_analise)
        arvore = parser.parsear()

        return {
            "sucesso": True,
            "arvore": arvore,
            "erro": None,
            "derivacao": arvore
        }
    except ErroSintaticoException as e:
        return {
            "sucesso": False,
            "arvore": None,
            "erro": str(e),
            "derivacao": None
        }
    except Exception as e:
        return {
            "sucesso": False,
            "arvore": None,
            "erro": f"Erro inesperado: {str(e)}",
            "derivacao": None
        }


def testar_parser():
    """Testa o parser com vários casos."""
    from gramatica_ll1 import construirGramatica, analisarLL1

    gramatica = construirGramatica()
    analise = analisarLL1(gramatica)

    print("=" * 60)
    print("TESTES DO PARSER - ALUNO 2")
    print("=" * 60)

    print("\n[TESTE 1] Expressão aritmética simples: 3 2 +")
    tokens1 = [
        ("START_CMD", None),
        ("EOL", None),
        ("LPAREN", None),
        ("INT", 3),
        ("INT", 2),
        ("OPERADOR", "+"),
        ("RPAREN", None),
        ("EOL", None),
        ("END_CMD", None),
        ("EOL", None),
    ]
    resultado = parsear(tokens1, analise)
    if resultado["sucesso"]:
        print("✓ Parsing bem-sucedido!")
        print(resultado["arvore"])
    else:
        print(f"✗ Erro: {resultado['erro']}")

    print("\n[TESTE 2] SET com variável: SET 42 X")
    tokens2 = [
        ("START_CMD", None),
        ("EOL", None),
        ("LPAREN", None),
        ("SET", None),
        ("INT", 42),
        ("ID", "X"),
        ("RPAREN", None),
        ("EOL", None),
        ("END_CMD", None),
        ("EOL", None),
    ]
    resultado = parsear(tokens2, analise)
    if resultado["sucesso"]:
        print("✓ Parsing bem-sucedido!")
        print(resultado["arvore"])
    else:
        print(f"✗ Erro: {resultado['erro']}")

    print("\n[TESTE 3] IF: IF 5 (3 2 +)")
    tokens3 = [
        ("START_CMD", None),
        ("EOL", None),
        ("LPAREN", None),
        ("IF", None),
        ("INT", 5),
        ("LPAREN", None),
        ("INT", 3),
        ("INT", 2),
        ("OPERADOR", "+"),
        ("RPAREN", None),
        ("RPAREN", None),
        ("EOL", None),
        ("END_CMD", None),
        ("EOL", None),
    ]
    resultado = parsear(tokens3, analise)
    if resultado["sucesso"]:
        print("✓ Parsing bem-sucedido!")
    else:
        print(f"✗ Erro: {resultado['erro']}")

    print("\n[TESTE 4] WHILE: WHILE 5 (3 2 +)")
    tokens4 = [
        ("START_CMD", None),
        ("EOL", None),
        ("LPAREN", None),
        ("WHILE", None),
        ("INT", 5),
        ("LPAREN", None),
        ("INT", 3),
        ("INT", 2),
        ("OPERADOR", "+"),
        ("RPAREN", None),
        ("RPAREN", None),
        ("EOL", None),
        ("END_CMD", None),
        ("EOL", None),
    ]
    resultado = parsear(tokens4, analise)
    if resultado["sucesso"]:
        print("✓ Parsing bem-sucedido!")
    else:
        print(f"✗ Erro: {resultado['erro']}")

    print("\n[TESTE 5] Erro: parêntese não balanceado")
    tokens5 = [
        ("START_CMD", None),
        ("EOL", None),
        ("LPAREN", None),
        ("INT", 3),
        ("INT", 2),
        ("OPERADOR", "+"),
        ("END_CMD", None),
        ("EOL", None),
    ]
    resultado = parsear(tokens5, analise)
    if not resultado["sucesso"]:
        print(f"✓ Erro detectado corretamente: {resultado['erro']}")
    else:
        print("✗ Erro não foi detectado!")

    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")
    print("=" * 60)


if __name__ == "__main__":
    testar_parser()