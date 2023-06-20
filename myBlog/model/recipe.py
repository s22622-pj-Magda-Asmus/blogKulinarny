from marshmallow import Schema, fields


class Recipe(object):
    def __init__(self, int, nazwa, skladniki, przygotowanie, img):
        self.int = int
        self.nazwa = nazwa
        self.skladniki = skladniki
        self.przygotowanie = przygotowanie
        self.img = img

    def __repr__(self):
        return "<Recipe(nazwa={self.nazwa!r})".format(self=self)


class RecipeSchema(Schema):
    nazwa = fields.Str()
    skladniki = fields.Str()
    przygotowanie = fields.Str()
