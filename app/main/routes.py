from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.main import main_blueprint as bp_main

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
def index():
    return "CSASSIST"