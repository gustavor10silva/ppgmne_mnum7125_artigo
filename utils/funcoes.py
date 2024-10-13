import unidecode
import re
import pandas as pd

def remover_acentos_e_caracteres(texto):
    """
    Descrição
    ----------
    Esta função substitui o caractere "ç" por "C" (independente de maiúscula ou minúscula),
    remove acentos de letras acentuadas e elimina caracteres especiais.

    Parâmetros
    ----------
    texto : str
        A string de entrada que será processada para remover acentos e caracteres especiais.

    Retorno
    -------
    texto_limpo : str
        A string modificada, sem acentos e caracteres especiais.
    """
    if pd.isna(texto):  # Verifica se é NaN
        return texto  # Retorna o valor original se for NaN
    
    # Substituir "ç" por "C" (tanto maiúsculo quanto minúsculo)
    texto = texto.replace("ç", "C").replace("Ç", "C")
    # Remover acentos
    texto_sem_acento = unidecode.unidecode(texto)
    # Remover caracteres especiais, mantendo apenas letras, números e espaços
    texto_limpo = re.sub(r'[^A-Za-z0-9\s]', '', texto_sem_acento)
    #Remove espaços
    texto_limpo = texto_limpo.strip()
    
    return texto_limpo
