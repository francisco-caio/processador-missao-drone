# 🚁 Processador de Missão de Drones

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-Relat%C3%B3rios-000000?style=for-the-badge&logo=json&logoColor=white)

Sistema em Python para processamento de telemetria de missões de mapeamento aéreo com drones.

O projeto simula o fluxo de uma operação de campo, registrando voos, coordenadas, altitude, quantidade de fotos capturadas e gerando relatórios em diferentes formatos para análise técnica e executiva.

## 📌 Sobre o Projeto

O **Processador de Missão de Drones** foi desenvolvido para organizar dados básicos de uma missão aérea e transformar essas informações em estatísticas e relatórios úteis.

A aplicação utiliza **Programação Orientada a Objetos (POO)** por meio da classe `ProcessadorMissao`, responsável por centralizar os dados da missão, registrar voos, calcular estatísticas e gerar arquivos de saída.

## ⚙️ Funcionalidades

- Registro de voos com ID, latitude, longitude, altitude, quantidade de fotos e data.
- Cálculo automático da área mapeada em metros quadrados (`m²`).
- Conversão da área mapeada para hectares.
- Cálculo de estatísticas de altitude:
  - altitude média;
  - altitude máxima;
  - altitude mínima.
- Cálculo de eficiência em fotos por voo.
- Geração de relatórios em:
  - CSV;
  - JSON;
  - TXT com resumo executivo.

## 🧠 Conceitos Aplicados

- Programação Orientada a Objetos (POO).
- Manipulação de arquivos com Python.
- Geração de relatórios estruturados.
- Serialização de dados em JSON.
- Escrita de arquivos CSV.
- Cálculo de estatísticas básicas.

## 📁 Estrutura do Projeto

```text
automacao-drones-dados/
├── processador_drone.py
├── README.md
├── .gitignore
├── relatorio_Mapeamento_Soja_Pecem_2026_20260513.csv
├── resumo_Mapeamento_Soja_Pecem_2026.json
└── executivo_Mapeamento_Soja_Pecem_2026.txt
```

## ▶️ Como Executar

No terminal, execute:

```bash
python processador_drone.py
```

Ao final da execução, o sistema gera os relatórios da missão nos formatos CSV, JSON e TXT.

## 📊 Exemplo de Saída

```text
total_voos: 3
total_fotos: 760
altitude_media: 120.0
area_mapeada_m2: 30000
area_mapeada_hectares: 3.0
eficiencia_fotos_por_voo: 253.3
```

## 🗺️ Roadmap / Próximos Passos

- [x] Organização automática dos relatórios em pastas dinâmicas via variáveis de ambiente.
- [x] Disparo automático de e-mails com os arquivos gerados em anexo.
- [ ] Implementação de tratamento de exceções (Try/Except) robusto para entradas de dados inválidas.
- [ ] Integração com banco de dados (SQLite/PostgreSQL) para persistir o histórico das missões.
- [ ] Criação de testes unitários para validar os cálculos estatísticos automaticamente.

## 🛠️ Tecnologias

```text
Python
CSV
JSON
Programação Orientada a Objetos
```

## 📄 Licença

Este projeto está disponível para fins de estudo, prática e evolução profissional.
