import re

class PhoneticEngine:
    """
    Motor Fonético Especialista (Padrão Metaphone BR).
    Adaptado para as regras ortográficas e fonéticas do Português Brasileiro.
    Utilizado para deduplicação profunda de nomes e identidades.
    """
    
    @staticmethod
    def get_phonetic_code(text):
        """
        Gera uma representação fonética (código) de uma string.
        Baseado no algoritmo Metaphone adaptado para PT-BR.
        """
        if not text:
            return ""
            
        # 1. Pré-processamento e Normalização
        t = text.upper().strip()
        
        # Remover acentuação básica
        t = re.sub(r'[ÁÀÂÃ]', 'A', t)
        t = re.sub(r'[ÉÈÊ]', 'E', t)
        t = re.sub(r'[ÍÌÎ]', 'I', t)
        t = re.sub(r'[ÓÒÔÕ]', 'O', t)
        t = re.sub(r'[ÚÙÛ]', 'U', t)
        t = t.replace('Ç', 'S')
        
        # Remover caracteres não alfabéticos
        t = re.sub(r'[^A-Z]', '', t)
        
        if not t:
            return ""

        # 2. Transformações Fonéticas PT-BR
        
        # Grupos de letras e sons complexos
        t = t.replace('PH', 'F')
        t = t.replace('SH', 'X')
        t = t.replace('CH', 'X')
        t = t.replace('TH', 'T')
        
        # GE, GI -> JE, JI
        t = re.sub(r'G(?=[EI])', 'J', t)
        # GU[EI] -> G[EI]
        t = re.sub(r'GU(?=[EI])', 'G', t)
        
        # QU[EI] -> K -> C
        t = re.sub(r'QU(?=[EI])', 'C', t)
        t = t.replace('K', 'C')
        
        # Sons de S (S, Z, X)
        t = t.replace('Z', 'S')
        # X com som de S em certas posições (simplificado para engine)
        t = t.replace('X', 'S')
        
        # Letras MUDAS ou semi-vogais
        t = t.replace('W', 'V')
        t = t.replace('Y', 'I')
        t = t.replace('H', '') # H é sempre mudo em PT-BR (exceto NH, LH que tratamos abaixo)
        
        # Voltar NH e LH para um código único
        # (Como removemos o H acima, precisamos tratar isso antes ou usar um token)
        # RE-DOing the H logic safely:
        t = text.upper().strip()
        t = re.sub(r'[ÁÀÂÃ]', 'A', t)
        t = re.sub(r'[ÉÈÊ]', 'E', t)
        t = re.sub(r'[ÍÌÎ]', 'I', t)
        t = re.sub(r'[ÓÒÔÕ]', 'O', t)
        t = re.sub(r'[ÚÙÛ]', 'U', t)
        t = t.replace('Ç', 'S')
        
        t = t.replace('LH', '1') # Token para som exclusivo
        t = t.replace('NH', '2') # Token para som exclusivo
        t = t.replace('PH', 'F')
        t = t.replace('TH', 'T')
        t = t.replace('CH', 'X')
        t = t.replace('SH', 'X')
        t = t.replace('H', '')
        
        # Nasalização (M e N no final de sílaba são idênticos)
        # Trocamos M por N em todo lugar para simplificar unificação
        t = t.replace('M', 'N')
        
        # Sibilantes Finais (S, Z, X no final da palavra)
        t = re.sub(r'[SZX]$', '3', t) # Token para sibilante final
        
        # Normalização de S/C/Z
        t = t.replace('Z', 'S')
        t = re.sub(r'C(?=[EI])', 'S', t)
        
        # 3. Redução de Duplicidade (LL -> L, SS -> S)
        res = ""
        for char in t:
            if not res or char != res[-1]:
                res += char
                
        return res

    def are_phonetically_identical(self, text_a, text_b):
        """Verifica se dois textos possuem a mesma representação fonética."""
        return self.get_phonetic_code(text_a) == self.get_phonetic_code(text_b)
