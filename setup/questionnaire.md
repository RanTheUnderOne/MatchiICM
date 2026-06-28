# Setup - MatchiICM Onboarding

Answer all questions in one pass. Your answers populate across workspace files.
Setup configures the factory, not the product.

## Agent Identity

1. **שם הסוכן / Agent name** (e.g. "דנה לוי נדל"ן")
   - Your answer: `{{AGENT_NAME}}`

2. **מספר טלפון בוואטסאפ** (e.g. "972501234567")
   - Your answer: `{{AGENT_PHONE}}`

3. **מספר רישיון תיווך** (e.g. "12345")
   - Your answer: `{{AGENT_LICENSE}}`

4. **אימייל** (e.g. "dana@nadlanai.org")
   - Your answer: `{{AGENT_EMAIL}}`

## Brand

5. **שם המותג / Brand name** (e.g. "נדלני AI", "Matchi")
   - Your answer: `{{BRAND_NAME}}`

6. **צבע מותג ראשי** (hex, e.g. "#1a365d")
   - Your answer: `{{BRAND_COLOR}}`

7. **חתימת וואטסאפ** (2-3 שורות, e.g. "דנה לוי | נדלני AI | 050-1234567")
   - Your answer: `{{WHATSAPP_SIGNATURE}}`

## Regions

8. **ערים למיקוד** (רשימה מופרדת בפסיקים, e.g. "חיפה, נתניה, תל אביב")
   - Your answer: `{{TARGET_CITIES}}`

9. **שכונות מועדפות** (אופציונלי. e.g. "כרמל, נווה שאנן, מרכז העיר")
   - Your answer: `{{TARGET_NEIGHBORHOODS}}`

## Voice (edits `_config/voice.md`)

10. **טון דיבור** (e.g. "מקצועי וחם", "ישיר וענייני", "צעיר ואנרגטי")
    - Your answer: `{{VOICE_TONE}}`

11. **שפת ברירת מחדל** (he / en / both)
    - Your answer: `{{DEFAULT_LANGUAGE}}`

12. **OpenAI API key** — set as `$OPENAI_API_KEY` env var on Hermes server. Shared across all bots. Never stored in workspace.
    - Your answer: `{{OPENAI_API_KEY}}`

## Tools

13. **Apify API token** (לסריקת פייסבוק ו-Yad2)
    - Your answer: `{{APIFY_TOKEN}}`

## Derived Fields

The following are computed from your answers above. Review but do not edit:

- `{{AGENT_FULL_SIGNATURE}}` ← `{{AGENT_NAME}} | {{BRAND_NAME}} | {{AGENT_PHONE}}`
- `{{MCP_USER_ID}}` ← `{{AGENT_EMAIL}}`
- `{{DEFAULT_TIMEZONE}}` ← `Asia/Jerusalem`

## After Setup

1. Verify: `grep -r "{{" .` returns nothing (no unresolved placeholders)
2. Run: `py scripts/icm_pipeline.py` - all 5 stages PASS
3. Type `status` to verify pipeline diagram shows READY
