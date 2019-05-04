from config import app
from controller_functions import index, show_register_page, process_new_user, show_dashboard, show_login_page, login, \
    users_logout, show_post_form, post_article, show_user_posts, show_edit_user_post, edit_article, show_profile_page, \
    upload_file, uploaded_file

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=show_register_page)

app.add_url_rule("/login", view_func=show_login_page)
app.add_url_rule("/login_user", view_func=login, methods=['POST'])
app.add_url_rule("/logout", view_func=users_logout, methods=["GET"])

app.add_url_rule("/process_new_user", view_func=process_new_user, methods=['POST'])
app.add_url_rule("/dashboard", view_func=show_dashboard)

app.add_url_rule("/post", view_func=show_post_form)
app.add_url_rule("/create_post", view_func=post_article, methods=['POST'])

app.add_url_rule("/profile/<id>", view_func=show_profile_page)
app.add_url_rule("/upload_file", view_func=upload_file, methods=["POST"])
app.add_url_rule("/uploaded/<profile_pic>", view_func=uploaded_file)
app.add_url_rule("/user/posts/<id>", view_func=show_user_posts)
app.add_url_rule("/user/posts/edit/<id>", view_func=show_edit_user_post)
app.add_url_rule("/edit_post/<id>", view_func=edit_article, methods=['POST'])
