from django.core.management.base import BaseCommand, CommandError
from util.upd_biblio import upd_biblio_soap
from plato.models import User
from django.shortcuts import get_object_or_404


class Command(BaseCommand):
	args = 'None'
	help = 'Upload the database of publication (Page) from the Telecom-ParisTech publication database'
	
	def handle(self, *args, **options):
		admin = get_object_or_404(User,login='petitpas')
		upd_biblio_soap(admin)
		self.stdout.write("It's updated!")
