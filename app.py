from pathlib import Path
import os

from flask import Flask, jsonify, request

from application.proplan_app_service import ProPlanApplicationService
from exceptions import InvalidRequestError
from services.proplan_facade import ProPlanServiceFacade
from services.repositories import ProPlanRepository

# Observer
from services.observers import (
    DeployRegistryObserver,
    AnalyticsRequestCounterObserver,
    DecisionLogObserver,
)

app = Flask(__name__)


@app.get("/")
def index():
    """
    Página inicial informativa do Activity Provider ProPlan.
    Não faz parte da especificação Inven!RA, mas ajuda nos testes.
    """
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
      <meta charset="UTF-8" />
      <title>ProPlan Activity Provider</title>
      <style>
        body {
          font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          margin: 2rem;
          line-height: 1.5;
        }
        h1 { font-size: 1.6rem; margin-bottom: 0.5rem; }
        code { background: #f3f3f3; padding: 0.1rem 0.25rem; border-radius: 4px; }
        ul { margin-top: 0.5rem; }
      </style>
    </head>
    <body>
      <h1>ProPlan – Activity Provider</h1>
      <p>
        Este serviço expõe os Web services RESTful necessários para integração com a
        arquitetura Inven!RA.
      </p>

      <h2>Endpoints disponíveis</h2>
      <ul>
        <li><code>GET /config-proplan</code> – página de configuração (config_url)</li>
        <li><code>GET /json-params-proplan</code> – parâmetros da atividade em JSON (json_params_url)</li>
        <li><code>GET /deploy-proplan?activityID=...</code> – deployment da instância (user_url)</li>
        <li><code>GET /analytics-list-proplan</code> – lista de analytics disponíveis (analytics_list_url)</li>
        <li><code>POST /analytics-proplan</code> – valores de analytics para uma instância (analytics_url)</li>
      </ul>

      <p>
        Para mais detalhes, consulte a documentação no repositório
        <a href="https://github.com/AndreMacielSousa/proplan-activity-provider">GitHub</a>
      </p>
    </body>
    </html>
    """


# -------------------------------------------------------------------------
# Composição (wiring) — isolada num único local.
# O objetivo é impedir que o módulo Flask acumule lógica de domínio.
# -------------------------------------------------------------------------

# Permite override por variável de ambiente (útil em dev/local)
BASE_URL = os.getenv("PROPLAN_BASE_URL", "https://proplan-activity-provider.onrender.com")
BASE_DIR = Path(__file__).resolve().parent

# Repositório + Facade + Application Service
repo = ProPlanRepository(base_url=BASE_URL, base_dir=BASE_DIR)
facade = ProPlanServiceFacade(repo)
app_service = ProPlanApplicationService(facade)

# Ligação dos observadores (Observer) no arranque
deploy_registry = DeployRegistryObserver()
analytics_counter = AnalyticsRequestCounterObserver()
decision_log = DecisionLogObserver()

facade.attach(deploy_registry)
facade.attach(analytics_counter)
facade.attach(decision_log)


# -------------------------------------------------------------------------
# Endpoints Inven!RA (HTTP thin endpoints)
# -------------------------------------------------------------------------

@app.get("/config-proplan")
def config_proplan():
    """
    config_url:
    Página HTML de configuração da atividade, embebida pela Inven!RA.
    """
    html = app_service.get_config_page()
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


@app.get("/json-params-proplan")
def json_params_proplan():
    """
    json_params_url:
    Devolve a lista de parâmetros da atividade, conforme especificação Inven!RA.
    """
    return jsonify(app_service.get_json_params())


@app.get("/deploy-proplan")
def deploy_proplan():
    """
    user_url (deploy):
    Recebe o identificador da instância na Inven!RA (activityID)
    e devolve o URL de acesso dessa instância.
    """
    try:
        activity_id = request.args.get("activityID")
        access_url = app_service.deploy_activity(activity_id)
        return access_url, 200, {"Content-Type": "text/plain; charset=utf-8"}
    except InvalidRequestError as e:
        return str(e), 400


@app.get("/analytics-list-proplan")
def analytics_list_proplan():
    """
    analytics_list_url:
    Lista dos analytics quantitativos e qualitativos que o ProPlan recolhe.
    """
    return jsonify(app_service.get_analytics_contract()), 200


@app.post("/analytics-proplan")
def analytics_proplan():
    """
    analytics_url:
    Recebe um JSON com { "activityID": "<id>" } e devolve
    analytics compatíveis com a Inven!RA.
    """
    try:
        data = request.get_json(silent=True) or {}
        activity_id = data.get("activityID")
        response = app_service.get_analytics(activity_id)
        return jsonify(response), 200
    except InvalidRequestError as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
