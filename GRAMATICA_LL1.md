# Gramática LL(1)

## Símbolo Inicial
programa

## Terminais
LPAREN, RPAREN, EOL, ID, INT, REAL, BLOCK, END_CMD, GET, IF, IFELSE, RES, SET, START_CMD, WHILE, !=, %, *, +, -, /, //, <, <=, ==, >, >=, ^, |

## Não-Terminais
comando, corpoaposvalor, corpocomando, linha, listacomando, listalinhas, operador, programa, valor

---

## Produções

comando →
  LPAREN corpocomando RPAREN

corpoaposvalor →
  valor operador
  | ε

corpocomando →
  RES valor
  | SET valor ID
  | GET ID
  | IF valor comando
  | IFELSE valor comando comando
  | WHILE valor comando
  | BLOCK listacomando
  | valor corpoaposvalor

linha →
  comando EOL

listacomando →
  linha listacomando
  | ε

listalinhas →
  linha listalinhas
  | ε

operador →
  +
  | -
  | *
  | |
  | /
  | //
  | %
  | ^
  | >
  | <
  | >=
  | <=
  | ==
  | !=

programa →
  START_CMD EOL listalinhas END_CMD EOL $

valor →
  INT
  | REAL
  | ID
  | comando
