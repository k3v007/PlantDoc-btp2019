from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.config import DevelopmentConfig
from app.models import db


app = create_app(DevelopmentConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
