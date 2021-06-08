# Compiladores
Repositorio perteneciente a la materia de "Compiladores" del periodo 21-2 que busca crear un **compilador** desde 0.

## V1 (Abril 2021)
Actualmente el proyecto puede realizar la creación de **AFNs** *(Autómatas Finitos No deterministas)* y **AFDs** *(Autómatas Finitos Deterministas)* con los que se pueden validar cadenas como pequeño preludio del desarrollo de un Evaluador de expresiones

## Todo
- [x] Integración de analizador léxico al programa principal
- [x] Revisión de errores en analizador léxico
- [ ] Construcción de analizador sintáctico
  - [x] Calculadora
    - [x] Notación Post-Fija
    - [x] Evaluador de expresiones
  - [x] [Construir AFN asociado a *Expresiones Regulares*](https://drive.google.com/file/d/1nMw-Tmyvoyn0qH-aouC0-bm3Lay4z5UF/view)
    - [x] Implementación con símbolos especiales (\\*, \\+, \\?, ...)
- [ ] [Análisis LL](https://drive.google.com/file/d/1mlB4ACLrKcQ8D-cdlvT9GMHLGt77AhMO/view)
  - [ ] [Gramática de gramáticas](https://drive.google.com/file/d/10th--Ndkvnp8YphKhJxvB40Uur5TkTQe/view)
  - [ ] Analizadores léxico y sintáctico para gramáticas de gramáticas
  - [ ] [Operación Firt & Follow](https://drive.google.com/file/d/1CqzPvBLwa9CJU2FDxNhKhc8uVCE3qcv8/view)
  - [ ] Construcción de la tabla LL(1)
  - [ ] Analizador léxico para la gramática de entrada
  - [ ] Algoritmo de analisis sintáctico LL(1)
  - [ ] Tabla LL(1)
  - [ ] Salida: True ó False
  - (Los analizadores léxicos deberán ser guardados en el directorio *afds/*)