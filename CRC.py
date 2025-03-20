def verifica_sir_binar(sir):
    if any(c not in '01' for c in sir):
        raise ValueError("Sirul introdus nu este binar")

def grad_polinom_generator(polinom):
    polinom = polinom.lstrip('0')
    return len(polinom) - 1 if polinom else -1

def extinde_mesaj(mesaj, grad):
    #while grad:
    #    mesaj*=10
    #    grad-=1
    #return mesaj
    mesaj_extins = mesaj + '0' * (grad)
    return mesaj_extins

def impartire_mesaj(mesaj, polinom):
    msg = list(mesaj)
    poly_len = len(polinom)
    
    print("Rezultate intermediare XoR: ")
    while len(msg) >= poly_len:
        for i in range(poly_len):
            msg[i] = str(int(msg[i]) ^ int(polinom[i]))
        
        while msg and msg[0] == '0':
            msg.pop(0)
        print(''.join(msg))
    
    return ''.join(msg) if msg else '0'



if __name__ == "__main__":
    mesaj = input("Introduceti mesajul transmis: ")
    verifica_sir_binar(mesaj)
    polinom_generator = input("Introduceti polinomul generator: ")
    verifica_sir_binar(polinom_generator)

    grad_polinom = grad_polinom_generator(polinom_generator)
    
    if(grad_polinom == -1):
        print("Polinomul generator este 0, nu-i bine")
        SystemExit
    if len(mesaj) < len(polinom_generator):
        print("Polinomul generator este mai mare decat mesajul, nu-i bine")
        SystemExit
    
    print("Gradul polinomului este:", grad_polinom)

    mesaj = extinde_mesaj(mesaj, grad_polinom)

    print("Mesajul extins este: ", mesaj)

    rest_mesaj = impartire_mesaj(mesaj, polinom_generator)

    print("Mesaj dupa impartire: ", rest_mesaj)

    mesaj_modificat = mesaj[0:-len(rest_mesaj)]+rest_mesaj

    print("Mesaj final:", mesaj_modificat)
