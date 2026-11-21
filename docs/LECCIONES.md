# Lecciones de la traducción de Mystery House

Lo aprendido, útil para traducir otros juegos de MSX en BASIC.

## Programas BASIC en cinta

* Para tocar un programa BASIC tokenizado conviene un detokenizador y un tokenizador propios que hagan la **ida y vuelta byte a byte** con el original antes de cambiar nada. Aquí `tools/msxbasic.py` y `tools/tokeniza.py` reproducen los dos programas exactos.
* No hay que fiarse de los punteros de enlace de las líneas: en este juego 22 están viejos (el programa se editó y se grabó sin recalcularlos; el BASIC los rehace al cargar). Para listar, recorrer hasta el 00h que cierra cada línea.
* La traducción se guarda como **líneas completas que sustituyen a las originales** (`trad/`), y `build.py` monta la cinta a partir de la original. Así el repositorio no lleva el programa entero.
* El tokenizador tiene que conocer el juego de caracteres japonés (kana y gráficos) para que los textos que no se traducen salgan iguales.

## Tildes que se vean en cualquier MSX

* Un código de 80h en adelante sale como kana en un MSX japonés y como letra con tilde en uno europeo. La solución en BASIC: copiar la fuente de la BIOS a la RAM, añadir los dibujos propios y apuntar CGPNT a la copia (con su slot). A partir de ahí todo lo que escribe PRINT usa nuestra fuente.
* Hay que bajar HIMEM (CLEAR ,&HE900) antes de cargar el programa grande y comprobar que el BASIC y sus variables no llegan a la fuente.

## BLOAD a la VRAM

* En MSX1, `BLOAD ...,R` con direcciones de VRAM carga en RAM o en ROM y salta ahí: el programa se cuelga o termina. Los datos se cargan en RAM y se pasan a la VRAM con LDIRVM (005Ch) desde una pequeña rutina llamada con USR.
* Un byte de control en RAM evita volver a pedir la cinta cada vez que se vuelve a empezar.

## Pruebas

* Jugar la partida entera en openMSX con guiones Tcl que solo pulsan teclas (`type` y `keymatrixdown`), con captura y volcado de variables tras cada orden, en una máquina japonesa y en una europea.
* En Tcl, el `$` dentro de `type "..."` hay que escaparlo (`\$`), y un `loadstate` dentro de un guion necesita `after realtime` antes de seguir con `after time`.
