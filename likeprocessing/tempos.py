import likeprocessing.processing as processing


class Tempo:

    def __init__(self, duree_ms: int):
        self.depart = processing.frameCount()
        self.duree_ms = duree_ms
        self.__on = False

    def set_tempo(self, duree_ms: int):
        self.depart = processing.frameCount()
        self.duree_ms = duree_ms

    def fin(self) -> bool:
        if ((processing.frameCount() - self.depart) / processing.getFrameRate()) * 1000 >= self.duree_ms:
            self.depart = processing.frameCount()
            self.__on = not self.__on
            return True
        else:
            return False

    def is_on(self):
        self.fin()
        return self.__on
