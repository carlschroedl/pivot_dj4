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
    ballots = Ballot.get_ballots_and_counts_for_poll(poll_id)
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
