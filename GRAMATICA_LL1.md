# Gramática LL(1)

## Símbolo Inicial
Programa

## Terminais
START_CMD, END_CMD, LPAREN, RPAREN, ID, INT, REAL, EOL  
+, -, *, /, %, ^, |  
RES, SET, GET, IF, IFELSE, WHILE, BLOCK  

## Não-Terminais
Programa  
ListaLinhas  
Linha  
Comando  
CorpoComando  
Valor  
CorpoAposValor  
Operador  
ListaComandosBloco  

---

## Produções

Programa -> START_CMD ListaLinhas END_CMD

ListaLinhas -> Linha ListaLinhas | ε

Linha -> Comando EOL

Comando -> LPAREN CorpoComando RPAREN

CorpoComando ->
    RES Valor
  | SET ID Valor
  | GET ID
  | IF Valor Comando
  | IFELSE Valor Comando Comando
  | WHILE Valor Comando
  | BLOCK ListaComandosBloco
  | Valor CorpoAposValor

CorpoAposValor ->
    Valor Operador CorpoAposValor
  | ε

Valor ->
    ID
  | INT
  | REAL
  | LPAREN CorpoComando RPAREN

Operador ->
    +
  | -
  | *
  | /
  | %
  | ^
  | |

ListaComandosBloco ->
    Comando ListaComandosBloco
  | ε