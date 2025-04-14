import argparse
import csv  # Gerar arquivo de saída
import os  # Salva o arquivo .csv no dispositivo
from pygbif import occurrences as occ  # Não ter de necessidade de acessar a API via link

# Comandos: Ações principais que o programa executa

# Argumentos: Valores necessários para os comandos

# Opções/Flags: Modificadores que alteram o comportamento dos comandos

# Saída: Resultados exibidos no terminal


def main():
    # Definindo o parser
    parser = argparse.ArgumentParser(description='Ferramenta CLI que utilize o GBIF para extrair registros de '
                                                 'ocorrências de uma especie marinha informada com base no bounding '
                                                 'box e no período de tempo informado')
    parser.add_argument('--specie', required=True,
                        help='Nome científico da espécie')
    parser.add_argument('--bbox', nargs=4, type=float, required=True,
                        help='Bounding box: minLong minLat maxLong maxLat')
    parser.add_argument('--limit', type=int, default=100,
                        help='Número máximo de registros (default: 100)')
    parser.add_argument('--begin_date',
                        help='Data inicial no formato YYYY-MM-DD ')
    parser.add_argument('--end_date',
                        help='Data final no formato YYYY-MM-DD')
    parser.add_argument('--out_csv', required=True,
                        help='Caminho do arquivo CSV de saída')
    args = parser.parse_args()

    # Verificando as datas
    if args.begin_date and not args.end_date:
        parser.error("--end_date requer --begin_date")
    if args.end_date and not args.begin_date:
        parser.error("--begin_date requer --end_date")

    # Verificar ordem das coordenadas
    min_long, min_lat, max_long, max_lat = args.bbox
    if not (-180 <= min_long <= 180) or not (-180 <= max_long <= 180):
        parser.error("Longitudes devem estar entre -180 e 180")
    if not (-90 <= min_lat <= 90) or not (-90 <= max_lat <= 90):
        parser.error("Latitudes devem estar entre -90 e 90")

    # Construir parâmetros e fazer a consulta
    base_url, params = api_builder(args)  # Nota: base_url não está sendo usado com pygbif
    occurrences = fetch_occurrences(params)
    args.out_csv = os.path.join(os.path.expanduser('~'), 'Downloads', 'dados.csv')
    if occurrences:
        processed_data = process_results(occurrences)
        save_to_csv(processed_data, args.out_csv)


def api_builder(args):
    min_long, min_lat, max_long, max_lat = args.bbox
    base_url = "https://api.gbif.org/v1/"
    params = {
        'scientificName': args.specie,
        'limit': args.limit,
        'geometry': f"POLYGON(({min_long} {min_lat}, {max_long} {min_lat}, {max_long} {max_lat}, "
                    f"{min_long} {max_lat}, {min_long} {min_lat}))"
    }
    if args.begin_date and args.end_date:
        params['eventDate'] = f"{args.begin_date},{args.end_date}"
    return base_url, params


def fetch_occurrences(params):
    """Faz a consulta à API GBIF usando os parâmetros construídos"""
    try:
        # Usando a biblioteca pygbif para buscar ocorrências nos dados
        result = occ.search(**params)

        if not result['results']:
            print("Nenhum registro encontrado com os critérios fornecidos.")
            return None

        return result['results']

    # Tratamento de exceção ao consultar a API
    except Exception as e:
        print(f"Erro ao consultar a API GBIF: {str(e)}")
        return None


# Processa todos os resultados
def process_results(occurrences):
    processed = []
    for record in occurrences:
        processed.append({
            'decimalLongitude': record.get('decimalLongitude'),
            'decimalLatitude': record.get('decimalLatitude'),
            'year': record.get('year'),
            'month': record.get('month'),
            'day': record.get('day')
        })
    return processed


def save_to_csv(data, filename):
    """Salva os dados processados em um arquivo CSV formatado corretamente"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['decimalLongitude', 'decimalLatitude', 'year', 'month', 'day']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

            writer.writeheader()
            for row in data:
                # Filtra e garante que todos os campos necessários existam
                if all(key in row and row[key] is not None for key in fieldnames):
                    writer.writerow({
                        'decimalLongitude': row['decimalLongitude'],
                        'decimalLatitude': row['decimalLatitude'],
                        'year': row['year'],
                        'month': row['month'],
                        'day': row['day']
                    })

        print(f"Dados salvos com sucesso em {filename}")
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {str(e)}")
        return False


if __name__ == '__main__':
    main()
