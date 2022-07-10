from django.db import models
from django.db.models import Count
from typing import Tuple, FrozenSet, Union, AnyStr

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
    
    @staticmethod
    def parse_abif(text) -> Tuple[Union[AnyStr, FrozenSet[AnyStr]], ...]:
        candidate_groups = text.split('>')
        ranking_list = []
        for candidate_group in candidate_groups:
            candidates_list = candidate_group.split('=')
            if 1 == len(candidates_list):
                ranking_list.append(candidates_list[0])
            else:
                ranking_list.append(frozenset(candidates_list))

        ranking_tuple = tuple(ranking_list)
        return ranking_tuple

    @staticmethod
    def get_ballots_and_counts_for_poll(poll_id):
        counted_ballots = Ballot.objects.filter(poll_id=poll_id).values('text').annotate(total=Count('text')).order_by('total')
        ballots = {}
        for ballot_count in counted_ballots:
            ballot = Ballot.parse_abif(ballot_count['text'])
            ballots[ballot] = ballot_count['total']
        
        return ballots