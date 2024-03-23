import django
django.setup()

from django.test import TestCase
from django.shortcuts import render, redirect
from django.db import transaction, DatabaseError, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import logging, time
from django.http import HttpResponse
from character_creation.openai_api_handler import openAI_api_handler as heroArchitect
from character_creation.views import parse_dice_notation
from character_creation.models import *
from accounts.models import HA_User

# Create your tests here.

logging.basicConfig(level=logging.INFO)
if __name__ == "__main__":
    LOGGER = logging.getLogger("general")
else:
    LOGGER = logging.getLogger(__name__)


def main():

    d6 = "d6"
    dice = parse_dice_notation("1"+d6)[1]
    print(dice)

if __name__ == "__main__":

    main()

