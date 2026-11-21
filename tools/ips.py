#!/usr/bin/env python3
"""Crea un parche IPS (original -> traducida) y comprueba que al aplicarlo sale idéntica.
Uso: python3 tools/ips.py orig.cas MysteryHouse_ES.cas releases/MysteryHouse_ES_v1.0.ips"""
import sys
def crea(a, b):
    n0 = len(a); a = a + b'\x00' * max(0, len(b) - len(a))
    dif = lambda k: k >= n0 or a[k] != b[k]
    out = bytearray(b'PATCH'); i = 0
    while i < len(b):
        if not dif(i): i += 1; continue
        if i == 0x454F46: i -= 1        # el desplazamiento «EOF» no se puede usar
        j = i
        while j < len(b) and j - i < 0xffff and any(dif(k) for k in range(j, min(j + 6, len(b)))): j += 1
        out += i.to_bytes(3, 'big') + (j - i).to_bytes(2, 'big') + b[i:j]; i = j
    return bytes(out + b'EOF')
def aplica(a, p):
    r = bytearray(a); k = 5
    while p[k:k+3] != b'EOF':
        o = int.from_bytes(p[k:k+3], 'big'); n = int.from_bytes(p[k+3:k+5], 'big')
        if len(r) < o + n: r += b'\x00' * (o + n - len(r))
        r[o:o+n] = p[k+5:k+5+n]; k += 5 + n
    return bytes(r)
if __name__ == '__main__':
    a = open(sys.argv[1], 'rb').read(); b = open(sys.argv[2], 'rb').read()
    p = crea(a, b); assert aplica(a, p) == b, 'el parche no reproduce la traducida'
    open(sys.argv[3], 'wb').write(p); print('IPS', len(p), 'bytes, comprobado')
