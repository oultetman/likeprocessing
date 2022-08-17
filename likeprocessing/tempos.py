import likeprocessing as processing


class Tempo:

    def __init__(self, duree_ms: int):
        self.depart = processing.frameCount
        self.duree_ms = duree_ms

    def set_tempo(self, duree_ms: int):
        self.depart = processing.frameCount
        self.duree_ms = duree_ms

    def fin(self) -> bool:
        if ((processing.frameCount - self.depart) / processing.getFrameRate()) * 1000 >= self.duree_ms:
            self.depart = processing.frameCount
            return True
        else:
            return False
