from config import app
import routes
from models import Users


if __name__ == '__main__':
    app.run(host='localhost',
            port=5000,
            debug=True)
