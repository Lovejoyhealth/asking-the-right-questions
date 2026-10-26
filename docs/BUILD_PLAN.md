# Build plan — "Are You Asking the Right Questions?"
## Meta Global AI Developer Hackathon, Startup track — locked Mon Oct 26, 2026

**The project (one line):** Muse Spark writes prediction-market questions from trending
topics; Brian's own audit engine — built and tested before this event — grades each
question for one-sided wording, hidden assumptions, order effects, and whether it can
be settled cleanly; flagged questions are rewritten and re-scored live. Their models
write the market, play the market, and fix the market. The referee is the only thing
in the room that isn't theirs.

**Title source:** Chief Liz Danvers' repeated line in *True Detective: Night Country* —
"We are just not seeing it. Not asking the right questions."

**Path decision (Brian's call, Mon Oct 26, 09:09 EDT):** the question audit, NOT the
cue-to-execution glasses build. Reason, in one line: the audit is ~2/3 built already and
needs nobody else; the glasses build starts from zero (no glasses in hand, Valor
outreach unmade, motion-data access unknown) inside 9 days. SecondSight stays parked
(build sheet + cue prototype already written) as the post-hackathon swing.

**Deadline: Wed Nov 4, 2026, 9:00pm ET**, via the cerebralvalley.ai portal.
**Plan rule: the entry is submittable by end of Tue Nov 3.** Nov 4 is buffer only.

**Judging weights:** Impact 30% · Use of Meta AI Tooling 25% · Demo 25% ·
Technical Depth & Execution 20%.

**Time budget (Brian's week is limited):** Brian's hours are for decisions, reviews,
and the demo video — target ~1 hour/day of his time, in one sitting. Atlas does the
assembly and reports at each checkpoint. Best Buy shifts for Oct 26–Nov 2 are
UNCONFIRMED — days below flex around them; no day carries more than one must-do.

---

## What already exists (do not rebuild)
- The audit engine: Bayesian model (Pyro) with uncertainty ranges; quantum module
  (PennyLane) for order effects; shuffled-data / permutation null checks.
  145 automated tests passing (as of the Oct 22 application).
- The Octagon audit run: 100 real AI-generated research questions scored
  (~1 in 8 one-sided; independent re-scoring agreed 95/100) + the 1-page PDF.
- The harvest → label → score → one-pager workflow, proven on the scanner project.

## The spine (never cut)
1. **Wording + assumption score** — is the question tilted or loaded? (exists)
2. **Settleability score** — NEW: can this question be settled cleanly?
   Named source + named date + one unambiguous outcome. (the only new axis)
3. **Rewrite loop** — Spark rewrites a flagged question; the engine re-scores it;
   the before/after is the demo moment.

## Cut order (frozen Oct 22, still in force, first cut first)
1. Shrink the Bayesian answer-run to a sample (fewer forecaster personalities,
   fewer repeats) — never cut the spine.
2. Drop the quantum order module from the LIVE demo path (keep it in the
   write-up + run it on the sample) if Fri Oct 30 ends behind.
3. Demo page goes static (pre-run results, one live rewrite) if Nov 1 ends behind.

---

## Day by day

### Mon Oct 26 — Setup day (Brian ~30 min)
- [ ] Acceptance email + Official Rules read (Atlas check in flight): confirm
      deadline/format, teammate rules, IP terms, and — critical — whether the
      submission needs a repo link. (If a repo link is required: a small public
      SHOWCASE repo — audit PDF + results + plain-English README. The engine
      stays private. Decision is Brian's, in daylight, if it comes up.)
- [x] Confirm how the $150 credits arrive. DONE Oct 26: Brian claimed via the
      form, put a card on the account per the email's own condition, and the
      $150 credit LANDED on the Billing page (his report: "FREE CREDIT HIT").
- [x] Get the Meta Model API key (dev.meta.ai/api-keys), stored in the Secure
      Vault (custom.meta-model-api). Tier rule enforced in the helper: model
      `muse-spark-1.3` (Standard) only; the contributor model is refused.
- [x] Checkpoint PASSED Oct 26: test call returned 200 on Standard, and a
      generation call produced a real forecast question. Token lesson: give
      generation calls max_tokens ≥ 1200 (reasoning eats small budgets).

### Tue Oct 27 — Spark writes the questions
- [ ] Generation hookup: Spark writes forecast questions from a short list of
      trending topics (we supply the topics; no live news scraping needed).
- [ ] Save 30–50 generated questions as the working set, frozen with timestamps.
- [ ] Checkpoint: the working set exists and at least a few questions are
      visibly flawed (if Spark writes only clean questions, seed topics with
      contested ones — the demo needs real flags).

### Wed Oct 28 — Spark plays the market
- [ ] Forecaster crowd: Spark personalities answer each question, each question
      asked in BOTH orders (options flipped), so the order-effect check has data.
- [ ] Engine scores the answers; order effects measured against shuffled nulls.
- [ ] Checkpoint: a results table exists for the working set (question, wording
      flags, order-effect size, engine verdict).

### Thu Oct 29 — The new axis: settleability
- [ ] Build the settleability check: does the question name a source, a date,
      and one unambiguous outcome? Three plain yes/no tests per question.
- [ ] Wire it into the score sheet next to the wording score.
- [ ] Checkpoint: every working-set question carries both scores.

### Fri Oct 30 — The rewrite loop
- [ ] Spark rewrites each flagged question using only the flag reasons
      (no engine internals shared with it).
- [ ] Engine re-scores the rewrites; before/after deltas recorded.
- [ ] Checkpoint: at least 5 clean before/after pairs for the demo.
      (Decision point: if behind, apply cut #2 here.)

### Sat Oct 31 – Sun Nov 1 — The demo page
- [ ] One page: paste/see a question → scores → flags explained in plain words →
      "rewrite it" → new scores. Live if possible; cut #3 if not.
- [ ] The Oct 31 BTC paper position settles in the background; ignore it.
- [ ] Checkpoint: Brian runs the page once, start to finish, on his phone.

### Mon Nov 2 — Demo video + write-up
- [ ] Video (target 2–3 min): the Danvers line as the opener; one bad question
      flagged live; the rewrite; the before/after scores; close on the referee
      line ("their models write the market — mine grades it").
- [ ] Submission text drafted from the application's own two answers, updated
      with real build results (no inflated claims; the 95/100 agreement and
      the test count are the credibility lines).
- [ ] Checkpoint: Brian watches the video once and approves the text.

### Tue Nov 3 — Submit
- [ ] Full submission filed by end of day. Nov 4 stays untouched buffer.
- [ ] Repo/showcase decision executed only if the rules check demands it.

### Wed Nov 4 — Buffer only
- [ ] 9:00pm ET deadline. Anything done today is a bonus fix, never the plan.

---

## Outside dependencies: NONE for the build
- **Rebecca Kossnick:** the acceptance lifted Brian's hold on the follow-up DM.
  Sending the short ask (teammate for insight only — what Forecast taught about
  what makes a question work) is Brian's separate call, any time this week.
  The plan neither needs her nor counts her. Nothing is drafted until he asks.
- **Valor Vision / SecondSight:** parked by the path decision. No outreach
  needed for this entry.

## Rules-check results (Mon Oct 26, verified — full note: acceptance-and-rules-check-2026-10-26.md)
- **Credits:** $150 Meta Model API credit, claimed via a Google Form in the Oct 26
  credits email; distributed in batches; check the dev.meta.ai Billing page.
  **Catch: a credit card must be on the account before the credits can be used or
  any API call made.** The email's safeguard is a "Spend Limit" notification on the
  Billing page (a notification = an alert, not a hard lock). Expected total use is a
  few dollars of the $150. Claim deadline = Nov 4, 9:00pm ET; claim early so credits
  land before Tue–Wed generation work. **Card decision is Brian's, pending.**
- **Repo link: NOT required** by any published rule. Engine stays private. Only open
  item: the Nov 4 submit form's fields sit behind the login; if a repo field appears,
  the showcase-repo choice applies then.
- **Deadline/format CONFIRMED:** Nov 4, 9:00pm ET, Cerebral Valley portal.
  Judging Nov 4–8, finals Nov 9.
- **Demo video is SCORED** (part of the 25% Demo slice) — the Mon Nov 2 video step
  is load-bearing, not polish.
- **IP CONFIRMED:** entrant retains ownership; organizers' license covers the
  Submission and anything provided/shared during the event. Unshared code untouched.
- **Teammates:** must themselves be accepted participants, and are named in the
  submission itself. No evidence Kossnick applied → she cannot be listed officially;
  any role for her is informal insight, outside the submission. Nothing to decide today.
- **Kickoff: TODAY Mon Oct 26, 12:00pm ET**, livestream on the Cerebral Valley
  platform. Workshops Oct 27–Nov 4 + Discord office hours.
- Partner credits exist for select participants (Baseten $100, Modal $100,
  Fireworks $25) for running Meta open-weights models — noted, not needed.

## Kickoff learnings (Brian's report from the livestream, Mon Oct 26, ~12:31pm ET)
First-hand from the kickoff; these supersede the public-pages check where they differ.
- **The repo needs to be public.** The morning rules check found no published rule
  requiring a repo link — the kickoff states the submission repo is public. Route
  decision is Brian's (see below): the recommended route is a NEW public repo for
  this project, not a flip of the private engine repo.
- **Pre-existing code must be declared.** The submission states what code existed
  before the event (the Bayesian engine, the quantum order module, the null-check
  machinery, the 145 tests) with its dates. Disclosure draft:
  files/prior-work-disclosure-draft-2026-10-26.md. The commit history under
  Brian's account is the timestamped proof; the disclosure and the history agree.
- **The video carries real weight** (confirmed scored, 25% Demo slice). Structure,
  Brian's direction: START BROAD with the bold vision — detectives, lawyers
  questioning witnesses, surveys, sales, LLMs prompting — "it all starts with the
  right questions," with the Danvers beat played for humor (a fictional detective
  solving crimes on the strength of asking the right question). THEN NARROW to one
  single problem for the code and the demo: AI writes prediction-market questions
  at scale, nobody independent checks them, one live question gets flagged and
  rewritten. Broad vision, single problem. Outline:
  files/video-outline-2026-10-26.md.
- Plain-language IP note for the repo decision: a public repo is VISIBLE, not
  given away. With no license file added, default copyright holds — people can
  read the code, they may not legally reuse it. Visibility is what the judges
  need; ownership does not move.

## Guardrails (standing, restated for the build)
- Paper/$0 discipline: the $150 event credits are the only spend; no card added.
- Standard tier only, everywhere, for code and prompts.
- The engine repo stays private; judges see only what the submission provides.
- Nothing is submitted before Brian approves the final text and video.
- Every claim in the write-up traces to a run that actually happened
  (no implied model runs, no inflated record).
