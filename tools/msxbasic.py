# Detokenizador MSX-BASIC con juego de caracteres japonés (Mystery House, 2026-11-04)
T1="END FOR NEXT DATA INPUT DIM READ LET GOTO RUN IF RESTORE GOSUB RETURN REM STOP PRINT CLEAR LIST NEW ON WAIT DEF POKE CONT CSAVE CLOAD OUT LPRINT LLIST CLS WIDTH ELSE TRON TROFF SWAP ERASE ERROR RESUME DELETE AUTO RENUM DEFSTR DEFINT DEFSNG DEFDBL LINE OPEN FIELD GET PUT CLOSE LOAD MERGE FILES LSET RSET SAVE LFILES CIRCLE COLOR DRAW PAINT BEEP PLAY PSET PRESET SOUND SCREEN VPOKE SPRITE VDP BASE CALL TIME KEY MAX MOTOR BLOAD BSAVE DSKO$ SET NAME KILL IPL COPY CMD LOCATE TO THEN TAB( STEP USR FN SPC( NOT ERL ERR STRING$ USING INSTR ' VARPTR CSRLIN ATTR$ DSKI$ OFF INKEY$ POINT > = < + - * / ^ AND OR XOR EQV IMP MOD \\".split()
T2="LEFT$ RIGHT$ MID$ SGN INT ABS SQR RND SIN LOG EXP COS TAN ATN FRE INP POS LEN STR$ VAL ASC CHR$ PEEK VPEEK SPACE$ OCT$ HEX$ LPOS BIN$ CINT CSNG CDBL FIX STICK STRIG PDL PAD DSKF FPOS CVI CVS CVD EOF LOC LOF MKI$ MKS$ MKD$".split()
TOK1={0x81+i:t for i,t in enumerate(T1)}
TOK2={0x81+i:t for i,t in enumerate(T2)}
KATA="。「」、・ヲァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜"
HIRA1="をぁぃぅぇぉゃゅょっ"
HIRA2="あいうえおかきくけこさしすせそ"
HIRA3="たちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわん"
G1="月火水木金土日年円時分秒百千万π┴┬┤├┼│─┌┐└┘╳大中小"
def ch(b):
    if 0x20<=b<0x7f: return chr(b)
    if 0xA1<=b<=0xDF: return KATA[b-0xA1]
    if 0x86<=b<=0x8F: return HIRA1[b-0x86]
    if 0x91<=b<=0x9F: return HIRA2[b-0x91]
    if 0xE0<=b<=0xFD: return HIRA3[b-0xE0]
    return '{%02X}'%b
def chstr(bs):
    s='';i=0
    while i<len(bs):
        b=bs[i]
        if b==1 and i+1<len(bs):
            c=bs[i+1]-0x40
            s+= G1[c-1] if 1<=c<=len(G1) else '{01%02X}'%bs[i+1]; i+=2; continue
        s+=ch(b); i+=1
    return s
import struct
def single(b):
    # BCD MSX
    e=b[0]; 
    if e==0: return '0'
    sign='-' if e&0x80 else ''
    e=(e&0x7f)-0x40
    dig=''.join('%02X'%x for x in b[1:]).rstrip('0') or '0'
    if 0<=e<=len(dig)+6 and e>=len(dig): return sign+dig+'0'*(e-len(dig))
    if 0<e<len(dig): return sign+dig[:e]+'.'+dig[e:]
    if e<=0 and e>-6: return sign+'.'+'0'*(-e)+dig
    return sign+'.'+dig+'E'+str(e)
def detok_line(b):
    s='';i=0;mode=None
    while i<len(b):
        c=b[i]
        if mode=='str':
            if c==0x22: mode=None; s+='"'; i+=1; continue
            if c==1: s+=chstr(b[i:i+2]); i+=2; continue
            s+=ch(c); i+=1; continue
        if mode=='rem':
            if c==1: s+=chstr(b[i:i+2]); i+=2; continue
            s+=ch(c); i+=1; continue
        if mode=='data':
            if c==0x22: s+='"'; i+=1; mode='datastr'; continue
            if c==0x3a: mode=None; s+=':'; i+=1; continue
            if c==1: s+=chstr(b[i:i+2]); i+=2; continue
            s+=ch(c); i+=1; continue
        if mode=='datastr':
            if c==0x22: mode='data'
            if c==1: s+=chstr(b[i:i+2]); i+=2; continue
            s+=ch(c); i+=1; continue
        if c==0x22: mode='str'; s+='"'; i+=1; continue
        if c==0x3a and b[i+1:i+2]==b'\xa1': s+='ELSE'; i+=2; continue
        if c==0x3a and b[i+1:i+3]==b'\x8f\xe6': s+="'"; mode='rem'; i+=3; continue
        if 0x11<=c<=0x1a: s+=str(c-0x11); i+=1; continue
        if c==0x0f: s+=str(b[i+1]); i+=2; continue
        if c==0x1c: s+=str(struct.unpack('<h',b[i+1:i+3])[0]); i+=3; continue
        if c in (0x0e,0x0d): s+=str(struct.unpack('<H',b[i+1:i+3])[0]); i+=3; continue
        if c==0x0c: s+='&H%X'%struct.unpack('<H',b[i+1:i+3])[0]; i+=3; continue
        if c==0x0b: s+='&O%o'%struct.unpack('<H',b[i+1:i+3])[0]; i+=3; continue
        if c==0x1d: s+=single(b[i+1:i+5])+'!'; i+=5; continue
        if c==0x1f: s+=single(b[i+1:i+9])+'#'; i+=9; continue
        if c==0xff: s+=TOK2.get(b[i+1],'{FF%02X}'%b[i+1]); i+=2; continue
        if c>=0x81 and c in TOK1:
            t=TOK1[c]; s+=t; i+=1
            if t=='REM': mode='rem'
            if t=='DATA': mode='data'
            continue
        s+=ch(c) if c>=0x20 else '{%02X}'%c; i+=1
    return s
def fin_linea(prog,i):
    """Devuelve el índice del 00 que cierra la línea que empieza en i (tras los 4 bytes de cabecera)."""
    q=False; rem=False
    while True:
        c=prog[i]
        if c==0: return i
        if q:
            if c==0x22: q=False
            i+=1; continue
        if rem: i+=1; continue
        if c==0x22: q=True; i+=1; continue
        if c==0x8f: rem=True; i+=1; continue
        if c in (0x0b,0x0c,0x0d,0x0e,0x1c): i+=3; continue
        if c==0x0f: i+=2; continue
        if c==0x1d: i+=5; continue
        if c==0x1f: i+=9; continue
        if c==0xff: i+=2; continue
        i+=1
def listar(prog, base=0x8001):
    """Lista por terminadores (los enlaces de la cinta pueden estar viejos: CLOAD los recalcula)."""
    out=[];p=0
    while p+4<=len(prog):
        nxt,ln=struct.unpack('<HH',prog[p:p+4])
        if nxt==0: break
        e=fin_linea(prog,p+4)
        out.append((ln,p,prog[p+4:e],detok_line(prog[p+4:e]),nxt))
        p=e+1
    return out
