import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# carrega arquivo ignorando metadados
caminho_arquivo = 'StressTest3_Semaforo_Pare-table.csv'
df = pd.read_csv(caminho_arquivo, skiprows=6)

# calcula metricas base
df['vazao_total'] = df['fluxo-vermelhos'] + df['fluxo-azuis']
df['delay_medio_global'] = np.where(df['vazao_total'] > 0, 
                                    (df['tempo-total-vermelhos'] + df['tempo-total-azuis']) / df['vazao_total'], 0)

# define filtros de cenario
proporcoes = [
    {"nome": "1:1 (Fluxo Simétrico)", "filtro": df['red-spawn'] == df['blue-spawn']},
    {"nome": "2:1 (Avenida Arterial)", "filtro": df['red-spawn'] == 2 * df['blue-spawn']}
]

# configura grid de subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
fig.suptitle('Análise do Cruzamento em Diferentes Proporções: Atraso e Vazão', fontsize=18, fontweight='bold')

cores = {'red light': '#e74c3c', 'stop sign': '#2980b9'}

# itera sobre proporcoes
for i, prop in enumerate(proporcoes):
    df_filtrado = df[prop["filtro"]]
    
    # calcula media agrupada
    df_agg = df_filtrado.groupby(['red-spawn', 'method'])[['delay_medio_global', 'vazao_total']].mean().reset_index()
    
    # plota grafico de atraso
    sns.lineplot(data=df_agg, x='red-spawn', y='delay_medio_global', hue='method', 
                 ax=axes[i, 0], marker='o', linewidth=2.5, markersize=8, palette=cores)
    axes[i, 0].set_title(f'Atraso Médio | {prop["nome"]}')
    axes[i, 0].set_ylabel('Atraso (Ticks)')
    axes[i, 0].set_xlabel('Densidade Via Principal (Spawn %)')
    axes[i, 0].grid(True, linestyle='--', alpha=0.7)
    
    # plota grafico de vazao
    sns.lineplot(data=df_agg, x='red-spawn', y='vazao_total', hue='method', 
                 ax=axes[i, 1], marker='s', linewidth=2.5, markersize=8, palette=cores, legend=False)
    axes[i, 1].set_title(f'Vazão Total | {prop["nome"]}')
    axes[i, 1].set_ylabel('Total de Carros Cruzaram')
    axes[i, 1].set_xlabel('Densidade Via Principal (Spawn %)')
    axes[i, 1].grid(True, linestyle='--', alpha=0.7)

# ajusta layout e exporta arquivo
plt.tight_layout()
plt.subplots_adjust(top=0.90, hspace=0.4)
plt.savefig('grid_graficos_exp3.png', dpi=300, bbox_inches='tight')
print("Gráficos salvos como 'grid_graficos.png'!")