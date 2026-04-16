from core.engines.mdm.taxonomy_loader import TaxonomyLoader
from core.engines.mdm.algorithms.normalizer import Normalizer
from core.engines.mdm.algorithms.exact_matcher import ExactMatcher
from core.engines.mdm.algorithms.pattern_matcher import PatternMatcher
from core.engines.mdm.algorithms.fuzzy_matcher import FuzzyMatcher
from core.engines.mdm.algorithms.scoring import ConfidenceScorer
from core.math.phonetic_engine import PhoneticEngine
import re
import pandas as pd
from version import __version__

class MDMEngine:
    """
    Controlador de Resolução de Domínio Enterprise.
    Orquestra as camadas de detecção e aplica regras de governança.
    """
    def __init__(self, taxonomy_path=None):
        from core.engines.mdm.taxonomy_loader import TaxonomyLoader
        self.loader = TaxonomyLoader(taxonomy_path)
        self.taxonomy = self.loader.get_taxonomy()
        self.weights = self.loader.get_weights()
        self.thresholds = self.loader.get_thresholds()
        
        self.exact_matcher = ExactMatcher(self.taxonomy, self.weights)
        self.pattern_matcher = PatternMatcher(self.taxonomy, self.weights)
        self.fuzzy_matcher = FuzzyMatcher(self.taxonomy, self.weights)
        self.scorer = ConfidenceScorer()
        
        # 🔗 Cache Fonético de Identidades (Performance)
        self._phonetic_taxonomy_map = {}
        for entry in self.taxonomy:
            label = entry.get("label", "")
            if label:
                p_code = PhoneticEngine.get_phonetic_code(label)
                if p_code not in self._phonetic_taxonomy_map:
                    self._phonetic_taxonomy_map[p_code] = []
                self._phonetic_taxonomy_map[p_code].append(entry["code"])

    def resolve(self, raw_value):
        """
        Orquestra a perícia MDM sobre um valor bruto.
        Retorna (best_code, confidence, trace_log, status).
        """
        if not raw_value or pd.isna(raw_value):
            return self._build_result(raw_value, "", "SKIPPED", 0, "Valor vazio")

        norm_val = Normalizer.deep_clean(raw_value)
        if not norm_val:
            return self._build_result(raw_value, "", "SKIPPED", 0, "Valor sem conteúdo após normalização")

        # 1. Coleta de Evidências (Sincronizado via taxonomia pré-carregada)
        hits = []
        hits.extend(self.exact_matcher.collect_evidences(norm_val))
        hits.extend(self.pattern_matcher.collect_evidences(norm_val))
        hits.extend(self.fuzzy_matcher.collect_evidences(norm_val))
        
        # 2. CAMADA DE INTELIGÊNCIA FONÉTICA (Metaphone BR)
        # Se as camadas anteriores falharem ou forem fracas, a fonética decide
        p_code = PhoneticEngine.get_phonetic_code(norm_val)
        if p_code and p_code in self._phonetic_taxonomy_map:
            for code in self._phonetic_taxonomy_map[p_code]:
                hits.append((code, 0.90, "PHONETIC_MATCH"))

        # 3. Consolidação e Scoring
        consolidated = ConfidenceScorer.consolidate(hits)
        top_two = ConfidenceScorer.top_candidates(consolidated, limit=2)

        if not top_two:
            return self._build_result(raw_value, norm_val, "UNKNOWN", 0.0, "Nenhum match detectado em nenhuma camada.")

        # 4. Análise de Ambiguidade
        best_code, best_data = top_two[0]
        score = best_data["score"]
        
        # Buscar label para uso na decisão
        match_entry = next((t for t in self.taxonomy if t["code"] == best_code), {})
        res_best_label = match_entry.get("label", "N/A")
        
        # Margem de confiança
        if len(top_two) > 1:
            second_code, second_data = top_two[1]
            margin = score - second_data["score"]
            if margin < self.thresholds.get("ambiguity_margin_min", 0.10):
                return self._build_result(raw_value, norm_val, "AMBIGUOUS", score, 
                                        f"Conflito entre {best_code} e {second_code}. Margem: {round(margin, 2)}",
                                        best_code, best_data["traces"])

        # 5. Decisão Final baseada em Thresholds e Extração de Persona
        status = "UNKNOWN"
        final_label = res_best_label
        
        if score >= self.thresholds.get("auto_classify", 0.85):
            status = "AUTO_CLASSIFIED"
            # Tentar Extrair Nome (Persona) se houver match forte
            # Remove o termo reconhecido da string original
            persona = norm_val.split("@")[0]
            # Limpeza agressiva: remove pontos, traços e o nome do setor se estiver contido
            # Ex: "financeiro.nome" -> "Nome"
            for t in best_data.get("traces", []):
                # Se for match aproximado ou exato, tentamos limpar o termo
                # Para simplificar, removemos keywords comuns da taxonomia
                keywords = best_data.get("keywords", []) # Se tivéssemos keywords
            
            # Heurística: se o nome do setor está no prefixo, removemos como palavra inteira
            # Buscamos o termo na taxonomia para remoção precisa
            # Remocao protegida: apenas se o código ou label forem tokens isolados
            terms_to_clean = [best_code, res_best_label]
            for t in terms_to_clean:
                if not t: continue
                pattern = rf"\b{re.escape(t.lower())}\b"
                persona = re.sub(pattern, "", persona, flags=re.IGNORECASE)
            
            # Limpeza de ruído residual
            persona = persona.replace(".", " ").replace("_", " ").strip().title()
            if len(persona) > 2:
                final_label = f"{persona} ({res_best_label})" if persona.upper() != res_best_label.upper() else res_best_label

        elif score >= self.thresholds.get("human_review", 0.45):
            status = "REVIEW_CANDIDATE"

        return self._build_result(raw_value, norm_val, status, score, 
                                 best_data["traces"][0]["layer"] if best_data["traces"] else "N/A",
                                 best_code, best_data["traces"], label_override=final_label)

    def _build_result(self, raw, norm, status, score, reason, code=None, trace=None, label_override=None):
        """Helper para construir o contrato de saída padrão."""
        
        # Buscar label amigável na taxonomia
        label = "N/A"
        pos = "Geral"
        if code:
            match = next((t for t in self.taxonomy if t["code"] == code), None)
            if match:
                label = label_override or match["label"]
                pos = match.get("position", "Geral")

        return {
            "input_original": raw,
            "input_normalized": norm,
            "status": status,
            "category_code": code,
            "category_label": label,
            "position_default": pos,
            "confidence": round(score, 3),
            "reason": reason,
            "trace": trace or []
        }

# --- Declaração de Versão do Módulo (Genaja Version Hook) ---
from version_hook import declare as _vdeclare
from version import __version__
_vdeclare(__name__, __version__, "Motor MDM Enterprise Unificado com Inteligência de Purificação e Persona Extraction")
