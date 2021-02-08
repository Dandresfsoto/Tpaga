from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField()
    amount = models.FloatField()

    def __str__(self):
        return self.name

    def get_image_url(self):
        url = None
        try:
            url = self.image.url
        except:
            pass
        return url

    def get_pretty_amount(self):
        return "$ {:20,.2f}".format(self.amount)
