#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, DataSet, KeyWord, Category
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate()
migrate.init_app(app, db, directory = 'migrations')

def make_shell_context():
    return dict(app=app, db=db, User=User, DataSet=DataSet, KeyWord=KeyWord, Category=Category)
manager.add_command('shel', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
