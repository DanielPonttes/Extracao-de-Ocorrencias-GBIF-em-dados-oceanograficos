import argparse
import csv
import os
import numpy as np
from datetime import datetime
from copernicusmarine import open_dataset

# Comando para login!
# copernicusmarine.login(username='<your_username>', password='<your_password>')

def main():
    parser = argparse.ArgumentParser(
        description='Extrai dados de temperatura e salinidade do Copernicus Marine Service')
    parser.add_argument('--csv', required=True, help='Arquivo CSV de entrada')
    parser.add_argument('--out_csv', required=True, help='Arquivo CSV de saída')
    parser.add_argument('--depth', type=float, default=0.494, help='Profundidade em metros')
    args = parser.parse_args()

    # Verificar credenciais
    # if not check_credentials():
        # return

    points = read_input_csv(args.csv)
    if not points:
        print("Nenhum dado válido encontrado no arquivo de entrada.")
        return

    results = []
    for point in points:
        try:
            # Verificar campos obrigatórios
            if not all(key in point and point[key].strip() for key in ['year', 'month', 'day']):
                continue

            # Converter valores
            lon = float(point['decimalLongitude'])
            lat = float(point['decimalLatitude'])
            year = int(float(point['year']))
            month = int(float(point['month']))
            day = int(float(point['day']))

            date = datetime(year, month, day)

            # Obter dados
            thetao, so = get_marine_data(lon, lat, date, args.depth)

            results.append({
                'decimalLongitude': lon,
                'decimalLatitude': lat,
                'year': year,
                'month': month,
                'day': day,
                'thetao': thetao,
                'so': so
            })
            print(f"✅ Processado: {lon},{lat} - {date.date()} - θ: {thetao:.2f}°C, S: {so:.2f} PSU")

        except Exception as e:
            print(f"⚠️ Erro no ponto: {str(e)}")
            continue

    if results:
        save_results(results, args.out_csv)
        print(f"\n🎉 Dados salvos em: {os.path.abspath(args.out_csv)}")
    else:
        print("❌ Nenhum dado válido processado.")


def check_credentials():
    """Verifica se o login foi feito corretamente"""
    try:
        # Teste simples de conexão
        open_dataset(
            dataset_id="cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m",
            minimum_longitude=0,
            maximum_longitude=0.1,
            minimum_latitude=0,
            maximum_latitude=0.1,
            start_datetime="2024-01-01",
            end_datetime="2024-01-02"
        )
        return True
    except Exception as e:
        print(f"❌ Erro de autenticação: {str(e)}")
        print("Execute no terminal: copernicusmarine login")
        return False


def get_marine_data(longitude, latitude, date, depth):
    """Obtém dados ajustando automaticamente a profundidade"""
    try:
        date_str = date.strftime("%Y-%m-%d")

        # Primeiro verificamos as profundidades disponíveis
        ds_info = open_dataset(
            dataset_id="cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m",
            minimum_longitude=longitude,
            maximum_longitude=longitude,
            minimum_latitude=latitude,
            maximum_latitude=latitude,
            start_datetime=date_str,
            end_datetime=date_str,
            minimum_depth=0,
            maximum_depth=10,
            variables=["thetao"]
        )

        # Encontra a profundidade mais próxima disponível
        available_depths = ds_info.depth.values
        closest_depth = min(available_depths, key=lambda x: abs(x - depth))
        print(f"Usando profundidade mais próxima: {closest_depth}m (solicitado: {depth}m)")

        # Agora obtemos os dados com a profundidade ajustada
        ds_thetao = open_dataset(
            dataset_id="cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m",
            minimum_longitude=longitude,
            maximum_longitude=longitude,
            minimum_latitude=latitude,
            maximum_latitude=latitude,
            start_datetime=date_str,
            end_datetime=date_str,
            minimum_depth=closest_depth,
            maximum_depth=closest_depth
        )
        thetao = float(ds_thetao.thetao.values[0][0][0][0]) if hasattr(ds_thetao, 'thetao') else np.nan

        # Repetir para salinidade
        ds_so = open_dataset(
            dataset_id="cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m",
            minimum_longitude=longitude,
            maximum_longitude=longitude,
            minimum_latitude=latitude,
            maximum_latitude=latitude,
            start_datetime=date_str,
            end_datetime=date_str,
            minimum_depth=closest_depth,
            maximum_depth=closest_depth
        )
        so = float(ds_so.so.values[0][0][0][0]) if hasattr(ds_so, 'so') else np.nan

        return thetao, so

    except Exception as e:
        print(f"Erro na API para {longitude},{latitude}: {str(e)}")
        return np.nan, np.nan


def read_input_csv(filename):
    """Lê o arquivo CSV de entrada"""
    try:
        with open(filename, 'r') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        print(f"Erro ao ler CSV: {str(e)}")
        return None


def save_results(data, filename):
    """Salva os resultados em CSV"""
    try:
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'decimalLongitude', 'decimalLatitude', 'year', 'month', 'day', 'thetao', 'so'
            ])
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Erro ao salvar CSV: {str(e)}")
        return False


if __name__ == '__main__':
    main()
    
