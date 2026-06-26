# Static Checker - Analisador Léxico (Etapa 7)

Este repositório contém a implementação do **Static Checker** (Analisador Léxico e infraestrutura inicial do Sintático) para a linguagem alvo **BobEnzo2026-1**, desenvolvida como parte da disciplina de Compiladores do curso de Engenharia da Computação.

## 👥 Equipe (EQ07)
* **Arthur Adriano Mendes Machado** - arthur.machado@aln.senaicimatec.edu.br - (71) 98113-0658
* **Davi Mattos Blumetti** - davi.blumetti@aln.senaicimatec.edu.br - (71) 99945-6673
* **Filipe Lorenzo Arraes Melo Alves** - filipe.alves@aln.senaicimatec.edu.br - (71) 99323-5659
* **Joao Maia Portela Coelho** - joao.coelho@aln.senaicimatec.edu.br - (71) 98857-0737

**Instituição:** SENAI CIMATEC  
**Professor:** Osvaldo Requião Melo  
**Semestre:** 2026.1  

---

## 📝 Descrição do Projeto
O sistema adota o modelo de tradução guiada pela sintaxe (*Syntax-Driven*), operando em três módulos integrados:
1. **Controlador Sintático (Orquestrador):** Gerencia o fluxo do arquivo e consome os átomos gerados sob demanda.
2. **Analisador Léxico:** Realiza a leitura de caracteres em caixa alta (*case-insensitive*), descarta comentários (`//` e `/* */`), filtra caracteres inválidos (Filtro de 1º Nível) e aplica a regra de **truncagem rigorosa de identificadores em 30 caracteres válidos**.
3. **Gerenciador de Tabelas:** Inicializa de forma estática as tabelas de palavras reservadas (`A01` a `A26`) e símbolos reservados (`B01` a `B22`), e mantém uma Tabela de Símbolos dinâmica para persistência única (sem duplicidade) de identificadores.

---

## 🛠️ Pré-requisitos
Para executar esta ferramenta, você precisará apenas do **Python 3.x** instalado em sua máquina. Nenhuma biblioteca externa ou dependência adicional é necessária.

Para verificar se possui o Python instalado, execute no terminal:
```bash
python --version
```

---

## ⚙️ Instruções de Uso
1. **Preparar o Arquivo Fonte:** Certifique-se de que o arquivo de código fonte que você deseja testar possui a extensão .261 e está localizado no mesmo diretório do script static_checker.py.

Exemplo de arquivo:
```bash
Teste.261
```


2. **Execução do Compilador:** Execute o programa principal utilizando o terminal de comandos:
```bash
python static_checker.py
```


3. **Fornecer os Parâmetros de Entrada:** O programa iniciará exibindo a interface de linha de comando e solicitará o nome do arquivo texto.
Conforme a especificação do projeto, **não é necessário digitar a extensão .261.**

Exemplo de Interação no Terminal:
```bash
=======================================
Static Checker - BobEnzo2026-1
=======================================
Digite o nome do arquivo fonte (sem a extensao): Teste

Analise concluida com sucesso!
-> Relatorio Lexico salvo em: Teste.LEX
-> Tabela de Simbolos salva em: Teste.TAB
```
