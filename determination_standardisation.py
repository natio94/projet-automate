from main import *
def est_standardisation(fichier):
    i = 0
    with open(fichier, 'r'):
        for line in fichier:
            if(i == 2 and line[0] != '1'):
                return 0

            u = int(line[2])

            if(i >= 5):
                if(line[2] == u):
                    return 0

            i += 1
    return 1

def est_deterministe(auto:Automate):
    if auto.nbEtatsInitiaux!=1:
        return 0
    etatSymb=[]
    for transi in auto.transitions:
        etatSymb.append(str(transi.depart)+str(transi.symbole))
    return len(etatSymb)==len(set(etatSymb))


def determinisation(auto:Automate):
    if est_deterministe(auto):
        print("L'automate est déjà déterministe")
        return auto
    if auto.nbEtatsInitiaux>1:
        etatsInit=auto.etatsInitiaux




t=Automate("automates/5")
print(est_deterministe(t))
t.affichage()
determinisation(t)
for etat in t.etats:
    print(etat)
n=t.etats[1]+t.etats[3]
print("eeee",*t.etats[3].transiSortante)
print('experience',n,'s',*n.transiSortante,"e",*n.transiEntrante)

