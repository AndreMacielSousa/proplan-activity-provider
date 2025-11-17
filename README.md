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

app.py # Implementação dos 5 endpoints RESTful
requirements.txt # Dependências (Flask + Gunicorn)
render.yaml # Configuração do serviço para Render (opcional)
json_params_url.json # Lista de parâmetros de configuração (GET)
analytics_url.json # Esquema de analytics (para GET e POST)
templates/config_proplan.html # Página HTML de configuração embebida

---

## 4. Testes recomendados

### GET – Parâmetros da atividade

POST https://proplan-activity-provider.onrender.com/analytics-proplan

Content-Type: application/json

{
"activityID": "TESTE123"
}


---

## 5. Estado da implementação (conforme pedido da semana 1)

### ✔️ Servidor Web funcional  
### ✔️ 5 Web services RESTful implementados  
### ✔️ HTML de configuração operacional  
### ✔️ Respostas JSON válidas e coerentes com a especificação  
### ✔️ Dados fictícios para testes (analytics)  
### ✔️ Deploy público no Render  
### ✔️ Repositório GitHub documentado  

---

## 6. Referências (formato APA)
Morgado, L., & Cassola, F. (2022). *Activity Providers na Inven!RA*. Universidade Aberta.  

Grilo, R., Baptista, R., Schlemmer, E., Gütl, C., Beck, D., Coelho, A., & Morgado, L. (2022).  
*Assessment and Tracking of Learning Activities on a Remote Computer Networking Laboratory Using the Inven!RA Architecture*.  

Cardoso, P., Morgado, L., & Coelho, A. (2020).  
*Authoring Game-Based Learning Activities that are Manageable by Teachers*.

---

## 7. Autor
**André Sousa – 1300012**  
Mestrado em Engenharia Informática e Tecnologia Web – Universidade Aberta  
Unidade Curricular: Arquitetura e Padrões de Software  
Ano letivo 2025/2026

