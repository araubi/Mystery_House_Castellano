# Mystery House (Micro Cabin / Arrow Soft, 1983): documentación técnica

Cinta original estudiada: `Mystery House (1983)(Micro Cabin)(Japanese MSX)(JP)(en-jp)[SHIFT][CLOAD].cas` (31.862 bytes, SHA-1 820b1d8d118cb36ad3369b33d29d74327b7cf018). No se incluye en este repositorio.

## Contenido de la cinta
| Fichero | Tipo | Tamaño | Qué es |
|---|---|---|---|
| MYS | BASIC (CLOAD) | 7.472 bytes, 226 líneas | Cargador: presentación (casa con LINE/PAINT, letras de sprites, música), instrucciones y `CLOAD` del principal |
| MYS22 | BASIC (CLOAD) | 23.424 bytes, 740 líneas | El juego |
| DATA | binario 1C00h-1DFFh | 512 bytes | Trazos del fantasma (grupos de 5 bytes: x1,y1,x2,y2,color) |
| MYSSP0 | binario 3E60h-3EAFh | 80 bytes | Patrones de sprite 51-52 (llamas del fantasma) |
| MYSSP1 | binario 3EA0h-3F5Fh | 192 bytes | Patrones de sprite 53-58 (diamante del final) |

Las direcciones de los binarios son de VRAM, pero se cargan con `BLOAD ...,R` en RAM/ROM: ver [CURIOSIDADES.md](CURIOSIDADES.md), puntos 1 y 2.

Herramientas propias (`tools/`): `msxbasic.py` (detokenizador con el juego de caracteres japonés), `tokeniza.py` (tokenizador), `cas.py` (lectura y montaje de la cinta). La ida y vuelta reproduce los dos programas **byte a byte**, incluidos los 22 enlaces viejos.

## Estructura del programa principal
| Líneas | Qué hace |
|---|---|
| 70-300 | Arranque, menú (partida nueva o grabada), reparto de objetos (3340) |
| 310-710 | Bucle principal: lee el verbo y el objeto con INKEY$, 3 letras |
| 720-1460 | Verbos: open 720, lig 1000, take 1020, search 1110, look 1250, unl 1270, move 1280, use 1340 |
| 1470-1540 | down / up |
| 1550-3030 | Movimiento: una línea por vista y tecla (← CHR$(29), → CHR$(28), ↑ CHR$(30), ↓ CHR$(31), BS CHR$(8) redibuja) |
| 3040-3310 | Ayuda (hel) |
| 3340-3490 | Reparto de objetos |
| 3500-3730 | Martillo, nota, cajas |
| 3890-5040 | Rutinas de dibujo (paredes, puertas, armarios, chimeneas, cuadros, escaleras, mesa…) |
| 5050-5960 | Vistas: combinaciones de rutinas |
| 5970-6290 | Hallazgos (vela, cerillas, llave, martillo, pico, nota, diamante) |
| 6300-6430 | Muertes |
| 6440-6530 | Final |
| 6540-7130 | Cuarto del fantasma |
| 7230-7420 | save y time |
| 7430-7940 | Final 2: sprites y anuncio de Diamond Adventure |
| 7950-7980 | Músicas |

El listado completo no se publica (es el código original); se obtiene de la cinta original con `python3 tools/lista.py orig.cas`.

## Variables
- **SC**: vista (1-41). Cada sala tiene 4 vistas.
- Objetos: valor = vista donde está; 100 = descubierto; 0 = en el inventario. **CA** vela, **MA** cerillas, **HA** martillo, **PI** pico, **K1** llave de las cajas de los cuadros, **K2** llave de las cajas de las chimeneas. **S1**/**S2**: vista de cada caja fuerte. **DA**: diamante (también la puerta de la calle).
- Puertas abiertas D1-D5, DB-DE, DDD; armarios RA-RH; TA mesa, HS escalera de mano, KK/WA pared, P1/P2 cuadros, F1/F2 chimeneas, ME nota, PC agujero.

## Mapa
Ver [mapa.png](mapa.png). Nombres de las salas puestos por nosotros:

| Sala | Vistas | Salidas (↑ salvo que se diga) |
|---|---|---|
| Calle | 1 | 1→2 (abrir puerta) |
| Vestíbulo PB | 2, 3, 4, 17 | 2→5, 3→13, 4 «up»→18, 17 calle (muerte) |
| Comedor | 5, 6, 7, 8 | 6→12, 8→17, 5 mover mesa + «down»→34 |
| Biblioteca | 9, 10, 11, 12 | 9→7, 11→15 |
| Salón | 13, 14, 15, 16 | 14→10, 16→4 |
| Vestíbulo 1.ª | 18, 19, 20, 21 | 18→28, 21→22, 20 «down»→3 |
| Estudio | 22, 23, 24, 25 | 25→19, 24→26 (tras romper la pared) |
| Balcón | 28, 29, 30 | 30→20; → en 28 y ← en 30: caída |
| Cuarto secreto | 26, 27, 41, (40) | 27→23, 41→2, 40 fantasma |
| Sótano | 34, 33, 31, 32 | 34/31 «up»→8, 33→32 (tras el agujero) |

## La traducción
- **Fuente propia en RAM.** El cargador (línea 12) baja HIMEM a E900h, copia la fuente de la BIOS a E800h con una rutina en código máquina (F110h) y apunta CGPNT (F91Fh) a la copia, con el slot calculado en BASIC. Así los dibujos nuevos se ven igual en un MSX japonés que en uno europeo.
- **Caracteres nuevos (80h-8Ah):** ♥ á é í ó ú ñ Ñ ¿ ¡ y el cuadro de «▣». Dibujados por nosotros (líneas 2600-2620 de `trad/es_MYS.txt`); el corazón sustituye al 81h de la fuente japonesa, que es el que usa el marco de la nota en el original. El tokenizador (`tools/tokeniza.py`) los traduce a esos códigos.
- **Arreglo del cuarto del fantasma y del final.** En vez de `BLOAD ...,R` a direcciones de VRAM, el programa carga los tres binarios una sola vez en RAM (EE00h trazos del fantasma, F000h y F050h sprites) y los pasa a la VRAM con dos rutinas LDIRVM llamadas con `USR1` (3E60h, 50h bytes) y `USR2` (3EA0h, C0h bytes). Un byte de control en F13Fh (77h) evita volver a cargarlos.
- **Órdenes en castellano** de tres letras; las inglesas siguen valiendo y da igual mayúsculas o minúsculas.
- **Orden `tiempo`** con horas, minutos y segundos correctos a 50 o 60 Hz.
- El resto del comportamiento del original se conserva tal cual (reparto fijo de objetos, `fin` borra el programa, la partida grabada no guarda las puertas).

Mapa de memoria de la versión traducida:

| Dirección | Uso |
|---|---|
| 8001h-DF0Fh | Programa BASIC (MYS22 traducido) |
| E800h-EC7Fh | Copia de la fuente (códigos 20h-8Fh en E900h-EC7Fh) |
| EC00h-EC57h | Dibujos propios 80h-8Ah |
| EE00h-EFFFh | Trazos del fantasma |
| F000h / F050h | Patrones de sprite del fantasma y del diamante |
| F110h | Copia de la fuente |
| F120h / F12Ch | USR1 / USR2 (LDIRVM) |
| F13Fh | Marca «binarios ya cargados» |
