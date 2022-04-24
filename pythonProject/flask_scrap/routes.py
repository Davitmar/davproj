from flask import Blueprint, request, render_template, redirect, url_for, flash, session, send_from_directory, \
    current_app, abort

from project.core.decorators import require_login
from project.db import db
from project.note.models import Note

route_bp = Blueprint('route', __name__)

@route_bp.route('/')
def home():
    page = '1'
    if request.args:
        if request.args.get('page'):
            page = request.args.get('page')
        if request.args.get('country'):
            c = request.args.get('country')
            q = Hamalsaran.query.filter_by(country=c).offset((int(page) - 1) * 20).limit(20).all()
            k = [{'name': j.name, 'country': j.country} for j in q]
            return jsonify(k)
    q = Hamalsaran.query.offset((int(page) - 1) * 20).limit(20).all()
    k = [{'name': j.name, 'country': j.country} for j in q]
    return jsonify(k)
