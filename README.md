# Dashboard ANS - Análise de Sinistros

## Sobre o Projeto
Este projeto é um dashboard para análise de sinistros de operadoras de saúde, desenvolvido principalmente com Python no backend e Vue.js no frontend. Como desenvolvedor com experiência em Python, o foco principal foi criar uma API robusta e eficiente para processamento dos dados.

## Principais Funcionalidades
- **Processamento de Dados** (Python/Pandas):
  - Análise de dados de sinistros por operadora
  - Cálculos automáticos de totais por período
  - Filtragem dos top 10 maiores valores

- **API REST** (Python/Flask):
  - Endpoints para consulta de dados anuais e trimestrais
  - Formatação automática de valores monetários
  - CORS habilitado para integração com frontend

- **Frontend** (Vue.js):
  - Dashboard interativo (implementado com auxílio da documentação Vue.js)
  - Visualização em cards e tabelas
  - Design responsivo com Tailwind CSS

## Stack Técnica
### Backend (Experiência Principal)
- Python 3.x
- Flask (Framework Web)
- Pandas (Análise de Dados)
- CSV para armazenamento

### Frontend (Aprendizado Durante o Projeto)
- Vue.js 3
- Tailwind CSS
- Componentes reativos

## Como Executar

### Backend (Python/Flask)
```bash
# Instalar dependências Python
pip install -r requirements.txt

# Executar a API Flask
cd dash
python api.py
```

### Frontend (Vue.js)
```bash
# Instalar dependências do Node.js
cd dash
npm install

# Iniciar servidor de desenvolvimento
npm run serve
```

## Estrutura do Projeto
```
caredemo/
├── banco_de_dados/     # Scripts Python para processamento
│   ├── executar_consulta_ano.py
│   └── executar_consulta_trimestre.py
├── dash/
│   ├── api.py          # API Flask
│   └── src/            # Frontend Vue.js
└── README.md
```

## Aprendizados
- Forte utilização de Pandas para manipulação de dados
- Desenvolvimento de API REST com Flask
- Introdução ao Vue.js e componentes reativos
- Integração entre Python e frontend moderno

## Próximos Passos
1. Implementar testes unitários com pytest
2. Adicionar mais visualizações de dados
3. Melhorar a documentação da API
4. Explorar mais recursos do Vue.js

## Autor
Romulo Lima - Desenvolvedor Python com interesse em frontend moderno
