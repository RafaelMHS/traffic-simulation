import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# carrega dados ignorando metadados
df = pd.read_csv('StressTest3_Semaforo_Pare-table.csv', skiprows=6)

# filtra cenario com proporcao 2:1
df_21 = df[df['red-spawn'] == 2 * df['blue-spawn']]

# calcula media agrupada
df_agg = df_21.groupby(['red-spawn', 'method'])[['fluxo-vermelhos', 'fluxo-azuis']].mean().reset_index()

# configura grid de subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Análise de Vazão: Inanição no Cenário 2:1', fontsize=16, fontweight='bold', y=1.05)
cores = {'red light': '#e74c3c', 'stop sign': '#2980b9'}

# plota grafico da via principal
sns.lineplot(data=df_agg, x='red-spawn', y='fluxo-vermelhos', hue='method', ax=axes[0], 
             marker='o', linewidth=2.5, palette=cores)
axes[0].set_title('Via Principal (Privilegiada)', fontsize=14)
axes[0].set_ylabel('Carros que Cruzaram')
axes[0].set_xlabel('Densidade Via Principal (Spawn %)')
axes[0].grid(True, linestyle='--', alpha=0.7)

# plota grafico da via secundaria
sns.lineplot(data=df_agg, x='red-spawn', y='fluxo-azuis', hue='method', ax=axes[1], 
             marker='s', linewidth=2.5, palette=cores, legend=False)
axes[1].set_title('Via Secundária (Penalizada)', fontsize=14)
axes[1].set_ylabel('Carros que Cruzaram')
axes[1].set_xlabel('Densidade Via Principal (Spawn %)')
axes[1].grid(True, linestyle='--', alpha=0.7)

# ajusta layout e exporta arquivo
plt.tight_layout()
plt.savefig('analise_vazao_individual_exp3.png', dpi=300, bbox_inches='tight')
print("Gráfico salvo como 'analise_vazao_individual.png'!")