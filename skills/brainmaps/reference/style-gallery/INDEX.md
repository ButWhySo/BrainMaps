# Style gallery: the owner's own screenshots

These are real screenshots the owner sent while correcting earlier output. Open every G image (there are fourteen) and every B image with your image viewer before you draw anything. If you cannot view images, the descriptions below are written so you can still follow them. After looking, write two lines for yourself: what you will copy, and which B failure you are most likely to repeat.

## G images: copy these

**G1-annotated-equation-navier-stokes.png** - the formula standard.
- The equation is printed large, as a clean typeset image, on a pale grey panel. A plain name sits above it ("Continuity Equation", "Momentum Equations").
- Under it, each term has its own short underlined label ("Pressure gradient", "Body force term", "Diffusion term") and a thin blue arrow from the label up to that exact term.
- Under each label, one or two plain sentences: what the term does in the physical world ("Fluid flows in the direction of largest change in pressure").
- One term is compound ("Total derivative"). It is expanded below into its own smaller formula, and that formula has its own labels and arrows ("Change of velocity with time", "Convective term").
- Nothing is decoration. Every arrow points at a symbol and every label is a name plus a meaning.

**G2-worked-problem-note-room10.png** - a problem note, from the owner's accepted RL board.
- A numbered heading in the hand-drawn font, an orange arrow leading into it, an orange rule between sections.
- Body in a monospace font, short lines broken by hand at about 55 characters, readable at 124% zoom.
- Order of lines: the rule ("GRPO averages the loss per answer"), the numbers ("short: 100 tokens, long: 400 tokens"), the arithmetic ("1/100 = 0.01 per token, 1/400 = 0.0025"), the consequence in plain words ("the model learns: when wrong, ramble"), then the fix with names.
- No adjectives, no summary sentence. Every line is something the reader can check.

**G3-coa-checking-errors-and-worked-examples.png** - the owner's COA board, error detection and CPU time.
- Big handwritten section title ("CHECKING THE ERROR", "Hamming Code"). Everything else is plain monospace notes, each note about 8 to 20 lines.
- Parity bit: definition, "Two types:", curved arrows from that note to one note per type.
- Each type note: rule, then "Example:", then data, count of ones, the bit added, the transmitted word. Two examples per type, one needing 0 and one needing 1.
- CPU time: formula, "or" the same formula in another form, "Where:" then one line per symbol with its unit, then "Example: Suppose... Then:" and the arithmetic line by line, ending in the unit (2 microseconds).
- Hamming code: the positions written as a small text table (`Positions: 1 2 3 4 5 6 7` / `Bits: P1 P2 D1 P4 D2 D3 D4`), then the steps "Step 2", "Step 3", each with its own check.
- A dashed coloured line groups related notes. Arrows connect a note to the next one that needs it.

**G4-coa-datapath-notes-and-ascii-diagrams.png** - the owner's COA board, hardware notes.
- Diagrams are drawn in text inside the note: boxes made of `+----+` and `|  |`, arrows made of `---->`, `v`, `|`. They sit next to the explanation of the same thing (ALU with operand A and B going in and Result and Status Flags coming out; control unit with clock and instruction register; single bus with CPU, Memory, Input, Output on one line).
- Every component note has the same slots: what it does, a list of the operations or signals, a tiny diagram, a numeric example ("A = 5, B = 3, A + B = 8, A - B = 2").
- Comparison notes use fixed slots: "Advantages:" list then "Disadvantages:" list.
- Notes are short enough to read without scrolling inside them. Elbow arrows join notes.

**G5-rl-landscape-paper-notes-overview.png** - the owner's paper-landscape board seen from far away (10% zoom).
- One rounded card per paper or method. Inside: a title, a few plain paragraphs, then a vertical flow of coloured stage boxes (blue, purple, orange, green) showing what that paper does step by step.
- Real figures from the papers sit as images beside the card, in their own frames.
- A coverage matrix ("Which paper works on which design stage") with a coloured row per paper and a coloured cell per stage.
- A large decision/flow tree on the right with figure thumbnails hanging off it.
- Lesson: the board uses many different shapes and media at once. Zoomed out you can already see which part is a card, which is a flow, which is a table, which is a figure.

## More G images: the owner's accepted RL board and paper-landscape board

**G6-state-and-test-green-answers-and-annotated-trajectory-formula.png**
- End of a room: "9. State and test". One line "STATE: say what each RL word is for an LLM." then Q1 to Q4 in blue monospace, each question directly followed by its answer in a green dashed box ("A: 0.9^4 = 0.6561.").
- Below: a large typeset formula, the trajectory probability. Each factor has an italic blue label with a grey arrow to it, and each label carries a number or a real-world case ("P(on | 65 F) = 0.9", "P(s0 = 65 F)"). A one-line caption under it says what was mapped (the thermostat example, Ch. 3).
- A yellow banner above the figures gives the source and licence once.

**G7-room-with-mixed-formats-figure-formula-chart-table-note.png**
- One room, seven blocks, seven formats: a book figure (agent-environment loop), a reward note with a token row and a "Where the number comes from:" list, a formula (return G_t) with a small example list (gamma 1.0, 0.9, 0.5 giving 1.0, 0.729, 0.125), a line chart of how fast gamma shrinks a reward with the colours named in the title, a two-column comparison table (token view vs bandit view), a "key fact" note with a mini trace.
- Numbered headings in the hand-drawn font, each with an orange arrow leading to it. Orange elbow arrows carry the eye along rows, so the reading order is visible.
- Each note answers "what is it, an example, why it matters".

**G8-code-box-token-diagram-book-figure-and-test.png**
- A code-style box (beige, rounded) holds the real chat template text with each line commented. Next to it a text diagram: `tokens: [system][user prompt ....][assistant answer]` over `loss on: no no YES`, then "Why:" in two lines.
- A book figure with its caption and chapter number under it, then "State and test" with green answer boxes.
- Under that, a heading "4.1 Theory in brief" and a cream card with bullets in the form `[Term: meaning]`, every new word defined in brackets right where it is used.

**G9-book-figures-with-captions-and-theory-card.png**
- Two book figures side by side (CartPole with force arrows and labelled variables; the RLHF loop with prompts, agent, completions, reward). Under each, a caption in plain words and the chapter number.
- Same card pattern below: teal heading, cream card, defined terms in brackets.

**G10-paper-card-with-flow-and-embedded-paper-figures.png**
- A paper card: left, the paper's own figures with their captions kept; right, a vertical flow in the owner's words ("Current PCB routing state", "Learned world model", "Predict several future outcomes", "Choose high-level routing decision", "Observe actual outcome") with a loop arrow back to the start.
- Below, a second framework figure with its original caption. Figures sit inside rounded frames, each frame one paper.

**G11-landscape-tree-labelled-arrows-to-figure-cards.png**
- A decision tree of the whole field (stage 0 to 5) in plain boxes. From a stage, a labelled arrow (the method name on the arrow) leads to a framed card holding that method's real figures.
- Dashed arrows mark a weaker link ("KiCad tool-call models"). Each box says what the stage is: "3. Physical PCB placement: footprints, coordinates, rotations".

**G12-paper-notes-with-stage-flowcharts.png**
- Paper notes at 40% zoom: a rounded title tag ("PCBWorld: RL for actual KiCad PCB routing"), then short paragraphs in the hand-drawn font, one formula line inline, then a coloured flowchart of the method's loop (blue steps, green end step).
- Beside it the next paper: stage boxes A, B, C with numbered sub-steps in small boxes; a reward breakdown (think 0.2, answer 0.4, logic 0.2, format 0.2) as four green boxes under one orange total.
- Each paper note states what it takes in, what it does not do, then the stages.

**G13-coverage-matrix-covered-green-gap-red.png**
- A matrix titled "Which paper works on which design stage". Columns are the stages in order, joined by arrows. Under each, green boxes for the papers that cover it, each with its method in one line (PPO, SFT then PPO).
- Red dashed boxes mark gaps ("NO PAPER TRAINS A MODEL FOR THIS STAGE", "No paper goes from natural-language requirements to a manufacturable board"). A two-item legend sits at the bottom.

**G14-overview-30-percent-zoom-tree-and-figure-cards.png**
- The whole landscape at 30%. Even this far out, the tree, the figure cards and the labelled arrows are distinguishable. Use it to judge whether a board has structure: if a zoomed-out view looks like a uniform grey wall, it has none.

## Extra rules from G6 to G14

8. Every "State and test" block puts each answer in a green dashed box directly under its question.
9. Every figure has a caption in plain words and its source chapter or paper under it. State the licence once in a banner, not under every figure.
10. Reading order is drawn: numbered headings and arrows from one block to the next.
11. Formula labels carry a number or concrete case, not only a name (G6).
12. New terms are defined in brackets where they first appear (G8, G9).
13. Where the source has a figure, embed it. Where it has none, draw a flow or chart. A room made only of text is a failure (B3).
14. Gaps are shown, in red, as visibly as coverage (G13).

## B images: do not produce these

**B1-bad-bare-nodes-and-yellow-placeholder.png** and **B2-bad-one-word-leaves.png**
- Map leaves with one or two words ("Rollouts", "Reward", "Agent", "State"). A reader learns nothing from them.
- A yellow dashed box reading "Place image: a dog trainer with a pouch of treats...". A placeholder is a missing deliverable. The owner asked "what are these yellow boxes?".
- Same tree shape and same colour scheme in every room.
- Fix: leaves read "term - what it is, in plain words"; the figure is embedded or drawn; each room's shape follows its content.

**B3-bad-wall-of-small-paragraphs.png** - the newest failure, from a board on operating-system kernels.
- The whole room is headings plus one long single-line paragraph under each. Lines run past the frame and off the screen. At 50% zoom the text is too small to read.
- Body text is set in the small hand-drawn font. G2 and G3 use monospace for body text and hand-drawn only for titles.
- There is no drawn thing in the room: no formula image, no diagram, no table, no figure, no step-by-step trace. The one worked example (a counter going 50 to 51 and losing an update) is buried inside a paragraph instead of being laid out line by line.
- Section numbers skip (4, 5, 7, 8, 10, 11, 13), so the reader cannot tell whether something is missing.
- A list of questions ("Q1. Which data is touched by an append?") overlaps the heading above it, and the answers are not next to the questions.
- Terms are defined in a block ("Critical section: ... Race condition: ... Mutual exclusion: ...") with no example for each and no picture of two threads interleaving.
- Fix: for each idea choose the format from G1 to G5 that fits it. A race condition is a two-column trace of two threads with the shared counter's value on every line. A term list is a table with an example column. Questions sit directly above their answers.

## Rules read off the images

1. Titles in the hand-drawn font; body text in monospace at 14 or larger.
2. Hard-wrap every note at about 55 to 75 characters. A note taller than 22 lines is two notes.
3. One idea per note, in this order: rule, example with numbers, consequence in plain words, name.
4. Every room has at least one formula image with arrows, one worked-number note, and one drawn thing that is not text (flow, table, figure, trace).
5. Numbering is continuous. Questions are followed by their answers.
6. Notes are joined by arrows in reading order. A reader follows the arrows and learns things in the order they are needed.
7. After building run `python3 scripts/audit_board.py board.excalidraw`. It catches the B3 failures. It does not replace opening the render and looking at it.
