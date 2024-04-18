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

def calcular_estatisticas_por_tamanho(df):
    estatisticas = df.groupby('PacketSize (bytes)')['Tempo'].agg(['mean', 'std']).reset_index()
    return estatisticas

# Função para gerar gráficos por tamanho de pacote
def gerar_graficos_por_tamanho(df, titulo):
    estatisticas = calcular_estatisticas_por_tamanho(df)
    plt.errorbar(estatisticas['PacketSize'], estatisticas['mean'], yerr=estatisticas['std'], fmt='-o', capsize=5)
    plt.title(titulo)
    plt.xlabel('Tamanho do Pacote (bytes)')
    plt.ylabel('Tempo (s)')
    plt.grid(True)

# Supõe-se que os dados já estão carregados em tp1_data, tp2_data, e tt_data e que existe uma coluna 'PacketSize'

# Adicionar coluna 'Tempo' a tp1_data, tp2_data e calcular para tc_data
tp1_data['Tempo'] = tp1_data['Time (ns)']
tp2_data['Tempo'] = tp2_data['Time (ns)']
tc_data = pd.DataFrame({'PacketSize': tt_data['PacketSize (bytes)'], 'Tempo': tc_data})

# Gerar os gráficos para Tp1, Tp2 e Tc por tamanho de pacote
plt.figure(figsize=(14, 10))

plt.subplot(3, 1, 1)
gerar_graficos_por_tamanho(tp1_data, 'Tempo de Processamento Tp1 por Tamanho de Pacote')

plt.subplot(3, 1, 2)
gerar_graficos_por_tamanho(tp2_data, 'Tempo de Processamento Tp2 por Tamanho de Pacote')

plt.subplot(3, 1, 3)
gerar_graficos_por_tamanho(tc_data, 'Tempo de Comunicação Tc por Tamanho de Pacote')

plt.tight_layout()
plt.savefig('tempos_por_tamanho_de_pacote.png')
plt.show()
