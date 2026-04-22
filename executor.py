def executarExpressao(tokens, memoria=None, resultados=None):
    if memoria is None:
        memoria = {}
    if resultados is None:
        resultados = []
    
    resultado_info = {
        'tipo': None,
        'operandos': [],
        'operadores': [],
        'memoria_var': None,
        'indice_res': None,
        'profundidade': 0
    }
    
    _processar_tokens(tokens, resultado_info, memoria, resultados)
    
    return resultado_info


def _processar_tokens(tokens, resultado_info, memoria, resultados):
    tokens_internos = tokens[1:-1]
    
    if len(tokens_internos) == 2 and tokens_internos[1] == "RES":
        # Comando (N RES)
        resultado_info['tipo'] = 'res_acesso'
        n = int(float(tokens_internos[0]))
        resultado_info['indice_res'] = n
    
    elif len(tokens_internos) == 2 and _eh_identificador(tokens_internos[1]):
        # Comando (V MEM) - armazenar em memória
        resultado_info['tipo'] = 'memoria_atrib'
        valor_token = tokens_internos[0]
        nome_var = tokens_internos[1]
        resultado_info['operandos'].append(valor_token)
        resultado_info['memoria_var'] = nome_var
        memoria[nome_var] = f"resultado_para_assembly"
    
    elif len(tokens_internos) == 1 and _eh_identificador(tokens_internos[0]):
        # Comando (MEM) - recuperar de memória
        resultado_info['tipo'] = 'memoria_acesso'
        nome_var = tokens_internos[0]
        resultado_info['memoria_var'] = nome_var
        if nome_var not in memoria:
            memoria[nome_var] = "0.0"
    
    else:
        # Expressão RPN normal
        resultado_info['tipo'] = 'expressao'
        _processar_rpn(tokens_internos, resultado_info, memoria, resultados)


def _processar_rpn(tokens, resultado_info, memoria, resultados):
    pilha_tipos = []
    profundidade = 0
    max_profundidade = 0
    i = 0
    
    while i < len(tokens):
        token = tokens[i]
        
        if token == "(":
            profundidade += 1
            max_profundidade = max(max_profundidade, profundidade)
            i += 1
            inicio = i
            
            contagem = 1
            while i < len(tokens) and contagem > 0:
                if tokens[i] == "(":
                    contagem += 1
                elif tokens[i] == ")":
                    contagem -= 1
                i += 1
            
            fim = i - 1
            sub_tokens = tokens[inicio:fim]
            
            sub_info = {
                'tipo': None,
                'operandos': [],
                'operadores': []
            }
            _processar_rpn(sub_tokens, sub_info, memoria, resultados)
            
            if sub_info['tipo'] is None:
                sub_info['tipo'] = 'expressao'
            
            pilha_tipos.append('valor')
            resultado_info['operandos'].append(sub_info)
            profundidade -= 1
            continue
        
        elif _eh_numero(token):
            pilha_tipos.append('valor')
            resultado_info['operandos'].append(token)
        
        elif _eh_identificador(token):
            pilha_tipos.append('valor')
            resultado_info['operandos'].append(token)
            if token not in memoria:
                memoria[token] = "0.0"
        
        elif token in ("+", "-", "*", "/", "//", "%", "^"):
            pilha_tipos.pop()
            pilha_tipos.pop()
            pilha_tipos.append('valor')
            resultado_info['operadores'].append(token)
        
        i += 1
    
    resultado_info['profundidade'] = max_profundidade


def _eh_numero(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def _eh_identificador(token):
    return token and all(c.isupper() for c in token) and token != "RES"

