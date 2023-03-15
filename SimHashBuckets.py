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
    return sh


def hamming(hash1, hash2):
    hash1 = int(hash1, 2)
    hash2 = int(hash2, 2)
    return bin(hash1 ^ hash2).count('1')


def hash2int(simhash, broj_pojasa):
    return int(simhash[broj_pojasa*16:(broj_pojasa+1)*16], 2)


def napravi_kandidate(n, simhashevi):
    #dict setova, key je indeks od elementa za koje imamo kandidate
    #u setu su indeksi elemena koji su kandidati za slicnost s njime
    kandidati = {}
    for i in range(n):
        kandidati[i] = set()
    
    #for petlja ide po 8 bandova koje pravimo za svaki hash
    for i in range(8):
        #dict setova, keyevi su intovi napravljeni od bandova
        #value su setovi u kojima su indeksi svih elmenata kojima je na toj poziciji taj band isti
        pojasi = {}
        for j in range(n):
            trenutni_simhash = simhashevi[j]
            trenutni_pojas = hash2int(trenutni_simhash, i)
            #sad imamo pojas od trenutnog simhasha za i-ti band
            #trebamo napuniti set u {pojas} na toj poziciji
            tekstovi_s_istim_pojasom = set()
            if trenutni_pojas in pojasi:
                tekstovi_s_istim_pojasom = pojasi[trenutni_pojas]
                for indeks_elementa in tekstovi_s_istim_pojasom:
                    #dodajemo ovaj indeks_elementa u kandidate od trenutni_simhash(odnosno j)
                    kandidati[j].add(indeks_elementa)
                    #dodajemo j u kandidate od indeks_elementa
                    kandidati[indeks_elementa].add(j)
            #ako je else, to znaci da za taj hashirani pojas nema jos niti jedan kandidat
            else:
                tekstovi_s_istim_pojasom = set()
            tekstovi_s_istim_pojasom.add(j)
            pojasi[trenutni_pojas] = tekstovi_s_istim_pojasom
    
    return kandidati


def main():
    n = int(sys.stdin.readline())
    simhashevi = {}
    for i in range(n):
        tekst = sys.stdin.readline()
        simhashevi[i] = simhash(tekst)
    
    q = int(sys.stdin.readline())
    kandidati = napravi_kandidate(n, simhashevi)
    for i in range(q):
        tekst = sys.stdin.readline().split()
        I, K = int(tekst[0]), int(tekst[1])
        slicni = set()

        for kandidat_indeks in kandidati[I]:
            if kandidat_indeks != I and hamming(simhashevi[kandidat_indeks], simhashevi[I]) <= K:
                slicni.add(kandidat_indeks)
        
        print(len(slicni))


if __name__=='__main__':
    main()