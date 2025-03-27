# Dashboard ANS

Dashboard para visualização de dados de sinistros das operadoras de saúde.

## Estrutura do Projeto

```
caredemo/
├── banco_de_dados/     # Scripts de processamento de dados
├── dash/              # Frontend Vue.js e API Flask
│   ├── src/          # Código fonte Vue.js
│   └── api.py        # API Flask
```

## Tecnologias Utilizadas

- Backend:
  - Python 3.x
  - Flask
  - Pandas

- Frontend:
  - Vue.js 3
  - Tailwind CSS

## Como Executar

1. Backend (API Flask):
```bash
cd dash
python api.py
```

2. Frontend (Vue.js):
```bash
cd dash
npm install
npm run serve
```

O frontend estará disponível em `http://localhost:8085` e a API em `http://localhost:5000`.

## Funcionalidades

- Visualização dos 10 maiores sinistros por operadora em 2024
- Visualização dos maiores sinistros por operadora no último trimestre
- Cálculo automático dos totais
- Interface responsiva e moderna
