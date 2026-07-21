"""
PROJETO: Processador de Dados de Drone
O que a GeoScan recebe fotos + coordenadas, processa, gera relatório
"""
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import csv
import json
from datetime import datetime

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

class ProcessadorMissao:
    def __init__(self, nome_missao):
        # Inicializa a missão com um nome e estrutura de dados para voos
        self.nome_missao = nome_missao
        self.voos = []
        self.fotos_processadas = 0

    def adicionar_voo(self, id_voo, lat, lng, alt, fotos, data):
        #Registra um voo de drone
        if fotos < 0:
            raise ValueError("Número de fotos não pode ser negativo.")    
        if alt < 0:
            raise ValueError("Altitude não pode ser negativa.")
        if lat  < -90 or lat > 90:
            raise ValueError("a latitude tem que estar entre -90 e 90 graus.")
        if lng < -180 or lng > 180:
            raise ValueError("a longitude tem que estar entre -180 e 180 graus.")
        
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
        #Calcula estatísticas da missão
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
        #Gera relatório CSV para análise
        data_hoje = datetime.now().strftime('%Y%m%d')
        nome_arquivo = f"relatorio_{self.nome_missao}_{data_hoje}.csv"
        nome_pasta = os.getenv("PASTA_RELATORIOS", "relatorios")
        if not os.path.exists(nome_pasta):
            os.makedirs(nome_pasta)
        caminho=os.path.join(nome_pasta,nome_arquivo) 



        with open(caminho, 'w', newline='', encoding='utf-8') as f:
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
        return caminho

    def gerar_json(self):
        #Gera relatório JSON para integração
        dados_stats = self.estatisticas() 
        nome_arquivo = f"resumo_{self.nome_missao}.json"
        #lendo a pasta de relatorios da env e criando essa pasta caso nao exista e 
        #salvando o arquivo json dentro dela
        nome_pasta = os.getenv("PASTA_RELATORIOS", "relatorios")
        if not os.path.exists(nome_pasta):
            os.makedirs(nome_pasta)
        caminho = os.path.join(nome_pasta, nome_arquivo)

        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados_stats, f, indent=2, ensure_ascii=False)

        print(f"JSON gerado: {nome_arquivo}")
        return caminho

    def resumo_executivo(self):
        #Gera texto resumido para relatório rápido
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
        nome_pasta = os.getenv("PASTA_RELATORIOS", "relatorios")
        if not os.path.exists(nome_pasta):
            os.makedirs(nome_pasta)
        caminho = os.path.join(nome_pasta, nome_arquivo)


        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(texto)

        print(f"Resumo executivo: {nome_arquivo}")
        return caminho
    
    def enviar_email(self, assunto, corpo,para,anexos=None):
        remetente =  os.getenv("EMAIL_USER")
        senha = os.getenv("EMAIL_PASSWORD")

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = para
        msg['Subject'] = assunto 
        msg.attach(MIMEText(corpo, 'plain')) 
        for caminho_arquivo in anexos :
            with open(caminho_arquivo, 'rb') as f:
                anexo_mime = MIMEBase('application', 'octet-stream')
                anexo_mime.set_payload(f.read())
                encoders.encode_base64(anexo_mime)
                nome_arquivo = os.path.basename(caminho_arquivo)
                anexo_mime.add_header('content-disposition', f'attachment; filename={nome_arquivo}')
                msg.attach(anexo_mime)
        try:
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
            servidor.quit()
            print(f"Email enviado para: {para}")
        except smtplib.SMTPAuthenticationError:
            print("Erro de autenticação: Verifique suas credenciais de email.")    
        except smtplib.SMTPException as e:
            print(f"Erro ao enviar email: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

# agora aqui vamos ver como todos esses métodos funcionam na prática, simulando uma missão real de drone
if __name__ == "__main__":
    print("INICIANDO PROCESSAMENTO DE MISSÃO")
    print("=" * 50)

    missao = ProcessadorMissao("Mapeamento_Soja_Pecem_2026")

    missao.adicionar_voo("V001", -3.71722, -38.54337, 120, 45, "2026-05-08")
    missao.adicionar_voo("V002", -3.71800, -38.54400, 115, 230, "2026-05-08")
    missao.adicionar_voo("V003", -3.71900, -38.54500, 125, 280, "2026-05-08")

    print("\n ESTATÍSTICAS:")
    final_stats = missao.estatisticas()
    for chave, valor in final_stats.items():
        print(f"   {chave}: {valor}")


    caminho_csv = missao.gerar_csv()
    caminho_json = missao.gerar_json()  
    caminho_txt = missao.resumo_executivo()

     
    missao.enviar_email (
        assunto='Relatório de Missão - Mapeamento Soja Pecém 2026',
        corpo=' Missão concluída com sucesso! Futuramente Relatórios em anexo.',
        para='kayo.mello1488@gmail.com',
        anexos=[caminho_csv, caminho_json, caminho_txt]
    ) 

    print("\n" + "=" * 50)
    print("MISSÃO PROCESSADA COM SUCESSO!")
    print("=" * 50)
