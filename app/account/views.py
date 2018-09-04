from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.email import send_email
from app.models import User, get_or_create
from app.account.forms import (
    ChangeEmailForm, ChangePasswordForm, CreatePasswordForm, LoginForm,
    RequestResetPasswordForm, ResetPasswordForm, InviteUserForm, RegistrationForm)

account = Blueprint('account', __name__)


@account.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    # Prefill email from landing page
    if request.args.get('email'):
        form = RegistrationForm(request.args)
    else:
        form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        confirm_link = url_for('account.confirm', token=token, _external=True)
        flash('A confirmation link has been sent to {}.'.format(user.email), 'warning')
        send_email(
            recipient=form.email.data,
            subject='Confirm Your Account',
            template='account/email/confirm',
            user_name=form.name.data,
            confirm_link=confirm_link
        )
        return redirect(url_for('main.index'))
    return render_template('account/register.html', form=form)

@account.route('/admin')
@login_required
def admin():
    """Admin dashboard page."""
    if not current_user.is_admin:
        flash("Admin user required.", 'warning')
        return redirect(url_for('main.index'))
    users = User.query.order_by(User.id).all()
    return render_template('account/admin.html',
        users=users
    )

@account.route('/admin/user/<id>', methods=['DELETE'])
@login_required
def user_delete(id):
    """Delete user API."""
    if not current_user.is_admin:
        flash("Admin user required.", 'warning')
        return redirect(url_for('main.index'))
    user = get_or_create(User, id=id)
    _user = User.query.get(id)
    if _user is None:
        flash('User does not exist!', 'warning')
    else:
        db.session.delete(_user)
        db.session.commit()
        flash('User {} deleted.'.format(_user.name), 'danger')

    return url_for('account.admin')

@account.route('/admin/invite', methods=['GET', 'POST'])
def user_invite():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        flash('User {} successfully invited'.format(user.name), 'success')
        send_email(
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user_name=user.name,
            user_email=user.email,
            invite_link=invite_link,
        )
        return redirect(url_for('account.admin'))
    return render_template('account/invite.html', form=form)

@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid email or password.', 'form-danger')
    return render_template('account/login.html', form=form)

@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('account.login'))

@account.route('/manage', methods=['GET', 'POST'])
@account.route('/manage/info', methods=['GET', 'POST'])
@login_required
def manage():
    """Display a user's account information."""
    return render_template('account/manage.html', user=current_user, form=None)

@account.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Respond to existing user's request to reset their password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_password_reset_token()
            reset_link = url_for(
                'account.reset_password', token=token, _external=True)
            flash('A password reset link has been sent to {}.'.format(
                form.email.data), 'warning')
            send_email(
                recipient=user.email,
                subject='Reset Your Password',
                template='account/email/reset_password',
                user_name=user.name,
                reset_link=reset_link,
                next=request.args.get('next')
            )
        return redirect(url_for('account.login'))
    return render_template('account/reset_password.html', form=form)

@account.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid email address.', 'form-danger')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.new_password.data):
            flash('Your password has been updated.', 'success')
            return redirect(url_for('account.login'))
        else:
            flash('The password reset link is invalid or has expired.',
                  'form-danger')
            return redirect(url_for('main.index'))
    return render_template('account/reset_password.html', form=form)

@account.route('/manage/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Original password is invalid.', 'form-danger')
    return render_template('account/manage.html', form=form)

@account.route('/manage/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for(
                'account.change_email', token=token, _external=True)
            flash('A confirmation link has been sent to {}.'.format(new_email),
                  'warning')
            send_email(
                recipient=new_email,
                subject='Confirm Your New Email',
                template='account/email/change_email',
                user_name=current_user._get_current_object().name,
                change_email_link=change_email_link
            )
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'form-danger')
    return render_template('account/manage.html', form=form)

@account.route('/manage/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash('Your email address has been updated.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('main.index'))

@account.route('/confirm-account')
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    token = current_user.generate_confirmation_token()
    confirm_link = url_for('account.confirm', token=token, _external=True)
    flash('A new confirmation link has been sent to {}.'.format(
        current_user.email), 'warning')
    send_email(
        recipient=current_user.email,
        subject='Confirm Your Account',
        template='account/email/confirm',
        # current_user is a LocalProxy, we want the underlying user object
        user_name=current_user._get_current_object().name,
        confirm_link=confirm_link
    )
    return redirect(url_for('main.index'))

@account.route('/confirm-account/<token>')
@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_account(token):
        flash('Your account has been confirmed.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('main.index'))

@account.route(
    '/join-from-invite/<int:user_id>/<token>', methods=['GET', 'POST'])
def join_from_invite(user_id, token):
    """
    Confirm new user's account with provided token and prompt them to set
    a password.
    """
    if current_user is not None and current_user.is_authenticated:
        flash('You are already logged in.', 'danger')
        return redirect(url_for('main.index'))

    new_user = User.query.get(user_id)
    if new_user is None:
        return redirect(404)

    if new_user.password_hash is not None:
        flash('You have already joined.', 'danger')
        return redirect(url_for('main.index'))

    if new_user.confirm_account(token):
        form = CreatePasswordForm()
        if form.validate_on_submit():
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            flash('Your password has been set. After you log in, you can '
                  'go to your "Account" page to review your account '
                  'information and settings.', 'success')
            return redirect(url_for('account.login'))
        return render_template('account/join_invite.html', form=form)
    else:
        flash('The confirmation link is invalid or has expired. Another '
              'invite email with a new link has been sent to you.', 'danger')
        token = new_user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user_id,
            token=token,
            _external=True)
        send_email(
            recipient=new_user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user_name=new_user.name,
            user_email=new_user.email,
            invite_link=invite_link
        )
    return redirect(url_for('main.index'))

@account.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:8] != 'account.' \
            and request.endpoint != 'static':
        return redirect(url_for('account.unconfirmed'))

@account.route('/unconfirmed')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('account/unconfirmed.html')
