from django.contrib.auth import get_user_model
from django.utils import timezone

import factory

from ..models import Competition, Team


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@email.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    @factory.post_generation
    def users(self, create, extracted):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)


class CompetitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Competition

    name = factory.Sequence(lambda n: 'competition%d' % n)
    start_date = timezone.now()
    end_date = None
    creator = factory.SubFactory(UserFactory)
