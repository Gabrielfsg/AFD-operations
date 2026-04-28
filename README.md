<h1 align="center">Operações com Autômatos Finitos Determinísticos</h1>

<p align="center">
  Manipulação e operações sobre AFDs (união, interseção, complemento, etc.) implementadas em Python, com leitura de arquivos do JFLAP.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/JFLAP-007396?style=for-the-badge&logo=java&logoColor=white"/>
</p>

## 📋 Sobre o projeto

Trabalho da disciplina de **Linguagens Formais e Autômatos** que implementa operações entre **Autômatos Finitos Determinísticos (AFDs)** em Python. O programa lê autômatos no formato `.jff` (JFLAP) e aplica operações como união, interseção e complemento.

## 🛠️ Tecnologias

- **Python 3**
- **JFLAP** (apenas para criação visual dos AFDs de teste)

## 📁 Estrutura

```
trab-operacoes-lfa/
├── main.py                       # Ponto de entrada
├── AutomatoFD.py                 # Classe AFD + operações
├── JFLAP7.1.jar                  # Ferramenta auxiliar (visualização)
└── Automatos_Para_Teste/         # AFDs de exemplo (.jff)
    ├── AFDTeste.jff
    ├── AFDM3.jff
    ├── prefixo_ab-sufixo_ab.jff
    └── ...
```

## ✅ Pré-requisitos

- Python 3.7+
- (Opcional) JFLAP para criar/editar autômatos visualmente

## 🚀 Como executar

```bash
cd trab-operacoes-lfa
python main.py
```

Os arquivos `.jff` em `Automatos_Para_Teste/` são usados como entrada para as operações.

## 🎯 Conceitos aplicados

- Modelagem de AFDs (estados, alfabeto, transições, estado inicial, finais)
- Operações de fechamento sobre linguagens regulares
- Parsing de XML (formato `.jff`)

---

Trabalho da disciplina de Linguagens Formais e Autômatos — [IFMG Formiga](https://www.formiga.ifmg.edu.br/).
