from django.contrib.auth import get_user_model
from django.utils import timezone

import factory

from ..models import Competition, Sport


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@email.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')


class SportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sport

    slug = factory.Sequence(lambda n: 'sport%d' % n)
    name = factory.Sequence(lambda n: 'sport%d' % n)


class CompetitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Competition

    name = factory.Sequence(lambda n: 'competition%d' % n)
    start_date = factory.LazyAttribute(lambda _: timezone.now())
    end_date = None
    creator = factory.SubFactory(UserFactory)
    sport = factory.SubFactory(SportFactory)
