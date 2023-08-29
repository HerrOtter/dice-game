from flask import request, url_for, redirect, flash
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.exc import IntegrityError

from .models import db, User, Game
from .utils import is_admin

# Models
class SetupTable(db.Model):
    """
    Used to keep track if the setup has been completed
    """
    __tablename__ = "_setup"
    complete = db.Column(db.Boolean, primary_key=True, default=True)

# Views
class AuthIndexView(AdminIndexView):

    @expose("/")
    def index(self):
        if not is_admin():
            return redirect(url_for("index"))
        return super().index()

class AuthModelView(ModelView):
    def is_accessible(self):
        return is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("index"))

class SetupView(BaseView):
    setup_complete = False

    def is_accessible(self):
        if self.setup_complete:
            return False

        # We found a setup entry in the database, prevent setups from occuring
        if db.session.execute(db.select(SetupTable)).first():
            self.setup_complete = True
            return False

        return True

    @expose("/", methods=["GET", "POST"])
    def index(self):
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            password_again = request.form.get("password_again")

            if username and password and password_again:
                if password == password_again:
                    user = User(username=username)
                    user.set_password(password)
                    user.admin = True

                    db.session.add(user)
                    try:
                        db.session.commit()
                    except IntegrityError:
                        flash("Username already exists", "error")

                    self.setup_complete = True

                    done = SetupTable()
                    db.session.add(done)
                    db.session.commit()
                    return redirect(url_for("index"))
                else:
                    flash("Repeated password does not match", "error")
            else:
                flash("Form value is missing", "error")

        return self.render("admin/setup.html", messages=["bla"])

class DiceView(AuthModelView):
    column_exclude_list = ["password"]
    form_excluded_columns = ["password"]

    page_size = 10

    create_modal = True
    edit_modal = True

class GameView(DiceView):
    can_edit = False

admin = Admin(name="!dice", index_view=AuthIndexView(), template_mode="bootstrap4")

admin.add_view(DiceView(User, db.session))
admin.add_view(GameView(Game, db.session))
admin.add_view(SetupView(name="setup", endpoint="setup"))
