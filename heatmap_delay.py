import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# carrega dados ignorando metadados iniciais
df = pd.read_csv('StressTest3_Semaforo_Pare-table.csv', skiprows=6)

# calcula atraso medio por veiculo
df['atraso_total'] = (df['tempo-total-vermelhos'] + df['tempo-total-azuis']) / (df['fluxo-vermelhos'] + df['fluxo-azuis'] + 0.0001)

# calcula media das repeticoes e formata tabela para comparacao
df_agg = df.groupby(['red-spawn', 'blue-spawn', 'method'])['atraso_total'].mean().reset_index()
df_pivot = df_agg.pivot(index=['red-spawn', 'blue-spawn'], columns='method', values='atraso_total').reset_index()

# calcula diferenca de atraso (semaforo - pare)
# positivo: vantagem para placa de pare
# negativo: vantagem para semaforo
df_pivot['diferenca_atraso'] = df_pivot['red light'] - df_pivot['stop sign']

# formata matriz do heatmap com eixo y invertido
matriz_calor = df_pivot.pivot(index='blue-spawn', columns='red-spawn', values='diferenca_atraso')
matriz_calor = matriz_calor.sort_index(ascending=False)

# define dimensoes da figura
plt.figure(figsize=(12, 8))

# fixa limites para estabilizar gradiente de cores
vmin_real = -15
vmax_real = 50

ax = sns.heatmap(matriz_calor, cmap='RdBu', center=0, annot=False, 
                 vmin=vmin_real, vmax=vmax_real)

plt.title('Zonas de Domínio: Placa de Pare vs. Semáforo', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Fluxo Via Arterial (red-spawn %)', fontsize=12)
plt.ylabel('Fluxo Via Secundária (blue-spawn %)', fontsize=12)

cbar = ax.collections[0].colorbar
cbar.set_label('Vantagem (Ticks Salvos)', fontsize=12)

# define marcadores especificos na escala
ticks_exatos = [-10, 0, 10, 20, 30, 40, 50]
cbar.set_ticks(ticks_exatos)

# aplica valores absolutos nos rotulos
cbar.set_ticklabels([str(abs(t)) for t in ticks_exatos])

# insere indicadores nominais nas extremidades
cbar.ax.set_title('Pare', fontweight='bold', color='#1e5b8e', pad=10)
cbar.ax.text(0.5, -0.02, 'Semáforo', transform=cbar.ax.transAxes, 
             ha='center', va='top', fontweight='bold', color='#d35400')

# ajusta layout e exporta arquivo
plt.tight_layout()
plt.savefig('heatmap_delay_exp3.png', dpi=300, bbox_inches='tight')
print("Heatmap salvo como 'heatmap_delay.png'!")