import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# carrega dados ignorando metadados
df = pd.read_csv('StressTest3_Semaforo_Pare-table.csv', skiprows=6)

# adiciona constante para evitar divisao por zero
epsilon = 0.0001

# calcula metricas de proporcao
df['razao_demanda'] = df['red-spawn'] / (df['blue-spawn'] + epsilon)
df['razao_fluxo'] = df['fluxo-vermelhos'] / (df['fluxo-azuis'] + epsilon)

# calcula indice de injustica
# valores positivos prejudicam via secundaria
# valores negativos prejudicam via principal
df['indice_injustica'] = df['razao_fluxo'] - df['razao_demanda']

# agrupa e formata dados para heatmaps
df_agg = df.groupby(['red-spawn', 'blue-spawn', 'method'])['indice_injustica'].mean().reset_index()

df_pare = df_agg[df_agg['method'] == 'stop sign'].pivot(index='blue-spawn', columns='red-spawn', values='indice_injustica').sort_index(ascending=False)
df_semaforo = df_agg[df_agg['method'] == 'red light'].pivot(index='blue-spawn', columns='red-spawn', values='indice_injustica').sort_index(ascending=False)

# configura grid de subplots
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
fig.suptitle('Raio-X da Injustiça: Proporção de Demanda vs. Proporção de Vazão', fontsize=18, fontweight='bold', y=1.02)

# fixa limites para estabilizar gradiente
vmin_trava = -3
vmax_trava = 3

# plota heatmap pare
sns.heatmap(df_pare, cmap='RdBu_r', center=0, ax=axes[0], vmin=vmin_trava, vmax=vmax_trava,
            cbar_kws={'label': 'Índice de Injustiça'})
axes[0].set_title('Placa de Pare', fontsize=16, fontweight='bold', pad=15)
axes[0].set_xlabel('Densidade Via Principal (red-spawn %)', fontsize=12)
axes[0].set_ylabel('Densidade Via Secundária (blue-spawn %)', fontsize=12)

# plota heatmap semaforo
sns.heatmap(df_semaforo, cmap='RdBu_r', center=0, ax=axes[1], vmin=vmin_trava, vmax=vmax_trava,
            cbar_kws={'label': 'Índice de Injustiça'})
axes[1].set_title('Semáforo Estático', fontsize=16, fontweight='bold', pad=15)
axes[1].set_xlabel('Densidade Via Principal (red-spawn %)', fontsize=12)
axes[1].set_ylabel('') # remove rotulo y

# insere texto explicativo
plt.figtext(0.5, -0.05, 'Vermelho: Via Secundária está sendo injustiçada (Inanição)  |  Branco: Equilíbrio Perfeito  |  Azul: Via Principal está sendo injustiçada (Espera à toa)', 
            ha='center', fontsize=13, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# ajusta layout e exporta arquivo
plt.tight_layout()
plt.savefig('heatmap_injustica_exp3.png', dpi=300, bbox_inches='tight')
print("Gráfico duplo salvo como 'heatmap_injustica.png'!")