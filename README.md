# S.O.R.O. - Sistema Organizacional para Registros de Ocorrências

Bem-vindo ao **S.O.R.O.**, um dashboard inteligente para análise, visualização e predição de ocorrências operacionais, desenvolvido para apoiar a tomada de decisão em serviços de emergência e salvamento.

## 📊 Visão Geral
O S.O.R.O. permite o acompanhamento detalhado de ocorrências como incêndios, salvamentos, colisões e outros eventos críticos, utilizando dados reais e técnicas de ciência de dados para gerar insights e recomendações.

---

## Funcionalidades
- **Dashboard Interativo:** Visualização de KPIs, gráficos dinâmicos e mapas de calor.
- **Filtros Avançados:** Selecione bairros, tipos de ocorrência e períodos para análises específicas.
- **Análise de Incêndios:** Ranking de causas, sazonalidade e recomendações automáticas.
- **Data Science & Machine Learning:**
  - Clusterização de ocorrências (K-Means)
  - Regressão e análise de fatores determinantes
  - Modelo preditivo para consumo de recursos
- **Monitoramento de Praias:** Análise de salvamentos, perfil de risco e alertas de tubarão.

---

## Como Executar
1. **Pré-requisitos:**
	- Python 3.8+
	- [Streamlit](https://streamlit.io/)
	- [Plotly](https://plotly.com/python/)
	- [scikit-learn](https://scikit-learn.org/)
	- [Pandas](https://pandas.pydata.org/)

2. **Instale as dependências:**
	```bash
	pip install -r requirements.txt
	```

3. **Execute o dashboard:**
	```bash
	streamlit run app.py
	```

4. **Acesse no navegador:**
	- O Streamlit irá exibir um link local (ex: http://localhost:8501)

---

## Estrutura dos Dados
O arquivo `dados_soro.csv` contém os registros das ocorrências, com campos como:
- `data_hora`: Data e hora do evento
- `tipo_ocorrencia`: Salvamento, Incêndio, Colisão, etc.
- `subtipo_ocorrencia`: Detalhamento do tipo
- `bairro`, `latitude`, `longitude`: Localização
- `qtd_total_vitimas`, `vitimas_fatais`: Vítimas envolvidas
- `tempo_resposta`: Tempo de resposta (minutos)
- `gravidade`: Classificação do evento
- `incendio_grupo`, `incendio_consumo_agua`, `usou_hidrante`: Dados específicos de incêndio

---

## Visualizações Disponíveis
- **Gráficos de Rosca e Boxplot:** Distribuição por tipo e tempo de resposta
- **Mapa de Calor:** Localização espacial das ocorrências
- **Linha do Tempo:** Evolução temporal dos casos
- **Ranking de Causas:** Principais causas de incêndio
- **Clusterização e Regressão:** Grupos e tendências de consumo de recursos
- **Alertas e Recomendações:** Sistema inteligente de avisos

---


## Créditos
Desenvolvido por alunos da turma de TADS 044:

**Arthur Silveira, Maíra Lourenço, Manoel Olímpio, Matheus Willian, Victor Gomes e Victoria Zambom**

Projeto acadêmico para fins de estudo e demonstração de técnicas de análise de dados aplicadas à segurança pública.

---

## Licença
Este projeto é distribuído sob a licença MIT. Sinta-se livre para usar, modificar e compartilhar!