def who_won(hive, territory, territories): # retourne true si victoire, false si défaite
    for terr in territories:
        if terr._name == territory:
            territory = terr
            break
    #print(territory._name)
    if territory._possession == False:
        
        bees = hive._bees
        tot_strength = 0
        for bee in bees:
            if bee._category == "fighter":
                #print(hive.calcul_upgrade_fight(bee)) 
                tot_strength = tot_strength + bee._strength * hive.calcul_upgrade_fight(bee)
        print(f"force {tot_strength} ")
        if tot_strength > territory._strength:
            hive._ressource[territory.ressource()] += territory.strength()
            hive._ressource["pollen"] += territory.strength()
            hive._level += 1
            return "good"
        else:
            return "notgood"
    else:
        
        return "mine"