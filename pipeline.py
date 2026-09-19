import json
# Pehle ye tha: from .llm import ask_json
from agents.llm import ask_json
# YA
from .llm import ask_json

def source_text(sources):
    return "\n\n".join(
        f"=== SOURCE: {s['name']} ===\n{s.get('text','[Image source]')}"
        for s in sources
    )

def run_pipeline(sources):
    material = source_text(sources)

    extraction = ask_json(f'''
You are the Extraction Agent.
Extract important factual claims from the sources. Focus on dates,
deadlines, requirements, amounts, names, instructions and conditions.
Return JSON:
{{"claims":[{{"id":"C1","claim":"...","source":"filename","evidence":"short quote"}}]}}
Never invent information.

SOURCES:
{material}
''')

    comparison = ask_json(f'''
You are the Comparison Agent.
Group claims referring to the same fact and compare their values.
Return JSON:
{{"groups":[{{"claim":"canonical claim","items":[{{"source":"filename","value":"...","evidence":"..."}}]}}]}}
Use only supplied information.

CLAIMS:
{extraction}
''')

    conflicts = ask_json(f'''
You are the Conflict Detection Agent.
Find contradictions, consistent claims and unclear claims.
Return JSON:
{{
"conflicts":[{{"claim":"...","status":"CONFLICT","explanation":"...","evidence":[{{"source":"...","text":"..."}}]}}],
"consistent":[{{"claim":"...","evidence":[{{"source":"...","text":"..."}}]}}],
"unclear":[{{"claim":"...","reason":"..."}}]
}}
Do not decide which source is correct unless the evidence explicitly establishes it.

COMPARISON:
{comparison}
''')

    final = ask_json(f'''
You are the Verification Agent.
Create the final evidence-based report from the pipeline below.
Preserve uncertainty. Do not invent facts.
Return JSON with keys:
summary, claims, conflicts, consistent, unclear.

EXTRACTION:
{extraction}

COMPARISON:
{comparison}

CONFLICT ANALYSIS:
{conflicts}
''')

    try:
        return json.loads(final)
    except Exception:
        return {"summary":"Invalid model response. Run again.",
                "claims":[],"conflicts":[],"consistent":[],"unclear":[]}
