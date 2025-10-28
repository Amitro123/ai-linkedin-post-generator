import reflex as rx

config = rx.Config(
    app_name="linkedin_post_generator",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)