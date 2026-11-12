---
name: brainmaps
description: Create complete, visual, editable Excalidraw mind palaces, chapter study boards, detailed diagrams, and source-faithful maps from PDFs, lectures, slides, research papers or notes. Use when asked for an Excalidraw file, mind palace, mind map, study board, revision board or a diagram matching the user's reference boards.
---

# BrainMaps

## Codex and Claude Code activation and execution

This skill is available through the BrainMaps plugin, and may also be invoked as `$brainmaps` where Codex exposes the skill. In Claude Code, invoke the plugin skill as `/brainmaps:brainmaps`. Resolve the skill directory from this file in either host; do not assume host-specific environment variables exist. Read this full `SKILL.md` and the bundled gallery before starting. Installing or uploading the plugin archive does not by itself mean that a particular conversation has enabled or loaded the plugin.

Resolve `SKILL_DIR` as the actual directory containing this `SKILL.md` (typically `${PLUGIN_ROOT}/skills/brainmaps` for plugin installations, or a `.agents/skills/brainmaps` location for manual standalone skill installations). Do not assume the plugin cache lives under `$HOME/.agents/skills`. All `reference/`, `scripts/` and `examples/` paths below are relative to **that directory**, never blindly relative to the user's repository. Read `$SKILL_DIR/reference/style-gallery/INDEX.md` and, where supported, actually view its G/B PNGs with the image-viewing tool. Preserve the gallery in the install. Do not ship placeholder images.

Write source maps, draft rooms, formula-cache files and resulting `.excalidraw` outside the installed skill directory, in a project-specific work directory. Execute the builder from that work directory, passing the absolute path to `build_board.py` and explicit input/output locations. For example, on Linux/macOS:

```bash
SKILL_DIR="${PLUGIN_ROOT}/skills/brainmaps" # plugin runtime; otherwise set to the actual SKILL.md folder
python3 -m pip install Pillow
mkdir -p work/excalidraw-board
cd work/excalidraw-board
python3 "$SKILL_DIR/scripts/build_board.py" rooms/ board.excalidraw --figs figs/ --cols 3
python3 "$SKILL_DIR/scripts/audit_board.py" board.excalidraw
```

The builder requires Python 3 and Pillow. For typeset formula images, additionally install `pdflatex` (TeX Live or MiKTeX) and `pdftocairo` (Poppler). Without both tools, formulas fall back to text; clearly report that loss rather than claiming typeset math was embedded. Before creating a board, run `python3 "$SKILL_DIR/scripts/check_install.py"` to check assets and runtime tools. The gallery images are **style references**, not elements to paste indiscriminately into the user's final board.

Codex has no guaranteed browser, web search, image preview or PDF OCR in every runtime. Use only tools actually available; when a source or figure cannot be inspected, state that limitation and do not claim complete source coverage. When a rendered preview is possible, inspect it before delivery. Preserve the user's actual content and cite figures appropriately.

You draw well without help. Where you fail is in deciding what goes on the board. Left alone you will produce a tidy outline with one-word nodes, formulas with no explanation, and a message saying everything is covered. The owner of this skill has rejected that output many times. Every rule below comes from a correction they actually gave. Read section 2 before each room, not only once.

## 0. First, look at the owner's screenshots (required)

The folder `reference/style-gallery/` holds seventeen screenshots the owner sent (G1 to G14 to copy, B1 to B3 to avoid) while correcting earlier work, and `INDEX.md` there describes each one in words. Before you plan any room:

1. Open `reference/style-gallery/INDEX.md`.
2. View every `G*.png` (what to copy) and every `B*.png` (what to avoid). If you cannot view images, the INDEX text describes them closely enough to follow.
3. Write two lines in your working notes: "I will copy: ..." and "The failure I am most likely to repeat: ...".
4. When the board is built, view your own render next to the G images and ask whether the same person who drew G2 and G3 would accept it. Then run `python3 scripts/audit_board.py board.excalidraw` and fix everything it prints.

If `reference/style-gallery/` does not exist, the skill was installed from text only. Say so in your first message, ask the owner for the zip, and until then follow section 9a, which restates the layout rules in words.

A model that skips this step produces the wall-of-paragraphs board (`B3`): long lines running off the frame, small hand-drawn body text, no formula images, no diagrams, no worked trace. That output was rejected as "one of the worst case things".

## 1. Pick the mode first, and say which one you picked

| The request sounds like | Mode | What is delivered |
|---|---|---|
| "teach / cover / mind palace / I will not read the slides" | A. Study palace | one `.excalidraw` file, one room per source section, full depth |
| "overview / summary / big picture / what covers what / where are the gaps" | B. Overview board | one screen; every node still carries its meaning; covered items and gaps marked differently |
| "convert this to excalidraw / one diagram / pipeline" | C. Single diagram | one diagram; a data node per stage showing what a running example looks like at that point |
| "exact style of this file" | D. Style match | measure the reference file (font family, sizes, colours, text density, arrow bindings) and reproduce it |

If they say they cannot copy from a file, print clipboard JSON in a code block: `{"type":"excalidraw/clipboard","elements":[...],"files":{}}`, pasted with Ctrl+V on the canvas.

A reference board they attach shows how much planning and explanation they expect. It is not a visual style to clone unless they ask for the exact style (mode D).

## 2. Corrections already given. Do not earn them again

| What the model produced | What the owner said | Do this instead |
|---|---|---|
| Map nodes with bare words: "Agent", "State" | "this is so bad, you defaulted to this everywhere" | every node is "term - what it is, in plain words" |
| Blocks of facts with no reasoning | "simply info bombing won't do, you need to explain everything you put in there and every line you write" | each line states a fact and the reason for it; delete lines that only name a topic |
| First draft of a chapter | "too much of a summary" | build and run every formula on numbers; show derivation steps |
| Rooms that list ideas in no order | "you are not telling a proper consistent flow... how will I know things before learning" | each block must be needed by the next; open each room with what the previous one left unsolved |
| Formula pasted with a sentence under it | "explain what every term does by pointing to that term" | formula anatomy: each term coloured, an arrow from the term to its label |
| A problem described in words only | "refer to the equations and the corrections, before and after, to make the point very clear" | term responsible, mechanism, numbers, formula before, formula after, cost of the fix |
| The same block layout for every topic | "content and format should be adaptive to the topic... create these like a human does" | choose table, flowchart, chart, anatomy, code, figure or Q and A from the content |
| Yellow boxes saying "Place image: a dog trainer..." | "what are these yellow boxes?" | never leave a placeholder; embed the real figure or draw it |
| A topic placed where a textbook would put it | "why is there GAE here? is it in the actual slides?" | place every topic where the source teaches it; cite the slide number |
| Boxes that rendered empty | "there are empty diagram boxes everywhere" | unique ids from one counter; render and look before sending |
| A variable that appears with no origin | "where does b come from?" | say where every variable and number comes from |
| Capabilities mapped item by item | "too atomic / narrow" | map against the whole end-to-end process, and mark what nothing covers |
| "Every number was recomputed, every page inspected" | "Did you run the checks?" | report only checks that ran; list the ones that did not |
| A board of long single-line paragraphs in the small hand-drawn font, no drawn formulas or diagrams (`B3`) | "This is one of the worst case things" | view the gallery first (section 0); G2 and G3 layout; run audit_board.py |
| Grep for banned phrases | "it is you who need to catch the whiff of that language" | re-read your own prose sentence by sentence |
| Fluent sentences that carry no fact | "clauses or phrases that sound like they make sense, but actually don't" | every sentence makes a checkable claim in plain English; see section 6 |
| A PDF with questions but thin answers | "where are the exam ready proper answers with proper steps? Don't leave any question unanswered, any type, even practice" | every question on the board has a full worked answer directly under it |
| Math written as plain text | "Dude, proper math rendering and formatting??" | render every formula as real math |
| Fewer diagrams and expansions than asked | "why is this shorter and less thorough than requested?" | count what was asked for against what was made, and report the difference |
| Teaching dripped in tiny steps across turns | "just give the complete thing again" | each room is complete and self-contained |
| One layout reused for every topic | "Do not generalise. Adapt per topic." | decide the form of each block from its content, topic by topic |
| Several partial files and long progress notes | wants one final file and short status | one merged file; status in a line |

## 3. Who reads the board

- They will not open the slides, book or papers. The board is the only source.
- They say they start with no knowledge of the topic and are weak at mathematics, and that once a thing is explained end to end they hold it firmly. So: small steps, no skipped algebra, every symbol named.
- They will sit an exam without help. Write so they can reproduce the reasoning alone: data stated first, then steps, then a check.
- They detect generated-sounding prose at once and stop trusting the page.

## 4. Workflow for mode A

1. Ingest all sources before writing.
   - Slides: text of every slide plus speaker notes. The notes hold the lecturer's reasoning and the questions asked in class. Slide wording may be filler; the technical content and its order are the curriculum.
   - Book: use the source repository or HTML when it exists. OCR output breaks formulas, tables, multi-column pages and code; cross-check anything taken from OCR.
   - Papers the slides cite: download the LaTeX source (`https://arxiv.org/e-print/<id>`) and grep the `.tex` for equations, settings and result tables. Use Semantic Scholar or a search to find papers and follow-ups. OCR a PDF only when there is no source.
   - No source for a PDF: ask the owner for an OCR zip. They convert the PDF at `https://oconvertor.com/tools/pdf-to-markdown` (it runs in their own browser) and send the zip: one markdown file linked to a folder of extracted images. Unzip it, read the markdown, use the images as figures. Check it against the PDF pages, because this OCR is known to: output multi-column pages in column order, flatten tables and code into plain text, mix headers, footers and page numbers into the body, export formulas as images, split reference lists into separate blocks, and return nothing for some pages. Every formula and table taken from OCR is compared with the page image before use.
   - Figures from the owner's own materials go on the board for private study with a credit line. If a licence is unclear and the board may be shared, redraw the figure and cite it.
   - Their earlier chats: when a chat-search tool exists this step is required. Search for earlier boards, PDFs and teaching on the same subject, read what they corrected, and apply it before writing.
2. Write state files and keep them current: `SOURCE_MAP.md` (one row per slide or section: formulas, examples, questions asked, papers, room, status), `NOTATION.md` (symbol, meaning, type, first use, clashes), `TODO.md`.
3. Before teaching, list what will be pulled in from outside the slides and where each item attaches (paper equation at slide 26, result table at slide 35, and so on).
4. Plan rooms in the source's order, one room per section.
5. Write each room with the recipe in section 5, then run the room audit in section 7.
6. Build with `scripts/build_board.py`, render, and look at every room.
7. Deliver one file. State rooms finished to full depth, rooms still shallow, checks that ran, and items written from memory.

Depth has priority over coverage. When the source is large, finish some rooms completely, stop at a section boundary, and say what remains. Do not thin every room to reach the end.

## 5. Room recipe

The room follows PQRST: Preview (opening block), Question (the questions the room answers), Read (the teaching blocks), State (the reader restates; the board gives a model restatement), Test (questions with full answers). Slide-complete means every definition, equation, example, worked number, diagram, annotation, table, caveat, step-by-step reveal, code fragment, class question and check on the slides is on the board.

Before writing each block ask: what would a careful lecturer put on the board for exactly this idea? A picture, a table, a derivation, a trace of one example, code, a question. A room made only of text blocks means this question was skipped.

1. Opening block: slides and papers covered; what the previous room established; what it left unsolved; the questions this room answers.
2. Recap block: any earlier idea needed here, restated in a few lines so nobody scrolls back.
3. Per concept: why it exists, mechanism in plain words, formula anatomy, the source's own worked example with every intermediate number, edge cases (zero, all equal, limit), cost or trade-off.
4. Per problem and fix: term responsible, mechanism, numbers, formula before and after, cost of the fix, measured effect if a paper reports one.
5. Every question the slides or notes ask: restated and answered at that point. Answer goes directly under its question.
6. Closing block: the opening questions with full answers.
7. Questions of every kind are answered, none left open: class questions from the notes, open-ended discussion questions (give a reasoned position, the evidence on each side, and what would settle it), numerical questions, and any practice you add (labelled "generated practice"). Exam-ready form: Given, To find, Formula with anatomy reference, Steps with every number, Answer, Check, plus the diagram a marker expects. For multiple choice, say why each wrong option is wrong.

Worked example of the standard. Weak:

```text
Length bias: GRPO divides by length, so long wrong answers are penalised less. Fix: Dr. GRPO.
```

Required:

```text
Push per token = advantage of the answer / number of tokens in it.
Two wrong answers, advantage -1:
  10 tokens:  -1 / 10  = -0.10 per token
  100 tokens: -1 / 100 = -0.01 per token
A token in the long wrong answer is discouraged ten times less, so wrong answers drift longer.
Before: (1/G) sum_i (1/|o_i|) sum_t (...)      After: (1/G) sum_i (1/L_max) sum_t (...)
After the fix every token gets -0.01: short wrong totals -0.1, long wrong totals -1.0.
Cost: the constant rescales the gradient, so the learning rate must be tuned with it.
```

## 5a. Formula anatomy: mark every term and explain it

Model: an annotated-equation poster. The equation is printed large. An arrow runs from each term to a label. The label has a short underlined NAME ("Pressure gradient", "Body force term") and one or two plain sentences on what that term does ("Fluid flows in the direction of largest change in pressure"). A compound term is expanded underneath with an equals sign into its own smaller formula, and that formula's parts get their own arrows.

Apply this to every equation and every expression that carries meaning, including ratios, conditions, inequalities and a line of code that computes a formula.

1. Title: the name of the equation. For a set of equations, name each one.
2. The whole formula once, large, rendered as real math.
3. One label per term. Operators, sums, indices, limits, exponents and constants are terms too. Each label says: NAME, what the term is, why it is in the formula, and what its sign or position means.
4. Expand any compound term in a second anatomy directly below it (two levels, as in the poster).
5. Under the anatomy: which quantities are learned, fixed or settings, with typical values; the formula run on the source's numbers with every intermediate value; one check; what happens when a term is zero, very large, or removed.
6. Equation gate, all answered on the board: what it computes, why it is needed, where in the algorithm it runs, how it is derived, the form it takes in code, the usual mistake.
7. When a later method changes the formula, draw before and after with the changed term in the same colour in both.

Diagram reading, for every figure and chart: what the picture is, what each object, arrow, colour and axis means, the order to read it in, which equation each part matches, the conclusion to draw, and one question an examiner could ask from it.

## 5b. Note patterns taken from the owner's own boards

These come from the boards the owner built by hand (a computer-architecture board of about 400 notes, and a research-papers board). They show what the owner writes when deciding what to revise from. Match the density and the moves. Choose the pattern by what the idea is.

Concept note. One-line definition, the rule, "Example:" with concrete values, then "Why?" answered by listing the cases:

```text
Hamming code can detect and correct single-bit errors.
It uses parity bits placed at positions that are powers of 2.
Number of parity bits. For m data bits and r parity bits:  2^r >= m + r + 1
Example: m = 4. Try r = 3:  2^3 >= 4 + 3 + 1,  8 >= 8 yes. So 3 parity bits are needed.
P1 checks positions 1, 3, 5, 7.   Why?  1 = 001, 3 = 011, 5 = 101, 7 = 111:
P1 checks the positions whose binary form has last bit 1.
```

Variant note, one per member of a family (modes, methods, algorithms), always the same slots so members can be compared: what it is, example instruction, meaning, small layout drawing, advantage, disadvantage, used for.

Formula note. Name the symbols first ("Suppose: n = number of tasks, k = stages, t = time per stage"), give the formula, then "Why?" and derive it in words ("the first instruction takes k cycles; after that one finishes every cycle; so k + n - 1").

Worked problem. Question, Given, then each case computed on its own lines with aligned equals signs, then the result and one sentence comparing it with the ideal value:

```text
Question: a pipeline has 4 stages, each takes 10 ns. Time for 100 instructions with and without it? Speedup?
Given: k = 4, n = 100, t = 10 ns
Without pipeline:  Time = n x k x t = 100 x 4 x 10 = 4000 ns
With pipeline:     Time = (k + n - 1) x t = 103 x 10 = 1030 ns
Speedup = 4000 / 1030 = 3.88.  The ideal is 4; the result is close because n is large.
```

Trace. A table of time steps against items that shows the mechanism running (cycle 1 to 7 against instructions I1 to I4, each cell the stage it is in).

Near-synonyms sorted out in one place: "Machine instruction = visible to the programmer. Microinstruction = internal control word. Microprogram = sequence of microinstructions."

Decision flow as a real flowchart with diamonds for the tests (instruction cycle: D7 = 1? I = 1?) and the action written on each branch.

Paper note (research board): the task as input -> output, what the paper shows, what it does NOT do, its pipeline as lettered stages with numbered steps, its key formula, its data and settings. Then one cross-paper matrix: which paper covers which stage of the whole process, with uncovered stages marked.

## 6. Writing rules

### Plain English comes first

The reader studies alone. A sentence that sounds right but says nothing costs them time and trust. Write so that a person can read the board once, on their own, and then explain the topic to someone else in their own words.

1. Every sentence must make a claim that could be wrong. If you cannot say what would make the sentence false, delete it.
2. One idea per sentence. Name who or what acts, then say what it does: "The clip stops the push on a token" and not "Stability is ensured through clipping".
3. Use short common words. Use the technical term only where it is the name of the thing, and gloss it.
4. Use a number where you were about to use an adjective: "ten times less", not "significantly less".
5. Use the same word for the same thing every time. Do not rotate synonyms (answer, response, output, completion) for one object.
6. No pronoun whose owner is unclear. Repeat the noun.
7. State cause and effect in order: what happens, then what follows from it.

Phrases that sound meaningful and carry no fact. Do not write them or anything like them:
"plays a crucial role", "is a powerful tool", "at its core", "in essence", "fundamentally", "under the hood", "leverages", "seamlessly", "robust", "strikes a balance between", "captures the essence of", "paves the way", "it is important to note", "a key insight", "elegant", "unlocks", "navigates the trade-off".

Weak, then required:

```text
Weak:     GRPO strikes a balance between exploration and stability.
Required: GRPO limits each update in one way: once a token's probability has changed by
          20 percent in the helpful direction, that token receives no further push.

Weak:     The KL term plays a crucial role in keeping training stable.
Required: The KL term subtracts a cost that grows as the policy's token probabilities move
          away from the frozen reference model's. A larger beta makes that cost larger.

Weak:     Entropy collapse fundamentally limits exploration.
Required: When one token holds almost all the probability at each step, the 8 sampled
          answers come out nearly identical, so no new solution is ever tried.
```

Own-words test, run on every block before it goes on the board: put the source away and state the block's point in two sentences, using no term you have not defined. If you cannot, you have not understood the source yet. Go back to it; do not paper over the gap with a fluent sentence.

### Other rules
- Bracket gloss at first use of every term, acronym and symbol: "KL divergence (a measure of how different two probability distributions are)". No jargon inside a gloss. Define once.
- Two symbols that look alike are defined side by side (reward r_i, ratio r_(i,t)).
- State for each quantity whether it is learned, fixed, or a setting, with typical values.
- Keep the source's examples and numbers. Mark your own numbers as illustrative.
- Separate "shown in the source" from "inferred by me". Flag conflicts between sources with both values.
- Lists for examples and cases. Tables for comparisons. Mermaid labels in plain words, no braces or symbols.
- Code: short enough to reproduce by hand, a comment on every line, a flowchart beside it.
- Reply in the language the user writes in.
- Banned: slogans; "X, not Y" contrasts nobody raised; "three things, not one"; invented rhetorical questions; "key takeaway", "notice that", "this is why", "now that we understand"; praise; emojis; em-dashes; repeated template labels on every block; analogy in place of mechanism.

## 7. Room audit: answer in writing before building

1. Which slides does this room cover, and is each formula, table, example and class question from them on the board?
2. Is there any term or symbol used before its gloss?
3. Is there any formula without anatomy, or any number without its arithmetic?
4. Could block N be understood by someone who read only blocks 1 to N-1?
5. Did every calculation run in code?
6. Was every paper equation matched against the paper source?
7. Read every sentence: does it make a claim that could be wrong, in words a first-year student knows? Would a working lecturer write it?
8. Own-words test passed for every block?

For important work, give the rendered room to a fresh reviewer told to act as a student who knows nothing: list undefined terms, steps that cannot be followed, unexplained figures, wrong arithmetic, filler. Fix and repeat until it passes.

## 8. Block file format

One file per room, `NN-name.txt`. Line 1: `# Room title`. Blocks separated by a line `====`. First line of a block is its heading, optionally prefixed by a kind; a digit after the kind is the width in columns (1 to 3).

| Kind | Body |
|---|---|
| (none) | text; long lines wrap; leading spaces keep indent |
| `@table` | cells separated by space-pipe-space; first row is the header; no pipe inside a cell |
| `@anat` | intro lines, then `$$ <latex segment> || <label>` lines, then `--`, then closing text. Each segment compiles alone: braces must balance inside it. Empty label = uncoloured |
| `@math` | text lines mixed with `$ <latex>` lines |
| `@flow` | Mermaid `flowchart TB` or `LR` |
| `@xy` | Mermaid `xychart-beta` with `line [...]` series; name the lines in the heading |
| `@code` | code |
| `@img` | line 1 file name in the figures folder; rest is the caption with reading instructions and credit |
| `@qa` | lines starting `A:` become answer boxes |

```bash
python3 scripts/build_board.py rooms/ board.excalidraw --figs figs/ --cols 4
```

Needs Python 3 with Pillow; `pdflatex` and `pdftocairo` for formula images (text fallback without them).

## 9. Without the scripts

- Top level: `{"type":"excalidraw","version":2,"elements":[...],"appState":{"viewBackgroundColor":"#ffffff"},"files":{}}`.
- Unique `id` per element from one global counter.
- Text in a shape: text has `containerId`; shape lists it in `boundElements`.
- Arrow `points` are relative to the arrow's own `x`,`y`.
- Images: `fileId`, `status:"saved"`, `scale:[1,1]`, plus a `files` entry with `mimeType`, `id`, `dataURL`.
- Size text from measured character width (about 11 px per character at size 20 in the hand-drawn font) and line height 1.25.
- Anatomy without LaTeX: write the formula as text, underline each term in its own colour, arrow from a same-colour label to the term.
- Render with `@excalidraw/excalidraw` `exportToSvg` in a headless browser and inspect. For clipboard JSON, pass elements through `restoreElements` first.

## 9a. Layout rules read off the owner's images

- Titles: hand-drawn font (fontFamily 1), size 20 to 28. Body: monospace (fontFamily 3), size 14 or more, never the hand-drawn font.
- Hard-wrap every note at 55 to 75 characters with newlines. One long line per paragraph is the main failure in `B3`.
- A note taller than about 22 lines becomes two notes joined by an arrow.
- Every room contains at least one formula image with arrows, one worked-number note, and one thing that is not text (flow, table, figure, trace).
- Section numbers are continuous. A list of questions is followed by its answers, not placed beside the heading.
- Run `scripts/audit_board.py` on the finished file. It flags long lines, wide notes, small fonts, overlaps, placeholders, one-word leaves, all-text rooms and unanswered questions. Fix each item. A pass is not proof of quality: still open the render.

## 10. Delivery message

Short. In this order: the output of audit_board.py (paste the summary line or the problems left); what was built and in which mode; rooms at full depth; rooms not yet at full depth; checks that actually ran; anything unverified or from memory; the next section to do. Use figure credits when a source's licence requires them.
