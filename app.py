import dash_bootstrap_components as dbc
from dash import Dash, html, page_container

from callbacks import register_callbacks
from components.navbar import build_topbar
from components.sidebar import build_sidebar
from config.logging import configure_logging
from config.settings import get_settings
from database.bootstrap import bootstrap_local_data

settings = get_settings()
configure_logging(settings.debug, settings.log_level)
bootstrap_local_data()


def create_app() -> Dash:
    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
        title="Portal de Viaticos",
    )
    app.layout = html.Div(
        [
            build_topbar(),
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(build_sidebar(), xl=2, lg=3, md=4, class_name="mb-4"),
                        dbc.Col(
                            html.Main(page_container, className="page-shell"),
                            xl=10,
                            lg=9,
                            md=8,
                        ),
                    ],
                    class_name="g-4",
                ),
                fluid=True,
                class_name="app-shell",
            ),
        ],
        className="app-background",
    )
    register_callbacks()
    return app


app = create_app()
server = app.server
