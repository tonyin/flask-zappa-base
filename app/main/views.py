from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('account.login'))
    return redirect(url_for('main.index'))
