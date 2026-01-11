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
- `services/proplan_facade.py` – Fachada interna (Facade) para orquestração dos pedidos
- `serializers/analytics_serializer.py` – Normalização/serialização das respostas de analytics
- `exceptions.py` – Exceções de validação (mapeadas para HTTP 400)

---

## 4. Testes recomendados

### POST

### PowerShell (Windows) – exemplo de teste do POST

```powershell
Invoke-WebRequest `
  -Method POST `
  -Uri https://proplan-activity-provider.onrender.com/analytics-proplan `
  -ContentType "application/json" `
  -Body '{"activityID":"TESTE123"}'
```

### GET

GET – Parâmetros da atividade
GET https://proplan-activity-provider.onrender.com/json-params-proplan

GET – Lista de analytics
GET https://proplan-activity-provider.onrender.com/analytics-list-proplan

GET – Configuração HTML
GET https://proplan-activity-provider.onrender.com/config-proplan


## 5. Padrão de criação aplicado (Factory Method)

Na segunda fase do projeto foi aplicado o padrão de criação Factory Method (Gamma et al., 1995) ao processo de obtenção dos dados analíticos usados pelo serviço analytics_url (POST /analytics-proplan).

Foi introduzida a interface AnalyticsRepository, que define o contrato que qualquer repositório de analytics deve cumprir. A implementação concreta atual é JsonAnalyticsRepository, que gera valores fictícios com base no esquema definido em analytics_url.json.

Para encapsular o ponto de variação — a origem e forma de criação dos repositórios — foi criada a classe RepositoryFactory, contendo o método estático create_analytics_repository(). Nesta fase, a fábrica devolve sempre uma instância de JsonAnalyticsRepository, mas o desenho permite substituir esta implementação por outra (por exemplo, uma baseada em base de dados relacional) sem alterar o endpoint.

O endpoint /analytics-proplan passa assim a depender apenas da abstração AnalyticsRepository, reduzindo o acoplamento e preparando o módulo para futura extensibilidade, tal como recomendado nas boas práticas de design de software e na unidade curricular de Arquitetura e Padrões de Software.

## 6. Padrão estrutural aplicado (Facade)

Na fase atual foi aplicado o padrão estrutural **Facade** (GAMMA et al., 1995) para reduzir o acoplamento entre a camada de endpoints Flask e o subsistema interno responsável pela validação do pedido, seleção do repositório e preparação/normalização das respostas.

No contexto Inven!RA, o Activity Provider é essencialmente **reativo** (não inicia interações; responde a pedidos). Por isso, a fachada não está “virada para a Inven!RA” (que define a sua API e não se adapta ao fornecedor), mas sim **virada para dentro**, funcionando como um “entreposto” de orquestração para os subcomponentes internos.

### 6.1. Alterações realizadas
Foi introduzido o componente `ProPlanServiceFacade` e, de forma incremental, os endpoints abaixo passaram a delegar nele:

- `POST /analytics-proplan` (analytics_url): valida `activityID`, obtém dados via repositório e devolve analytics no formato esperado.
- `GET /analytics-list-proplan` (analytics_list_url): devolve o contrato (quantAnalytics/qualAnalytics) através do mesmo ponto arquitetural, reforçando coerência entre “o que se anuncia” e “o que se devolve”.

Este desenho permite manter os endpoints “magros” (parsing e códigos HTTP) e concentrar as regras/compromissos do subsistema no Facade, melhorando legibilidade, manutenção e extensibilidade.

### 6.2. Estrutura introduzida no repositório
- `services/proplan_facade.py` – implementação do `ProPlanServiceFacade`
- `serializers/analytics_serializer.py` – ponto único para normalização (nesta fase com comportamento pass-through)
- `exceptions.py` – exceções de validação (ex.: `InvalidRequestError`)

## 7. Padrão comportamental aplicado (Observer)

Na fase atual do projeto foi aplicado o padrão comportamental **Observer** (Gamma et al., 1995) ao núcleo de orquestração interna do Activity Provider, concretamente ao componente `ProPlanServiceFacade`.

### 7.1. Motivação

O Activity Provider ProPlan é, por natureza, um sistema **reativo**, respondendo a eventos externos como:
- pedidos de deploy de instâncias (`user_url`);
- pedidos de recolha de analytics (`analytics_url`).

Neste contexto, identificou-se a necessidade de desacoplar o fluxo principal de orquestração (validação, obtenção e devolução de dados) de responsabilidades transversais, como:
- registo de deploys;
- contagem de pedidos de analytics;
- manutenção de rastos qualitativos associados ao ciclo de vida da instância.

O padrão Observer permite explicitar estes pontos de variação sem introduzir dependências diretas entre a fachada e essas funcionalidades secundárias.

### 7.2. Ponto de aplicação no projeto

O componente `ProPlanServiceFacade` atua simultaneamente como:
- **Facade** (padrão estrutural), concentrando a orquestração interna;
- **Subject** do padrão Observer, emitindo eventos de domínio relevantes.

Foram definidos eventos explícitos de ciclo de vida:
- `ActivityDeployed` – emitido após o deploy de uma instância;
- `AnalyticsRequested` – emitido aquando de pedidos ao serviço `analytics_url`.

### 7.3. Observadores concretos implementados

Foram implementados os seguintes *ConcreteObservers*, registados no arranque da aplicação:

- `DeployRegistryObserver` – regista metadados mínimos do deploy por `activityID`;
- `AnalyticsRequestCounterObserver` – contabiliza pedidos ao serviço de analytics por instância;
- `DecisionLogObserver` – mantém um rasto textual (mock) de eventos relevantes, preparando a evolução futura para analytics qualitativos persistentes.

Estas implementações são deliberadamente leves e em memória, sendo suficientes para demonstrar o padrão e mantendo o sistema alinhado com a fase atual do projeto.

### 7.4. Benefícios arquiteturais

A aplicação do padrão Observer permite:
- reduzir o acoplamento entre a fachada e funcionalidades transversais;
- introduzir novos mecanismos de monitorização ou análise sem alterar os endpoints;
- reforçar a extensibilidade e legibilidade do código;
- tornar explícita a natureza orientada a eventos do Activity Provider.

O comportamento observável dos endpoints permanece inalterado, garantindo compatibilidade com a especificação Inven!RA.

## 8. Referências

GAMMA, E.; HELM, R.; JOHNSON, R.; VLISSIDES, J. **Design patterns: elements of reusable object-oriented software**. Reading: Addison-Wesley, 1995.

MORGADO, L.; CASSOLA, F. **Activity Providers na Inven!RA**. Lisboa: Universidade Aberta, 2022.

GRILO, R. et al. Assessment and tracking of learning activities on a remote computer networking laboratory using the Inven!RA architecture. *[S.l.]*, 2022.

CARDOSO, P.; MORGADO, L.; COELHO, A. Authoring game-based learning activities that are manageable by teachers. *[S.l.]*, 2020.

## 9. Autor
André Sousa – 1300012
Mestrado em Engenharia Informática e Tecnologia Web – Universidade Aberta
Unidade Curricular: Arquitetura e Padrões de Software
Ano letivo 2025/2026