# -*- coding: utf-8 -*-
# Integrantes do grupo:
# André Vinícius Zicka Schmidt - GitHub: andrevzs
# Gabriel Fischer Domakoski - GitHub: fochu3013
#
# Nome do grupo no Canvas: RA2 19

"""
Testes Unitários para o Parser LL(1) - Aluno 2

Este módulo implementa testes completos do analisador sintático,
cobrindo:
- Expressões RPN válidas simples e aninhadas
- Commandos especiais (RES, SET, GET)
- Estruturas de controle (IF, IFELSE, WHILE)
- Blocos de comandos (BLOCK)
- Erros sintáticos e detecção de anomalias
"""

from parser import Parser, parsear, NodoArvore, ErroSintaticoException
from gramatica_ll1 import construirGramatica, analisarLL1, EPSILON, EOF


class ConversorTokensLexer:
    """
    Converte tokens vindos do lexer em formato adequado para o parser.
    
    O lexer retorna uma lista de strings simples.
    O parser espera: [(tipo, valor), ...]
    
    Esta classe mapeia os tokens do lexer para tipos apropriados.
    """
    
    @staticmethod
    def converter(tokens_lexer):
        """
        Converte lista de tokens do lexer para formato esperado pelo parser.
        
        Args:
            tokens_lexer: Lista de strings (saída do lexer)
            
        Returns:
            Lista de tuplas (tipo, valor)
        """
        tokens_convertidos = []
        
        # Types mapeados
        TIPOS = {
            "START_CMD": "START_CMD",
            "END_CMD": "END_CMD",
            "RES": "RES",
            "SET": "SET",
            "GET": "GET",
            "IF": "IF",
            "IFELSE": "IFELSE",
            "WHILE": "WHILE",
            "BLOCK": "BLOCK",
        }
        
        OPERADORES = {"+", "-", "*", "|", "/", "%", "^"}
        DELIMITADORES = {"(", ")"}
        
        # Especial: EOL é inserido automaticamente entre linhas
        
        for token in tokens_lexer:
            # Classificar o token
            if token in TIPOS:
                tokens_convertidos.append((token, token))
            elif token == "(":
                tokens_convertidos.append(("LPAREN", "("))
            elif token == ")":
                tokens_convertidos.append(("RPAREN", ")"))
            elif token in OPERADORES:
                tokens_convertidos.append(("OPERADOR", token))
            elif ConversorTokensLexer._eh_numero(token):
                if "." in token:
                    tokens_convertidos.append(("REAL", float(token)))
                else:
                    tokens_convertidos.append(("INT", int(token)))
            elif ConversorTokensLexer._eh_identificador(token):
                tokens_convertidos.append(("ID", token))
            else:
                # Token desconhecido - reportar erro
                raise ValueError(f"Token desconhecido: '{token}'")
        
        return tokens_convertidos
    
    @staticmethod
    def _eh_numero(token):
        """Verifica se token é número inteiro ou real."""
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def _eh_identificador(token):
        """Verifica se token é identificador (todas maiúsculas)."""
        return token.isupper() and len(token) > 0


class TestadorParser:
    """Executa testes do parser com relatório detalhado."""
    
    def __init__(self):
        self.gramatica = construirGramatica()
        self.analise_ll1 = analisarLL1(self.gramatica)
        self.testes_executados = 0
        self.testes_passou = 0
        self.testes_falharam = 0
    
    def _construir_programa_completo(self, tokens_linhas):
        """
        Constrói um programa completo com START/END.
        
        Args:
            tokens_linhas: Lista de listas de tokens (cada sublista é uma linha)
                          
        Returns:
            Lista de tokens do programa completo
        """
        tokens = [("START_CMD", "START_CMD"), ("EOL", None)]
        
        for linha_tokens in tokens_linhas:
            tokens.extend(linha_tokens)
            tokens.append(("EOL", None))
        
        tokens.extend([
            ("END_CMD", "END_CMD"),
            ("EOL", None)
        ])
        
        return tokens
    
    def _testar_caso(self, nome, tokens, esperado_sucesso, descricao=""):
        """
        Executa um caso de teste.
        
        Args:
            nome: Nome do teste
            tokens: Lista de tokens a parsear
            esperado_sucesso: True se esperamos sucesso, False se esperamos erro
            descricao: Descrição adicional
        """
        self.testes_executados += 1
        print(f"\n{'='*70}")
        print(f"[TESTE {self.testes_executados}] {nome}")
        if descricao:
            print(f"Descrição: {descricao}")
        print(f"{'='*70}")
        
        resultado = parsear(tokens, self.analise_ll1)
        
        if resultado["sucesso"] == esperado_sucesso:
            self.testes_passou += 1
            print("[PASSOU]")
            
            if resultado["sucesso"]:
                print(f"\nArvore sintatica:")
                print("-" * 70)
                print(resultado["arvore"])
                print("-" * 70)
            else:
                print(f"\nErro detectado corretamente:")
                print(f"  {resultado['erro']}")
        else:
            self.testes_falharam += 1
            print("[FALHOU]")
            print(f"Esperado: {'sucesso' if esperado_sucesso else 'erro'}")
            print(f"Obtido: {'sucesso' if resultado['sucesso'] else 'erro'}")
            if resultado["erro"]:
                print(f"Erro: {resultado['erro']}")
    
    def teste_expressao_simples(self):
        """Teste 1: Expressão aritmética simples."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("INT", 3),
                ("INT", 2),
                ("OPERADOR", "+"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Expressão Aritmética Simples",
            tokens,
            True,
            "Soma RPN: (3 2 +)"
        )
    
    def teste_expressao_aninhada(self):
        """Teste 2: Expressão aritmética aninhada."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("LPAREN", "("),
                ("INT", 3),
                ("INT", 2),
                ("OPERADOR", "+"),
                ("RPAREN", ")"),
                ("INT", 5),
                ("OPERADOR", "*"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Expressão Aritmética Aninhada",
            tokens,
            True,
            "Multiplicação de expressão: ((3 2 +) 5 *)"
        )
    
    def teste_multiplos_operadores(self):
        """Teste 3: Expressão com múltiplos operadores."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("INT", 10),
                ("INT", 5),
                ("OPERADOR", "-"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Subtração RPN",
            tokens,
            True,
            "Subtração: (10 5 -)"
        )
    
    def teste_divisao_real(self):
        """Teste 4: Divisão real."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("REAL", 20.0),
                ("REAL", 4.5),
                ("OPERADOR", "|"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Divisão Real",
            tokens,
            True,
            "Divisão real: (20.0 4.5 |)"
        )
    
    def teste_potencia(self):
        """Teste 5: Potenciação."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("INT", 2),
                ("INT", 3),
                ("OPERADOR", "^"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Potenciação",
            tokens,
            True,
            "Potência: (2 3 ^)"
        )
    
    def teste_resto_divisao(self):
        """Teste 6: Resto da divisão."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("INT", 17),
                ("INT", 5),
                ("OPERADOR", "%"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Resto da Divisão",
            tokens,
            True,
            "Resto: (17 5 %)"
        )
    
    def teste_identificador(self):
        """Teste 7: Identificador (variável)."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("ID", "X"),
                ("INT", 2),
                ("OPERADOR", "+"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Identificador em Operação",
            tokens,
            True,
            "Soma com variável: (X 2 +)"
        )
    
    def teste_set_comando(self):
        """Teste 8: Comando SET."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("SET", "SET"),
                ("INT", 42),
                ("ID", "CONTADOR"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Comando SET",
            tokens,
            True,
            "SET: (SET 42 CONTADOR)"
        )
    
    def teste_get_comando(self):
        """Teste 9: Comando GET."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("GET", "GET"),
                ("ID", "RESULTADO"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Comando GET",
            tokens,
            True,
            "GET: (GET RESULTADO)"
        )
    
    def teste_res_comando(self):
        """Teste 10: Comando RES."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("RES", "RES"),
                ("INT", 1),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Comando RES",
            tokens,
            True,
            "RES: (RES 1)"
        )
    
    def teste_if_simples(self):
        """Teste 11: Estrutura IF."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("IF", "IF"),
                ("INT", 5),
                ("LPAREN", "("),
                ("INT", 3),
                ("INT", 2),
                ("OPERADOR", "+"),
                ("RPAREN", ")"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Estrutura IF Simples",
            tokens,
            True,
            "IF: (IF 5 (3 2 +))"
        )
    
    def teste_ifelse(self):
        """Teste 12: Estrutura IFELSE."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("IFELSE", "IFELSE"),
                ("INT", 5),
                ("LPAREN", "("),
                ("INT", 10),
                ("RPAREN", ")"),
                ("LPAREN", "("),
                ("INT", 20),
                ("RPAREN", ")"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Estrutura IFELSE",
            tokens,
            True,
            "IFELSE: (IFELSE 5 (10) (20))"
        )
    
    def teste_while(self):
        """Teste 13: Estrutura WHILE."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("WHILE", "WHILE"),
                ("ID", "CONT"),
                ("LPAREN", "("),
                ("INT", 1),
                ("INT", 2),
                ("OPERADOR", "+"),
                ("RPAREN", ")"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Estrutura WHILE",
            tokens,
            True,
            "WHILE: (WHILE CONT (1 2 +))"
        )
    
    def teste_block(self):
        """Teste 14: Bloco de comandos."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("BLOCK", "BLOCK"),
                ("LPAREN", "("),
                ("SET", "SET"),
                ("INT", 5),
                ("ID", "X"),
                ("RPAREN", ")"),
                ("EOL", None),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Bloco de Comandos",
            tokens,
            True,
            "BLOCK: (BLOCK ((SET 5 X)))"
        )
    
    def teste_multiplas_linhas(self):
        """Teste 15: Múltiplas linhas."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("INT", 3),
                ("INT", 2),
                ("OPERADOR", "+"),
                ("RPAREN", ")")
            ],
            [
                ("LPAREN", "("),
                ("SET", "SET"),
                ("INT", 10),
                ("ID", "RESULT"),
                ("RPAREN", ")")
            ],
            [
                ("LPAREN", "("),
                ("GET", "GET"),
                ("ID", "RESULT"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Múltiplas Linhas",
            tokens,
            True,
            "Programa com 3 linhas"
        )
    
    def teste_erro_parentese_faltante(self):
        """Teste 16: Erro - parêntese faltante."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("INT", 3),
                ("INT", 2),
                ("OPERADOR", "+")
                # Falta RPAREN
            ]
        ])
        self._testar_caso(
            "ERRO: Parêntese Faltante",
            tokens,
            False,
            "Detecta parêntese de abertura não fechada"
        )
    
    def teste_erro_operador_faltante(self):
        """Teste 17: Erro - operador faltante."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("INT", 3),
                ("INT", 2),
                ("RPAREN", ")")
                # Falta operador em RPN
            ]
        ])
        self._testar_caso(
            "ERRO: Operador Faltante em RPN",
            tokens,
            False,
            "Valor sem operador após outro valor"
        )
    
    def teste_erro_set_sem_id(self):
        """Teste 18: Erro - SET sem ID."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("SET", "SET"),
                ("INT", 42),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "ERRO: SET sem Identificador",
            tokens,
            False,
            "SET deve ter ID como terceiro argumento"
        )
    
    def teste_aninhamento_profundo(self):
        """Teste 19: Aninhamento profundo."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("LPAREN", "("),
                ("LPAREN", "("),
                ("INT", 1),
                ("INT", 2),
                ("OPERADOR", "+"),
                ("RPAREN", ")"),
                ("INT", 3),
                ("OPERADOR", "*"),
                ("RPAREN", ")"),
                ("INT", 4),
                ("OPERADOR", "-"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "Aninhamento Profundo",
            tokens,
            True,
            "Expressão com 3 níveis de aninhamento: (((1 2 +) 3 *) 4 -)"
        )
    
    def teste_set_com_expressao(self):
        """Teste 20: SET com expressão como valor."""
        tokens = self._construir_programa_completo([
            [
                ("LPAREN", "("),
                ("SET", "SET"),
                ("LPAREN", "("),
                ("INT", 5),
                ("INT", 3),
                ("OPERADOR", "+"),
                ("RPAREN", ")"),
                ("ID", "VAR"),
                ("RPAREN", ")")
            ]
        ])
        self._testar_caso(
            "SET com Expressão",
            tokens,
            True,
            "SET: (SET (5 3 +) VAR)"
        )
    
    def executar_todos_testes(self):
        """Executa todos os testes."""
        print("\n" + "="*70)
        print("TESTES COMPLETOS DO PARSER LL(1) - ALUNO 2")
        print("="*70)
        
        # Verificar se gramática é LL(1)
        print(f"\nValidação da Gramática:")
        print(f"  Gramática é LL(1)? {self.analise_ll1['eh_ll1']}")
        if not self.analise_ll1['eh_ll1']:
            print(f"  Conflitos encontrados: {len(self.analise_ll1['conflitos'])}")
            for conflito in self.analise_ll1['conflitos']:
                A, terminal, _, _ = conflito
                print(f"    - ({A}, {terminal})")
        print()
        
        # Testes de casos válidos
        self.teste_expressao_simples()
        self.teste_expressao_aninhada()
        self.teste_multiplos_operadores()
        self.teste_divisao_real()
        self.teste_potencia()
        self.teste_resto_divisao()
        self.teste_identificador()
        self.teste_set_comando()
        self.teste_get_comando()
        self.teste_res_comando()
        self.teste_if_simples()
        self.teste_ifelse()
        self.teste_while()
        self.teste_block()
        self.teste_multiplas_linhas()
        
        # Testes de casos com erro
        self.teste_erro_parentese_faltante()
        self.teste_erro_operador_faltante()
        self.teste_erro_set_sem_id()
        
        # Testes especiais
        self.teste_aninhamento_profundo()
        self.teste_set_com_expressao()
        
        # Relatório final
        self._relatorio_final()
    
    def _relatorio_final(self):
        """Imprime relatório final dos testes."""
        print("\n" + "="*70)
        print("RELATORIO FINAL")
        print("="*70)
        print(f"Total de testes: {self.testes_executados}")
        print(f"Testes passaram: {self.testes_passou} [OK]")
        print(f"Testes falharam: {self.testes_falharam} [ERRO]")
        
        percentual = (self.testes_passou / self.testes_executados * 100) if self.testes_executados > 0 else 0
        print(f"Taxa de sucesso: {percentual:.1f}%")
        
        if self.testes_falharam == 0:
            print("\n[OK] TODOS OS TESTES PASSARAM!")
        else:
            print(f"\n[ERRO] {self.testes_falharam} teste(s) falharam")
        print("="*70 + "\n")


def main():
    """Executa os testes."""
    testador = TestadorParser()
    testador.executar_todos_testes()


if __name__ == "__main__":
    main()
