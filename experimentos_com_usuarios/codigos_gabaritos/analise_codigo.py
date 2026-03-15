import sys
import os
from difflib import SequenceMatcher
import sacrebleu
from rouge_score import rouge_scorer

def ler_arquivo(caminho):
    """Lê o conteúdo de um arquivo .egua."""
    if not os.path.exists(caminho):
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
        sys.exit(1)
    
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read().strip()

def calcular_similiaridade(texto1, texto2):
    """Calcula a similaridade baseada na razão de semelhança (difflib)."""
    return SequenceMatcher(None, texto1, texto2).ratio()

def calcular_metricas(candidato, referencia):
    """
    Calcula as métricas BLEU, ROUGE-L, chrF e Similaridade.
    
    Args:
        candidato (str): O código gerado/escrito pelo usuário.
        referencia (str): O código do gabarito.
    """
    
    # 1. BLEU Score (sacrebleu espera listas de strings)
    # O BLEU padrão compara n-grams de palavras.
    bleu = sacrebleu.corpus_bleu([candidato], [[referencia]])
    
    # 2. chrF Score (Character n-gram F-score)
    # Muito útil para linguagens de programação onde a sintaxe é rígida.
    chrf = sacrebleu.corpus_chrf([candidato], [[referencia]])
    
    # 3. ROUGE-L (Longest Common Subsequence)
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)
    rouge = scorer.score(referencia, candidato)
    rouge_l_fmeasure = rouge['rougeL'].fmeasure
    
    # 4. Similaridade (Sequence Matcher)
    similaridade = calcular_similiaridade(candidato, referencia)

    return {
        "BLEU": bleu.score,
        "chrF": chrf.score,
        "ROUGE-L": rouge_l_fmeasure * 100, # Convertendo para escala 0-100
        "Similaridade": similaridade * 100 # Convertendo para escala 0-100
    }

def main():
    # Definição dos arquivos
    arquivo_usuario = '.../codigo.egua'   # Substitua pelo caminho real se necessário
    arquivo_gabarito = '.../tipo_1.egua' # Substitua pelo caminho real se necessário

    print(f"--- Avaliando código Égua ---")
    print(f"Lendo: {arquivo_usuario}")
    print(f"Gabarito: {arquivo_gabarito}\n")

    codigo_usuario = ler_arquivo(arquivo_usuario)
    codigo_gabarito = ler_arquivo(arquivo_gabarito)

    metricas = calcular_metricas(codigo_usuario, codigo_gabarito)

    print("--- Resultados ---")
    print(f"BLEU:         {metricas['BLEU']:.2f}")
    print(f"chrF:         {metricas['chrF']:.2f}")
    print(f"ROUGE-L:      {metricas['ROUGE-L']:.2f}")
    print(f"Similaridade: {metricas['Similaridade']:.2f}%")

    # Interpretação rápida
    if metricas['Similaridade'] == 100.0:
        print("\nResultado: O código é idêntico ao gabarito.")
    elif metricas['Similaridade'] > 80.0:
        print("\nResultado: O código está muito próximo do gabarito.")
    else:
        print("\nResultado: Há diferenças significativas na estrutura ou lógica.")

if __name__ == "__main__":
    main()
