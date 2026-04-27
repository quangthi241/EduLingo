

**PRODUCT REQUIREMENT DOCUMENT**

**EduLingo AI**

*Intelligent English Learning Tutor with Personalized AI Pathways*

Version 1.0  |  April 2026  |  Academic Research & Product Specification

# **1\. Executive Summary**

EduLingo AI is a web-based intelligent tutoring system (ITS) that applies artificial intelligence to deliver **personalized English learning experiences** aligned with the Common European Framework of Reference for Languages (CEFR). The platform directly addresses a documented gap: most e-learning platforms offer static, one-size-fits-all curricula that fail to adapt to individual learner proficiency, learning style, and goals.

A 2025 systematic review across 85 studies confirms AI-powered personalized learning significantly improves student performance, engagement, and motivation. EduLingo AI operationalizes these findings through three core AI components: (1) an adaptive CEFR placement engine using Computer Adaptive Testing (CAT); (2) a dynamic learning path recommendation algorithm; and (3) an LLM-powered AI Tutor chatbot constrained to English learning domains.

| Target Users | CEFR Scope | AI Components | Platform |
| :---: | :---: | :---: | :---: |
| Students & adult learners A1–B2 | A1 · A2 · B1 · B2 | 3 distinct AI systems | Web (mobile-responsive) |

# **2\. Research Foundation & Problem Statement**

## **2.1 Problem Statement**

**Core problem:** Traditional English learning platforms treat all learners identically, ignoring individual proficiency, learning styles, and goals — producing low engagement, high dropout rates, and suboptimal outcomes, especially for A1–B1 learners who need the most scaffolding.

Evidence base for the problems this product addresses:

* Static curricula fail to adapt content to learner ability and needs; this gap is well-documented by deep learning and data mining research (Scientific Reports, Aug 2025).

* Human CEFR placement achieves only 80–85% accuracy; AI-assisted systems reach 95% (SmallTalk2Me benchmark, 2024).

* Spaced repetition — grounded in Ebbinghaus' Forgetting Curve — is absent from most web learning platforms, reducing long-term vocabulary retention (Kharwal et al., 2022).

* LLM-based conversational tutors show \+75% improvement in speaking scores over 8-week programs when used consistently (Gliglish research, 2024).

* Platforms that align to learners' individual styles show stronger academic engagement than purely proficiency-based adaptation (Qu et al., European Journal of Education, 2025).

## **2.2 Market Benchmark Analysis**

| Platform | CEFR Align | Adaptive Path | AI Tutor Chat | Spaced Rep. | Analytics | Web-First |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Duolingo | Partial | Yes | No | Yes | Basic | No (App) |
| Gliglish | No | No | Yes | No | Basic | Yes |
| Rosetta Stone | No | Partial | No | No | No | Yes |
| EF SET | Full | No | No | No | No | Yes |
| **EduLingo AI** | **Full A1–B2** | **Yes (AI)** | **Yes (LLM)** | **Yes (SM-2)** | **Advanced** | **Yes** |

## **2.3 AI Theoretical Framework**

| Framework | Description | Application in EduLingo AI |
| ----- | ----- | ----- |
| **Knowledge Tracing (BKT)** | Models probability a learner has mastered a skill based on interaction history | Tracks mastery per CEFR skill tag; drives content advancement and review triggers |
| **Spaced Repetition (SM-2)** | Schedules review at optimally spaced intervals using Ebbinghaus Forgetting Curve | Vocabulary and grammar flashcard scheduler inside lesson modules |
| **Constructivist Learning** | Knowledge built through interaction, feedback, and active language use | AI Tutor drives dialogue-based learning rather than passive content delivery |

# **3\. Product Goals & Success Metrics**

## **3.1 Product Goals**

1. Deliver accurate CEFR placement to every new learner within 15 minutes of registration.

2. Generate a fully personalized weekly learning path based on placement score, goal, skill gaps, and available study time.

3. Provide an always-on AI Tutor that responds to English learning questions calibrated to the learner's CEFR level.

4. Dynamically re-adjust the learning path based on quiz performance and spaced repetition schedules.

5. Give learners transparent, data-driven progress visibility across all four CEFR skills.

## **3.2 Key Performance Indicators**

| Metric | Measurement | Target | Priority |
| ----- | ----- | ----- | :---: |
| **CEFR Placement Accuracy** | Agreement with certified evaluator (n=30 test cases) | ≥ 85% | Critical |
| **Learning Path Relevance** | Learner satisfaction survey (1–5 scale) | ≥ 4.0 / 5.0 | High |
| **AI Tutor Helpfulness** | Post-chat thumbs up/down rating | ≥ 80% positive | High |
| **Lesson Completion Rate** | % recommended lessons completed per week | ≥ 60% | High |
| **7-Day Retention** | Users returning within 7 days of registration | ≥ 40% | Medium |
| **Vocabulary Recall** | Re-test score on SR cards after 7 days | ≥ 75% recall | Medium |
| **AI Response Latency** | Time from user send to first token | \< 3 seconds | High |
| **AI Topic Containment** | % off-topic chatbot replies (benchmark set) | \< 5% | Critical |

# **4\. User Personas**

| Persona 1 — Beginner Learner (Primary User) |
| ----- |
| **Profile:** Nguyen Thi Mai, 22, university student. Estimated CEFR: A1–A2. **Goal:** Build foundational English for job applications. Studies 30–45 minutes/day. **Pain Points:** Does not know where to start. Overwhelmed by generic apps. Discouraged without personalized feedback. **Needs:** Clear CEFR placement, a structured step-by-step path, instant AI support, visible progress. |

| Persona 2 — Intermediate Self-Improver |
| ----- |
| **Profile:** Tran Van Hung, 28, working professional. Estimated CEFR: B1. **Goal:** Prepare for business communication and interviews. Studies 20 minutes/day. **Pain Points:** Knows basics but struggles with fluency and advanced grammar. Generic lessons waste his time. **Needs:** A path that skips known content, conversational AI practice, grammar correction, writing feedback. |

| Persona 3 — Administrator |
| ----- |
| **Profile:** Academic staff or teacher managing course content and learner data. **Needs:** CRUD for lessons with CEFR tagging, user overview, learner-path visibility, and AI insight dashboards. |

# **5\. Functional Requirements**

## **FR-01 · Authentication & User Profile**

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| **FR-01-1** | Users register with full name, email, and password; email validated by format check. | Must-Have |
| **FR-01-2** | Passwords stored using bcrypt hashing (minimum cost factor 12). | Must-Have |
| **FR-01-3** | JWT-based session management with 7-day expiry and refresh token support. | Must-Have |
| **FR-01-4** | Role-based access control: roles are 'learner' and 'admin'; enforced via middleware per endpoint. | Must-Have |
| **FR-01-5** | Learner profile stores: CEFR level, learning goal, weak skills, daily study minutes, skill preference order. | Must-Have |
| **FR-01-6** | OAuth 2.0 social login via Google as alternative authentication path. | Should-Have |

## **FR-02 · Adaptive CEFR Placement Assessment**

The placement test classifies learners at A1, A2, B1, or B2 using a **Computer Adaptive Testing (CAT) approach** — item difficulty adjusts in real time per answer correctness. Adaptive tests pinpoint proficiency with fewer questions than linear tests (Bridge, 2025; EF SET, 2024).

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| **FR-02-1** | Pre-test survey collects: learning goal (communication / TOEIC / foundation), daily study time (15/30/45/60+ min), target skill. | Must-Have |
| **FR-02-2** | Test bank: minimum 60 items tagged by CEFR level and skill type. CAT algorithm selects next item via IRT difficulty parameter. | Must-Have |
| **FR-02-3** | Test terminates after 20 questions or when ability estimate standard error drops below threshold; \~10–15 minutes. | Must-Have |
| **FR-02-4** | Scoring produces: overall CEFR band, per-skill subscores (Vocabulary, Grammar, Reading, Listening), and skill weakness ranking. | Must-Have |
| **FR-02-5** | Score report rendered immediately: CEFR level card, radar chart of skill scores, recommended next action CTA. | Must-Have |
| **FR-02-6** | Learner may re-take placement after 30 days; prior results archived in profile. | Should-Have |

## **FR-03 · AI-Powered Personalized Learning Path**

The recommendation engine generates a weekly learning path using a **multi-factor weighted scoring model**. Unlike simple if-else rules, the system considers four input variables simultaneously and re-adjusts dynamically after each session (ALPOA principles, IJBES 2024).

| Input Variable | Description | Weight |
| ----- | ----- | :---: |
| **CEFR Placement Score** | Numeric ability estimate from CAT (0–100 per skill, normalized) | 40% |
| **Weak Skill Priority** | Lowest-scoring skills get higher lesson weight in path selection | 30% |
| **Learning Goal** | Communication / TOEIC / Foundation maps to different lesson type distributions | 20% |
| **Daily Study Time** | Minutes/day determines lessons per week (15 min → 3 lessons; 60 min → 10 lessons) | 10% |

**Dynamic Re-adjustment Rules:**

* Quiz score \< 60% → lesson re-queued at higher priority; CEFR level held for that skill.

* 3 consecutive quiz scores ≥ 85% in one skill → system proposes next CEFR level for that skill.

* Spaced repetition (SM-2) schedules vocabulary review at 1, 3, 7, 14, and 30 days post-exposure.

## **FR-04 · Lesson Content & In-Lesson Practice**

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| **FR-04-1** | Each lesson: title, CEFR tag, skill tag, estimated duration, content body, end-of-lesson quiz (5–10 questions). | Must-Have |
| **FR-04-2** | Content types: vocabulary sets (word \+ definition \+ example), grammar explanations, short reading passages (100–300 words), listening comprehension (audio \+ transcript). | Must-Have |
| **FR-04-3** | Quiz question types: multiple choice, fill-in-the-blank, sentence rearrangement, matching pairs. | Must-Have |
| **FR-04-4** | Each quiz answer triggers immediate AI-generated feedback explaining correct/incorrect reasoning. | Must-Have |
| **FR-04-5** | Vocabulary items from lessons are automatically added to the learner's spaced repetition deck. | Must-Have |
| **FR-04-6** | AI generates additional practice exercises on demand within a lesson context. | Should-Have |

## **FR-05 · AI Tutor Chatbot**

The AI Tutor uses an LLM API with a **structured system prompt** that constrains responses to English learning topics, calibrates language complexity to the learner's CEFR level, and enforces pedagogically sound reply formats.

**System Prompt Architecture:**

* Role constraint: 'You are an English tutor specializing in CEFR A1–B2. Only answer questions about English language learning.'

* Level adaptation: learner CEFR level injected per session; simpler language for A1/A2, richer explanations for B1/B2.

* Format instruction: explain concept → give example → offer a practice prompt.

* Fallback: off-topic questions receive a polite redirect without invoking the full LLM completion.

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| **FR-05-1** | Chat interface supports text input; displays conversation history per session with timestamps. | Must-Have |
| **FR-05-2** | Supported intents: grammar explanation, vocabulary lookup, sentence correction, translation to English, exercise generation, writing feedback. | Must-Have |
| **FR-05-3** | AI Tutor responses always calibrated to the learner's current CEFR level stored in profile. | Must-Have |
| **FR-05-4** | Out-of-scope detection: non-English-learning questions receive a redirect message without full LLM invocation. | Must-Have |
| **FR-05-5** | Chat history persisted for 30 days; learner can scroll and re-read prior sessions. | Should-Have |
| **FR-05-6** | Suggested prompts displayed on empty chat to guide interactions (e.g., 'Explain present perfect tense'). | Should-Have |
| **FR-05-7** | Writing mode: learner pastes an English paragraph and receives structured feedback (grammar, vocabulary, clarity). | Should-Have |

## **FR-06 · Progress Tracking & Analytics**

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| **FR-06-1** | Learner dashboard: current CEFR level (overall \+ per skill), weekly lesson completion rate, streak counter, total vocabulary learned. | Must-Have |
| **FR-06-2** | Skill radar chart showing per-skill proficiency (Vocabulary, Grammar, Reading, Listening, Writing) updated after every quiz. | Must-Have |
| **FR-06-3** | Learning history: chronological list of completed lessons with date, score, and time spent. | Must-Have |
| **FR-06-4** | Spaced repetition deck status: cards due today, cards mastered, cards in review queue. | Must-Have |
| **FR-06-5** | Milestone notifications when learner achieves a CEFR level upgrade for any skill. | Should-Have |
| **FR-06-6** | Weekly progress report via in-app notification and optional email digest. | Could-Have |

## **FR-07 · Admin Panel**

| ID | Requirement | Priority |
| ----- | ----- | :---: |
| **FR-07-1** | Lesson CRUD: create, read, update, delete lessons; requires CEFR tag, skill tag, content, and quiz before publishing. | Must-Have |
| **FR-07-2** | User management: view all users with current CEFR level, lessons completed, and last active date. | Must-Have |
| **FR-07-3** | AI insight dashboard: most-skipped lessons, most-asked AI Tutor topics, average placement scores per CEFR level. | Should-Have |
| **FR-07-4** | Placement test item bank management: add, edit, tag, and retire test items. | Should-Have |

# **6\. Non-Functional Requirements**

| Category | Requirement | Specification | Priority |
| ----- | ----- | ----- | :---: |
| **Performance** | API Response Time | 95th percentile \< 500ms non-AI; \< 3s AI Tutor first token | Critical |
| **Performance** | Concurrent Users | Stable for ≥ 100 concurrent users without degradation | High |
| **Security** | Encryption | TLS 1.3 in transit; bcrypt (cost ≥ 12\) for passwords at rest | Critical |
| **Security** | Authorization | RBAC enforced server-side on all protected API endpoints | Critical |
| **Security** | PII Handling | User emails and learning data not shared; LLM API calls exclude PII | Critical |
| **Reliability** | Uptime | ≥ 99.5% uptime for demo environment | High |
| **Usability** | Accessibility | WCAG 2.1 AA contrast ratios; keyboard-navigable core flows | Medium |
| **Usability** | Responsive Design | All pages functional on desktop (1280px+) and mobile (375px+) | High |
| **AI Accuracy** | Placement | CEFR classification agrees with certified evaluator in ≥ 85% of test cases | Critical |
| **AI Safety** | Topic Containment | Off-topic AI Tutor response rate \< 5% on benchmark of 100 prompts | Critical |
| **Maintainability** | Code Quality | Backend unit test coverage ≥ 70%; documented via OpenAPI 3.0 | Medium |

# **7\. System Architecture & Technology Stack**

## **7.1 Three-Tier Architecture**

| Layer | Components | Responsibilities |
| ----- | ----- | ----- |
| **Presentation** | ReactJS 18 \+ TypeScript, Tailwind CSS, React Query | Renders all UI; communicates with backend via REST API; manages client-side session state. |
| **Application** | FastAPI (Python 3.11), JWT middleware, CAT Engine, Recommendation Engine, LLM Gateway | Business logic, auth, adaptive test, learning path scoring, AI Tutor prompt orchestration. |
| **Data & AI Services** | PostgreSQL 16, Redis, Anthropic Claude API (claude-sonnet) | Persistent storage; session/query caching; LLM completions for AI Tutor and quiz feedback. |

## **7.2 Technology Decisions**

| Domain | Technology | Rationale |
| ----- | ----- | ----- |
| **Frontend** | ReactJS 18 \+ TypeScript | Component reuse, strong typing, large ecosystem for educational UIs. |
| **Styling** | Tailwind CSS | Rapid UI with consistent design tokens; no custom CSS overhead. |
| **Backend** | FastAPI (Python 3.11) | Async for LLM streaming; Python ecosystem for AI/ML; OpenAPI auto-documentation. |
| **Database** | PostgreSQL 16 | Relational integrity for user-lesson-progress; JSONB for flexible quiz metadata. |
| **Caching** | Redis | Session store; cache test items and recommendation scores. |
| **AI LLM** | Anthropic Claude API | Best-in-class system prompt adherence; critical for domain-constrained tutoring. |
| **Auth** | JWT \+ bcrypt | Stateless, SPA-compatible; industry-standard password hashing. |
| **Deployment** | Docker \+ Docker Compose | Environment consistency; single-command demo setup. |

# **8\. Core Data Model**

All entities include created\_at / updated\_at audit timestamps. Key relationships are listed in the right column.

| Entity | Key Fields | Relationships |
| ----- | ----- | ----- |
| **users** | id, name, email (unique), password\_hash, role, cefr\_level, learning\_goal, daily\_study\_minutes, weak\_skills\[\] | 1:1 learner\_profile; 1:N lesson\_progress; 1:N chat\_sessions; 1:N flashcards |
| **placement\_tests** | id, user\_id, score\_overall, score\_vocabulary, score\_grammar, score\_reading, score\_listening, cefr\_result, taken\_at | N:1 users |
| **test\_items** | id, question\_text, options (JSONB), correct\_answer, cefr\_level, skill\_type, difficulty\_irt | Used in CAT engine item selection |
| **lessons** | id, title, cefr\_level, skill\_type, content\_body (JSONB), estimated\_minutes, is\_published, created\_by | 1:N lesson\_quizzes; referenced in learning\_paths |
| **lesson\_quizzes** | id, lesson\_id, question\_text, question\_type, options (JSONB), correct\_answer, ai\_explanation | N:1 lessons |
| **learning\_paths** | id, user\_id, generated\_at, week\_number, lesson\_ids\[\] (ordered), status | N:1 users; refs lessons |
| **lesson\_progress** | id, user\_id, lesson\_id, status, quiz\_score, time\_spent\_seconds, completed\_at | N:1 users; N:1 lessons |
| **flashcards** | id, user\_id, term, definition, example, cefr\_level, next\_review\_date, ease\_factor, interval\_days, repetition\_count | N:1 users; SM-2 fields |
| **chat\_messages** | id, session\_id, role (user/assistant), content, created\_at | N:1 chat\_sessions |

# **9\. Screen Inventory & UX Flows**

## **9.1 Screen List**

| \# | Screen | Key Elements | Access |
| :---: | ----- | ----- | :---: |
| 01 | **Landing Page** | Hero, feature highlights, sample lesson preview, CTA | Public |
| 02 | **Register / Login** | Registration form, OAuth button, validation feedback | Public |
| 03 | **Onboarding Survey** | Goal selection, daily time, skill preference | New Learner |
| 04 | **Placement Test** | Adaptive question display, progress bar, answer submission | New Learner |
| 05 | **Placement Results** | CEFR level card, skill radar chart, next-step CTA | Post-test |
| 06 | **Learning Dashboard** | CEFR level, weekly path cards, streak, AI Tutor shortcut | Learner |
| 07 | **Lesson Detail** | Content body, vocabulary highlights, embedded audio, quiz CTA | Learner |
| 08 | **Lesson Quiz** | Question display, answer selection, AI feedback, score summary | Learner |
| 09 | **Flashcard Review** | SM-2 flip cards, self-rating (Again/Hard/Good/Easy) | Learner |
| 10 | **AI Tutor Chat** | Chat thread, input box, suggested prompts, CEFR badge, history | Learner |
| 11 | **Progress Dashboard** | Radar chart, lesson history, streak calendar, flashcard stats | Learner |
| 12 | **Admin — Lesson Manager** | Lesson table, CRUD modal, CEFR/skill filter, publish toggle | Admin |
| 13 | **Admin — User Overview** | User table with CEFR, lesson count, last active, search | Admin |
| 14 | **Admin — AI Insights** | Most-skipped lessons, common AI topics, placement averages | Admin |

## **9.2 Key User Flows**

**Flow A — New Learner Onboarding:** 

Register → Onboarding Survey → Placement Test (20 adaptive questions, \~12 min) → View Results & CEFR Level → Learning Dashboard with personalized Week 1 path → Start first recommended lesson.

**Flow B — Daily Study Session:** 

Login → Dashboard (due lessons \+ flashcard count) → Complete lesson → Take quiz → AI feedback → Flashcard review (SM-2 due cards) → Chat with AI Tutor if questions arise → View updated progress.

**Flow C — CEFR Level Upgrade:** 

System detects 3 consecutive quizzes ≥ 85% in Vocabulary → Notification: 'You are ready for A2 Vocabulary\!' → Learner confirms → Path regenerated with A2 vocabulary lessons → Milestone badge awarded.

# **10\. AI Component Specification**

## **10.1 CAT Placement Engine**

The CAT engine maintains a learner **ability estimate (θ)** updated per answer using a simplified IRT Bayesian update: θ(n+1) \= θ(n) \+ α × (response − P(correct|θ, difficulty)). Items are selected to maximize information at the current θ. This is methodologically sound, academically defensible, and significantly more rigorous than if-else CEFR assignment.

## **10.2 Learning Path Recommendation — Scoring Function**

Lesson scoring formula applied to every candidate lesson for a given learner:

| score(lesson) \= 0.40 × skill\_relevance                \+ 0.30 × weakness\_alignment                \+ 0.20 × goal\_match                \+ 0.10 × time\_fit |
| :---- |

Lessons ranked descending by score; top N assigned to current week. Re-runs after every session using updated skill scores. This is a **weighted scoring model** — more rigorous than if-else and fully explainable in a thesis report.

## **10.3 Spaced Repetition — SM-2 Implementation**

* Learner rates recall after each card: Again (0) / Hard (1) / Good (2) / Easy (3).

* Ease Factor (EF) initialized at 2.5; adjusted: Good → unchanged; Hard → EF −0.15; Easy → EF \+0.15; Again → EF −0.20, interval reset to 1 day.

* Next interval: I(n+1) \= I(n) × EF × stability\_multiplier. Minimum interval: 1 day.

* Cards due today surfaced first in Flashcard Review screen.

## **10.4 AI Tutor — System Prompt & Safety**

| SYSTEM: You are EduLingo, an English language tutor. Learner CEFR level: {level}. Only answer questions about English learning (grammar, vocabulary, writing, pronunciation, reading, listening). Adapt complexity to CEFR {level}. Format: explain concept → give 2 examples → offer a practice prompt. Off-topic: respond 'I can only help with English learning topics. Try asking  about grammar, vocabulary, or practice exercises\!' |
| :---- |

**Evaluation Protocol:** 

* Benchmark: 100 test prompts (80 in-scope, 20 out-of-scope). Target: ≥ 96 correctly handled.

* A/B test two system prompt variants; select winner by helpfulness rating after 500 conversations.

* Monthly audit: sample 50 conversations for quality and boundary adherence.

# **11\. Scope, Constraints & Development Roadmap**

## **11.1 In Scope (v1.0)**

* All Must-Have requirements in Sections 5 and 6

* CEFR levels: A1, A2, B1, B2

* Skills: Vocabulary, Grammar, Reading, Listening (Writing via AI Tutor)

* Platform: Web only (desktop \+ mobile responsive)

* Languages: Vietnamese UI with English content

## **11.2 Out of Scope (v1.0)**

* Native mobile application (iOS / Android)

* Speech recognition or pronunciation scoring — roadmapped for v2.0

* C1 / C2 CEFR content levels

* Payment gateway and subscription management

* Real-time peer practice or multiplayer features

## **11.3 Development Roadmap**

| Phase | Duration | Deliverables | Status |
| ----- | ----- | ----- | :---: |
| **Phase 1** | Weeks 1–2 | Database schema, Auth API, Placement test bank (60 items), CAT engine | Planned |
| **Phase 2** | Weeks 3–4 | Recommendation engine, Learning path API, Lesson CRUD, Admin panel | Planned |
| **Phase 3** | Weeks 5–6 | AI Tutor integration, system prompt v1, out-of-scope filter, chat UI | Planned |
| **Phase 4** | Weeks 7–8 | Spaced repetition engine, Flashcard UI, Progress dashboard with charts | Planned |
| **Phase 5** | Weeks 9–10 | End-to-end testing, performance tuning, UI polish, demo content seeding | Planned |
| **Demo** | Week 11 | Full demo environment deployed; evaluation metrics collected and documented | Planned |

# **12\. AI Evaluation Framework**

A rigorous evaluation framework is essential for academic credibility. The following protocol defines how each AI component is measured:

| AI Component | Evaluation Method | Metric | Target |
| ----- | ----- | ----- | :---: |
| **CAT Placement Engine** | Compare with certified CEFR evaluator; n \= 30 test cases | % agreement with ground truth | ≥ 85% |
| **Recommendation Engine** | Learner survey (n ≥ 20): 'Do lessons match your level and goals?' | Mean satisfaction score (1–5) | ≥ 4.0 |
| **Recommendation Engine** | Lesson completion rate after week 2 (relevance proxy) | % lessons completed | ≥ 60% |
| **Spaced Repetition** | Vocabulary recall test on words studied 7 days ago (n ≥ 20\) | % correct recall | ≥ 75% |
| **AI Tutor — Helpfulness** | Post-conversation rating; sample 200 conversations | % positive rating | ≥ 80% |
| **AI Tutor — Containment** | Benchmark set: 100 prompts (80 in / 20 out-of-scope); manual review | % correctly handled | ≥ 96% |
| **AI Tutor — Level Adapt.** | Linguists rate 20 A1 and 20 B1 responses for complexity match | % rated 'appropriate' | ≥ 80% |

# **13\. References**

* Tapalova, O. & Zhiyenbayeva, N. (2022). Artificial intelligence in education: AIEd for personalised learning pathways. Electronic Journal of e-Learning.

* Kharwal, A. et al. (2022). Spaced Repetition Based Adaptive E-Learning Framework. ICDLAIR 2021, Springer LNNS vol. 441\.

* Raj, N.S. & Renumol, V.G. (2024). Adaptive learning path recommendation model driven by real-time analytics. Journal of Computers in Education, 11, 121–148.

* Qu, Y. et al. (2025). Future of Language Learning: AI-Driven Adaptive Platforms. European Journal of Education, 60(1).

* Guo, S. & Abdul Halim, H. (2025). AI-enabled mobile learning platforms for English teaching in universities. Scientific Reports, 15, 15873\.

* Wang, Q. (2025). AI-driven autonomous interactive English learning language tutoring system. Sage Journals.

* SmallTalk2Me (2024). CEFR AI Assessment: 95% accuracy benchmark. https://smalltalk2.me/assessment

* Bridge (2025). Using AI Tools for English Language Proficiency Placement. BridgeUniverse Blog.

* IJBES (2024). Adaptive Learning Path Optimization Algorithm (ALPOA). Vol. 9, No. 02, pp. 28–36.

* Electronics MDPI (2024). Leveraging AI in E-Learning: Personalized Learning and Adaptive Assessment. Electronics, 13(18), 3762\.

