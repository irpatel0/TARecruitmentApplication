from flask import render_template, flash, redirect, url_for, request
from app import db
from app.auth import auth_blueprint as bp_auth
import sqlalchemy as sqla