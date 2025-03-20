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
