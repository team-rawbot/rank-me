from django.contrib.auth import get_user_model
from game.models import Competition
import factory
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@email.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')


class CompetitionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Competition

    name = factory.Sequence(lambda n: 'competition%d' % n)
    start_date = timezone.now()
    end_date = timezone.now()
    slug = "liip-competition"
    creator_id = 1
