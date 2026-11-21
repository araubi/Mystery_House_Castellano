#!/usr/bin/env python3
"""Saca los listados de los dos programas BASIC de una cinta de Mystery House (original o traducida).
Uso: python3 tools/lista.py orig.cas   -> out/MYS.txt y out/MYS22.txt"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import msxbasic as M, cas as C
bl = C.bloques(open(sys.argv[1], 'rb').read())
os.makedirs('out', exist_ok=True)
for k, n in ((1, 'MYS'), (3, 'MYS22')):
    with open(os.path.join('out', n + '.txt'), 'w', encoding='utf-8') as f:
        for ln, p, raw, t, nx in M.listar(bl[k]): f.write('%d %s\n' % (ln, t))
    print('out/%s.txt' % n)
