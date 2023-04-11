class Tor:
    """cette classe permet de créer des objets tout ou rien.
    Ces objets on deux états True ou False.
    On peut détecter le passage de False à True : front_montant et
    son contraire True à False : front_descendant
    Cette classe possède une variable instance qui enregistre les instances crées.
    Ce qui permet de reprendre le contrôle sur celle-ci"""
    instances = []

    def __init__(self):
        self._etat = False
        self._front_montant = False
        self._front_descendant = False
        Tor.instances.append(self)


    def __del__(self):
        """permet de détruire un objets Tor correctement"""
        Tor.instances.remove(self)

    def etat(self):
        return self._etat

    def front_montant(self)->bool:
        return self._front_montant

    def front_descendant(self)->bool:
        return self._front_descendant

    def on(self):
        if not self._etat:
            self._front_montant =True
            self._etat = True

    def off(self):
        if self._etat:
            self._front_descendant =True
            self._etat = False

    @classmethod
    def reset_front(cls):
        for instance in cls.instances:
            instance._front_montant = False
            instance._front_descendant = False
            if isinstance(instance,Tor_mono):
                instance.off()

    @classmethod
    def all_on(cls):
        for instance in cls.instances:
            instance.on()

    @classmethod
    def all_off(cls):
        for instance in cls.instances:
            instance.off()

class Tor_mono(Tor):
    def on(self):
        if not self._etat:
            self._front_montant = True
            self._etat = True
