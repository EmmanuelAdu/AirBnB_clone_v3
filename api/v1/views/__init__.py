#!/usr/bin/python3
"""
Creates a Blueprint instance with `url_prefix` set to `/api/v1`.
"""


from flask import Blueprint
from models.state import State


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
