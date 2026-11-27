import json
import re
from typing import Dict, Any
import config

# Try importing google-genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

SYSTEM_INSTRUCTION = """
You are an expert UPSC Civil Services Examination (CSE) Mentor and Current Affairs Specialist.
Your task is to analyze official PIB (Press Information Bureau) releases and transform them into concise, high-yield study material for UPSC aspirants.

CRITICAL LANGUAGE RULE:
- ALL OUTPUT MUST BE 100% IN ENGLISH ONLY.
- Under NO circumstances should any Hindi, Devanagari script (e.g. हिन्दी), or regional language text be included in any field.
- If the original article, title, or ministry name is in Hindi or mixed, TRANSLATE IT COMPLETELY INTO FLUENT, PROFESSIONAL ENGLISH.

Syllabus Framework:
- GS-1: Indian Heritage & Culture, History, Geography, Society.
- GS-2: Governance, Constitution, Polity, Social Justice, International Relations.
- GS-3: Technology, Economic Development, Bio-diversity, Environment, Security & Disaster Management.
- GS-4: Ethics, Integrity and Aptitude.
- Prelims Pointer: Specific factual schemes, portals, acronyms, or reports.

Guidelines:
1. Filter aggressively: Discard purely ceremonial speeches, protocol greetings, condolences, routine state government political visits, or minor routine transfers. Only mark RELEVANT if it has substantive value for UPSC CSE.
2. If NOT relevant, set "is_relevant": false.
3. If RELEVANT, produce:
   - "title_en": Title translated/refined in clear English.
   - "ministry_en": Ministry name in English (e.g. "Ministry of Ayush", "Vice President's Secretariat").
   - "gs_paper": One of ["GS-1", "GS-2", "GS-3", "GS-4", "Prelims Pointer"]
   - "short_summary": 60-80 words plain-English summary answering What, Why, and Key provisions.
   - "prelims_facts": 2-3 crisp bullet points in English with factual data.
   - "mains_pointer": 1 sentence in English explaining its dimension for Mains answer writing.
"""

USER_PROMPT = """
Analyze this PIB release:
Title: {title}
Ministry: {ministry}
Content: {content}

Respond ONLY with valid JSON in this exact structure (ENGLISH ONLY):
{{
  "is_relevant": true/false,
  "relevance_reason": "Short reason in English",
  "title_en": "Title in 100% English",
  "ministry_en": "Ministry name in 100% English",
  "gs_paper": "GS-1 / GS-2 / GS-3 / GS-4 / Prelims Pointer",
  "short_summary": "60 to 80 words crisp summary in English",
  "prelims_facts": "• Bullet 1\\n• Bullet 2 (English only)",
  "mains_pointer": "Significance for Mains answer writing (English only)"
}}
"""

class UPSCNewsAgent:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.client = None
        if self.api_key and GENAI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[Agent] Warning: Could not initialize Gemini client: {e}")

    def analyze(self, title: str, ministry: str, content: str) -> Dict[str, Any]:
        """
        Analyzes PIB release content using Gemini Flash model.
        Falls back to rule-based analysis if API key is not configured.
        """
        if not self.client:
            return self._fallback_rule_analyzer(title, ministry, content)

        # Try models in order of availability
        models_to_try = ["gemini-flash-latest", "gemini-3.8-flash", "gemini-2.5-flash"]
        truncated_content = content[:4000] if content else title
        prompt = USER_PROMPT.format(title=title, ministry=ministry, content=truncated_content)

        for model_name in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        temperature=0.2,
                    )
                )

                result_text = response.text.strip()
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]

                data = json.loads(result_text)
                return data

            except Exception as e:
                # Try next model in list
                continue

        # If all API calls fail, gracefully fall back to heuristic rule analyzer
        return self._fallback_rule_analyzer(title, ministry, content)

    def _contains_indic_script(self, text: str) -> bool:
        """Checks if text contains Devanagari or other Indic Unicode characters."""
        return any('\u0900' <= char <= '\u0d7f' for char in text)

    def _fallback_rule_analyzer(self, title: str, ministry: str, content: str) -> Dict[str, Any]:
        """
        Fallback heuristic analyzer when Gemini API is not yet provided or unreachable.
        Enforces 100% English only.
        """
        # If title or content is mostly in Hindi / Devanagari script and we don't have LLM to translate, discard it
        if self._contains_indic_script(title) and not any(c.isascii() and c.isalpha() for c in title):
            return {
                "is_relevant": False,
                "relevance_reason": "Non-English release skipped (English-only mode active).",
                "title_en": "",
                "ministry_en": "",
                "gs_paper": "None",
                "short_summary": "",
                "prelims_facts": "",
                "mains_pointer": ""
            }

        text = f"{title} {ministry} {content}".lower()

        # Routine ceremonial filters
        ignore_keywords = ["condoles", "pays tribute", "greets", "inaugurates cricket", "birthday", "felicitates"]
        if any(w in text for w in ignore_keywords):
            return {
                "is_relevant": False,
                "relevance_reason": "Ceremonial or protocol update.",
                "title_en": title,
                "ministry_en": ministry,
                "gs_paper": "None",
                "short_summary": "",
                "prelims_facts": "",
                "mains_pointer": ""
            }

        # GS classification heuristics
        gs_paper = "GS-3"
        if any(w in text for w in ["constitution", "court", "election", "judiciary", "bilateral", "treaty", "parliament", "foreign"]):
            gs_paper = "GS-2"
        elif any(w in text for w in ["culture", "heritage", "monument", "tribal", "archaeological", "history"]):
            gs_paper = "GS-1"
        elif any(w in text for w in ["economy", "rbi", "inflation", "gdp", "space", "isro", "environment", "climate", "agriculture", "fertilizer"]):
            gs_paper = "GS-3"
        elif any(w in text for w in ["ethics", "integrity", "vigilance", "anti-corruption"]):
            gs_paper = "GS-4"

        # Generate a brief English summary snippet
        clean_content = "".join([c for c in content if ord(c) < 128])
        clean_title = "".join([c for c in title if ord(c) < 128]).strip() or "PIB Press Release"
        clean_ministry = "".join([c for c in ministry if ord(c) < 128]).strip() or "Government of India"

        summary_snippet = (clean_content[:250] + "...") if len(clean_content) > 250 else clean_content
        if not summary_snippet:
            summary_snippet = f"Press Release by {clean_ministry}: {clean_title}."

        return {
            "is_relevant": True,
            "relevance_reason": f"Heuristic match on key administrative topics ({gs_paper}).",
            "title_en": clean_title,
            "ministry_en": clean_ministry,
            "gs_paper": gs_paper,
            "short_summary": summary_snippet,
            "prelims_facts": f"• Nodal Ministry: {clean_ministry}\n• Topic: {clean_title}",
            "mains_pointer": "Relevant for socio-economic policy and governance analysis."
        }

if __name__ == "__main__":
    agent = UPSCNewsAgent()
    sample_title = "Cabinet approves PM-PRANAM scheme to promote alternative fertilizers"
    sample_min = "Ministry of Chemicals and Fertilizers"
    sample_content = "The Cabinet Committee on Economic Affairs today approved the PM-PRANAM scheme with an outlay to incentivize States and Union Territories to promote alternative fertilizers and balanced use of chemical fertilizers."
    res = agent.analyze(sample_title, sample_min, sample_content)
    print("Agent Result:", json.dumps(res, indent=2))
