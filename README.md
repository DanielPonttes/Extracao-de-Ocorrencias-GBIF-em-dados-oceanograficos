# Desafios-Estagiarios-Backend---SIAPESQ

# Ferramenta de Extração de Dados Oceanográficos

## 📌 Visão Geral
Ferramenta CLI que:
1. Extrai registros de ocorrências de espécies marinhas do GBIF
2. Obtém dados de temperatura e salinidade do Copernicus Marine Service
3. Gera relatórios em CSV para análise

## 🛠️ Pré-requisitos
- Python 3.10+
- Conta no [Copernicus Marine Service](https://marine.copernicus.eu/)
- Acesso à API do GBIF

## ⚙️ Instalação
```bash
git clone https://github.com/DanielPonttes/Desafios-Estagiarios-Backend---SIAPESQ.git
cd Desafios-Estagiarios-Backend---SIAPESQ
pip install -r requirements.txt
copernicusmarine login  # Siga as instruções para autenticação
