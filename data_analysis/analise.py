import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcular_tc(tp1, tp2, tt):
    """Calcula o tempo de comunicação com base nos tempos de processamento e no tempo total."""
    return (tt - 2 * (tp1 + tp2)) / 2

def calcular_medias_desvios(dados):
    """Calcula a média e o desvio padrão dos dados fornecidos."""
    media = dados.mean()
    desvio_padrao = dados.std()
    return media, desvio_padrao

# Carregar os dados dos arquivos CSV
tp1_data = pd.read_csv('data1.csv')
tp2_data = pd.read_csv('data2.csv')
tt_data = pd.read_csv('data_tt.csv')

# Verificar se todas as tabelas têm o mesmo número de medições
assert len(tp1_data) == len(tp2_data) == len(tt_data), "Os arquivos CSV devem ter o mesmo número de linhas"

# Calcular o tempo de comunicação
tc_data = calcular_tc(tp1_data['Time (ns)'], tp2_data['Time (ns)'], tt_data['Time (ns)'])

# Calcular médias e desvios padrões
media_tp1, desvio_tp1 = calcular_medias_desvios(tp1_data['Time (ns)'])
media_tp2, desvio_tp2 = calcular_medias_desvios(tp2_data['Time (ns)'])
media_tc, desvio_tc = calcular_medias_desvios(tc_data)

# Criar gráficos
plt.figure(figsize=(10, 8))

# Gráfico para Tp1
plt.subplot(3, 1, 1)
plt.plot(tp1_data['Time (ns)'], label='Tp1')
plt.axhline(media_tp1, color='r', linestyle='--', label=f'Média: {media_tp1:.2f}')
plt.fill_between(range(len(tp1_data)), media_tp1 - desvio_tp1, media_tp1 + desvio_tp1, color='r', alpha=0.2, label=f'Desvio Padrão: {desvio_tp1:.2f}')
plt.title('Tempo de Processamento Tp1')
plt.xlabel('Amostras')
plt.ylabel('Tempo (s)')
plt.legend()

# Gráfico para Tp2
plt.subplot(3, 1, 2)
plt.plot(tp2_data['Time (ns)'], label='Tp2')
plt.axhline(media_tp2, color='g', linestyle='--', label=f'Média: {media_tp2:.2f}')
plt.fill_between(range(len(tp2_data)), media_tp2 - desvio_tp2, media_tp2 + desvio_tp2, color='g', alpha=0.2, label=f'Desvio Padrão: {desvio_tp2:.2f}')
plt.title('Tempo de Processamento Tp2')
plt.xlabel('Amostras')
plt.ylabel('Tempo (s)')
plt.legend()

# Gráfico para Tc
plt.subplot(3, 1, 3)
plt.plot(tc_data, label='Tc')
plt.axhline(media_tc, color='b', linestyle='--', label=f'Média: {media_tc:.2f}')
plt.fill_between(range(len(tc_data)), media_tc - desvio_tc, media_tc + desvio_tc, color='b', alpha=0.2, label=f'Desvio Padrão: {desvio_tc:.2f}')
plt.title('Tempo de Comunicação Tc')
plt.xlabel('Amostras')
plt.ylabel('Tempo (s)')
plt.legend()

# Ajustar layout dos gráficos
plt.tight_layout()

# Salvar os gráficos em um arquivo
plt.savefig('tempos_de_processamento_e_comunicacao.png')

plt.show()
aa
