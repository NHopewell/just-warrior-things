from django.views import generic

from .models import WarriorPost


class WarriorPostListView(generic.ListView):
    model = WarriorPost
    template_name = 'warriorpost_list'