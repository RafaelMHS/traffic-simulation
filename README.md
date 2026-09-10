# Smart Intersection: Agent-Based Traffic Control Simulation

Um ambiente de simulação em NetLogo e pipeline de análise em Python construído para avaliar a eficiência, vazão e equidade de diferentes métodos de controle de tráfego urbano (Placa de Pare vs. Semáforo Estático).

Este projeto utiliza **Modelagem Baseada em Agentes (ABM)** combinada com parâmetros reais de Engenharia de Tráfego para comprovar matematicamente o fenômeno de inanição (*starvation*) em cruzamentos e estabelecer uma *baseline* rigorosa para futuras implementações de Inteligência Artificial (Aprendizado por Reforço).

---

## Metodologia 

Para garantir que a simulação refletisse o trânsito real, os agentes (veículos) não possuem atrasos puramente estocásticos. Cada agente é instanciado com um `score-reacao` e uma `lentidao` única que dita seu perfil psicológico durante toda a viagem.

As mecânicas do cruzamento foram modeladas estritamente sob as diretrizes do **Highway Capacity Manual (HCM)**:

*   **Critical Gap (Placa de Pare):** O líder da fila calcula brechas seguras no fluxo transversal baseando-se no seu nível de agressividade/atenção.
*   **Follow-up Time (Placa de Pare):** Veículos subsequentes na fila utilizam um tempo de reação drasticamente menor, seguindo o líder em "pelotão".
*   **Start-up Lost Time & Saturation Headway (Semáforo):** Apenas os 4 primeiros veículos da fila sofrem a inércia da arrancada no sinal verde. Do 5º em diante, o fluxo escoa de forma contínua e eficiente.

---

## Histórico de Experimentos (Evolução do Modelo)

O desenvolvimento das análises seguiu uma abordagem iterativa, refinando a mecânica dos agentes e o rigor estatístico a cada etapa:

*   **Experimento 1 (Prova de Conceito):** Avaliação inicial da viabilidade do modelo com **6.100 cenários**. Serviu para validar a arquitetura básica do cruzamento e os scripts iniciais em Python para extração de dados.
*   **Experimento 2 (Stress Test Bruto):** Teste de estresse em larga escala gerando **245.000 cenários**. Utilizou a mecânica clássica de atrasos estocásticos puros (versão anterior do código). Provou estatisticamente a ocorrência de inanição (*starvation*) na Placa de Pare, mapeando as zonas de domínio absoluto.
*   **Experimento 3 (Simulação Pareada e Refinada):** O modelo mais atualizado. Incorpora todas as regras de atraso e inércia do *HCM* atreladas ao comportamento do agente. Executado com **24.500 cenários rigorosamente pareados** (mesmo *random-seed* para ambos os métodos de controle), garantindo precisão e eliminando o desperdício computacional.

---

## Coleta de Dados e Principais Descobertas

O experimento utilizou o recurso **BehaviorSpace** para executar uma matriz de **24.500 cenários pareados** (35x35 densidades de *spawn*, 2 métodos, 10 random seeds). Os dados brutos foram processados via `Pandas` e visualizados via `Seaborn/Matplotlib`.

Os resultados revelaram três diagnósticos fundamentais sobre o gargalo urbano:

### 1. A Ineficiência do Tempo (Atraso)
O Semáforo Estático pune o sistema em cenários de baixo volume. O tempo de ciclo fixo obriga a via principal a parar para vias secundárias fantasmas, gerando uma taxa de atraso acumulado significativamente maior que a Placa de Pare em madrugadas ou zonas residenciais.

### 2. O Colapso e a Inanição (Vazão)
A Placa de Pare colapsa completamente em cenários de volume assimétrico (ex: 2:1). Devido à exigência mecânica do *Critical Gap*, a via secundária entra em estado de **Inanição (*Starvation*)**, tendo seu escoamento esmagado e limitado a ~1.400 veículos, enquanto o Semáforo limpa a mesma malha ultrapassando 1.700 veículos.

### 3. O Mapa da Equidade (Injustiça)
Um cálculo de proporção de demanda vs. proporção de vazão `(Fluxo Real / Demanda Real)` comprova que nenhum dos métodos tradicionais é inerentemente justo. O gradiente revela zonas claras de domínio onde um fluxo "rouba" o tempo do outro.

---

## Como Executar

### 1. Simulação (NetLogo)
*   Abra o arquivo `Traffic_Simulation.nlogo` no NetLogo 6.x.
*   Selecione o método desejado (`stop sign` ou `red light`).
*   Ajuste as taxas de `red-spawn` e `blue-spawn`.
*   Clique em `setup` e depois em `go`.

### 2. Análise de Dados (Python)
*   Certifique-se de ter as bibliotecas instaladas: `pip install pandas matplotlib seaborn numpy`
*   Coloque o arquivo `.csv` gerado pelo BehaviorSpace na mesma pasta.
*   Execute os scripts de plotagem para gerar os *heatmaps* dinâmicos:
    ```bash
    python plot_analytics.py
    ```

---

## Próximos Passos
*   **Fase 2:** Implementação de um Semáforo Atuado (Rule-based) utilizando laços virtuais de presença para cortar ciclos vazios.
*   **Fase 3:** Expansão da malha viária (Grid) para observar o efeito *Gridlock* sistêmico.
*   **Fase 4:** Integração de um agente autônomo treinado via **Q-Learning** para controle dinâmico e descentralizado da rede.
