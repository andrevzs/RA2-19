# Integrantes do grupo:
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Nome do grupo no Canvas: RA2 19

from gramatica_ll1 import EPSILON, EOF


class ErroSintaticoException(Exception):
    pass


class NodoArvore:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.filhos = []

    def add_filho(self, nodo):
        self.filhos.append(nodo)

    def __repr__(self):
        if self.tipo == "epsilon":
            return "ε"
        return f"{self.valor}"

    def __str__(self):
        return self._string_com_indentacao(0)

    def _string_com_indentacao(self, nivel=0):
        indent = "  " * nivel

        if not self.filhos:
            return f"{indent}{self.valor}"

        linhas = [f"{indent}{self.valor}"]
        for filho in self.filhos:
            linhas.append(filho._string_com_indentacao(nivel + 1))

        return "\n".join(linhas)

    def para_dict(self):
        return {
            "tipo": self.tipo,
            "valor": self.valor,
            "filhos": [f.para_dict() for f in self.filhos]
        }


class Parser:
    def __init__(self, tokens, gramatica_analise):
        self.tokens = tokens
        self.pos = 0
        self.tabela = gramatica_analise["tabela"]
        self.first = gramatica_analise["first"]
        self.follow = gramatica_analise["follow"]
        self.eh_ll1 = gramatica_analise["eh_ll1"]
        self.conflitos = gramatica_analise["conflitos"]

        if not self.eh_ll1:
            raise ErroSintaticoException("Gramática não é LL(1)")

    def _token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return EOF

    def _valor_token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][1]
        return None

    def _avancar(self):
        self.pos += 1

    def _casa_com(self, esperado):
        tipo = self._token_atual()
        valor = self._valor_token_atual()

        if tipo == esperado or valor == esperado:
            nodo = NodoArvore("terminal", esperado)
            self._avancar()
            return nodo

        raise ErroSintaticoException(f"Esperado {esperado}, encontrado {tipo}")

    def parsear(self):
        arvore = self._parsear_programa()

        if self._token_atual() != EOF:
            raise ErroSintaticoException("Tokens restantes após parsing")

        return arvore

    def _parsear_programa(self):
        nodo = NodoArvore("programa")

        nodo.add_filho(self._casa_com("START_CMD"))
        nodo.add_filho(self._casa_com("EOL"))
        nodo.add_filho(self._parsear_listalinhas())
        nodo.add_filho(self._casa_com("END_CMD"))
        nodo.add_filho(self._casa_com("EOL"))

        return nodo

    def _parsear_listalinhas(self):
        nodo = NodoArvore("listalinhas")

        if self._token_atual() == "LPAREN":
            nodo.add_filho(self._parsear_linha())
            nodo.add_filho(self._parsear_listalinhas())
        else:
            nodo.add_filho(NodoArvore("epsilon", "ε"))

        return nodo

    def _parsear_linha(self):
        nodo = NodoArvore("linha")

        nodo.add_filho(self._parsear_comando())
        nodo.add_filho(self._casa_com("EOL"))

        return nodo

    def _parsear_comando(self):
        nodo = NodoArvore("comando")

        nodo.add_filho(self._casa_com("LPAREN"))
        nodo.add_filho(self._parsear_corpocomando())
        nodo.add_filho(self._casa_com("RPAREN"))

        return nodo

    def _parsear_corpocomando(self):
        nodo = NodoArvore("corpocomando")
        token = self._token_atual()

        if token == "RES":
            nodo.add_filho(self._casa_com("RES"))
            nodo.add_filho(self._parsear_valor())

        elif token == "SET":
            nodo.add_filho(self._casa_com("SET"))
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._casa_com("ID"))

        elif token == "GET":
            nodo.add_filho(self._casa_com("GET"))
            nodo.add_filho(self._casa_com("ID"))

        elif token == "IF":
            nodo.add_filho(self._casa_com("IF"))
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_comando())

        elif token == "IFELSE":
            nodo.add_filho(self._casa_com("IFELSE"))
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_comando())
            nodo.add_filho(self._parsear_comando())

        elif token == "WHILE":
            nodo.add_filho(self._casa_com("WHILE"))
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_comando())

        elif token == "BLOCK":
            nodo.add_filho(self._casa_com("BLOCK"))
            nodo.add_filho(self._parsear_listacomando())

        else:
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_corpoaposvalor())

        return nodo

    def _parsear_corpoaposvalor(self):
        nodo = NodoArvore("corpoaposvalor")

        if self._token_atual() in ["INT", "REAL", "ID", "LPAREN"]:
            nodo.add_filho(self._parsear_valor())
            nodo.add_filho(self._parsear_operador())
        else:
            nodo.add_filho(NodoArvore("epsilon", "ε"))

        return nodo

    def _parsear_valor(self):
        nodo = NodoArvore("valor")
        token = self._token_atual()

        if token in ["INT", "REAL", "ID"]:
            nodo.add_filho(self._casa_com(token))
        elif token == "LPAREN":
            nodo.add_filho(self._parsear_comando())
        else:
            raise ErroSintaticoException("Valor inválido")

        return nodo

    def _parsear_operador(self):
        nodo = NodoArvore("operador")
        valor = self._valor_token_atual()

        operadores = {
            "+", "-", "*", "/", "//", "%", "^", "|",
            ">", "<", ">=", "<=", "==", "!="
        }

        if valor in operadores:
            nodo.add_filho(NodoArvore("terminal", valor))
            self._avancar()
        else:
            raise ErroSintaticoException("Operador inválido")

        return nodo


def parsear(tokens, analise):
    try:
        parser = Parser(tokens, analise)
        arvore = parser.parsear()

        return {"sucesso": True, "arvore": arvore, "erro": None}
    except Exception as e:
        return {"sucesso": False, "arvore": None, "erro": str(e)}