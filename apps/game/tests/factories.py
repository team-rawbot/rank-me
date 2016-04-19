from django.contrib.auth import get_user_model
from django.utils import timezone

import factory

from ..models import Competition


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@email.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')


class CompetitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Competition

    name = factory.Sequence(lambda n: 'competition%d' % n)
    start_date = factory.LazyAttribute(lambda _: timezone.now())
    end_date = None
    creator = factory.SubFactory(UserFactory)
