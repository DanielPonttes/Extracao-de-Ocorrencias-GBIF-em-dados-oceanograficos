
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

```

## 🚀 Como Usar

### Parte 1: Extração de Ocorrências (GBIF)

```bash
python gbifer.py --specie "Thunnus obesus" --bbox -180 -90 180 90 --limit 500 --begin_date 2020-01-01 --end_date 2024-01-01 --out_csv ocorrencias.csv

```

### Parte 2: Extração de Dados Oceanográficos

```bash
python dmarine.py --csv ocorrencias.csv --out_csv dados_oceanograficos.csv --depth 0.5
```


## 📊 Saída Esperada

Arquivo CSV contendo:
```
decimalLongitude,decimalLatitude,year,month,day,thetao,so
-45.12,12.45,2022,5,15,25.3,36.7
-46.78,13.01,2022,5,16,24.8,36.5
```

## ⚠️ Limitações

* Algumas localizações podem retornar dados faltantes (NaN)
* Datas anteriores a 1993 podem ter cobertura limitada

## 🤝 Contribuição

1. Faça um fork do projeto

2. Crie sua branch (git checkout -b feature/nova-funcionalidade)

3. Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')

4. Push para a branch (git push origin feature/nova-funcionalidade)

5. Abra um Pull Request
