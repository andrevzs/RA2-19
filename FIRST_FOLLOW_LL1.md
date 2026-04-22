# FIRST e FOLLOW

## FIRST

FIRST(Programa) = { START_CMD }

FIRST(ListaLinhas) = { LPAREN, ε }

FIRST(Linha) = { LPAREN }

FIRST(Comando) = { LPAREN }

FIRST(CorpoComando) = {  
BLOCK, GET, ID, IF, IFELSE, INT, LPAREN, REAL, RES, SET, WHILE  
}

FIRST(Valor) = { ID, INT, REAL, LPAREN }

FIRST(CorpoAposValor) = { ID, INT, REAL, LPAREN, ε }

FIRST(Operador) = { +, -, *, /, %, ^, | }

FIRST(ListaComandosBloco) = { LPAREN, ε }

---

## FOLLOW

FOLLOW(Programa) = { $ }

FOLLOW(ListaLinhas) = { END_CMD }

FOLLOW(Linha) = { END_CMD, LPAREN, RPAREN }

FOLLOW(Comando) = {  
%, *, +, -, /, EOL, ID, INT, LPAREN, REAL, RPAREN, ^, |  
}

FOLLOW(CorpoComando) = { RPAREN }

FOLLOW(Valor) = {  
%, *, +, -, /, ID, INT, LPAREN, REAL, ^, |  
}

FOLLOW(CorpoAposValor) = { RPAREN }

FOLLOW(Operador) = { RPAREN }

FOLLOW(ListaComandosBloco) = { RPAREN }