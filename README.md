# FASE 2 - Analisador Sintático LL(1)

Pontifícia Universidade Católica do Paraná (PUCPR)  
Linguagens Formais e Compiladores - 2026  
Prof. Frank Coelho de Alcantara  

##  Integrantes da equipe

- André Vinícius Zicka Schmidt  
- Gabriel Fischer Domakoski  

---

##  Visão Geral

Este projeto implementa a **Fase 2** do trabalho da disciplina, consistindo na construção de um **analisador sintático LL(1)** para uma linguagem baseada em **notação polonesa reversa (RPN)**.

A linguagem suporta:

- Expressões aritméticas aninhadas
- Comandos especiais (`RES`, `SET`, `GET`)
- Estruturas de controle (`IF`, `IFELSE`, `WHILE`, `BLOCK`)
- Leitura e interpretação de tokens estruturados
- Integração com execução e geração de assembly

---

##  Gramática LL(1)

A gramática da linguagem foi **refatorada para o formato LL(1)**, eliminando ambiguidades e conflitos.

Foram implementados:

- Cálculo dos conjuntos **FIRST**
- Cálculo dos conjuntos **FOLLOW**
- Construção da **tabela de análise LL(1)**

A validação da gramática confirmou que:

Gramática é LL(1)? True

---

##  Analisador Sintático

O parser foi implementado como um **analisador descendente recursivo LL(1)**.

Características:

- Consome tokens gerados pelo lexer
- Valida a estrutura sintática do programa
- Constrói uma **árvore sintática**
- Detecta e reporta erros sintáticos

---

##  Como Executar

Executar o fluxo principal:

```bash
python main.py teste1.txt
python main.py teste2.txt
python main.py teste3.txt
```

---

##  Formato do Programa

Todo programa deve obrigatoriamente seguir o formato:

```
(START)
...
(END)
```

As expressões e comandos devem estar contidos entre essas duas marcações.

---

##  Sintaxe das Estruturas de Controle

As estruturas seguem o padrão da linguagem: uso de parênteses e notação pós-fixada (RPN).

### IF

Executa um comando se a condição for verdadeira:

```
(IF condicao comando)
```

Exemplo:

```
(IF (3 2 >) (SET 1 FLAG))
```

---

### IFELSE

Executa um comando para verdadeiro e outro para falso:

```
(IFELSE condicao comando_verdadeiro comando_falso)
```

Exemplo:

```
(IFELSE (X 0 >) (SET 1 POS) (SET 0 POS))
```

---

### WHILE

Executa repetidamente enquanto a condição for verdadeira:

```
(WHILE condicao comando)
```

Exemplo:

```
(WHILE (FLAG 0 >) (SET (FLAG 1 -) FLAG))
```

---

### BLOCK

Agrupa múltiplos comandos:

```
(BLOCK (comando1) (comando2) ...)
```

---

##  Operadores Suportados

### Aritméticos

```
+   Adição  
-   Subtração  
*   Multiplicação  
|   Divisão real  
/   Divisão inteira  
//  Divisão inteira explícita  
%   Resto da divisão  
^   Potenciação  
```

### Relacionais

```
>   maior  
<   menor  
>=  maior ou igual  
<=  menor ou igual  
==  igual  
!=  diferente  
```

---

##  Formatos de Entrada (lerTokens)

A função `lerTokens(arquivo)` aceita três formatos:

### 1. Código-fonte da linguagem

```
(3 2 +)
(IF ...)
```

---

### 2. Formato da Fase 1

```
Linha 1: ['(', '3', '2', '+', ')']
Linha 2: ['(', 'IF', ... ')']
```

---

### 3. Lista Python por linha

```
['(', '3', '2', '+', ')']
```

---

Também aceita tokens estruturados:

```
('INT', 3)
('OPERADOR', '+')
('EOL', None)
```

---

##  Saída do Programa

Durante a execução, o sistema:

- Exibe os tokens gerados
- Executa as expressões
- Indica sucesso ou erro sintático

---

##  Execução no CPulator

Na geração de assembly:

- Os resultados são armazenados na memória em:

```
RES_LINHA_X
```

- Os valores são armazenados como **double (IEEE 754)**

Exemplo:

```
405A8000 → 106.0
```

O resultado pode ser verificado no CPulator acessando:

```
Memory → RES_LINHA_X
```

---

##  Conclusão

O projeto implementa:

- Gramática LL(1) válida
- Parser funcional
- Suporte a estruturas de controle
- Integração completa com execução e assembly
