# Gère le fonctionnement d'un joueur
# Joue les coups

class Player:
    def __init__(self, color, IA=False):
        self.IA = IA
        self.color = color

    def take_action(self):
        move = None
        stack = None

        
        return move, stack
    
    def evaluate_position(self, board: Board):
        # pour chacun de mes pions je récupère leur nombre de points max et je les ajoute à la valeur de la position 
        pass
            # pour calculer le nombre de points max : 
                # je récupère la position des piles par rapport à un pion -> dans dalles.
                    # avec dalle il faut que je calcule la distance entre un pion donné et toutes les autres piles. 
                # je les associes aux points
                # je prends le max

        # Je fais pareil pour les joueurs ennemis en les soustrayant à cette même valeur
