import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# carrega dados ignorando metadados iniciais
df = pd.read_csv('StressTest3_Semaforo_Pare-table.csv', skiprows=6)

# calcula atraso medio por via evitando divisao por zero
df['atraso_vermelhos'] = np.where(df['fluxo-vermelhos'] > 0, 
                                  df['tempo-total-vermelhos'] / df['fluxo-vermelhos'], 0)
df['atraso_azuis'] = np.where(df['fluxo-azuis'] > 0, 
                              df['tempo-total-azuis'] / df['fluxo-azuis'], 0)

# filtra cenario com proporcao 2:1 entre vias
df_21 = df[df['red-spawn'] == 2 * df['blue-spawn']]

# calcula media de atraso agrupada
df_agg = df_21.groupby(['red-spawn', 'method'])[['atraso_vermelhos', 'atraso_azuis']].mean().reset_index()

# define figura com dois subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Análise de Atraso: A diferença entre as Vias (Cenário 2:1)', fontsize=16, fontweight='bold', y=1.05)
cores = {'red light': '#e74c3c', 'stop sign': '#2980b9'}

# plota grafico da via principal
sns.lineplot(data=df_agg, x='red-spawn', y='atraso_vermelhos', hue='method', ax=axes[0], 
             marker='o', linewidth=2.5, palette=cores)
axes[0].set_title('Atraso na Via Principal (Privilegiada)', fontsize=14)
axes[0].set_ylabel('Atraso Médio (Ticks)')
axes[0].set_xlabel('Densidade Via Principal (Spawn %)')
axes[0].grid(True, linestyle='--', alpha=0.7)

# plota grafico da via secundaria
sns.lineplot(data=df_agg, x='red-spawn', y='atraso_azuis', hue='method', ax=axes[1], 
             marker='s', linewidth=2.5, palette=cores, legend=False)
axes[1].set_title('Atraso na Via Secundária (Penalizada)', fontsize=14)
axes[1].set_ylabel('Atraso Médio (Ticks)')
axes[1].set_xlabel('Densidade Via Principal (Spawn %)')
axes[1].grid(True, linestyle='--', alpha=0.7)

# ajusta layout e exporta arquivo
plt.tight_layout()
plt.savefig('analise_atraso_individual_exp3.png', dpi=300, bbox_inches='tight')
print("Gráfico de atrasos individuais salvo como 'analise_atraso_individual.png'!")