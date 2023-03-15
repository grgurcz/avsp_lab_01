import sys
from hashlib import md5


def generiraj_jedinke(tekst):
    return tekst.split()


def simhash(tekst):
    sh = [0] * 128

    jedinke = generiraj_jedinke(tekst)

    for jedinka in jedinke:
        sazetak = md5(jedinka.encode()).hexdigest()
        sazetak = bin(int(sazetak, 16))[2:].rjust(128, "0")
        
        for i in range(128):
            if sazetak[i] == '1':
                sh[i] += 1
            else:
                sh[i] -= 1
    
    for i in range(128):
        if sh[i] >= 0:
            sh[i] = '1'
        else:
            sh[i] = '0'
    
    sh = ''.join(sh)
    return int(sh, 2)


def hamming(hash1, hash2):
    return bin(hash1 ^ hash2).count('1')


def main():
    n = int(sys.stdin.readline())
    simhashevi = {}
    for i in range(n):
        tekst = sys.stdin.readline()
        simhashevi[i] = simhash(tekst)
    
    q = int(sys.stdin.readline())
    for i in range(q):
        tekst = sys.stdin.readline().split()
        I, K = int(tekst[0]), int(tekst[1])
        count = 0
        for i in range(n):
            if i != I:
                if hamming(simhashevi[i], simhashevi[I]) <= K:
                    count += 1
        print(count)


if __name__=='__main__':
    main()