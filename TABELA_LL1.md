# Tabela LL(1)

## Entradas da Tabela de Parsing

### comando

M[comando, LPAREN] = comando → LPAREN corpocomando RPAREN

### corpoaposvalor

M[corpoaposvalor, ID] = corpoaposvalor → valor operador
M[corpoaposvalor, INT] = corpoaposvalor → valor operador
M[corpoaposvalor, LPAREN] = corpoaposvalor → valor operador
M[corpoaposvalor, REAL] = corpoaposvalor → valor operador
M[corpoaposvalor, RPAREN] = corpoaposvalor → ε

### corpocomando

M[corpocomando, BLOCK] = corpocomando → BLOCK listacomando
M[corpocomando, GET] = corpocomando → GET ID
M[corpocomando, ID] = corpocomando → valor corpoaposvalor
M[corpocomando, IF] = corpocomando → IF valor comando
M[corpocomando, IFELSE] = corpocomando → IFELSE valor comando comando
M[corpocomando, INT] = corpocomando → valor corpoaposvalor
M[corpocomando, LPAREN] = corpocomando → valor corpoaposvalor
M[corpocomando, REAL] = corpocomando → valor corpoaposvalor
M[corpocomando, RES] = corpocomando → RES valor
M[corpocomando, SET] = corpocomando → SET valor ID
M[corpocomando, WHILE] = corpocomando → WHILE valor comando

### linha

M[linha, LPAREN] = linha → comando EOL

### listacomando

M[listacomando, LPAREN] = listacomando → linha listacomando
M[listacomando, RPAREN] = listacomando → ε

### listalinhas

M[listalinhas, END_CMD] = listalinhas → ε
M[listalinhas, LPAREN] = listalinhas → linha listalinhas

### operador

M[operador, %] = operador → %
M[operador, *] = operador → *
M[operador, +] = operador → +
M[operador, -] = operador → -
M[operador, /] = operador → /
M[operador, ^] = operador → ^
M[operador, |] = operador → |

### programa

M[programa, START_CMD] = programa → START_CMD EOL listalinhas END_CMD EOL $

### valor

M[valor, ID] = valor → ID
M[valor, INT] = valor → INT
M[valor, LPAREN] = valor → comando
M[valor, REAL] = valor → REAL
