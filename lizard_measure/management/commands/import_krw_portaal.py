# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.template import defaultfilters


class Command(BaseCommand):
    args = ''
    help = 'Import KRW portaal xml files'

    def handle(self, *args, **options):
        print 'Import KRW portaal'
