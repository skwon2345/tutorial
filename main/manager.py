from main import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()

# To migrate, execute the following commands
# docker-compose exec backend sh
# python3 manage.py db init
# python3 manager.py db migrate
# python3 manager.py db upgrade
