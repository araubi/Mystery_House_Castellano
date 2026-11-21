# Lectura y escritura de CAS (Mystery House)
H=bytes.fromhex('1FA6DEBACC137D74')
def bloques(d):
    pos=[];i=0
    while (j:=d.find(H,i))>=0: pos.append(j);i=j+8
    return [d[p+8:(pos[k+1] if k+1<len(pos) else len(d))] for k,p in enumerate(pos)]
def alinea(b):
    # los bloques del CAS empiezan en múltiplo de 8
    return b+b'\0'*((-len(b))%8)
def monta(bl):
    out=bytearray()
    for b in bl:
        out+=b'\0'*((-len(out))%8)
        out+=H+b
    return bytes(out)
