from sympy import *

x, y, z, a, b = symbols('x y z a b')


class SousContrainte:
    def __init__ (self, equation, second_membre, variable_sortante):
        self.equation = equation
        self.second_membre = second_membre
        self.variable_sortante = variable_sortante

    def get_coef(self, coef):
        for operande in self.equation.args:
            if str(operande).__contains__(coef):
                return operande.args[0]

    def get_ratio(self):
        return self.second_membre / self.get_coef('x')


def init_sous_contraintes():
    sous_contrainte_1 = SousContrainte((2 * x + y + z), 18, z)
    sous_contrainte_2 = SousContrainte((2 * x + 3 * y + a), 42, a)
    sous_contrainte_3 = SousContrainte((3 * x + y + b), 24, b)

    return sous_contrainte_1, sous_contrainte_2, sous_contrainte_3

def min_ratio(sous_contraintes):
    min = 99999
    sous_contrainte_return = None
    for sous_contrainte in sous_contraintes:
        ratio = sous_contrainte.get_ratio()
        if ratio < min:
            min = ratio
            sous_contrainte_return = sous_contrainte

    return sous_contrainte_return


def operators_are_negatives(zed):
    for operator in zed.args:
        operator = str(operator)
        if not operator.startswith('-') and not operator.isdigit():
            return false
    return true


def move_integers(sous_contrainte):
    for operande in sous_contrainte.equation.args:
        if str(operande).isdigit():
            sous_contrainte.second_membre -= operande
            sous_contrainte.equation = Add(sous_contrainte.equation, - operande)


if __name__ == '__main__':
    sous_contraintes = init_sous_contraintes()
    zed = (3 * x + 2 * y)
    
    while not operators_are_negatives(zed):
        print(sous_contraintes[0].equation, sous_contraintes[1].equation, sous_contraintes[2].equation)
        sous_contrainte_echange = min_ratio(sous_contraintes)
        equation_echange = solve(Eq(sous_contrainte_echange.equation, sous_contrainte_echange.second_membre), x)[0]
        
        for sous_contrainte in sous_contraintes:
            sous_contrainte.equation = sous_contrainte.equation.subs(x, equation_echange)
            
        zed = simplify(zed.subs(x, equation_echange))