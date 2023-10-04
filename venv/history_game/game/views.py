import random
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Event, Match, User
from .forms import PlayerNameForm
from django.contrib import messages
import pandas as pd


# Adds Event data from a CSV file
# def add_data():
#     data = pd.read_csv("data.csv")
#     for index, row in data.iterrows():
#         event = Event(name=row["Name"],
#                       date=row["Date"],
#                       description=row["Description"],
#                       topic=row["Topic"],
#                       category=row["Category"])
#         event.save()


def index(request):
    """View function for home page of site."""
    # There is no logged in user
    if "_auth_user_id" not in request.session.keys():
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        # First event - chooses the middle event
        starting_event = Event.objects.all()[len(Event.objects.all()) // 2]
        match = Match(user_playing=request.user)
        match.save()
        match.event_list.add(starting_event.id)

        # Set the match ID to the session of the user for later use
        # Game will reset if session is cleared (Done this way because of anonymous users)
        request.session["match"] = match.id

        return HttpResponseRedirect(reverse('play'))
    else:
        # Reset match details if user gets here
        delete_match_details(request)

        # Generate counts of some of the main objects
        num_events = Event.objects.all().count()
        num_matches_total = Match.objects.all().count()
        num_matches_user = Match.objects.filter(user_playing=request.user).count()
        highest_highscore = User.objects.order_by("-highscore")[0].highscore
        user_highscore = User.objects.filter(pk=request.user.id)[0].highscore

        context = {
            'num_events': num_events,
            'num_matches_total': num_matches_total,
            'num_matches_user': num_matches_user,
            'highest_highscore': highest_highscore,
            'user_highscore': user_highscore
        }

        # Render the HTML template index.html with the data in the context variable
        return render(request, 'index.html', context=context)


def play(request):
    # There is no logged in user
    if "_auth_user_id" not in request.session.keys():
        return HttpResponseRedirect(reverse('login'))

    # Redirect users to main page if session has somehow been cleared
    if not is_session_valid(request):
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        match = get_object_or_404(Match, pk=request.session["match"])
        selection = request.POST.getlist('timeline-selection')[0][9:]
        event_to_place = get_object_or_404(Event, pk=request.session["event_to_place"])

        # End game if user made wrong selection
        if not is_selection_correct(match, event_to_place, selection):
            return HttpResponseRedirect(reverse('lost_game'))

        # Add correctly selected event to match object
        match.event_list.add(event_to_place.id)

        # Player won game, go to win page
        if match.event_list.all().count() == Event.objects.all().count():
            return HttpResponseRedirect(reverse('won_game'))

        # More events left, continue game
        return HttpResponseRedirect(reverse('play'))
    else:
        match = get_object_or_404(Match, pk=request.session["match"])
        event_to_place, events_left = get_event_to_place(match, request)
        request.session["event_to_place"] = event_to_place.id

        context = {
            'match': match,
            'new_event': event_to_place,
            'events_left': events_left.count()
        }

        return render(request, "game/play.html", context=context)


def get_event_to_place(match, request):
    if match.event_list.all().count() != Event.objects.all().count():
        events_left = Event.objects.exclude(id__in=(match.event_list.all()))

        # Session has been cleared but game has not been won
        # (need to make sure players can't get here from the loss page)
        if "event_to_place" not in request.session.keys():
            event_to_place = events_left[random.randint(0, events_left.count() - 1)]  # Randomly select an event
        else:
            # The event in the session has been placed correctly already
            if get_object_or_404(Event, pk=request.session["event_to_place"]) in match.event_list.all():
                event_to_place = events_left[random.randint(0, events_left.count() - 1)]
            # The event in the session has not been placed (happens if player make an invalid selection)
            else:
                event_to_place = get_object_or_404(Event, pk=request.session["event_to_place"])
    else:
        event_to_place = match.event_list.all().reverse()[0]

    return event_to_place, events_left


def lost_game(request):
    if request.method == 'POST':
        if "Play Again" in request.POST.get('selection'):
            return HttpResponseRedirect(reverse('play')) # Post on /index instead
        return HttpResponseRedirect(reverse('index'))
    else:
        # Redirect users to main page if session has somehow been cleared
        if not is_session_valid(request):
            return HttpResponseRedirect(reverse('index'))

        update_highscore(request)
        match = get_object_or_404(Match, pk=request.session["match"])
        num_events = match.event_list.count() - 1
        event_to_place = get_object_or_404(Event, pk=request.session["event_to_place"])
        event_before, event_after = get_event_before_and_after(match, event_to_place)

        context = {
            'num_events': num_events,
            'event_to_place': event_to_place,
            'event_before': event_before,
            'event_after': event_after
        }

        delete_match_details(request)

        return render(request, "game/lose.html", context=context)


def won_game(request):
    if request.method == 'POST':
        if "Play Again" in request.POST.get('selection'):
            return HttpResponseRedirect(reverse('play')) # Post on /index instead
        return HttpResponseRedirect(reverse('index'))
    else:
        # Redirect users to main page if session has somehow been cleared
        if not is_session_valid(request):
            return HttpResponseRedirect(reverse('index'))

        update_highscore(request)
        match = get_object_or_404(Match, pk=request.session["match"])
        match.game_won = True
        match.save()
        delete_match_details(request)
        return render(request, "game/win.html", context={'match': match})


def is_session_valid(request):
    if "match" in request.session.keys():
        return True
    return False


def update_highscore(request):
    match = get_object_or_404(Match, pk=request.session["match"])
    num_events = match.event_list.count() - 1
    user = get_object_or_404(User, pk=request.user.id)

    if user.highscore < num_events:
        user.highscore = num_events
        user.save()


def delete_match_details(request):
    if "match" in request.session.keys():
        del request.session["match"]
    if "event_to_place" in request.session.keys():
        del request.session["event_to_place"]


def is_selection_correct(match, event_to_place, selection):
    if selection == "end":
        selected_event = match.event_list.all().reverse()[0]
        if event_to_place.date < selected_event.date:
            return False
        else:
            return True

    selected_event = get_object_or_404(Event, pk=selection)
    selected_event_index = list(match.event_list.all()).index(selected_event)

    if event_to_place.date > selected_event.date:
        return False

    if selected_event_index == 0:
        return True

    event_before = match.event_list.all()[selected_event_index - 1]

    if event_to_place.date < event_before.date:
        return False
    return True


def get_event_before_and_after(match, event_to_place):
    event_before = None
    event_after = None

    # Not an optimised way to do this
    for index, event in enumerate(match.event_list.all()):
        if event.date > event_to_place.date:
            if index != 0:
                event_before = match.event_list.all()[index-1]
            event_after = match.event_list.all()[index]
            break

    if not event_before and not event_after:
        event_before = match.event_list.all().reverse()[0]

    return event_before, event_after



