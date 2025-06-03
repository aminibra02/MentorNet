from app import app, db # Make sure db is imported
import os

def create_tables():
    # We need to ensure this path is relative to the project root, not 'app' directory
    # The db path is already configured in app/__init__.py using project_root,
    # so we can directly use the app.config value or construct it similarly.
    # For simplicity and consistency, let's reconstruct it here as well,
    # or rely on the fact that db operations need app_context.
    # The app.config['SQLALCHEMY_DATABASE_URI'] is 'sqlite:///path/to/site.db'
    # We need to extract the path part.
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    db_path_prefix = 'sqlite:///'
    if db_uri.startswith(db_path_prefix):
        db_path = db_uri[len(db_path_prefix):]
    else:
        # Fallback or error if the URI format is unexpected
        # For this specific case, we know the structure.
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', os.pardir))
        db_path = os.path.join(project_root, 'site.db')


    if not os.path.exists(db_path):
        with app.app_context(): # Essential for db operations outside of a request
            db.create_all()
        print(f"Database tables created at {db_path}")
    else:
        print(f"Database already exists at {db_path}")

if __name__ == '__main__':
    create_tables()
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
