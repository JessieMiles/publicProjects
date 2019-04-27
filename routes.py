from config import app
from controller_functions import index, show_register_page, process_new_user, show_dashboard, show_login_page, login

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=show_register_page)

app.add_url_rule("/login", view_func=show_login_page)
app.add_url_rule("/login_user", view_func=login, methods=['POST'])

app.add_url_rule("/process_new_user", view_func=process_new_user, methods=['POST'])
app.add_url_rule("/dashboard", view_func=show_dashboard)


