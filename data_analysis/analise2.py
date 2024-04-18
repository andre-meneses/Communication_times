import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcular_tc(tp1, tp2, tt):
    """Calcula o tempo de comunicação com base nos tempos de processamento e no tempo total."""
    return (tt - 2 * (tp1 + tp2)) / 2

def calcular_medias_desvios_por_grupo(df, group_col, value_col):
    """Calcula as médias e desvios padrão para cada grupo de valores no dataframe."""
    estatisticas = df.groupby(group_col)[value_col].agg(['mean', 'std']).reset_index()
    return estatisticas

# Carregar os dados dos arquivos CSV
tp1_data = pd.read_csv('data1.csv')
tp2_data = pd.read_csv('data2.csv')
tt_data = pd.read_csv('data_tt.csv')

# Converter tempos para segundos
tp1_data['Time (s)'] = tp1_data['Time (ns)'] * 1e-9
tp2_data['Time (s)'] = tp2_data['Time (ns)'] * 1e-9
tt_data['Time (s)'] = tt_data['Time (ns)'] * 1e-9

# Calcular o tempo de comunicação
tc_data = calcular_tc(tp1_data['Time (s)'], tp2_data['Time (s)'], tt_data['Time (s)'])
tc_data = pd.DataFrame({'PacketSize (bytes)': tt_data['PacketSize (bytes)'], 'Time (s)': tc_data})

# Calcular médias e desvios padrões por tamanho de pacote
stats_tp1 = calcular_medias_desvios_por_grupo(tp1_data, 'PacketSize (bytes)', 'Time (s)')
stats_tp2 = calcular_medias_desvios_por_grupo(tp2_data, 'PacketSize (bytes)', 'Time (s)')
stats_tc = calcular_medias_desvios_por_grupo(tc_data, 'PacketSize (bytes)', 'Time (s)')

# Função para gerar gráficos por tamanho de pacote
def gerar_graficos(estatisticas, titulo):
    plt.errorbar(estatisticas['PacketSize (bytes)'], estatisticas['mean'], yerr=estatisticas['std'], fmt='-o', capsize=5)
    plt.title(titulo)
    plt.xlabel('Tamanho do Pacote (bytes)')
    plt.ylabel('Tempo (s)')
    plt.grid(True)

# Gerar os gráficos para Tp1, Tp2 e Tc por tamanho de pacote
plt.figure(figsize=(14, 10))

plt.subplot(3, 1, 1)
gerar_graficos(stats_tp1, 'Tempo de Processamento Tp1 por Tamanho de Pacote')

plt.subplot(3, 1, 2)
gerar_graficos(stats_tp2, 'Tempo de Processamento Tp2 por Tamanho de Pacote')

plt.subplot(3, 1, 3)
gerar_graficos(stats_tc, 'Tempo de Comunicação Tc por Tamanho de Pacote')

plt.tight_layout()
plt.savefig('tempos_por_tamanho_de_pacote.png')
plt.show()

