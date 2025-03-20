import random

def verifica_sir(sir):
    if len(sir) % 7 != 0 or any(c not in '01' for c in sir):
        raise ValueError("Sirul trebuie sa fie format dintr-un numar multiplu de 7 de caractere binare.")

def construieste_matrice(sir):
    linii = len(sir) // 7
    matrice = [list(map(int, sir[i*7:(i+1)*7])) for i in range(linii)]
    return matrice

def calculeaza_paritate(matrice):
    linii = len(matrice)
    coloane = 7
    
    for linie in matrice:
        linie.append(sum(linie) % 2)
    
    paritate_coloane = [(sum(matrice[i][j] for i in range(linii)) % 2) for j in range(coloane)]
    
    paritate_coloane.append(sum(paritate_coloane) % 2)
    matrice.append(paritate_coloane)

def afiseaza_matrice(matrice):
    for linie in matrice:
        print(" ".join(map(str, linie)))

def transmite_mesaj(matrice):
    return "".join("".join(map(str, linie)) for linie in matrice)

def corupe_mesaj(mesaj):
    pozitie = random.randint(0, len(mesaj) - 1)
    mesaj_corupt = list(mesaj)
    mesaj_corupt[pozitie] = '1' if mesaj[pozitie] == '0' else '0'
    return "".join(mesaj_corupt), pozitie

def detecteaza_eroare(matrice_originala, matrice_recalculata):
    for i in range(len(matrice_originala)):
        for j in range(len(matrice_originala[0])):
            if matrice_originala[i][j] != matrice_recalculata[i][j]:
                return i, j
    return None

if __name__ == "__main__":
    sir = input("Introduceti un sir de biti multiplu de 7: ")
    verifica_sir(sir)
    
    matrice = construieste_matrice(sir)
    calculeaza_paritate(matrice)
    print("Matricea cu paritate calculata:")
    afiseaza_matrice(matrice)
    
    mesaj_transmis = transmite_mesaj(matrice)
    print("Mesaj transmis:", mesaj_transmis)
    
    mesaj_corupt, pozitie_corupta = corupe_mesaj(mesaj_transmis)
    print("Mesaj corupt:", mesaj_corupt)
    
    matrice_corupta = construieste_matrice(mesaj_corupt[:-8])
    calculeaza_paritate(matrice_corupta)
    eroare = detecteaza_eroare(matrice, matrice_corupta)

    print("Matricea corupta:", afiseaza_matrice(matrice_corupta))
    
    if eroare:
        print(f"Eroare detectata la pozitia: {eroare}")
    else:
        print("Nu s-a detectat nicio eroare.")
