# Tabela LL(1)

## Regras principais

M[Programa, START_CMD] =  
Programa -> START_CMD ListaLinhas END_CMD

---

M[ListaLinhas, LPAREN] =  
ListaLinhas -> Linha ListaLinhas  

M[ListaLinhas, END_CMD] =  
ListaLinhas -> ε

---

M[Linha, LPAREN] =  
Linha -> Comando EOL

---

M[Comando, LPAREN] =  
Comando -> LPAREN CorpoComando RPAREN

---

## CorpoComando

M[CorpoComando, RES] =  
CorpoComando -> RES Valor  

M[CorpoComando, SET] =  
CorpoComando -> SET ID Valor  

M[CorpoComando, GET] =  
CorpoComando -> GET ID  

M[CorpoComando, IF] =  
CorpoComando -> IF Valor Comando  

M[CorpoComando, IFELSE] =  
CorpoComando -> IFELSE Valor Comando Comando  

M[CorpoComando, WHILE] =  
CorpoComando -> WHILE Valor Comando  

M[CorpoComando, BLOCK] =  
CorpoComando -> BLOCK ListaComandosBloco  

M[CorpoComando, ID] =  
CorpoComando -> Valor CorpoAposValor  

M[CorpoComando, INT] =  
CorpoComando -> Valor CorpoAposValor  

M[CorpoComando, REAL] =  
CorpoComando -> Valor CorpoAposValor  

M[CorpoComando, LPAREN] =  
CorpoComando -> Valor CorpoAposValor  

---

## Valor

M[Valor, ID] = Valor -> ID  
M[Valor, INT] = Valor -> INT  
M[Valor, REAL] = Valor -> REAL  
M[Valor, LPAREN] = Valor -> LPAREN CorpoComando RPAREN  

---

## CorpoAposValor

M[CorpoAposValor, ID] =  
CorpoAposValor -> Valor Operador CorpoAposValor  

M[CorpoAposValor, INT] =  
CorpoAposValor -> Valor Operador CorpoAposValor  

M[CorpoAposValor, REAL] =  
CorpoAposValor -> Valor Operador CorpoAposValor  

M[CorpoAposValor, LPAREN] =  
CorpoAposValor -> Valor Operador CorpoAposValor  

M[CorpoAposValor, RPAREN] =  
CorpoAposValor -> ε  

---

## Operador

M[Operador, +] = Operador -> +  
M[Operador, -] = Operador -> -  
M[Operador, *] = Operador -> *  
M[Operador, /] = Operador -> /  
M[Operador, %] = Operador -> %  
M[Operador, ^] = Operador -> ^  
M[Operador, |] = Operador -> |  

---

## ListaComandosBloco

M[ListaComandosBloco, LPAREN] =  
ListaComandosBloco -> Comando ListaComandosBloco  

M[ListaComandosBloco, RPAREN] =  
ListaComandosBloco -> ε  

---

## Observação

A tabela não apresenta conflitos, confirmando que a gramática é LL(1).