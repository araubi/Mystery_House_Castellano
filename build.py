#!/usr/bin/env python3
"""Monta la cinta traducida de Mystery House a partir de la cinta ORIGINAL (no incluida).
Uso: python3 build.py [orig.cas] [MysteryHouse_ES.cas]
La cinta original debe ser la de SHA-1 820b1d8d118cb36ad3369b33d29d74327b7cf018."""
import sys, os, hashlib
A = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(A, 'tools'))
import msxbasic as M, tokeniza as T, cas as C
SHA = '820b1d8d118cb36ad3369b33d29d74327b7cf018'

def aplica(lst, fich):
    lineas = dict(lst)
    for l in open(fich, encoding='utf-8'):
        l = l.rstrip('\n')
        if not l.strip() or l.startswith('#'): continue
        n, _, t = l.partition(' ')
        if t.strip() == '': lineas.pop(int(n), None)   # línea vacía = borrar
        else: lineas[int(n)] = t
    return sorted(lineas.items())

def main(orig, sal):
    d = open(orig, 'rb').read()
    if hashlib.sha1(d).hexdigest() != SHA:
        sys.exit('La cinta no es la original esperada (SHA-1 %s)' % SHA)
    bl = C.bloques(d)
    for k, n in ((1, 'MYS'), (3, 'MYS22')):
        lst = [(ln, t) for ln, p, raw, t, nx in M.listar(bl[k])]
        nuevo = aplica(lst, os.path.join(A, 'trad', 'es_%s.txt' % n))
        bl[k] = T.tokeniza(nuevo) + b'\0' * 7
        print(n, len(bl[k]), 'bytes')
    open(sal, 'wb').write(C.monta(bl))
    print('Escrito', sal, hashlib.sha1(open(sal, 'rb').read()).hexdigest())

if __name__ == '__main__':
    a = sys.argv[1:] + ['orig.cas', 'MysteryHouse_ES.cas'][len(sys.argv[1:]):]
    main(os.path.join(A, a[0]) if not os.path.isabs(a[0]) else a[0], a[1])
