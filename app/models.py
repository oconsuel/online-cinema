import os
from flask import url_for
import sqlalchemy as sa
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import markdown
from app import db