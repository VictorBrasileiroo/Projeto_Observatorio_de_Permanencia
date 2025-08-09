import os
import json
import joblib
import pandas as pd
import numpy as np
from django.conf import settings

class ModeloPredicaoService:
    def __init__(self):
        self.modelo = None
        self.meta = None
        self._carregar_modelo()

    def _carregar_modelo(self):
        try:
            modelo_path = os.path.join(settings.BASE_DIR, 'ml_model', 'gradient_boosting_dropout.pkl')
            meta_path = os.path.join(settings.BASE_DIR, 'ml_model', 'model_meta.json')

            if not os.path.exists(modelo_path):
                raise FileNotFoundError(f"modelo não encontrado")
            
            if not os.path.exists(meta_path):
                raise FileNotFoundError(f"meta dados não encontrados")
            
            self.modelo = joblib.load(modelo_path)

            with open(meta_path, 'r') as f:
                self.meta = json.load(f)

        except Exception as ex:
            raise

    def _converter_estudante_para_modelo(self, estudante):
        return {
            'Age at enrollment': estudante.idade_ingresso,
            'Gender': estudante.genero,
            'Daytime/evening attendance': estudante.turno_aulas,
            'Scholarship holder': int(estudante.bolsista),
            'Educational special needs': int(estudante.necessidades_especiais),
            'Curricular units 1st sem (approved)': estudante.disciplinas_aprovadas_1per,
            'Curricular units 1st sem (enrolled)': estudante.disciplinas_matriculadas_1per,
            'Curricular units 1st sem (grade)': estudante.nota_media_1per,
            'Curricular units 2nd sem (approved)': estudante.disciplinas_aprovadas_2per,
            'Curricular units 2nd sem (enrolled)': estudante.disciplinas_matriculadas_2per,
            'Curricular units 2nd sem (grade)': estudante.nota_media_2per,
        }
    
    def prever_evasao_estudante(self, estudante):
        if not self.modelo or not self.meta:
            raise Exception("Modelo não carregado")
        
        dados_modelo = self._converter_estudante_para_modelo(estudante)

        return self._executar_predicao(dados_modelo)
    
    def _executar_predicao(self, dados_modelo):
        df = pd.DataFrame([dados_modelo])

        features_esperadas = self.meta['features_expected']

        for i in features_esperadas:
            if i not in df.columns:
                df[i] = np.nan

        df = df[features_esperadas]

        probabilidade = float(self.modelo.predict_proba(df)[:, 1][0])

        faixa_risco = self.meta['risk_bands']
        if probabilidade >= faixa_risco['high']:
            nivel_risco = 'Alto'
        elif probabilidade >= faixa_risco['low']:
            nivel_risco = 'Médio'
        else:
            nivel_risco = 'Baixo'

        threshold = self.meta['best_threshold']
        previsao = 'Evasão' if probabilidade >= threshold else 'Não evasão'

        return {
            'previsao': previsao,
            'probabilidade': probabilidade,
            'nivel_risco': nivel_risco,
        }

modelo_service = ModeloPredicaoService()