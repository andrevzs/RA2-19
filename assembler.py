class GeradorAssembly:
    def __init__(self):
        self.codigo = []
        self.registrador_livre = 0
        self.pilha = []
        self.variaveis_memoria = {}
        self.constantes_float = {}
        self.labels_const = 0
        self.labels = 0
        self.resultados_linhas = set()

    def _novo_label_const(self):
        self.labels_const += 1
        return f"C_{self.labels_const}"

    def _novo_label(self):
        self.labels += 1
        return f"L_{self.labels}"

    def _label_resultado_linha(self, numero_linha):
        return f"RES_LINHA_{numero_linha}"

    def _proximo_registrador(self):
        if self.registrador_livre > 7:
            raise RuntimeError("Excedeu limite de registradores VFP (d0-d7)")
        reg = self.registrador_livre
        self.registrador_livre += 1
        return f"d{reg}"

    def _reiniciar_estado_expressao(self):
        self.registrador_livre = 0
        self.pilha = []

    def _registrar_variavel(self, nome_var):
        if nome_var not in self.variaveis_memoria:
            self.variaveis_memoria[nome_var] = nome_var

    def _registrar_resultado_linha(self, numero_linha):
        self.resultados_linhas.add(numero_linha)

    def _emit(self, linha):
        self.codigo.append(linha)

    def _carrega_constante_float(self, valor_str, reg_destino):
        try:
            valor_float = float(valor_str)
            valor_str = str(valor_float)
        except ValueError:
            pass

        if valor_str not in self.constantes_float:
            label = self._novo_label_const()
            self.constantes_float[valor_str] = label
        else:
            label = self.constantes_float[valor_str]

        self._emit(f"    LDR r0, ={label}")
        self._emit(f"    VLDR {reg_destino}, [r0]")

    def _salvar_resultado_linha(self, numero_linha):
        label = self._label_resultado_linha(numero_linha)
        self._registrar_resultado_linha(numero_linha)
        self._emit(f"    LDR r0, ={label}")
        self._emit("    VSTR d0, [r0]")

    def iniciar_programa(self):
        self.codigo = []
        self._emit(".text")
        self._emit(".global _start")
        self._emit("_start:")
        self._emit("")

    def finalizar_programa(self):
        self._emit("fim:")
        self._emit("    B fim")

        if self.constantes_float:
            self._emit("")
            self._emit(".align 3")
            for valor_str, label in self.constantes_float.items():
                self._emit(f"{label}: .double {valor_str}")

        self._emit("")
        self._emit(".data")
        self._emit(".align 3")

        for numero_linha in sorted(self.resultados_linhas):
            self._emit(f"{self._label_resultado_linha(numero_linha)}: .double 0.0")

        for nome_var in self.variaveis_memoria:
            self._emit(f"{nome_var}: .double 0.0")

    def _gerar_numero(self, numero_str):
        reg = self._proximo_registrador()

        try:
            float(numero_str)
        except ValueError:
            raise ValueError(f"Número inválido: {numero_str}")

        self._carrega_constante_float(numero_str, reg)
        self.pilha.append(reg)
        return reg

    def _gerar_variavel(self, nome_var):
        reg = self._proximo_registrador()
        self._registrar_variavel(nome_var)

        self._emit(f"    LDR r0, ={nome_var}")
        self._emit(f"    VLDR {reg}, [r0]")
        self.pilha.append(reg)
        return reg

    def _gerar_operacao(self, operador):
        if len(self.pilha) < 2:
            raise RuntimeError(f"Pilha insuficiente para operação {operador}")

        reg_b = self.pilha.pop()
        reg_a = self.pilha.pop()

        if operador == "+":
            self._emit(f"    VADD.F64 {reg_a}, {reg_a}, {reg_b}")

        elif operador == "-":
            self._emit(f"    VSUB.F64 {reg_a}, {reg_a}, {reg_b}")

        elif operador == "*":
            self._emit(f"    VMUL.F64 {reg_a}, {reg_a}, {reg_b}")

        elif operador == "/":
            self._emit(f"    VDIV.F64 {reg_a}, {reg_a}, {reg_b}")

        elif operador == "//":
            loop = self._novo_label()
            fim = self._novo_label()

            self._emit(f"    VCVT.S32.F64 s0, {reg_a}")
            self._emit(f"    VCVT.S32.F64 s1, {reg_b}")
            self._emit("    VMOV r1, s0")   # dividendo
            self._emit("    VMOV r2, s1")   # divisor
            self._emit("    MOV r3, #0")    # quociente

            self._emit(f"{loop}:")
            self._emit("    CMP r1, r2")
            self._emit(f"    BLT {fim}")
            self._emit("    SUB r1, r1, r2")
            self._emit("    ADD r3, r3, #1")
            self._emit(f"    B {loop}")

            self._emit(f"{fim}:")
            self._emit("    VMOV s2, r3")
            self._emit(f"    VCVT.F64.S32 {reg_a}, s2")

        elif operador == "%":
            loop = self._novo_label()
            fim = self._novo_label()

            self._emit(f"    VCVT.S32.F64 s0, {reg_a}")
            self._emit(f"    VCVT.S32.F64 s1, {reg_b}")
            self._emit("    VMOV r1, s0")   # dividendo
            self._emit("    VMOV r2, s1")   # divisor

            self._emit(f"{loop}:")
            self._emit("    CMP r1, r2")
            self._emit(f"    BLT {fim}")
            self._emit("    SUB r1, r1, r2")
            self._emit(f"    B {loop}")

            self._emit(f"{fim}:")
            self._emit("    VMOV s2, r1")
            self._emit(f"    VCVT.F64.S32 {reg_a}, s2")

        elif operador == "^":
            loop = self._novo_label()
            fim = self._novo_label()

            self._emit(f"    VCVT.S32.F64 s0, {reg_a}")
            self._emit("    VMOV r1, s0")
            self._emit(f"    VCVT.S32.F64 s1, {reg_b}")
            self._emit("    VMOV r2, s1")
            self._emit("    MOV r3, #1")

            self._emit(f"{loop}:")
            self._emit("    CMP r2, #0")
            self._emit(f"    BEQ {fim}")
            self._emit("    MUL r3, r3, r1")
            self._emit("    SUB r2, r2, #1")
            self._emit(f"    B {loop}")

            self._emit(f"{fim}:")
            self._emit("    VMOV s2, r3")
            self._emit(f"    VCVT.F64.S32 {reg_a}, s2")

        else:
            raise ValueError(f"Operador desconhecido: {operador}")

        self.pilha.append(reg_a)
        return reg_a

    def _gerar_sub_expressao(self, sub_info):
        if sub_info["tipo"] != "expressao":
            return

        for operando in sub_info["operandos"]:
            if isinstance(operando, dict):
                self._gerar_sub_expressao(operando)
            else:
                try:
                    self._gerar_numero(operando)
                except ValueError:
                    self._gerar_variavel(operando)

        for operador in sub_info["operadores"]:
            self._gerar_operacao(operador)

    def adicionar_linha(self, numero_linha, resultado_executor):
        self._reiniciar_estado_expressao()
        self._emit(f"    @ Linha {numero_linha}")

        if resultado_executor["tipo"] == "expressao":
            self._gerar_sub_expressao(resultado_executor)

        elif resultado_executor["tipo"] == "memoria_atrib":
            nome_var = resultado_executor["memoria_var"]
            self._registrar_variavel(nome_var)

            for operando in resultado_executor["operandos"]:
                try:
                    self._gerar_numero(operando)
                except ValueError:
                    self._gerar_variavel(operando)

            if self.pilha:
                valor_reg = self.pilha[-1]
                self._emit(f"    LDR r0, ={nome_var}")
                self._emit(f"    VSTR {valor_reg}, [r0]")

        elif resultado_executor["tipo"] == "memoria_acesso":
            nome_var = resultado_executor["memoria_var"]
            self._registrar_variavel(nome_var)
            self._emit(f"    LDR r0, ={nome_var}")
            self._emit("    VLDR d0, [r0]")

        elif resultado_executor["tipo"] == "res_acesso":
            indice = resultado_executor["indice_res"]
            linha_alvo = numero_linha - indice

            if 1 <= linha_alvo < numero_linha:
                label = self._label_resultado_linha(linha_alvo)
                self._registrar_resultado_linha(linha_alvo)
                self._emit(f"    LDR r0, ={label}")
                self._emit("    VLDR d0, [r0]")
            else:
                self._emit("    @ RES invalido, carregando 0.0")
                self._carrega_constante_float("0.0", "d0")

        if resultado_executor["tipo"] == "expressao" and self.pilha:
            resultado_final = self.pilha[-1]
            if resultado_final != "d0":
                self._emit("    @ Resultado final em registrador diferente de d0")
                self._emit(f"    LDR r0, ={self._label_resultado_linha(numero_linha)}")
                self._emit(f"    VSTR {resultado_final}, [r0]")
                self._emit(f"    VLDR d0, [r0]")
                self._registrar_resultado_linha(numero_linha)
            else:
                self._salvar_resultado_linha(numero_linha)

        elif resultado_executor["tipo"] in ("memoria_atrib", "memoria_acesso", "res_acesso"):
            self._salvar_resultado_linha(numero_linha)

        self._emit("")

    def obter_codigo(self):
        return "\n".join(self.codigo)


def gerarAssembly(resultado_executor):
    gerador = GeradorAssembly()
    gerador.iniciar_programa()
    gerador.adicionar_linha(1, resultado_executor)
    gerador.finalizar_programa()
    return gerador.obter_codigo()