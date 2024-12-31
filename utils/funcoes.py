import unidecode
import re
import pandas as pd
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
import pickle
from collections import defaultdict

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


def constroi_lista(df:pd.DataFrame, coluna:str):
    lista = list(df[df['Curso'].isin(['LCE','LCEFISICA', 'LCEMATEMATICA', 'LCEQUIMICA','EAQ','ECV','EAS','OCEANO'])][coluna].dropna().unique()) #'LCE','LCEFISICA', 'LCEMATEMATICA', 'LCEQUIMICA','EAQ','ECV','EAS','OCEANO'
    return lista


def get_hora_aula_materia(professor,materia, turma, df):
    resultado = df.query("Semestre_Curso == @turma and Materia == @materia and Professor == @professor")
    if not resultado.empty:
        return float(resultado['Total_Horas'].iloc[0])
    else:
        return 0


def get_turno(turma, df):
    resultado = df.query("Semestre_Curso == @turma")
    if not resultado.empty:
        return resultado['Tipo_Curso'].iloc[0]
    else:
        return 0
    

def get_campus(turma,disciplina, df):
    resultado = df.query("Semestre_Curso == @turma and Materia == @disciplina")
    return not resultado.empty


# Função para criar a grade horária visualizada por turma
def plotar_grade_horaria(df):
    # Obter todas as turmas únicas
    turmas = df['Turma'].unique()
    
    for turma in turmas:
        # Filtrar o DataFrame para a turma atual
        df_turma = df[df['Turma'] == turma]

        # Criar um pivot table para visualização
        grade_horaria = df_turma.pivot(index='Dia', columns='Periodo', values='Professor')

        # Plotar a grade horária manualmente
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.axis('off')
        table = ax.table(cellText=grade_horaria.values,
                         rowLabels=grade_horaria.index,
                         colLabels=grade_horaria.columns,
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.auto_set_column_width(col=list(range(len(grade_horaria.columns))))
        plt.title(f'Grade Horária - Turma {turma}')
        plt.show()


# Função para criar a grade horária visualizada por professor
def plotar_grade_horaria_por_professor(df):
    # Obter todos os professores únicos
    professores = df['Professor'].unique()
    
    for professor in professores:
        # Filtrar o DataFrame para o professor atual
        df_professor = df[df['Professor'] == professor]

        # Criar um pivot table para visualização
        grade_horaria = df_professor.pivot(index='Dia', columns='Periodo', values='Turma')

        # Plotar a grade horária manualmente
        fig, ax = plt.subplots(figsize=(12, 2))
        ax.axis('off')
        table = ax.table(cellText=grade_horaria.values,
                         rowLabels=grade_horaria.index,
                         colLabels=grade_horaria.columns,
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.auto_set_column_width(col=list(range(len(grade_horaria.columns))))
        plt.title(f'Grade Horária - Professor {professor}')
        plt.show()