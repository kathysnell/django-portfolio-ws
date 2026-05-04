from django.db import models
from colorfield.fields import ColorField
from core.models import BaseContent

NUM_BOXES = 1
BOXES = range(1, NUM_BOXES + 1)

class Card(BaseContent):
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    roundedcorners = models.BooleanField(default=False, verbose_name="Rounded Corners")

    def __str__(self):
        return f"Card {self.front} / {self.back} (Box {self.box}, Active: {self.active})"

    @property
    def front(self):
        sides = getattr(self, 'active_sides', self.sides.filter(active=True))
        return next((s for s in sides if s.is_front), None)

    @property
    def back(self):
        sides = getattr(self, 'active_sides', self.sides.filter(active=True))
        return next((s for s in sides if not s.is_front), None)

    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]

        if new_box in BOXES:
            self.box = new_box
            self.save()

        return self

class CardSide(BaseContent):
    card = models.ForeignKey(
        Card, 
        on_delete=models.CASCADE, 
        related_name='sides' # All sides for this card
    )
    is_front = models.BooleanField(default=True)
    bordercolor = ColorField(default='#000000', verbose_name="Border Color")

   
class BodyContent(BaseContent):
    pass
