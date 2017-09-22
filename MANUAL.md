# MeS.py

Trabalho de Modelagem e Simulação

Manual do Usuário

## Interface Usuário

<img src=misc/overall.png>

### Área 1:

Aqui ficam os “Dados de Entrada”, por onde o usuário pode definir parâmetros, a velocidade, e a execução da simulação.

### Área 2:

Aqui fica o “Relógio” e a “Lista de Eventos Futuros” do sistema.

### Área 3:

Aqui ficam as “Estatísticas” da simulação:
* Número de Entidades nas Filas (mínimo, máximo e médio)
* Taxa Média de Ocupação dos recursos (Carregador e Balança)
* Tempo de uma Entidade na Fila (mínimo, máximo e médio)
* Tempo de Ciclo (mínimo, máximo e médio)
* Contador de Viagens e Entidades

Aqui também fica o botão de salvar as estatísticas.

<img src=misc/inputs.png>

### Área 1:

Aqui o usuário define o “nº de caminhões” no sistema. O número pode ir de 1 a 100 caminhões.

Nota: Esse campo só pode ser alterado enquanto não houver uma simulação em execução (mesmo que esteja pausada).

### Área 2:

Aqui o usuário define a “velocidade” de simulação.

### Área 3:

Aqui o usuário define a função de distribuição do “Tempo de Carga”.

Nota: Esse campo só pode ser alterado enquanto não houver uma simulação em execução (mesmo que esteja pausada).

### Área 4:

Aqui o usuário define a função de distribuição do “Tempo de Pesagem”.

Nota: Esse campo só pode ser alterado enquanto não houver uma simulação em execução (mesmo que esteja pausada).

### Área 5:

Aqui o usuário define a função de distribuição do “Tempo de Transporte”.

Nota: Esse campo só pode ser alterado enquanto não houver uma simulação em execução (mesmo que esteja pausada).

### Área 6:

Aqui o usuário pode iniciar/continuar e pausar uma simulação.

Para iniciar uma nova simulação deve-se primeiro parar a que está em execução.

### Área 7:

Aqui o usuário pode parar uma simulação.

### Área 8:

Aqui o usuário pode salvar as atuais estatísticas num arquivo.

O arquivo com as estatísticas é criado na mesma pasta do arquivo de execução do programa. Seu nome segue a regra “Output 'data'.txt”, sendo 'data' a data e horário que as estatísticas foram salvas.

## Definindo uma função de distribuição:

Para definir uma função de distribuição, o usuário deve digitar na seguinte regra:

“função(parâmetros)” (sem aspas).

Para função, podes escolher uma das seguintes:

### CONS → Para uma função constante.

Para essa função, há apenas um parâmetro: o número constante.

Deves então colocar o número dentro dos parênteses.

Ex: “CONS(10)” para uma função que retorna sempre 10

### NORM → Para uma função de distribuição normal

Para essa função, há dois parâmetros: a média e o desvio padrão.

Deves então colocar respectivamente esses dois parâmetros, separados por vírgula.

Ex: “NORM(8, 1.5)” para uma função de distribuição normal com média 8 e desvio padrão 1.5.

Podes também definir uma semente, a qual diferenciará a sequência de variáveis aleatórias geradas por essa função. Ela deve ser um número inteiro positivo, e vir por último nos parênteses, separada por vírgula.

Ex: “NORM(8, 1.5, 13)” para uma função de distribuição normal com média 8 e desvio padrão 1.5, e sua semente será 13. (a semente padrão é 0)

### EXPO → Para uma função de distribuição exponencial

Para essa função, há um parâmetro: a taxa de decaimento.

Deves então colocar esse parâmetro dentro dos parênteses.

Ex: “EXPO(0.3)” para uma função de distribuição exponencial com taxa de decaimento 0.3.

Podes também definir uma semente, a qual diferenciará a sequência de variáveis aleatórias geradas por essa função. Ela deve ser um número inteiro positivo, e vir por último nos parênteses, separada por vírgula.

Ex: “EXPO(0.3, 13)” para uma função de distribuição exponencial com taxa de decaimento 0.3, e sua semente será 13. (a semente padrão é 0)

### TRIA → Para uma função de distribuição triangular

Para essa função, há três parâmetro: o valor mínimo, a moda, e o valor máximo.

Deves então colocar respectivamente esses três parâmetros, separados por vírgula.

Ex: “TRIA(2, 5, 6)” para uma função de distribuição triangular com valor mínimo 2, moda 5, e valor máximo 6.

Podes também definir uma semente, a qual diferenciará a sequência de variáveis aleatórias geradas por essa função. Ela deve ser um número inteiro positivo, e vir por último nos parênteses, separada por vírgula.

Ex: “TRIA(2, 5, 6, 13)” para uma função de distribuição triangular com valor mínimo 2, moda 5, e valor máximo 6, e sua semente será 13. (a semente padrão é 0)

### UNIF → Para uma função de disribuição uniforme

Para essa função, há dois parâmetro: o valor mínimo, e o valor máximo.

Deves então colocar respectivamente esses dois parâmetros, separados por vírgula.

Ex: “UNIF(2, 6)” para uma função de distribuição triangular com valor mínimo 2, e valor máximo 6.

Podes também definir uma semente, a qual diferenciará a sequência de variáveis aleatórias geradas por essa função. Ela deve ser um número inteiro positivo, e vir por último nos parênteses, separada por vírgula.

Ex: “UNIF(2, 6, 13)” para uma função de distribuição triangular com valor mínimo 2, e valor máximo 6, e sua semente será 13. (a semente padrão é 0)
