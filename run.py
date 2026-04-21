from app import app
from config.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    app.run(debug=settings.debug)
