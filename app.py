from datetime import timedelta
from website import create_app

app = create_app()

# session is set to expire after 1 day
app.permanent_session_lifetime = timedelta(days=1)

if __name__ == "__main__":
    app.run(debug=True)