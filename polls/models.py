from django.db import models

class Poll(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
        
    def __str__(self) -> str:
        return self.name + ": " + self.text

class Ballot(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.text