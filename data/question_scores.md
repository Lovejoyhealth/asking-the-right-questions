# Question scores — working set of Oct 26, 2026

Deterministic text scoring by `src/audit_questions.py` (standard library only, no AI calls). Scored against the freeze date Oct 26, 2026. FLAG = a plain finding from the wording itself. REVIEW = a human should look; the scorer is not issuing a verdict.

## Counts

- Questions scored: 48
- Questions with at least one flag: 31
- NO_SOURCE_CUE: 9
- NUMERIC_CLAIM_REVIEW: 21
- PAST_DATE: 5

## Flagged questions, with reasons

### Q01 — AI models and releases
> Will OpenAI publicly release GPT-5 by December 31, 2026?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"

### Q02 — AI models and releases
> Will Google DeepMind release Gemini 3 Ultra before June 30, 2027?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"

### Q03 — AI models and releases
> Will Anthropic publicly release Claude Opus 5 by March 31, 2027?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"

### Q04 — AI models and releases
> Will Meta publicly release Llama 4 by November 15, 2026?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"

### Q05 — US politics and the 2026 midterms
> Will the Democratic Party hold a majority of seats in the US House of Representatives on January 3, 2027?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"

### Q06 — US politics and the 2026 midterms
> Will the Republican Party hold a majority of seats in the US Senate on January 3, 2027?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"

### Q07 — US politics and the 2026 midterms
> Will voter turnout in the November 3, 2026 midterm elections exceed 50 percent of eligible voters as reported by December 31, 2026?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "50 percent of eligible"

### Q09 — the US economy and jobs
> Will the US unemployment rate be below 4 percent on December 31, 2026 as reported by the Bureau of Labor Statistics?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "4 percent on December"

### Q10 — the US economy and jobs
> Will US nonfarm payroll employment exceed 160 million by July 31, 2026 according to the Bureau of Labor Statistics?
- **PAST_DATE** (FLAG): The deadline in the wording is already in the past (before Oct 26, 2026), so the question can no longer be settled in the future. Evidence: "July 31, 2026 (parsed as 2026-07-31)"
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "160 million by July"

### Q11 — the US economy and jobs
> Will the US economy have added at least 2 million jobs by December 31, 2026 according to the Bureau of Labor Statistics?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "2 million jobs by"

### Q12 — the US economy and jobs
> Will the US labor force participation rate be above 62 percent on January 1, 2027 as reported by the Federal Reserve Economic Data?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "62 percent on January"

### Q13 — interest rates and the Federal Reserve
> Will the Federal Reserve federal funds target rate be at or below 4 percent on December 31, 2026?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "4 percent on December"

### Q14 — interest rates and the Federal Reserve
> Will the Federal Reserve announce at least one interest rate cut before June 30, 2026?
- **PAST_DATE** (FLAG): The deadline in the wording is already in the past (before Oct 26, 2026), so the question can no longer be settled in the future. Evidence: "June 30, 2026 (parsed as 2026-06-30)"

### Q15 — interest rates and the Federal Reserve
> Will the Federal Reserve federal funds target rate be above 3 percent on January 1, 2027?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "3 percent on January"

### Q17 — housing and rent
> Will the US national median rent be above $2000 in December 2026 according to Apartment List?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "$2000"

### Q18 — housing and rent
> Will the average asking rent in New York City exceed $3600 per month on December 31, 2026 according to StreetEasy?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "$3600"

### Q19 — housing and rent
> Will the Freddie Mac 30-year fixed mortgage rate be below 6 percent on June 30, 2027?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "6 percent on June"

### Q20 — housing and rent
> Will US single-family housing starts exceed 11 million annualized units in any month before December 31, 2027 according to the Census Bureau?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "11 million annualized units"

### Q23 — climate and extreme weather
> Will global average sea level rise exceed 105 millimeters above the 1993 baseline according to NASA by December 31 2026?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "105 millimeters above the"

### Q24 — climate and extreme weather
> Will California record at least 500000 acres burned by wildfires in 2026 according to Cal Fire by January 15 2027?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "500000 acres burned by"

### Q25 — public health
> Will the US CDC report that national adult smoking prevalence is below 10 percent as of December 31, 2026 according to published CDC data?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "10 percent as of"

### Q33 — pro sports championships
> Will the Kansas City Chiefs win Super Bowl LX by February 8, 2026?
- **PAST_DATE** (FLAG): The deadline in the wording is already in the past (before Oct 26, 2026), so the question can no longer be settled in the future. Evidence: "February 8, 2026 (parsed as 2026-02-08)"

### Q35 — pro sports championships
> Will the Boston Celtics win the 2026 NBA Championship by June 30, 2026?
- **PAST_DATE** (FLAG): The deadline in the wording is already in the past (before Oct 26, 2026), so the question can no longer be settled in the future. Evidence: "June 30, 2026 (parsed as 2026-06-30)"

### Q41 — energy and gas prices
> Will the US national average price for regular gasoline exceed 4 dollars per gallon on December 31, 2026 according to AAA?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "4 dollars per gallon"

### Q42 — energy and gas prices
> Will the Henry Hub natural gas spot price close above 5 dollars per MMBtu on June 30, 2027 according to the US Energy Information Administration?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "5 dollars per MMBtu"

### Q43 — energy and gas prices
> Will Brent crude oil futures settle above 100 dollars per barrel on September 30, 2026 according to ICE?
- **PAST_DATE** (FLAG): The deadline in the wording is already in the past (before Oct 26, 2026), so the question can no longer be settled in the future. Evidence: "September 30, 2026 (parsed as 2026-09-30)"
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "100 dollars per barrel"

### Q44 — energy and gas prices
> Will the average US residential electricity price exceed 18 cents per kilowatt hour on December 31, 2026 according to the US Energy Information Administration?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "18 cents per kilowatt"

### Q45 — big tech companies
> Will Apple reach a market capitalization of over 4 trillion dollars at any time before December 31, 2026?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "4 trillion dollars at"

### Q46 — big tech companies
> Will Microsoft report quarterly revenue above 75 billion dollars in any earnings announcement made on or before June 30, 2027?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "75 billion dollars in"

### Q47 — big tech companies
> Will Alphabet report more than 3 billion monthly active YouTube users in any public disclosure by December 31, 2026?
- **NUMERIC_CLAIM_REVIEW** (REVIEW): The question states a specific number. A human must verify that figure against a source before the question is used; the scorer does not judge the figure itself. Evidence: "3 billion monthly active"

### Q48 — big tech companies
> Will Amazon launch a fully autonomous delivery drone service for commercial customers in the United States before July 1, 2027?
- **NO_SOURCE_CUE** (FLAG): The wording names no source or authority that settles the answer (no 'according to', official body, announcement, or result cue in the text). Evidence: "no settling-authority cue from the scorer's cue list appears in the question text"
