# ProPlan – Activity Provider (Semana 1)

## 1. Enquadramento
O **ProPlan** é um módulo *Activity Provider* integrado na arquitetura **Inven!RA**, permitindo a simulação de cenários de gestão de projetos. Esta semana foi implementada a **infraestrutura mínima** exigida para a fase inicial: um *web service* testável, respondendo aos cinco pedidos RESTful definidos na especificação oficial da Inven!RA (Morgado & Cassola, 2022).

A implementação foi realizada em **Python + Flask**, com alojamento na plataforma **Render**.

---

## 2. Endpoints REST implementados (Semana 1)

| Serviço Inven!RA           | Método | Endpoint                                                                                      | Função                                                                                               |
|----------------------------|--------|------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| `config_url`              | GET    | `/config-proplan`                                                                              | Devolve HTML com os campos de configuração da atividade                                              |
| `json_params_url`         | GET    | `/json-params-proplan`                                                                         | Devolve a lista de parâmetros definidos em `json_params_url.json`                                    |
| `user_url` (deploy)       | GET    | `/deploy-proplan?activityID=<id>`                                                              | Gera e devolve o *launch URL* da instância                                                           |
| `analytics_list_url`      | GET    | `/analytics-list-proplan`                                                                      | Devolve a lista de analytics quantitativos e qualitativos disponibilizados pelo ProPlan              |
| `analytics_url`           | POST   | `/analytics-proplan`                                                                           | Recebe `activityID` e devolve analytics fictícios de exemplo, conforme o esquema Inven!RA            |

Base URL do serviço já publicado:  
**https://proplan-activity-provider.onrender.com**

---

## 3. Conteúdo incluído no repositório

- `app.py` – Implementação dos 5 endpoints RESTful  
- `requirements.txt` – Dependências (Flask + Gunicorn)  
- `render.yaml` – Configuração do serviço para Render  
- `json_params_url.json` – Lista de parâmetros de configuração  
- `analytics_url.json` – Esquema de analytics (quantitativos e qualitativos)  
- `templates/config_proplan.html` – Página HTML de configuração embebida  

---

## 4. Testes recomendados

### POST – Analytics da atividade
```http
POST https://proplan-activity-provider.onrender.com/analytics-proplan
Content-Type: application/json

{
  "activityID": "TESTE123"
}

GET – Parâmetros da atividade
GET https://proplan-activity-provider.onrender.com/json-params-proplan

GET – Lista de analytics
GET https://proplan-activity-provider.onrender.com/analytics-list-proplan

GET – Configuração HTML
GET https://proplan-activity-provider.onrender.com/config-proplan

## 5. Padrão de criação aplicado (Factory Method)

Na segunda fase do projeto foi aplicado o padrão de criação Factory Method (Gamma et al., 2000) ao processo de obtenção dos dados analíticos usados pelo serviço analytics_url (POST /analytics-proplan).

Foi introduzida a interface AnalyticsRepository, que define o contrato que qualquer repositório de analytics deve cumprir. A implementação concreta atual é JsonAnalyticsRepository, que gera valores fictícios com base no esquema definido em analytics_url.json.

Para encapsular o ponto de variação — a origem e forma de criação dos repositórios — foi criada a classe RepositoryFactory, contendo o método estático create_analytics_repository(). Nesta fase, a fábrica devolve sempre uma instância de JsonAnalyticsRepository, mas o desenho permite substituir esta implementação por outra (por exemplo, uma baseada em base de dados relacional) sem alterar o endpoint.

O endpoint /analytics-proplan passa assim a depender apenas da abstração AnalyticsRepository, reduzindo o acoplamento e preparando o módulo para futura extensibilidade, tal como recomendado nas boas práticas de design de software e na unidade curricular de Arquitetura e Padrões de Software.

## 6. Referencias

Morgado, L., & Cassola, F. (2022). Activity Providers na Inven!RA. Universidade Aberta.

Grilo, R., Baptista, R., Schlemmer, E., Gütl, C., Beck, D., Coelho, A., & Morgado, L. (2022).
Assessment and Tracking of Learning Activities on a Remote Computer Networking Laboratory Using the Inven!RA Architecture.

Cardoso, P., Morgado, L., & Coelho, A. (2020).
Authoring Game-Based Learning Activities that are Manageable by Teachers.

Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (2000). Padrões de Projeto: Soluções Reutilizáveis de Software Orientado a Objetos. Bookman.

## 7. Autor
André Sousa – 1300012
Mestrado em Engenharia Informática e Tecnologia Web – Universidade Aberta
Unidade Curricular: Arquitetura e Padrões de Software
Ano letivo 2025/2026