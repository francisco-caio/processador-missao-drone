"""
PROJETO: Processador de Dados de Drone
O que a GeoScan recebe fotos + coordenadas, processa, gera relatório
"""

import csv
import json
from datetime import datetime

class ProcessadorMissao:
    def __init__(self, nome_missao):
        # Inicializa a missão com um nome e estrutura de dados para voos
        self.nome_missao = nome_missao
        self.voos = []
        self.fotos_processadas = 0

    def adicionar_voo(self, id_voo, lat, lng, alt, fotos, data):
        """Registra um voo de drone"""
        voo = {
            "id": id_voo,
            "latitude": lat,
            "longitude": lng,
            "altitude": alt,
            "fotos": fotos,
            "data": data,
            "processado_em": datetime.now().isoformat()
        }
        self.voos.append(voo)
        self.fotos_processadas += fotos
        print(f" Voo {id_voo} registrado: {fotos} fotos @ {alt}m")

    def estatisticas(self):
        """Calcula estatísticas da missão"""
        if not self.voos:
            return {}

        altitudes = [v["altitude"] for v in self.voos]
        total_fotos = sum(v["fotos"] for v in self.voos)

        # Área estimada cada voo cobre ~100m x 100m = 10.000m²
        area_total = len(self.voos) * 10000

        return {
            "missao": self.nome_missao,
            "total_voos": len(self.voos),
            "total_fotos": total_fotos,
            "altitude_media": round(sum(altitudes) / len(altitudes), 2),
            "altitude_max": max(altitudes),
            "altitude_min": min(altitudes),
            "area_mapeada_m2": area_total,
            "area_mapeada_hectares": round(area_total / 10000, 2),
            "eficiencia_fotos_por_voo": round(total_fotos / len(self.voos), 1)
        }

    def gerar_csv(self):
        """Gera relatório CSV para análise"""
        data_hoje = datetime.now().strftime('%Y%m%d')
        nome_arquivo = f"relatorio_{self.nome_missao}_{data_hoje}.csv"

        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(["Missao", "ID_Voo", "Latitude", "Longitude",
                               "Altitude", "Fotos", "Data", "Area_m2"])

            for voo in self.voos:
                escritor.writerow([
                    self.nome_missao,
                    voo["id"],
                    voo["latitude"],
                    voo["longitude"],
                    voo["altitude"],
                    voo["fotos"],
                    voo["data"],
                    10000
                ])

        print(f"CSV gerado: {nome_arquivo}")
        return nome_arquivo

    def gerar_json(self):
        """Gera relatório JSON para integração"""
        dados_stats = self.estatisticas() 
        nome_arquivo = f"resumo_{self.nome_missao}.json"

        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_stats, f, indent=2, ensure_ascii=False)

        print(f"JSON gerado: {nome_arquivo}")
        return nome_arquivo

    def resumo_executivo(self):
        """Gera texto resumido para relatório rápido"""
        resumo_stats = self.estatisticas()

        texto = f"""
        RELATÓRIO DE MISSÃO: {resumo_stats['missao']}
        

        Resumo da Operação:
        • Total de voos: {resumo_stats['total_voos']}
        • Fotos capturadas: {resumo_stats['total_fotos']}
        • Área mapeada: {resumo_stats['area_mapeada_hectares']} hectares
        • Altitude média: {resumo_stats['altitude_media']}m

        Eficiência: {resumo_stats['eficiencia_fotos_por_voo']} fotos/voo

        Status: MISSÃO CONCLUÍDA
        Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """

        nome_arquivo = f"executivo_{self.nome_missao}.txt"
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(texto)

        print(f"Resumo executivo: {nome_arquivo}")
        return texto


# agora aqui vamos ver como todos esses métodos funcionam na prática, simulando uma missão real de drone
if __name__ == "__main__":
    print("INICIANDO PROCESSAMENTO DE MISSÃO")
    print("=" * 50)

    missao = ProcessadorMissao("Mapeamento_Soja_Pecem_2026")

    missao.adicionar_voo("V001", -3.71722, -38.54337, 120, 250, "2026-05-08")
    missao.adicionar_voo("V002", -3.71800, -38.54400, 115, 230, "2026-05-08")
    missao.adicionar_voo("V003", -3.71900, -38.54500, 125, 280, "2026-05-08")

    print("\n ESTATÍSTICAS:")
    final_stats = missao.estatisticas()
    for chave, valor in final_stats.items():
        print(f"   {chave}: {valor}")

    print("\n GERANDO RELATÓRIOS:")
    missao.gerar_csv()
    missao.gerar_json()
    missao.resumo_executivo()

    print("\n" + "=" * 50)
    print("MISSÃO PROCESSADA COM SUCESSO!")
    print("=" * 50)
