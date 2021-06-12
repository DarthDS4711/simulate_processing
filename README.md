# Simulación Paginacion Simple

Este proyecto consiste en la simulación del algoritmo Round Robin con paginación simple

## Description

Este proyecto tiene como propósito simular el algortimo de 
planificación Round Robin, en cual esta basado en el diagrama de 
cinco estados, como lo son listo, nuevo, bloqueado y
terminado por citar algunos. Además de incluir la paginación simple como 
una técnica de memoria, en la que limitaremos la memoria que tenga el programa
en ejecución.

## Getting Started

### Dependencies

* Windows 7 en adelante
* Python 3.7.1
* Colorama

### Installing

* El programa puede ser descargado desde la rama release del repositorio
* Además se tiene que instalar la libreria colorama de python

### Executing program

* Se abre el archivo main.py
* Se indica el número de procesos a ejecutar
* Presionando I bloqueamos por 5 seg el proceso
* Presionando P o A se pausa el programa
* Presionado N se agrega un nuevo proceso
* Presionando B se obtiene la tabla bcp de los procesos
* Presionando C se continua después de presionar P y B 
```
## Help

Any advise for common problems or issues.
No ingresar letras en lugar de números
```

## Authors

Contributors names and contact info

* Daniel Santiago Alatorre 

## Version History
* 2.4.0 t2(alpha 2)
    * Mejoras visuales de la tabla de paginación
    * Segunda alpha de la paginación simple
    * Inclusión de estados en los procesos
    * Funciones de agregar, eliminar de la tabla de paginación añadidas
* 2.4.0 t1(alpha 1)
    * Inclusión visual de la tabla de paginación
    * Primera alpha de la paginación simple
    * Inclusión de la tecla a, A para pausar el programa
    * Reubicación de elementos visuales
* 2.3.0 G (release)
    * Corrección errores visualización tabla bcp
    * Version de lanzamiento Algoritmo Round Robin
* 2.3.0 S (semi release)
    * Corrección errores visualización tabla bcp
    * Pre-candidata a lanzamiento
* 2.3.0 T1 (Beta 1)
    * Cambio del algoritmo de planificación de FCFS a Round Robin
    * Corrección de errores con los contadores del programa
    * Corrección de errores por procesos ya finalizados que entran a ser ejecutados
    * Primera beta del algoritmo Round Robin
* 2.2.1 S (Semi release)
    * Corrección errores de la tabla bcp generada con la tecla b
* 2.2.1 test
    * Inclusión de los 5 estados
    * Implementación de la entrada/salida por teclado
    * Mayor visualización del contenido por colorama
    * Corrección de errores presentados en la beta
* 2.2.0 beta
    * Initial Beta

## License

This project is licensed under the [GNU] License - see the LICENSE.md file for details
