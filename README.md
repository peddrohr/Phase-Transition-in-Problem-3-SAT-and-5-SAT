# Trabalho Prático: Transição de Fase no Problema 3-SAT e 5-SAT

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySAT](https://img.shields.io/badge/PySAT-1.8.dev14-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5.0-orange)

Este repositório contém o código e a documentação para o trabalho prático da disciplina **Lógica para Computação**, ministrada pelo **Prof. Dr. Alexandre Arruda**. O objetivo é investigar o fenômeno de transição de fase no problema da satisfazibilidade booleana (SAT), com foco nos casos 3-SAT e 5-SAT.

---

## 📋 Descrição do Projeto

O problema SAT consiste em determinar se existe uma atribuição de valores verdadeiros (verdadeiro ou falso) para as variáveis de uma fórmula booleana que a torne verdadeira. No caso do **k-SAT**, a fórmula está na forma normal conjuntiva (CNF), com exatamente **k literais por cláusula**.

O fenômeno de **transição de fase** ocorre em função da razão **α = m/n**, onde:
- **m**: Número de cláusulas.
- **n**: Número de variáveis.

À medida que α aumenta, o comportamento do problema muda drasticamente:
1. **Fase Subcrítica (α < αc)**: As instâncias são quase sempre satisfazíveis.
2. **Fase Supercrítica (α > αc)**: As instâncias são quase sempre insatisfazíveis.
3. **Ponto Crítico (α = αc)**: Ocorre uma transição abrupta entre as duas fases.

Este trabalho visa identificar o ponto crítico **αc** e analisar como a probabilidade de satisfazibilidade varia em função de α.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.8 ou superior.
- Dependências listadas no arquivo `requirements.txt`.

### Instalação

#### 1. Clone o repositório:
   git clone https://github.com/peddrohr/Phase-Transition-in-Problem-3-SAT-and-5-SAT
   cd transicao-fase-sat
   
   
#### 2. Crie um ambiente virtual (opcional, mas recomendado):
    python -m venv .venv
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
    

#### 3. Instale as dependências:
    pip install -r requirements.txt

#### 4. Executando o Código
    python .src/main.py

---

## 📊 Resultados Esperados
O código gera dois tipos de gráficos para cada valor de n (número de variáveis):

1. Probabilidade de Satisfazibilidade:

    * Mostra como a probabilidade de uma instância ser satisfazível varia em função de α.

2. Tempo Médio de Execução:

   * Mostra o tempo médio que o solver leva para resolver as instâncias em função de α.

---

## 👥 Autores
<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/180479512?v=4" width="100px;" alt="@peddrohr"/><br>
        <sub>
          <b>Pedro Henrique</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/57305990?v=4" width="100px;" alt="@douglas-jpg"/><br>
        <sub>
          <b>Douglas de Lima</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

---

## 📜 Licença
* Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

---

## 🔗 Referências
  * PySAT Documentation
  * Matplotlib Documentation

Understanding SAT and Phase Transitions