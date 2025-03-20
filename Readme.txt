Tema 1
========

- explicatii, chestii, tatamare

- Examen
	se considera un polinom de 20 de biti si polinomul generator dat. 
	Vedeti daca trece prin retea.
____________________________________________________________________
Paritate Bidimensionala
=======================

- coduri de detectare e erorilor transmise prin retea (nu le si corectez)

Paritate Unidimensionala
	- transmit un mesaj 
	+ validez ca mesajul este multiplu de 7 biti (14)
	
	ex: 	M = 10101101110101
	
	- dupa fiecare 7 biti adaug un bit de paritate 
		- arata daca am nr. par de 1 
		- adaug un bit de 1 sau 0 pentru ca cei 7 biti sa contina NUMAR PAR DE 1
		
		1010110 (0)  1110101 (1)
		// pus-am 0 pt ca aveam nr par de 1 (adica 4 de 1)
					 // pus-am 1 pt ca aveam nr impar de 1 (adica 5 de 1) si am mai pus un 1 ca sa fie nr. par de 1
					 
- nu prea bine pt ca la mai mult de o eroare se poate sa nu imi dau seama ca-i greseala

____________________________________________________________________
PARITATE Bidimensionala
========================

date intrare 
	ex: 	M = 1110110 1010010 0010101
	
	+ verific sa fie lungime multiplu de 7
	+ verific sa contina doar valori binare
	
	+ construim o matrice cu 7 coloane si oricate linii (in functie de lungime mesaj)
	
		1110110 | 1		// coloana biti de paritate 
		1010010 | 1
		0010101 | 1
		___________
		0110001	| 1	// colt de bit semnificativ 
		// linie biti de paritate 
		
		// afisam matricea cu bitii calculati 
		+ afisam o matrice de 8 coloane si oricate linii 
		
		+ afisam mesajul nou construit, care se transmite 
		+ se creaza citind matricea pe linii 
			1110110 | 1 1010010 | 1 0010101 | 1 0110001	| 1
			
		+ aleg cu random sa se corupa o pozitie (un bit din mesajul initial)
		- trebuie sa detectez unde se afla bitul corupt 
		+ compar bitul de paritate de pe linie si bitul de paritate de pe coloana 
			
			construim matricea si comparam bitul de paritate de pe coloana cu bitul de paritate din matricea initiala, efectiv compar bitii de paritate dintr-o noua matrice cu cei din matricea initiala (pe care sper ca o ai salvata)
				
		+ afisez pozitia bitului corupt 
		
____________________________________________________________________
CRC (Cyclic redundancy check)
			
	- se pare ca nu conteaza daca e sau nu multiplu de 7 acilea 
	- se lucreaza pe biti, 
	
	M(x) = 101110101110101011
	C(x) = X^3 + X + 1 	// polinom generator
	
	// pot ori sa fac polinom si sa impart 
	// ori sa fac pe biti 
	
	- retin grad polinom generator (gradu 3 acilea)
	
	1 * X ^ 3 + 0 * X ^ 2 + 1 * X + 1 = 1011
	
	+ scriu polinomul ca mai sus, il fac sub forma de biti 
	(sau direct ca biti dar elimin biti pana ajung la primul 1 pt a identifica gradul polinomului generator)
	
	+ facem XoR pe biti 
		- 0 pentru valori egale	(0,0) (1,1)
		- 1 pentru valori diferite (0,1) (1,0)
		
	+ construim T(x) - mesaj extins 
		- la mesajul initial adaug un numar de 0 in functie de gradul polinomului 
		+ adaug k de 0 la final, k fiind gradul polinom (000 in exemplul cu grad 3)
	
	T(x) = 101110101110101011 000
		   
		101110101110101011 000
		1011
		====
		0000
			10101110101011 000	// cobor ce mai am sus, pot sa tai toti de 0 pana am primul 1
			1011
			====
			000
			   11110101011 000
			   1011
			   ====
			   0
			    1000101011 000
				1011
				====
				00
				  11101011 000
				  1011
				  ====
				  0
				   1011011 000
				   1011
				   ====
				   0000
					   0
					    11 000
						10 11
						====
						0
						 1 110
						 1 011
						 =====
						 0 
						   101	// lungime rest e mai mica decat cea a polinom generator, ma opresc 
						   
	fac XoR de la dreapta (SAU PUR SI SIMPLU LE ADUN, FARA TRANSPORT)
	
	M'(x) = T(x) + M(x)
	
	M'(x) = 101110101110101011 000 + 
							   101
          = 101110101110101011 101
	
	+ afisam M'(x) 				

	(doar ca sa nu crapam lipsiti de inteligentza)
	
		facem M'(x) XoR C(x), daca e 000 e bun, altfel nu 
	
					   