# FIRST e FOLLOW

## FIRST

FIRST(comando) = { LPAREN }

FIRST(corpoaposvalor) = { ID, INT, LPAREN, REAL, ε }

FIRST(corpocomando) = { BLOCK, GET, ID, IF, IFELSE, INT, LPAREN, REAL, RES, SET, WHILE }

FIRST(linha) = { LPAREN }

FIRST(listacomando) = { LPAREN, ε }

FIRST(listalinhas) = { LPAREN, ε }

FIRST(operador) = { %, *, +, -, /, ^, | }

FIRST(programa) = { START_CMD }

FIRST(valor) = { ID, INT, LPAREN, REAL }

---

## FOLLOW

FOLLOW(comando) = { %, *, +, -, /, EOL, ID, INT, LPAREN, REAL, RPAREN, ^, | }

FOLLOW(corpoaposvalor) = { RPAREN }

FOLLOW(corpocomando) = { RPAREN }

FOLLOW(linha) = { END_CMD, LPAREN, RPAREN }

FOLLOW(listacomando) = { RPAREN }

FOLLOW(listalinhas) = { END_CMD }

FOLLOW(operador) = { RPAREN }

FOLLOW(programa) = { $ }

FOLLOW(valor) = { %, *, +, -, /, ID, INT, LPAREN, REAL, RPAREN, ^, | }
