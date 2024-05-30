"""
Modul sadrzi implementaciju merge sort algoritma
"""

def merge(L, R):
    """
    Funkcija spaja dve sortirane liste u jednu rezultujucu

    Argumenti:
    - `L`: `leva` lista
    - `R`: `desna` lista
    """
    # broj elemenata u listama
    n = len(L)
    m = len(R)

    # indeksi listi L i R, respektivno
    i = 0
    j = 0

    # izlazna lista
    sorted = []

    # dokle god u obe liste ima neispitanih elemenata, proveravaj tekuce
    while i < n and j < m:
        if L[i] < R[j]:
            # element `leve` liste je manji, dodaj u sortiranu i pomeri indeks
            sorted.append(L[i])
            i += 1
        else:
            # element `desne` liste je manji, dodaj u sortiranu i pomeri indeks
            sorted.append(R[j])
            j += 1

    # u jednoj od listi je ostalo elemenata, proveri koja je lista i kopiraj
    # preostale elemente u rezultujucu listu
    if i < n:
        sorted.extend(L[i:])
    else:
        sorted.extend(R[j:])

    return sorted


def sort(A):
    # bazni slucaj (lista od jednog elementa)
    n = len(A)
    if n == 1:
        return A

    # prepolovi listu i sortiraj polovine
    mid = n//2
    L = sort(A[:mid])
    R = sort(A[mid:])

    # spoji liste i vrati rezultat spajanja
    return merge(L, R)