# 📅 Sistema de Agendamento e Gerenciamento de Clientes

### Aplicação Web Full Stack | Python • Flask • SQLite

Sistema web desenvolvido para facilitar o gerenciamento de clientes e agendamentos, oferecendo uma solução digital para profissionais autônomos, clínicas e pequenas empresas que precisam organizar seus atendimentos.

A aplicação integra autenticação de usuários, cadastro de clientes, gerenciamento de compromissos, calendário, pesquisa de registros e funcionalidades de suporte, utilizando uma interface responsiva.

🔗 **[Acessar aplicação online](https://agenda-5p0a.onrender.com/login)**

---

## 🎯 Objetivo do projeto

Desenvolver uma aplicação web para centralizar o cadastro de clientes e a organização de agendamentos, simplificando processos administrativos e facilitando o acompanhamento dos atendimentos.

O projeto utiliza Python e Flask no backend, SQLite para persistência dos dados e tecnologias web para construção da interface.

## 🚀 Funcionalidades

### 🔐 Autenticação de usuários
- Cadastro de novos usuários.
- Login e logout.
- Proteção de senhas utilizando hash.
- Gerenciamento de sessões.
- Recuperação de senha por e-mail.

### 👥 Gerenciamento de clientes
- Cadastro de clientes.
- Edição e exclusão de registros.
- Armazenamento de nome, e-mail e telefone.
- Campo para observações.
- Listagem individualizada por usuário.

### 📆 Gerenciamento de agendamentos
- Criação de agendamentos por data e horário.
- Associação de agendamentos a clientes cadastrados.
- Edição e exclusão de compromissos.
- Listagem organizada por data e horário.
- Consulta de eventos para integração com calendário.

### 🔎 Pesquisa e navegação
- Busca de clientes cadastrados.
- Pesquisa de agendamentos por título e descrição.
- Acesso às funcionalidades administrativas.

### 📩 Suporte
- Formulário de contato.
- Envio de solicitações por e-mail.
- Página de treinamento para usuários.

## 🛠️ Tecnologias utilizadas

| Categoria | Tecnologias |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Interface | Bootstrap 5 |
| Banco de dados | SQLite |
| Templates | Jinja2 |
| Autenticação | Werkzeug |
| E-mail | Flask-Mail |
| Deploy | Gunicorn |

## 🗄️ Banco de dados

O sistema utiliza SQLite para armazenar e organizar os dados.

**Principais tabelas:**

**Usuários (`usuarios`)**
- Identificador do usuário.
- Nome e e-mail.
- Hash da senha.
- Token de recuperação de senha.

**Clientes (`clientes`)**
- Identificador do cliente.
- Identificação do usuário responsável.
- Nome, e-mail e telefone.
- Observações.

**Agendamentos (`agendamentos`)**
- Identificador do agendamento.
- Identificação do usuário e do cliente.
- Título do compromisso.
- Data e horário.
- Descrição.

## 🧠 Competências técnicas demonstradas

O desenvolvimento deste projeto envolve:

- Desenvolvimento web Full Stack.
- Implementação de rotas com Flask.
- Operações CRUD com banco de dados SQLite.
- Consultas SQL com filtros e relacionamentos.
- Gerenciamento de autenticação e sessões.
- Integração entre frontend e backend.
- Manipulação de formulários e requisições HTTP.
- Desenvolvimento de interfaces responsivas.
- Criação de endpoints com respostas JSON.
- Integração com serviços de e-mail.

## 🌐 Demonstração

Acesse a aplicação:

**[Sistema de Agendamento Online](https://agenda-5p0a.onrender.com/login)**

## 👩‍💻 Desenvolvedora

**Carine Lima**

Estudante de Engenharia de Software | Desenvolvedora Full Stack

Desenvolvendo soluções digitais com foco em funcionalidade, organização e experiência do usuário.

**GitHub:** [github.com/CarineLimma](https://github.com/CarineLimma)

**Portfólio:** [carinelimadev.netlify.app](https://carinelimadev.netlify.app)

---

⭐ Se você gostou deste projeto, considere deixar uma estrela no repositório!
