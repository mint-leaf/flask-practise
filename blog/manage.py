import os
from app import creat_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = creat_app(os.environ.get("FLASK_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


@manager.command
def test():
    """run the unit test"""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestResult(verbosity=2).run(tests)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

