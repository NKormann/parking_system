# PARKING SYSTEM

## Descrição

**PARKING SYSTEM** é uma aplicação web de gerenciamento de estacionamento, desenvolvida com Django (Backend) e Vue.js + Vuetify (Frontend). A aplicação permite registrar veículos, controlar entradas e saídas, gerenciar clientes, planos mensais e contratos de estacionamento para clientes rotativos e mensalistas.

A aplicação foi projetada para facilitar o controle de veículos em um estacionamento, aplicando regras de negócios específicas, como a diferenciação entre clientes rotativos (pagamento por tempo de uso) e clientes mensalistas (pagamento recorrente com isenção de cobrança por cada entrada e saída).

A **documentação completa da API** está disponível em:  
**[http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)**.

## Funcionalidades Principais

- **Cadastro de Clientes**: Registre clientes com nome e cartão de identificação (CARD_ID).
- **Cadastro de Veículos**: Adicione veículos vinculados a clientes ou veículos rotativos sem vínculo de cliente.
- **Gestão de Planos**: Administre planos de clientes, como planos mensais com data de vencimento.
- **Gestão de Contratos**: Defina regras de contratos para clientes rotativos (por exemplo, cobrança por minutos de uso).
- **Controle de Movimentos de Estacionamento**: Registre entradas e saídas de veículos no estacionamento e aplique as cobranças adequadas conforme as regras do contrato.
- **Relatórios de Movimentação**: Monitore todas as movimentações de veículos e os valores cobrados ou isentos.

## Tecnologias Utilizadas

- **Backend**: Django (Django REST Framework)
- **Frontend**: Vue.js, Vuetify
- **Banco de Dados**: SQLite (pode ser facilmente substituído por PostgreSQL, MySQL, etc.)
- **API REST**: Django REST Framework para comunicação entre o frontend e o backend

---

## Índice

1. [Instalação](#instalação)
2. [Configuração do Backend](#configuração-do-backend)
3. [Configuração do Frontend](#configuração-do-frontend)
4. [Executando a Aplicação](#executando-a-aplicação)
5. [Regras de Negócio](#regras-de-negócio)
6. [APIs](#apis)
7. [Contribuindo](#contribuindo)
8. [Licença](#licença)

---

## Instalação

### Pré-requisitos

- Python 3.8+ (para o backend)
- Node.js e npm (para o frontend)
- Git

### Clonando o Repositório

Primeiro, clone o repositório para a sua máquina local:

```bash
git clone https://github.com/seu-usuario/parking-system.git
cd parking-system
```

---

## Configuração do Backend

1. **Crie um ambiente virtual e ative-o**:

```bash
python -m venv venv
source venv/bin/activate  # no Windows, use venv\Scripts\activate
```

2. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados**:

Execute as migrações para criar as tabelas do banco de dados:

```bash
python manage.py migrate
```

4. **Crie um superusuário (para acessar o Django Admin)**:

```bash
python manage.py createsuperuser
```

5. **Carregar dados iniciais (opcional)**:

Se você tiver um arquivo de fixtures para dados de exemplo, pode carregá-lo usando:

```bash
python manage.py loaddata data.json
```

---

## Configuração do Frontend

1. **Instale as dependências do Vue.js**:

No diretório `frontend`, instale as dependências usando npm:

```bash
cd frontend
npm install
```

2. **Iniciar o servidor de desenvolvimento**:

```bash
npm run serve
```

---

## Executando a Aplicação

1. **Iniciar o servidor do Django (Backend)**:

```bash
python manage.py runserver
```

Isso irá iniciar o backend na URL: `http://localhost:8000/`

2. **Iniciar o servidor do Vue.js (Frontend)**:

```bash
npm run serve
```

Isso irá iniciar o frontend na URL: `http://localhost:8080/`

Agora você pode acessar a aplicação completa no navegador.

---

## Regras de Negócio

A aplicação PARKING SYSTEM segue as seguintes regras de negócios:

1. **Clientes Mensalistas**:
   - São clientes que possuem planos vinculados. Não são cobrados por entrada e saída.
   - Sempre que houver um movimento de entrada ou saída de um mensalista, o valor deve ser "Mensalista" e não 0.0.

2. **Clientes Rotativos**:
   - São clientes que não possuem um plano mensal. A cobrança é feita com base nas regras de contratos configuradas.
   - O sistema deve permitir a configuração de contratos e suas regras de cobrança baseadas em minutos.

3. **Movimentação de Veículos**:
   - Entrada e saída de veículos podem ser registradas usando a **placa** do veículo ou o **CARD_ID** do cliente.
   - Para clientes rotativos, o sistema deve calcular o valor com base nas regras do contrato.
   - Tentativas de entrada de veículos que já estão no estacionamento devem ser bloqueadas.

4. **Cadastro de Veículos**:
   - Veículos rotativos podem ser cadastrados sem vínculo com um cliente.
   - Ao tentar cadastrar um veículo com uma placa já existente para outro cliente, o cadastro deve ser bloqueado.

---

## APIs

A aplicação utiliza **Django REST Framework** para fornecer APIs que permitem a comunicação entre o frontend e o backend. Aqui estão algumas das principais APIs:

- **GET /api/v1/customer/** - Listar todos os clientes.
- **POST /api/v1/customer/** - Criar um novo cliente.
- **GET /api/v1/vehicle/** - Listar todos os veículos.
- **POST /api/v1/vehicle/** - Criar um novo veículo.
- **GET /api/v1/plan/** - Listar todos os planos.
- **POST /api/v1/plan/** - Criar um novo plano.
- **GET /api/v1/parkmovement/** - Listar todos os movimentos de estacionamento.
- **POST /api/v1/parkmovement/** - Criar um novo movimento de entrada.
- **POST /api/v1/parkmovement/<id>/exit/** - Registrar a saída de um veículo.

A documentação completa da API pode ser acessada em:
**[http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)**.

Essas APIs seguem o padrão REST e são acessíveis via requisições HTTP.
