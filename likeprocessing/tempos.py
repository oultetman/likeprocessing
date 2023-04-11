import likeprocessing.processing as processing


class Tempo:

    def __init__(self, duree_ms: int, work=True):
        """t=Tempo(500) créer un objet de temporisation t de durée 500 ms qui se relance indéfiniment"""
        self.depart = processing.frameCount()
        self.duree_ms = duree_ms
        self.work = work
        if self.work:
            self.on = True
        else:
            self.on = False

    def flip(self):
        self.on = not self.on

    def set_tempo(self, duree_ms: int):
        """permet de réinitialiser la temporisation avec une nouvelle valeur."""
        self.depart = processing.frameCount()
        self.duree_ms = duree_ms

    def reset(self):
        """force le redémarrage de la temporisation."""
        self.on = self.work
        self.depart = processing.frameCount()

    def fin(self) -> bool:
        """renvoie True lorsque la temporisation est terminée. Pour notre exemple au bout de 500 ms."""
        if ((processing.frameCount() - self.depart) / processing.getFrameRate()) * 1000 >= self.duree_ms:
            self.depart = processing.frameCount()
            self.flip()
            return True
        else:
            return False

    def is_on(self):
        """renvoie True si la temporisation est à on."""
        self.fin()
        return self.on

    def is_off(self):
        """renvoie True si la temporisation est à off."""
        return not self.is_on()


class Monostable(Tempo):
    def __init__(self, duree_ms: int, work=True):
        """t=Monostable(500) créer un objet de temporisation t de durée 500 ms qui ne relance pas indéfiniment"""
        super().__init__(duree_ms, work)
        self.__stop = True
        self.trigger_value = False

    def fin(self):
        """renvoie True lorsque la temporisation est terminée. Pour notre exemple au bout de 500 ms."""
        if not self.__stop and (
                (processing.frameCount() - self.depart) / processing.getFrameRate()) * 1000 >= self.duree_ms:
            self.flip()
            self.__stop = True
            return True
        else:
            return False

    def reset(self):
        """force le redémarrage de la temporisation."""
        super().reset()
        self.__stop = False

    def trigger(self,value:bool):
        if self.trigger_value is False:
            if value is True:
                self.reset()
        self.trigger_value = value

class Pwm(Tempo):
    def __init__(self, period_ms: int,duty_cycle:int=50,**kwargs):
        """crée générateur de signaux carré de période periode_ms et de rapport cyclique duty_cycle"""
        work = kwargs.get("work",True)
        nb_cycle = kwargs.get("nb_cycle")
        super().__init__(period_ms, work)
        self.duty_cycle = min(max(duty_cycle,0),100)
        self.nb_cycle = nb_cycle
        self.compteur_cycle = 0

    def reset(self):
        """force le redémarrage de la temporisation."""
        super().reset()
        self.compteur_cycle = 0

    def fin(self) -> bool:
        """renvoie True lorsque la temporisation est terminée. Pour notre exemple au bout de 500 ms."""
        if ((processing.frameCount() - self.depart) / processing.getFrameRate()) * 1000 >= self.duree_ms:
            if self.nb_cycle is None or self.compteur_cycle<self.nb_cycle-1:
                super().reset()
                if self.nb_cycle is not None:
                    self.compteur_cycle+=1
            return True
        else:
            if ((processing.frameCount() - self.depart) / processing.getFrameRate()) * 1000 >= self.duree_ms*self.duty_cycle/100:
                if self.work == self.on:
                    self.flip()
            return False

    def fin_cycle(self)->bool:
        """retourne si le cycle nombre de cycle est atteint"""
        if self.nb_cycle is None:
            return False
        return self.compteur_cycle>=self.nb_cycle-1
