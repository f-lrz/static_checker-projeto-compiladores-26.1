import sys
import os

# =====================================================================
# 1. Gerenciador de Tabelas e Estruturas

# Tabela estática de Palavras e Símbolos Reservados
RESERVED_WORDS = {
    "BOOLEAN": "A01", "BREAK": "A02", "CHARACTER": "A03", "DECLARATIONS": "A04",
    "ELSE": "A05", "ENDDECLARATIONS": "A06", "ENDFUNCTION": "A07", "ENDFUNCTIONS": "A08",
    "ENDIF": "A09", "ENDPROGRAM": "A10", "ENDWHILE": "A11", "FALSE": "A12",
    "FUNCTIONS": "A13", "FUNCTYPE": "A14", "IF": "A15", "INTEGER": "A16",
    "PARAMTYPE": "A17", "PRINT": "A18", "PROGRAM": "A19", "REAL": "A20",
    "RETURN": "A21", "STRING": "A22", "TRUE": "A23", "VARTYPE": "A24",
    "VOID": "A25", "WHILE": "A26"
}

RESERVED_SYMBOLS = {
    ";": "B01", ",": "B02", ":": "B03", ":=": "B04", "?": "B05",
    "(": "B06", ")": "B07", "[": "B08", "]": "B09", "{": "B10",
    "}": "B11", "+": "B12", "-": "B13", "*": "B14", "/": "B15",
    "%": "B16", "==": "B17", "!=": "B18", "#": "B18", "<": "B19",
    "<=": "B20", ">": "B21", ">=": "B22"
}

class SymbolTableEntry:
    def __init__(self, index, code, lexeme, qtd_antes, qtd_depois, line):
        self.index = index
        self.code = code
        self.lexeme = lexeme
        self.qtd_antes = qtd_antes
        self.qtd_depois = qtd_depois
        self.tipo_simb = "" # Pode ser preenchido futuramente (IN, FP, ST, etc)
        self.linhas = [line]

class SymbolTable:
    def __init__(self):
        self.entries = {}
        self.next_index = 1

    def add_or_get(self, lexeme, code, line, qtd_antes, qtd_depois):
        # Evita duplicidade usando o lexema como chave
        if lexeme in self.entries:
            entry = self.entries[lexeme]
            # Atualiza quantidade antes se a nova aparição for maior
            if qtd_antes > entry.qtd_antes:
                entry.qtd_antes = qtd_antes
            # Registra até as 5 primeiras linhas
            if len(entry.linhas) < 5:
                entry.linhas.append(line)
            return entry.index
        else:
            entry = SymbolTableEntry(self.next_index, code, lexeme, qtd_antes, qtd_depois, line)
            self.entries[lexeme] = entry
            self.next_index += 1
            return entry.index

# 2. Analisador Léxico

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.length = len(source_code)

    def is_valid_char(self, char):
        # Filtro de 1º nível: caracteres válidos ASCII básicos
        val = ord(char)
        return val == 9 or val == 10 or val == 13 or (32 <= val <= 126)

    def next_char(self):
        if self.pos < self.length:
            c = self.source[self.pos]
            self.pos += 1
            if c == '\n':
                self.line += 1
            return c
        return ''

    def peek_char(self):
        if self.pos < self.length:
            return self.source[self.pos]
        return ''

    def get_next_token(self, symbol_table):
        while self.pos < self.length:
            c = self.peek_char()

            # Pula caracteres inválidos (Filtro 1º nível)
            if not self.is_valid_char(c):
                self.next_char()
                continue

            # Pula espaços em branco
            if c.isspace():
                self.next_char()
                continue

            # Tratamento de Comentários
            if c == '/':
                self.next_char()
                if self.peek_char() == '/': # Comentário de Linha
                    while self.peek_char() != '\n' and self.peek_char() != '':
                        self.next_char()
                    continue
                elif self.peek_char() == '*': # Comentário de Bloco
                    self.next_char()
                    while True:
                        if self.peek_char() == '':
                            break # Fim de arquivo antes de fechar comentário
                        if self.peek_char() == '*':
                            self.next_char()
                            if self.peek_char() == '/':
                                self.next_char()
                                break
                        else:
                            self.next_char()
                    continue
                else:
                    return ('/', "B15", self.line, None) # Divisão normal

            # Operadores Relacionais e Compostos
            if c in [':', '=', '!', '<', '>']:
                op = c
                self.next_char()
                if self.peek_char() == '=':
                    op += '='
                    self.next_char()
                
                if op in RESERVED_SYMBOLS:
                    return (op, RESERVED_SYMBOLS[op], self.line, None)

            # Símbolos Simples
            if c in RESERVED_SYMBOLS:
                self.next_char()
                return (c, RESERVED_SYMBOLS[c], self.line, None)

            # Identificadores e Palavras Reservadas
            if c.isalpha() or c == '_':
                start_line = self.line
                lexeme_raw = ""
                
                # Lê a palavra inteira (pode ter 100 caracteres)
                while self.peek_char().isalnum() or self.peek_char() == '_':
                    lexeme_raw += self.next_char()
                
                # Regra de truncagem em 30 caracteres válidos e caixa alta
                qtd_antes = len(lexeme_raw)
                lexeme_formatado = lexeme_raw.upper()[:30]
                qtd_depois = len(lexeme_formatado)

                # Verifica se é Palavra Reservada
                if lexeme_formatado in RESERVED_WORDS:
                    return (lexeme_formatado, RESERVED_WORDS[lexeme_formatado], start_line, None)
                
                # Se não é palavra reservada, é identificador genérico (C01)
                # Nota: A classificação fina (C01, C02) depende do contexto sintático.
                codigo_atomo = "C01" # Por padrão: Variable
                
                # Inserção/Busca na Tabela de Símbolos
                index = symbol_table.add_or_get(lexeme_formatado, codigo_atomo, start_line, qtd_antes, qtd_depois)
                return (lexeme_formatado, codigo_atomo, start_line, index)

            # Números e Constantes (Simples, pode ser expandido conforme gramática)
            if c.isdigit():
                start_line = self.line
                num_str = ""
                while self.peek_char().isdigit():
                    num_str += self.next_char()
                
                # Simplificação: intConst
                codigo_atomo = "C06" 
                qtd_antes = len(num_str)
                lexeme_formatado = num_str[:30]
                qtd_depois = len(lexeme_formatado)
                index = symbol_table.add_or_get(lexeme_formatado, codigo_atomo, start_line, qtd_antes, qtd_depois)
                return (lexeme_formatado, codigo_atomo, start_line, index)

            # Fallback para pular caracter desconhecido
            self.next_char()

        return ("EOF", "EOF", self.line, None)

# 3. Programa Principal (Analisador Sintático Inicial)

def main():
    print("=======================================")
    print("Static Checker - BobEnzo2026-1")
    print("=======================================")
    
    # Interface de linha de comando para receber o nome do arquivo 
    filename_input = input("Digite o nome do arquivo fonte (sem a extensao): ").strip()
    
    filename = filename_input
    if not filename.endswith(".261"):
        filename += ".261"
    
    if not os.path.exists(filename):
        print(f"ERRO: Arquivo '{filename}' nao encontrado.")
        sys.exit(1)

    # Lendo o código fonte
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        source_code = f.read()

    # Inicialização das estruturas
    symbol_table = SymbolTable()
    lexer = Lexer(source_code)
    tokens_list = []

    # Laço de Varredura (Loop Principal)
    while True:
        lexeme, code, line, index = lexer.get_next_token(symbol_table)
        if code == "EOF":
            break
        
        tokens_list.append({
            "lexeme": lexeme,
            "code": code,
            "line": line,
            "index": index
        })

    # Exportação dos Relatórios
    base_name = filename_input.replace(".261", "")
    lex_file = f"{base_name}.LEX"
    tab_file = f"{base_name}.TAB"

    # Cabeçalho da Equipe EQ07 
    header = """Código da Equipe: EQ07
Componentes:
Arthur Adriano Mendes Machado; arthur.machado@aln.senaicimatec.edu.br; (71) 98113-0658
Davi Mattos Blumetti; davi.blumetti@aln.senaicimatec.edu.br; (71) 99945-6673
Filipe Lorenzo Arraes Melo Alves; filipe.alves@aln.senaicimatec.edu.br; (71) 99323-5659
Joao Maia Portela Coelho; joao.coelho@aln.senaicimatec.edu.br; (71) 98857-0737
---------------------------------------------------------
"""

    # Geração do Arquivo .LEX
    with open(lex_file, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(f"RELATÓRIO DA ANÁLISE LÉXICA.\nTexto fonte analisado: {filename}\n\n")
        for t in tokens_list:
            idx_str = f"indiceTabSimb: {t['index']}," if t['index'] else ""
            f.write(f"Lexeme: {t['lexeme']:<15} Código: {t['code']}, {idx_str:<20} Linha: {t['line']}.\n")

    # Geração do Arquivo .TAB
    with open(tab_file, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(f"RELATÓRIO DA TABELA DE SÍMBOLOS.\nTexto fonte analisado: {filename}\n\n")
        for lexeme, entry in sorted(symbol_table.entries.items(), key=lambda x: x[1].index):
            linhas_str = "(" + ", ".join(map(str, entry.linhas)) + ")"
            f.write(f"Entrada: {entry.index}, Código: {entry.code}, Lexeme: {entry.lexeme},\n")
            f.write(f"QtdCharsAntesTrunc: {entry.qtd_antes}, QtdCharDepoisTrunc: {entry.qtd_depois},\n")
            f.write(f"TipoSimb: {entry.tipo_simb} Linhas: {linhas_str}.\n")
            f.write("-" * 40 + "\n")

    print(f"\nAnalise concluida com sucesso!")
    print(f"-> Relatorio Lexico salvo em: {lex_file}")
    print(f"-> Tabela de Simbolos salva em: {tab_file}")

if __name__ == "__main__":
    main()