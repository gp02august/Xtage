from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='new_admin').exists():  # Change 'admin' to 'new_admin'
            User.objects.create_superuser(
                username='new_admin',
                email='admin@example.com',
                password='yourpassword'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))