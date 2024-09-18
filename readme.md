# Library Management

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Create Docker Network](#create-docker-network)
  - [Start RabbitMq Service](#start-rabbitmq-service)
  - [Setting Up frontend](#setting-up-frontend)
  - [Setting Up backend](#setting-up-backend)
  
- [Contributing](#contributing)
- [License](#license)


## Introduction
 The Library Management is an application built with <a href="https://www.django-rest-framework.org/">Django Rest Framework</a>. The system is composed of two independent API services: a frontend and a backend. These services communicate with each other via RabbitMQ, which acts as a message broker to ensure efficient and reliable data exchange between them.
 The architecture is designed to be scalable and modular, allowing the frontend and backend services to operate independently while maintaining seamless interaction through RabbitMQ.
    <br/>
 <a href="https://www.rabbitmq.com/">RabbitMQ </a> is an open-source message broker software that facilitates communication between applications through a messaging queue system. It enables efficient data transmission by allowing services to send and receive messages asynchronously, ensuring reliable message delivery, load balancing, and fault tolerance. By decoupling services, RabbitMQ improves scalability and helps manage high-throughput data processing in distributed systems


Technologies used

- Backend: Python & Django Rest Framework (DRF)
- Database: PostgreSQL
- REST API documentation: Swagger UI(drf-spectacular)
- Testing: Django's built-in test framework (APITestCase, APIClient)
- Containerization - Docker
- Message Queuing: RabbitMQ

## Getting Started

To run this web application on your local machine, follow the steps below:

### Prerequisites

Before getting started, ensure that you have the following software installed on your machine:

- Python: Download and install Python from the official website: https://www.python.org/downloads/
- GIT: Download and install GIT from the official website: https://git-scm.com/downloads
- Docker: 
  - For Windows or macOS, download and install Docker Desktop from the official website: https://www.docker.com/products/docker-desktop/
  - On Linux, you can install Docker Engine directly using your package manager without needing Docker Desktop. [Follow the official Docker Engine installation instructions.](https://docs.docker.com/engine/install/)


### Installation

Step-by-step guide on how to install the project and its dependencies.

1. Clone the repository to your local machine using Git: <br>
HTTPS

```bash
git clone https://github.com/bosukeme/library-managment.git
```

SSH
```bash
git clone git@github.com:bosukeme/library-managment.git
```

<br>

2. Navigate to the project directory

```bash
cd library-managment
```

### Create Docker Network

```bash
    docker network create --driver bridge shared-network
```

### Start RabbitMq Service

```bash
    docker-compose -f docker-compose-rabbitmq.yaml up --build
```

Once this successfully starts up. Proceed to setting up the frontend service and the backend service 

### Setting Up frontend:

Follow the link : ...

### Setting Up backend:

Follow the link : ...


## Contributing
If you would like to contribute, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bugfix.
- Submit a pull request.


## Authors

Ukeme Wilson
- <a href="https://www.linkedin.com/in/ukeme-wilson-4825a383/">Linkedin</a>.
- <a href="https://medium.com/@ukemeboswilson">Medium</a>.
- <a href="https://www.ukemewilson.sbs/">Website</a>.

