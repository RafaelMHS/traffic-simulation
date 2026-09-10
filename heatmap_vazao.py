import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# carrega arquivo ignorando metadados e soma fluxos
df = pd.read_csv('StressTest3_Semaforo_Pare-table.csv', skiprows=6)
df['vazao_total'] = df['fluxo-vermelhos'] + df['fluxo-azuis']

# calcula media de vazao por cenario
df_agg = df.groupby(['red-spawn', 'blue-spawn', 'method'])['vazao_total'].mean().reset_index()

# pivota dados para comparacao de metodos
df_pivot = df_agg.pivot(index=['red-spawn', 'blue-spawn'], columns='method', values='vazao_total').reset_index()

# calcula diferenca de vazao
# positivo: pare escoa mais
# negativo: semaforo escoa mais
df_pivot['diferenca_vazao'] = df_pivot['stop sign'] - df_pivot['red light']

# formata matriz para heatmap com eixo y invertido
matriz_calor = df_pivot.pivot(index='blue-spawn', columns='red-spawn', values='diferenca_vazao')
matriz_calor = matriz_calor.sort_index(ascending=False) 

# define dimensoes da figura
plt.figure(figsize=(12, 8))

sns.heatmap(matriz_calor, cmap='RdBu', center=0, annot=False, cbar_kws={'label': 'Vantagem em Vazão (Total de Carros)'})

plt.title('Zonas de Domínio de Vazão: Placa de Pare vs. Semáforo', fontsize=16, fontweight='bold')
plt.xlabel('Fluxo Via Arterial (red-spawn %)', fontsize=12)
plt.ylabel('Fluxo Via Secundária (blue-spawn %)', fontsize=12)

# ajusta layout e exporta arquivo
plt.tight_layout()
plt.savefig('heatmap_vazao_exp3.png', dpi=300, bbox_inches='tight')
print("Heatmap de vazão salvo como 'heatmap_vazao.png'!")