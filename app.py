import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.get("/")
def index():
    """
    Página inicial informativa do Activity Provider ProPlan.
    Não faz parte da especificação Inven!RA, mas ajuda nos testes humanos.
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
        h1 {
          font-size: 1.6rem;
          margin-bottom: 0.5rem;
        }
        code {
          background: #f3f3f3;
          padding: 0.1rem 0.25rem;
          border-radius: 4px;
        }
        ul {
          margin-top: 0.5rem;
        }
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
        Para mais detalhes, consulte a documentação no repositório GitHub.
        https://github.com/AndreMacielSousa/proplan-activity-provider
      </p>
    </body>
    </html>
    """


# Domínio público do serviço (Render)
BASE_URL = "https://proplan-activity-provider.onrender.com"

# Carregamento dos ficheiros JSON de suporte 


BASE_DIR = Path(__file__).resolve().parent

JSON_PARAMS_PATH = BASE_DIR / "json_params_url.json"
ANALYTICS_SCHEMA_PATH = BASE_DIR / "analytics_url.json"


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Em caso de erro no ficheiro, o serviço continua com valores por omissão
        return default


JSON_PARAMS = load_json(
    JSON_PARAMS_PATH,
    default=[],
)

ANALYTICS_SCHEMA = load_json(
    ANALYTICS_SCHEMA_PATH,
    default={"quantAnalytics": [], "qualAnalytics": []},
)

# "Base de dados" em memória para a semana 1 (mock)
DEPLOYED_ACTIVITIES = {}


# Endpoints Inven!RA 

@app.get("/config-proplan")
def config_proplan():
    
    # config_url: Página HTML de configuração da atividade, embebida pela Inven!RA.
    
    return render_template("config_proplan.html")


@app.get("/json-params-proplan")
def json_params_proplan():
    
    # json_params_url:   Devolve a lista de parâmetros da atividade (nome e tipo), conforme especificação Inven!RA.
    
    return jsonify(JSON_PARAMS)


@app.get("/deploy-proplan")
def deploy_proplan():
    """
    user_url (deploy):
    Recebe o identificador da instância na Inven!RA (activityID)
    e devolve o URL de lançamento (launch URL) dessa instância.
    Nesta primeira semana os dados são apenas simulados.
    """
    activity_id = request.args.get("activityID")

    if not activity_id:
        return "Parâmetro 'activityID' em falta.", 400

    # URL da instância da atividade ProPlan
    access_url = f"{BASE_URL}/atividade/{activity_id}"

    # Guardar em memória para futura extensão (não é obrigatório nesta semana)
    DEPLOYED_ACTIVITIES[activity_id] = {
        "access_url": access_url,
        "params": {},
    }

    # A especificação permite devolver simplesmente o URL em texto plano
    return access_url, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.get("/analytics-list-proplan")
def analytics_list_proplan():
    """
    analytics_list_url:
    Lista dos analytics quantitativos e qualitativos que o ProPlan recolhe.
    Usa o ficheiro analytics_url.json como esquema.
    """
    return jsonify(ANALYTICS_SCHEMA)


@app.post("/analytics-proplan")
def analytics_proplan():
    """
    analytics_url:
    Recebe um JSON com { "activityID": "<id>" } e devolve
    analytics fictícios para essa instância, num formato
    compatível com a Inven!RA.
    """
    data = request.get_json(silent=True) or {}
    activity_id = data.get("activityID")

    if not activity_id:
        return jsonify({"error": "Campo 'activityID' em falta."}), 400

    # Exemplo de estudante fictício
    student_id = "1001"

    # Construção de valores de exemplo com base no esquema
    quant_values = []
    for qa in ANALYTICS_SCHEMA.get("quantAnalytics", []):
        name = qa.get("name")
        type_ = qa.get("type")

        # Valores puramente ilustrativos para a semana 1
        if type_ == "integer":
            example = 0
            if name == "decisions_count":
                example = 12
            elif name == "total_time_seconds":
                example = 3600
            elif name == "cost_variance":
                example = -500
            elif name == "schedule_variance_days":
                example = 2
            elif name == "client_satisfaction_score":
                example = 4
            elif name == "replans_count":
                example = 1

            quant_values.append(
                {
                    "name": name,
                    "type": type_,
                    "value": example,
                }
            )

    qual_values = []
    for qa in ANALYTICS_SCHEMA.get("qualAnalytics", []):
        name = qa.get("name")
        type_ = qa.get("type")

        if type_ == "URL":
            if name == "decision_log_url":
                value = f"{BASE_URL}/analytics/{activity_id}/{student_id}/decision-log"
            elif name == "timeline_url":
                value = f"{BASE_URL}/analytics/{activity_id}/{student_id}/timeline"
            else:
                value = f"{BASE_URL}/analytics/{activity_id}/{student_id}/{name}"
        elif type_ == "text/plain":
            if name == "postmortem_reflection":
                value = (
                    "Reflexão de exemplo: o grupo conseguiu cumprir o prazo, "
                    "mas com ligeiro aumento de custo para manter a qualidade."
                )
            else:
                value = "Texto de exemplo."
        else:
            value = None

        qual_values.append(
            {
                "name": name,
                "type": type_,
                "value": value,
            }
        )

    response = [
        {
            "inveniraStdID": student_id,
            "quantAnalytics": quant_values,
            "qualAnalytics": qual_values,
        }
    ]

    return jsonify(response)


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    # Execução local para desenvolvimento
    app.run(host="0.0.0.0", port=5000, debug=True)
