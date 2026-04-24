.text
.global _start
_start:

    @ Linha 1
    LDR r0, =C_1
    VLDR d0, [r0]
    LDR r0, =C_2
    VLDR d1, [r0]
    VADD.F64 d0, d0, d1
    LDR r0, =RES_LINHA_1
    VSTR d0, [r0]

    @ Linha 2
    @ RES invalido, carregando 0.0
    LDR r0, =C_3
    VLDR d0, [r0]
    LDR r0, =RES_LINHA_2
    VSTR d0, [r0]

    @ Linha 3
    LDR r0, =C_4
    VLDR d0, [r0]
    LDR r0, =CONTADOR
    VSTR d0, [r0]
    LDR r0, =RES_LINHA_3
    VSTR d0, [r0]

    @ Linha 4
    LDR r0, =CONTADOR
    VLDR d0, [r0]
    LDR r0, =RES_LINHA_4
    VSTR d0, [r0]

    @ Linha 5
    LDR r0, =C_2
    VLDR d0, [r0]
    LDR r0, =C_5
    VLDR d1, [r0]
    VADD.F64 d0, d0, d1
    LDR r0, =C_6
    VLDR d2, [r0]
    LDR r0, =C_7
    VLDR d3, [r0]
    VMUL.F64 d2, d2, d3
    VDIV.F64 d0, d0, d2
    LDR r0, =RES_LINHA_5
    VSTR d0, [r0]

    @ Linha 6
    LDR r0, =C_8
    VLDR d0, [r0]
    LDR r0, =C_5
    VLDR d1, [r0]
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s1, d1
    VMOV r1, s0
    VMOV r2, s1
    MOV r3, #0
L_1:
    CMP r1, r2
    BLT L_2
    SUB r1, r1, r2
    ADD r3, r3, #1
    B L_1
L_2:
    VMOV s2, r3
    VCVT.F64.S32 d0, s2
    LDR r0, =RES_LINHA_6
    VSTR d0, [r0]

    @ Linha 7
    LDR r0, =C_9
    VLDR d0, [r0]
    LDR r0, =C_10
    VLDR d1, [r0]
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s1, d1
    VMOV r1, s0
    VMOV r2, s1
L_3:
    CMP r1, r2
    BLT L_4
    SUB r1, r1, r2
    B L_3
L_4:
    VMOV s2, r1
    VCVT.F64.S32 d0, s2
    LDR r0, =RES_LINHA_7
    VSTR d0, [r0]

    @ Linha 8
    LDR r0, =C_2
    VLDR d0, [r0]
    LDR r0, =C_11
    VLDR d1, [r0]
    VCVT.S32.F64 s0, d0
    VMOV r1, s0
    VCVT.S32.F64 s1, d1
    VMOV r2, s1
    MOV r3, #1
L_5:
    CMP r2, #0
    BEQ L_6
    MUL r3, r3, r1
    SUB r2, r2, #1
    B L_5
L_6:
    VMOV s2, r3
    VCVT.F64.S32 d0, s2
    LDR r0, =RES_LINHA_8
    VSTR d0, [r0]

    @ Linha 9
    LDR r0, =C_12
    VLDR d0, [r0]
    LDR r0, =VAR
    VSTR d0, [r0]
    LDR r0, =RES_LINHA_9
    VSTR d0, [r0]

    @ Linha 10
    LDR r0, =VAR
    VLDR d0, [r0]
    LDR r0, =RES_LINHA_10
    VSTR d0, [r0]

    @ Linha 11
    LDR r0, =C_13
    VLDR d0, [r0]
    LDR r0, =C_2
    VLDR d1, [r0]
    VADD.F64 d0, d0, d1
    LDR r0, =C_5
    VLDR d2, [r0]
    VSUB.F64 d0, d0, d2
    LDR r0, =RES_LINHA_11
    VSTR d0, [r0]

    @ Linha 12
    LDR r0, =C_14
    VLDR d0, [r0]
    LDR r0, =C_2
    VLDR d1, [r0]
    VMUL.F64 d0, d0, d1
    LDR r0, =RES_LINHA_12
    VSTR d0, [r0]

    @ Linha 13
    LDR r0, =C_15
    VLDR d0, [r0]
    LDR r0, =C_6
    VLDR d1, [r0]
    VDIV.F64 d0, d0, d1
    LDR r0, =RES_LINHA_13
    VSTR d0, [r0]

    @ Linha 14
    LDR r0, =RES_LINHA_13
    VLDR d0, [r0]
    LDR r0, =RES_LINHA_14
    VSTR d0, [r0]

    @ Linha 15
    LDR r0, =VAR
    VLDR d1, [r0]
    LDR r0, =C_16
    VLDR d2, [r0]
    VADD.F64 d1, d1, d2
    @ Resultado final em registrador diferente de d0
    LDR r0, =RES_LINHA_15
    VSTR d1, [r0]
    VLDR d0, [r0]

    @ Linha 16
    LDR r0, =C_5
    VLDR d0, [r0]
    LDR r0, =C_2
    VLDR d1, [r0]
    @ Resultado final em registrador diferente de d0
    LDR r0, =RES_LINHA_16
    VSTR d1, [r0]
    VLDR d0, [r0]

    LDR r0, =C_3
    VLDR d7, [r0]
    VCMP.F64 d0, d7
    VMRS APSR_nzcv, FPSCR
    BEQ L_7
    @ Linha 17
    LDR r0, =C_13
    VLDR d0, [r0]
    LDR r0, =FLAG
    VSTR d0, [r0]
    LDR r0, =RES_LINHA_17
    VSTR d0, [r0]

L_7:
L_8:
    @ Linha 18
    LDR r0, =FLAG
    VLDR d1, [r0]
    LDR r0, =C_3
    VLDR d2, [r0]
    @ Resultado final em registrador diferente de d0
    LDR r0, =RES_LINHA_18
    VSTR d2, [r0]
    VLDR d0, [r0]

    LDR r0, =C_3
    VLDR d7, [r0]
    VCMP.F64 d0, d7
    VMRS APSR_nzcv, FPSCR
    BEQ L_9
    @ Linha 19
    LDR r0, =SET
    VLDR d1, [r0]
    LDR r0, =FLAG
    VLDR d3, [r0]
    LDR r0, =C_13
    VLDR d4, [r0]
    VSUB.F64 d3, d3, d4
    LDR r0, =FLAG
    VLDR d6, [r0]
    @ Resultado final em registrador diferente de d0
    LDR r0, =RES_LINHA_19
    VSTR d6, [r0]
    VLDR d0, [r0]

    B L_8
L_9:
fim:
    B fim

.align 3
C_1: .double 3.14
C_2: .double 2.0
C_3: .double 0.0
C_4: .double 10.5
C_5: .double 3.0
C_6: .double 4.0
C_7: .double 5.0
C_8: .double 15.0
C_9: .double 20.0
C_10: .double 6.0
C_11: .double 8.0
C_12: .double 100.5
C_13: .double 1.0
C_14: .double -5.0
C_15: .double 12.0
C_16: .double 5.5

.data
.align 3
RES_LINHA_1: .double 0.0
RES_LINHA_2: .double 0.0
RES_LINHA_3: .double 0.0
RES_LINHA_4: .double 0.0
RES_LINHA_5: .double 0.0
RES_LINHA_6: .double 0.0
RES_LINHA_7: .double 0.0
RES_LINHA_8: .double 0.0
RES_LINHA_9: .double 0.0
RES_LINHA_10: .double 0.0
RES_LINHA_11: .double 0.0
RES_LINHA_12: .double 0.0
RES_LINHA_13: .double 0.0
RES_LINHA_14: .double 0.0
RES_LINHA_15: .double 0.0
RES_LINHA_16: .double 0.0
RES_LINHA_17: .double 0.0
RES_LINHA_18: .double 0.0
RES_LINHA_19: .double 0.0
CONTADOR: .double 0.0
VAR: .double 0.0
FLAG: .double 0.0
SET: .double 0.0