from html import escape

from django.test import TestCase

from .models import Poll, Ballot

from django.urls import reverse

class PollIndexViewTests(TestCase):
    def test_no_polls(self):
        """
        If no polls exist, an appropriate message is displayed
        """

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['poll_list'], [])
        self.assertNotContains(response, "<li></li>", html=True)

    def test_two_polls(self):
        """
        Ensure the name of a poll shows up in the index
        """
        poll1 = Poll.objects.create(name="Poll 1", text="first poll")
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, poll1.name)


    def test_two_polls(self):
        """
        Ensure the names of two polls show up in the index
        """
        poll1 = Poll.objects.create(name="Poll 1", text="first poll")
        poll2 = Poll.objects.create(name="Poll 2", text="second poll")
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, poll1.name)
        self.assertContains(response, poll2.name)

class PollDetailViewTests(TestCase):
    def test_view_poll_detail(self):
        """
        Create a poll and ensure it is visible
        """
        poll = Poll.objects.create(name="who?", text="Who dat?")
        url = reverse('polls:detail', args=(poll.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, poll.name)
        self.assertContains(response, poll.text)

class BallotIndexViewTests(TestCase):
    def test_no_ballots(self):
        poll = Poll.objects.create(name="What?", text="What's that?")
        url = reverse('polls:ballots', args=(poll.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['ballot_list'], [])
        self.assertNotContains(response, "<li></li>", html=True)
    
    def test_one_ballot(self):
        poll = Poll.objects.create(name="What?", text="What's that?")
        vote_url = reverse('polls:vote', args=(poll.id,))
        ballot = 'A>B>C'
        response = self.client.post(vote_url, {'ballot': ballot}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, escape(ballot))
    
    def test_two_ballots(self):
        poll = Poll.objects.create(name="What?", text="What's that?")
        vote_url = reverse('polls:vote', args=(poll.id,))
        ballot1 = 'A>B>C'
        response1 = self.client.post(vote_url, {'ballot': ballot1}, follow=True)
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, escape(ballot1))
        ballot2 = 'A>C>B'
        response2 = self.client.post(vote_url, {'ballot': ballot2}, follow=True)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, escape(ballot1))
        self.assertContains(response2, escape(ballot2))

class BallotModelTests(TestCase):
    poll = None

    def setUp(self):
        self.poll = Poll.objects.create(name='What is your quest?', text="What are you even doing?")

    def test_no_ballots(self):
        ballots = Ballot.get_ballots_and_counts_for_poll(self.poll.id)
        self.assertEqual(ballots, {})

    def test_one_ballot(self):
        Ballot.objects.create(poll_id=self.poll.id, text='A>B>C')
        ballots = Ballot.get_ballots_and_counts_for_poll(self.poll.id)
        self.assertEqual(ballots, {('A','B','C'):1})

    def test_two_duplicate_ballots(self):
        Ballot.objects.create(poll_id=self.poll.id, text='A>B>C')
        Ballot.objects.create(poll_id=self.poll.id, text='A>B>C')
        ballots = Ballot.get_ballots_and_counts_for_poll(self.poll.id)
        self.assertEqual(ballots, {('A','B','C'):2})

    def test_two_unique_ballots(self):
        Ballot.objects.create(poll_id=self.poll.id, text='A>B>C')
        Ballot.objects.create(poll_id=self.poll.id, text='C>B>A')
        ballots = Ballot.get_ballots_and_counts_for_poll(self.poll.id)
        self.assertEqual(ballots, {
            ('A','B','C'):1,
            ('C','B','A'):1,
        })

    def test_mix_of_duplicate_and_unique_ballots(self):
        for _ in range(3):
            Ballot.objects.create(poll_id=self.poll.id, text='A>B>C')

        Ballot.objects.create(poll_id=self.poll.id, text='C>B>A')
        Ballot.objects.create(poll_id=self.poll.id, text='C>B>A')

        Ballot.objects.create(poll_id=self.poll.id, text='B>C>A')
        
        ballots = Ballot.get_ballots_and_counts_for_poll(self.poll.id)
        self.assertEqual(ballots, {
            ('A','B','C'):3,
            ('C','B','A'):2,
            ('B','C','A'):1,
        })