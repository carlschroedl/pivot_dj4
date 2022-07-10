from typing import Tuple
from attr import frozen
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from votelib.evaluate.condorcet import RankedPairs
from votelib.convert import RankedToCondorcetVotes
from .models import Poll, Ballot
from django.db.models import Count

from typing import Tuple, FrozenSet, Union, AnyStr

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

condorcet_converter = RankedToCondorcetVotes()
ranked_pairs_evaluator = RankedPairs()

class PollIndexView(generic.ListView):
    model = Poll
    template_name = 'polls/poll_index.html'

class BallotIndexView(generic.ListView):
    model = Ballot
    template_name = 'polls/ballot_index.html'

class PollView(generic.DetailView):
    model = Poll
    template_name = 'polls/poll.html'

def result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    counted_ballots = Ballot.objects.filter(poll_id=poll.id).values('text').annotate(total=Count('text')).order_by('total')
    ballots = {}
    for ballot_count in counted_ballots:
        ballot = parse_abif(ballot_count['text'])
        ballots[ballot] = ballot_count['total']

    print(repr(ballots))

    condorcet_tally = condorcet_converter.convert(ballots)

    result = ranked_pairs_evaluator.evaluate(condorcet_tally, 99)
    print(repr(result))
    return render(request, 'polls/result.html', {
            'poll': poll,
            'result': result,
    })

def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        user_ballot = request.POST['ballot']
    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'error_message': "You didn't provide a ballot.",
        })
    else:
        Ballot(poll_id=poll.id, text=user_ballot).save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:ballots', args=(poll.id,)))
