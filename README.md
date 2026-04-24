# FASE 2 - Analisador Sintático LL(1)

Pontificia Universidade Catolica do Parana (PUCPR)

**Linguagens Formais e Compiladores - 2026**  
Prof. Frank Coelho de Alcantara

## Integrantes da equipe
- Andre Vinicius Zicka Schmidt
- Gabriel Fischer Domakoski

## Visao geral
Este projeto implementa a Fase 2 do trabalho: analisador sintatico LL(1) para uma linguagem em notacao polonesa reversa (RPN), com suporte a:
- Expressoes aritmeticas aninhadas
- Comandos especiais (`RES`, `SET`, `GET`)
- Estruturas de controle (`IF`, `IFELSE`, `WHILE`, `BLOCK`)
- Geracao e leitura de tokens estruturados

## Como executar
Executar o fluxo principal:

```bash
python main.py teste1.txt
```

Executar o teste de leitura de tokens:

```bash
python teste_ler_tokens.py
```

## Sintaxe das estruturas de controle
As estruturas seguem o padrao de parenteses da linguagem e operadores pos-fixados.

### IF
Executa um comando quando a condicao for verdadeira.

```text
(IF condicao comando)
```

Exemplo:

```text
(IF (3 2 >) (SET 1 FLAG))
```

### IFELSE
Executa um comando no caso verdadeiro e outro no caso falso.

```text
(IFELSE condicao comando_verdadeiro comando_falso)
```

Exemplo:

```text
(IFELSE (X 0 >) (SET 1 POS) (SET 0 POS))
```

### WHILE
Repete um comando enquanto a condicao for verdadeira.

```text
(WHILE condicao comando)
```

Exemplo:

```text
(WHILE (FLAG 0 >) (SET (FLAG 1 -) FLAG))
```

### BLOCK
Agrupa multiplos comandos como um unico bloco.

```text
(BLOCK (comando1) (comando2) ...)
```

## Operadores suportados
- Aritmeticos: `+`, `-`, `*`, `|`, `/`, `//`, `%`, `^`
- Relacionais: `>`, `<`, `>=`, `<=`, `==`, `!=`

## Formatos de entrada aceitos por `lerTokens`
A funcao `lerTokens(arquivo)` aceita tres formatos:

1. Codigo-fonte da linguagem (uma expressao/comando por linha)
2. Formato da Fase 1 com prefixo de linha:

```text
Linha 1: ['(', '3', '2', '+', ')']
Linha 2: ['(', 'IF', '...', ')']
```

3. Lista Python por linha:

```text
['(', '3', '2', '+', ')']
```

Tambem aceita arquivo ja estruturado com uma tupla por linha, por exemplo:

```text
('INT', 3)
('OPERADOR', '+')
('EOL', None)
```
