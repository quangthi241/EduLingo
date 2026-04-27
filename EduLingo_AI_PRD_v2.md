**PRODUCT REQUIREMENT DOCUMENT**

**EduLingo AI — v2.0**

*AI-Powered Private Learning Pathway for English Mastery*

Version 2.0  |  April 2026  |  Revised Skill Taxonomy & UX Specification

---

# 1. Executive Summary

EduLingo AI is a web-based intelligent tutoring system that uses AI to generate **private learning pathways** for every English learner, aligned with CEFR A1–B2. Version 2.0 refocuses the product around a **skill-first pedagogy**: four productive/receptive skills and two cross-cutting sub-skills.

| Main Skills (4) | Sub-Skills (2) | CEFR Scope | AI Components | Platform |
| :---: | :---: | :---: | :---: | :---: |
| **Listening · Reading · Speaking · Writing** | **Grammar · Vocabulary** | A1–B2 | 4 distinct AI systems | Web (responsive) |

**Core differentiator:** every learner receives a private path, generated and continuously re-tuned by AI, that targets their exact skill gaps and matches their study time, goal, and preferred skill mix.

---

# 2. Skill Taxonomy (v2 Change)

## 2.1 Four Main Skills

| Skill | Definition | Primary Assessment |
| ----- | ----- | ----- |
| **Listening** | Comprehension of spoken English across accents and speeds | Audio comprehension MCQs, dictation, gap-fill |
| **Reading** | Comprehension, inference, and skimming of written passages | Passage + MCQs, inference questions, speed reading |
| **Speaking** | Pronunciation, fluency, intonation, conversational production | Mic-based AI scoring (pronunciation, fluency, intonation), shadowing, role-play |
| **Writing** | Coherent written production across common registers | Guided prompts, AI feedback on grammar, vocabulary, clarity |

## 2.2 Two Sub-Skills (cross-cutting)

| Sub-Skill | Role in Pathway |
| ----- | ----- |
| **Grammar** | Tagged on every lesson and quiz; drives a separate mastery score that boosts/weakens pathway weighting across all 4 main skills |
| **Vocabulary** | Auto-extracted from all skill lessons; surfaced through SM-2 spaced repetition; tracked as its own mastery score |

Sub-skills are **not standalone tracks** — they live inside each of the four main skills, but their mastery is measured independently so the AI can diagnose "your Reading is B1 but your Grammar is holding you at A2."

---

# 3. Problem Statement & Research Foundation

Traditional e-learning treats learners identically and teaches skills in isolation. The research base supporting EduLingo AI v2:

- **Static curricula** fail to adapt content to learner ability (Scientific Reports, Aug 2025).
- **AI-assisted CEFR placement** reaches 95% accuracy vs. 80–85% human (SmallTalk2Me benchmark, 2024).
- **Spaced repetition** (Ebbinghaus) is absent from most web platforms, reducing retention (Kharwal et al., 2022).
- **LLM conversational tutors** drive +75% speaking gains over 8 weeks (Gliglish, 2024).
- **Pronunciation ASR** using wav2vec2/Whisper-based models achieves phoneme-level accuracy suitable for CEFR A1–B2 scoring (2025 research consensus).

## AI Theoretical Framework

| Framework | Application |
| ----- | ----- |
| **Bayesian Knowledge Tracing (BKT)** | Mastery per skill × sub-skill, updated every quiz/exercise |
| **Item Response Theory (IRT)** | CAT placement and dynamic difficulty selection |
| **Spaced Repetition (SM-2)** | Vocabulary and grammar-rule flashcards |
| **Constructivist Dialogue** | AI Tutor drives active production, not passive consumption |

---

# 4. Product Goals & KPIs

## 4.1 Goals

1. Deliver accurate CEFR placement across all 4 skills within 15 minutes.
2. Generate a private weekly pathway from placement, goal, weak-skill ranking, and daily study time.
3. Provide an always-on AI Tutor calibrated to the learner's CEFR level.
4. Re-adjust the pathway after every session based on quiz performance and SR schedule.
5. Give learners transparent progress across all 4 skills + 2 sub-skills.

## 4.2 KPIs

| Metric | Target | Priority |
| ----- | ----- | :---: |
| CEFR Placement Accuracy (per skill) | ≥ 85% agreement w/ evaluator | Critical |
| Pathway Relevance (learner survey) | ≥ 4.0 / 5.0 | High |
| AI Tutor Helpfulness | ≥ 80% positive | High |
| Lesson Completion Rate / week | ≥ 60% | High |
| Speaking Score Improvement (8-week) | +15 pts average | High |
| 7-Day Retention | ≥ 40% | Medium |
| Vocabulary Recall (7-day SR re-test) | ≥ 75% | Medium |
| AI Response Latency (first token) | < 3 s | High |
| AI Topic Containment | < 5% off-topic | Critical |

---

# 5. User Personas

| Persona | Profile | Primary Needs |
| ----- | ----- | ----- |
| **Beginner (Mai, 22)** | A1–A2, 30–45 min/day, job-prep goal | Clear placement, step-by-step path, instant AI support |
| **Self-Improver (Hung, 28)** | B1, 20 min/day, business communication | Skip-known-content path, Speaking practice, Writing feedback |
| **Speaking-Focused (Linh, 19)** | A2, IELTS Speaking goal | Heavy Speaking track, pronunciation drills, role-play |
| **Admin (Academic Staff)** | Manages content | Lesson CRUD, learner oversight, AI insights |

---

# 6. Functional Requirements

## FR-01 · Authentication & Profile

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| FR-01-1 | Email registration + bcrypt (cost ≥ 12) | Must |
| FR-01-2 | JWT 7-day session + refresh token | Must |
| FR-01-3 | RBAC: `learner`, `admin` | Must |
| FR-01-4 | Profile: CEFR per skill, goal, weak skills, daily minutes, skill priority order | Must |
| FR-01-5 | Google OAuth | Should |

## FR-02 · Adaptive CEFR Placement (4-Skill CAT)

The placement test returns a **per-skill CEFR band** using Computer Adaptive Testing with IRT.

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| FR-02-1 | Pre-test survey: goal (Communication / TOEIC / Foundation / IELTS), daily minutes (15/30/45/60+), priority skills | Must |
| FR-02-2 | Item bank ≥ 80 items tagged by CEFR + skill + sub-skill | Must |
| FR-02-3 | Separate mini-CAT per skill — Listening, Reading, Grammar/Vocab (written), Writing prompt, Speaking prompt | Must |
| FR-02-4 | Speaking mini-test: 2 read-aloud + 1 picture description; ASR + AI scoring | Must |
| FR-02-5 | Writing mini-test: 1 short prompt (80–120 words); LLM rubric scoring | Must |
| FR-02-6 | Terminates per skill at SE threshold or 5–8 items; total ≈ 18–22 min | Must |
| FR-02-7 | Score report: overall band + **per-skill** bands + sub-skill scores + radar + weakness ranking | Must |
| FR-02-8 | Retake allowed after 30 days; history archived | Should |

## FR-03 · AI-Powered Private Learning Pathway

Private weekly path built from a multi-factor weighted scoring model, re-run after every session.

### 3.1 Input Variables

| Input | Weight |
| ----- | :---: |
| Per-skill CEFR score | 35% |
| Weak-skill priority (ranks bottom 2 skills higher) | 30% |
| Sub-skill mastery delta (Grammar/Vocab gaps) | 15% |
| Learning goal (Communication / TOEIC / IELTS / Foundation) | 12% |
| Daily study time (minutes → lessons per week) | 8% |

### 3.2 Pathway Composition Rules

- A weekly path blends all 4 main skills by the learner's priority ratio (default 25/25/25/25; adjustable).
- At least one Speaking and one Writing exercise per week, regardless of priority (prevents passive learning).
- Vocab SR cards and Grammar drills are inserted between main-skill lessons.
- Dynamic re-adjustment:
  - Quiz < 60% → lesson re-queued at higher priority; CEFR held for that skill.
  - 3 consecutive ≥ 85% in a skill → propose next CEFR level for that skill only.
  - Speaking fluency score < 70 → add 2 shadowing exercises next week.
  - Writing clarity score < 70 → add 1 guided writing next week.

## FR-04 · Lesson Content & In-Lesson Practice

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| FR-04-1 | Each lesson: title, CEFR tag, main-skill tag, sub-skill tag(s), content, quiz | Must |
| FR-04-2 | Content types: reading passage, audio + transcript, video, vocabulary sets, grammar explanations, speaking prompts, writing prompts | Must |
| FR-04-3 | Quiz types per skill: MCQ, fill-blank, rearrange, match, dictation, pronunciation, short-answer | Must |
| FR-04-4 | Immediate AI feedback per answer | Must |
| FR-04-5 | New vocabulary auto-added to learner's SR deck | Must |
| FR-04-6 | On-demand AI practice generator within any lesson | Should |

## FR-05 · Skill Practice Modules (v2 new)

Each main skill has a dedicated practice surface, accessible from the Practice sidebar.

### 5.1 Listening Practice

| ID | Requirement |
| ----- | ----- |
| FR-05L-1 | Audio player with replay, slow-speed (0.75×), playback-count limit |
| FR-05L-2 | Modes: Comprehension (MCQ), Dictation (type what you hear), Fill Missing Words |
| FR-05L-3 | Transcript reveal after submission |
| FR-05L-4 | CEFR-graded audio library, accent variety (US/UK/AU) |

### 5.2 Reading Practice

| ID | Requirement |
| ----- | ----- |
| FR-05R-1 | Passage display 100–400 words, CEFR-graded |
| FR-05R-2 | Modes: Comprehension (MCQ), Skimming (timed main-idea), Inference, Speed Reading (WPM) |
| FR-05R-3 | Inline vocabulary tap-to-define; tapped words auto-added to SR deck |
| FR-05R-4 | Per-passage tags: new vocab count, grammar focus |
| FR-05R-5 | AI Hint button (costs one hint token per exercise set) |

### 5.3 Speaking Practice (v2 new — was v2.0 roadmap in v1)

| ID | Requirement |
| ----- | ----- |
| FR-05S-1 | Browser mic capture via Web Audio API; 30 s max per prompt |
| FR-05S-2 | Modes: Pronunciation (read-aloud), Shadowing (echo native audio), Role-play (AI turn-taking), Free Talk (60 s) |
| FR-05S-3 | AI scoring: Pronunciation (phoneme-level), Fluency (WPM + pause), Intonation (pitch contour match) — each 0–100 |
| FR-05S-4 | Structured AI feedback: 1–3 positive notes + 1–3 improvement notes with examples |
| FR-05S-5 | Native reference audio always available for comparison |
| FR-05S-6 | Waveform visualization during recording + playback |

### 5.4 Writing Practice

| ID | Requirement |
| ----- | ----- |
| FR-05W-1 | Modes: Guided Writing (prompt + scaffold), Sentence Building, Paragraph Correction, Free Writing |
| FR-05W-2 | LLM rubric scoring: Grammar, Clarity, Vocabulary (0–100 each) |
| FR-05W-3 | Inline corrections with original → suggested diff |
| FR-05W-4 | Writing tips panel (CEFR-appropriate) |
| FR-05W-5 | Submit for Review → structured feedback card |

## FR-06 · AI Tutor Chatbot

| ID | Requirement |
| ----- | ----- |
| FR-06-1 | Constrained LLM prompt: English-learning only; CEFR-calibrated complexity |
| FR-06-2 | Supported intents: grammar, vocab, correction, translation-to-English, exercise generation, writing feedback, pronunciation tips |
| FR-06-3 | Format: explain → 2 examples → practice prompt |
| FR-06-4 | Out-of-scope redirect without full LLM call |
| FR-06-5 | Chat history 30 days; suggested prompts on empty state |
| FR-06-6 | Writing-review mode: paste paragraph → structured feedback |

## FR-07 · Progress Tracking

| ID | Requirement |
| ----- | ----- |
| FR-07-1 | Dashboard: overall CEFR, streak, weekly completion, vocab learned |
| FR-07-2 | **Skill radar: 4 main skills + 2 sub-skills (6 axes)** |
| FR-07-3 | Per-skill CEFR history with progression line |
| FR-07-4 | SR deck status: due today, mastered, in review |
| FR-07-5 | Milestone notifications per skill level-up |
| FR-07-6 | Weekly email/in-app progress digest |

## FR-08 · Admin Panel

| ID | Requirement |
| ----- | ----- |
| FR-08-1 | Lesson CRUD with CEFR + main-skill + sub-skill tags; publish requires quiz |
| FR-08-2 | User management: CEFR per skill, lessons done, last active |
| FR-08-3 | AI Insights: most-skipped lessons, top AI Tutor topics, placement averages per skill |
| FR-08-4 | Test item bank management per skill |
| FR-08-5 | Speaking-audio QA: sample learner recordings for AI-score calibration |

---

# 7. Non-Functional Requirements

| Category | Requirement | Priority |
| ----- | ----- | :---: |
| Performance | 95p < 500 ms non-AI; AI first token < 3 s; Speaking ASR < 5 s | Critical |
| Concurrency | ≥ 100 concurrent users | High |
| Security | TLS 1.3, bcrypt cost ≥ 12, RBAC server-side, PII never sent to LLM | Critical |
| Audio Privacy | Speaking recordings stored ≤ 30 days; learner can delete anytime | Critical |
| Reliability | ≥ 99.5% uptime demo | High |
| A11y | WCAG 2.1 AA; keyboard-nav core flows; captions on all audio | Medium |
| Responsive | 375px mobile → 1440px+ desktop | High |
| AI Accuracy — Placement | ≥ 85% agreement per skill | Critical |
| AI Accuracy — Speaking | Pronunciation score within ±10 of certified rater on benchmark (n=40) | Critical |
| AI Safety | < 5% off-topic AI Tutor response | Critical |
| Maintainability | Backend test coverage ≥ 70%; OpenAPI 3.0 docs | Medium |

---

# 8. System Architecture

## 8.1 Three-Tier

| Layer | Components |
| ----- | ----- |
| Presentation | React 18 + TypeScript, Tailwind CSS, React Query, Web Audio API |
| Application | FastAPI (Python 3.11), JWT middleware, CAT Engine, Pathway Engine, LLM Gateway, Speech Gateway |
| Data & AI | PostgreSQL 16, Redis, Anthropic Claude (tutor + rubric scoring), OpenAI Whisper / wav2vec2 (Speaking ASR + pronunciation), S3-compatible object store (audio) |

## 8.2 New in v2

- **Speech Gateway** service: handles mic upload → transcription → phoneme alignment → scoring pipeline.
- **Pathway Engine** v2: supports 6-axis skill state (4 main + 2 sub), dynamic re-weighting per session.
- **Audio object storage** with 30-day retention policy.

---

# 9. Core Data Model (v2 changes)

Only entities that changed from v1 are shown; unchanged entities retain v1 structure.

| Entity | Key Fields (v2) | Change |
| ----- | ----- | ----- |
| users | + `cefr_per_skill` JSONB (keys: listening, reading, speaking, writing, grammar, vocabulary), + `skill_priority_order` array | expanded |
| placement_tests | + `score_speaking`, `score_writing`, per-skill `cefr_result` JSONB | expanded |
| lessons | + `main_skill` enum(listening/reading/speaking/writing), + `sub_skills[]` | replaced old `skill_type` |
| lesson_progress | + `sub_scores` JSONB (pronunciation, fluency, intonation, grammar, clarity, vocabulary) | expanded |
| **speaking_attempts** (new) | id, user_id, lesson_id, audio_url, transcript, score_pronunciation, score_fluency, score_intonation, ai_feedback, created_at | new table |
| **writing_submissions** (new) | id, user_id, lesson_id, content_text, score_grammar, score_clarity, score_vocabulary, ai_feedback, created_at | new table |
| flashcards | + `card_type` enum(vocabulary, grammar_rule) | expanded |

---

# 10. Screen Inventory & UX Flows

## 10.1 Screen List (20 frames in design)

| # | Screen | Status |
| :---: | ----- | :---: |
| 01 | Landing Page | existing |
| 02 | Register / Login | existing |
| 03 | Onboarding Survey (v2: 4-skill priority picker) | **update** |
| 04 | Placement Test (v2: 4-skill CAT + Speaking + Writing prompts) | **update** |
| 05 | Placement Results (v2: 6-axis radar) | **update** |
| 06 | Learning Dashboard | existing |
| 07 | Lesson Detail | existing |
| 08 | Lesson Quiz | existing |
| 09 | Flashcard Review (SM-2) | existing |
| 10 | AI Tutor Chat | existing |
| 11 | Progress Dashboard (v2: 6-axis skill tracking) | **update** |
| 12 | Admin — Lesson Manager (v2: main+sub skill tags) | **update** |
| 13 | Admin — User Overview | existing |
| 14 | Admin — AI Insights (v2: speaking-score distribution) | **update** |
| 15 | Grammar Practice (sub-skill) | existing |
| 16 | Vocabulary Practice (sub-skill) | existing |
| 17 | Listening Practice (main skill) | existing |
| 18 | Writing Practice (main skill) | existing |
| **19** | **Speaking Practice (main skill)** | **new in v2** |
| **20** | **Reading Practice (main skill)** | **new in v2** |

## 10.2 Key User Flows

**Flow A — New Learner Onboarding (v2):**
Register → Survey (goal + daily minutes + skill priority) → 4-skill CAT (incl. Speaking mic + Writing prompt) → Per-skill Results + radar → Private Week 1 path → First lesson.

**Flow B — Daily Study (v2):**
Login → Dashboard (today's plan mixed across skills) → Lesson or Practice module → Quiz / Speaking attempt / Writing submission → Immediate AI feedback → Flashcards → Progress updates.

**Flow C — Skill-Specific Upgrade:**
3 consecutive ≥ 85% in one skill → Notification "Ready for A2 Speaking!" → Learner confirms → Next-level lessons for that skill only (other skills unchanged) → Badge earned.

**Flow D — Pronunciation Fix (new):**
Speaking score < 70 for 2 sessions → System proposes focused Shadowing pack → Learner completes 5 drills → Score re-evaluated → Path re-balanced.

---

# 11. AI Component Specification

## 11.1 Multi-Skill CAT Engine
- Separate ability estimate θ per skill; IRT-based Bayesian update per item.
- Speaking and Writing use rubric-based scoring, mapped to CEFR bands (A1=0–40, A2=41–60, B1=61–80, B2=81–100).

## 11.2 Pathway Engine (v2 Scoring)

```
score(lesson) = 0.35 × skill_relevance
              + 0.30 × weakness_alignment
              + 0.15 × subskill_gap_fit
              + 0.12 × goal_match
              + 0.08 × time_fit
```

Top-N selection per skill, balanced by priority ratio, with mandatory inclusion of ≥ 1 Speaking and ≥ 1 Writing lesson/week.

## 11.3 Speaking AI Pipeline (new)

```
Mic → Audio Upload → Whisper ASR → Transcript
                                → Phoneme Alignment (wav2vec2)
                                → Pronunciation Score (phoneme match %)
                                → Fluency Score (WPM + pause variance)
                                → Intonation Score (pitch contour DTW vs. reference)
                                → LLM Feedback Generator (structured notes)
```

**Evaluation:** n=40 recordings rated by certified IELTS Speaking examiner; AI score must be within ±10 of human for ≥ 80% of cases.

## 11.4 Writing AI Rubric

LLM prompt returns JSON: `{ grammar: 0-100, clarity: 0-100, vocabulary: 0-100, corrections: [...], suggestions: [...] }`. Validation against CEFR writing descriptors.

## 11.5 SR Engine — SM-2
Unchanged from v1; now supports two card types (vocabulary, grammar_rule).

## 11.6 AI Tutor — System Prompt

```
SYSTEM: You are EduLingo, an English tutor. Learner CEFR per skill: {cefr_json}.
Only answer English-learning questions (grammar, vocab, listening, reading, speaking, writing).
Adapt complexity to lowest active CEFR in the relevant skill.
Format: explain → 2 examples → practice prompt.
Off-topic: "I can only help with English learning topics..."
```

---

# 12. Scope

## 12.1 In Scope (v2.0)
- All Must-Have requirements in §6 and §7
- CEFR A1–B2 across all 4 main skills
- **Speaking** (moved in from v1 roadmap)
- Vietnamese UI + English content
- Web (responsive 375–1440+)

## 12.2 Out of Scope (v2.0)
- Native mobile apps
- C1 / C2 content
- Payments / subscriptions
- Real-time peer practice
- Multi-language UI beyond Vietnamese + English

---

# 13. Development Roadmap

| Phase | Duration | Deliverables |
| ----- | ----- | ----- |
| P1 | Weeks 1–2 | DB schema v2, Auth, 4-skill placement item bank (80+ items), CAT engine |
| P2 | Weeks 3–4 | Pathway Engine v2, Lesson CRUD with main+sub skill tags, Admin |
| P3 | Weeks 5–6 | AI Tutor, Reading + Listening Practice modules |
| P4 | Weeks 7–8 | Speech Gateway, Speaking Practice, pronunciation scoring |
| P5 | Weeks 9–10 | Writing Practice, rubric scoring, SR engine, Progress v2 |
| P6 | Week 11 | E2E testing, seed content, demo deploy, evaluation |

---

# 14. AI Evaluation Framework

| Component | Method | Target |
| ----- | ----- | :---: |
| Placement (per skill) | Agreement w/ evaluator n=30 | ≥ 85% |
| Pathway Relevance | Survey n≥20 (1–5) | ≥ 4.0 |
| Pathway Lesson Completion | Week-2 completion % | ≥ 60% |
| Speaking Score Calibration | Examiner-rated n=40 | ±10 for ≥ 80% |
| Writing Score Calibration | Rater-rated n=30 | ±10 for ≥ 80% |
| SR Recall | 7-day re-test n≥20 | ≥ 75% |
| AI Tutor Helpfulness | Post-chat rating n=200 | ≥ 80% |
| AI Tutor Containment | 100-prompt benchmark | ≥ 96% |

---

# 15. v1 → v2 Change Log

| Area | v1 | v2 |
| ----- | ----- | ----- |
| Skills model | 4 skills (Vocab, Grammar, Reading, Listening) + Writing via AI Tutor | **4 main (L/R/S/W) + 2 sub (Grammar/Vocab)** |
| Speaking | Out of scope | **In scope, full practice module + ASR scoring** |
| Writing | Tutor-only | **Dedicated practice module + rubric scoring** |
| Placement | Single overall CEFR | **Per-skill CEFR + sub-skill scores** |
| Pathway inputs | 4 factors | **5 factors incl. sub-skill gap fit** |
| Progress radar | 4 axes | **6 axes (4 main + 2 sub)** |
| New screens | — | **Speaking Practice (#19), Reading Practice (#20)** |
| New data tables | — | `speaking_attempts`, `writing_submissions` |
| New services | — | Speech Gateway |

---

# 16. References

All v1 references retained, plus:

- Radford, A. et al. (2023). Robust Speech Recognition via Large-Scale Weak Supervision (Whisper).
- Baevski, A. et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations.
- British Council (2024). CEFR Speaking Descriptors — A1 through C2.
- Cambridge Assessment (2025). Automated Scoring of L2 Writing: Rubric Alignment Study.
