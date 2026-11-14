export const meta = {
  name: "leukerbad-cross-vendor",
  description: "Per track: synthesize all 20 company briefs and playbooks into one cross-vendor solutions page (team plays, decision tree, combos, no-hardware options)",
  phases: [
    { title: "Cross-vendor synthesis", detail: "one page per track from the company briefs and playbooks" },
  ],
}

const ROOT = args.root
const TODAY = args.today
const SLUGS = ['AGIBOT', 'Binabik-AI', 'coprod', 'D-Robotics', 'Dobot', 'Flexiv', 'Galaxea', 'Galbot', 'Genisom-AI', 'Leadshine', 'Magiclab', 'Omnicor-AI', 'OriginFlow', 'ROKAE', 'SKYLANDX', 'Spirit-AI', 'Unitree', 'UniX-AI', 'WUJI', 'XREAL']

const CH = [
  { code: 'T01', folder: 'T01-Autonomous-Urban-Services', title: 'Autonomous Urban Services', tagline: 'Let robots become intelligent service partners of the future city.',
    dirs: ['Autonomous delivery & urban logistics', 'Smart cleaning & facility maintenance', 'Public-space service robots', 'Autonomous urban inspection', 'Smart guidance & information services', 'Autonomous navigation & path planning', 'Human-robot interaction in complex cities'] },
  { code: 'T02', folder: 'T02-Resilient-and-Safe-City', title: 'Resilient & Safe City', tagline: 'Use robots to build a safer, more resilient future city.',
    dirs: ['Emergency rescue robots', 'Autonomous inspection in hazardous environments', 'Infrastructure safety monitoring', 'Disaster response & environment sensing', 'Smart security monitoring', 'Autonomous navigation in complex terrain', 'Human-robot collaborative emergency response'] },
  { code: 'T03', folder: 'T03-Sustainable-City', title: 'Sustainable City', tagline: 'Use robotics to drive a greener, more sustainable future.',
    dirs: ['Smart waste sorting & collection', 'Environmental monitoring robots', 'Energy-efficient robotic systems', 'Sustainable urban infrastructure', 'Water & energy management', 'Smart recycling & resource optimization', 'Environmental data collection & analysis'] },
  { code: 'T04', folder: 'T04-Elderly-Care-and-Rehabilitation', title: 'Elderly Care & Rehabilitation', tagline: 'Let robots help people live healthier, more independent and dignified lives.',
    dirs: ['Daily living assistance for seniors', 'Smart care robots', 'Rehabilitation training robots', 'Mobility assistance & support', 'Human-robot interaction & companionship', 'Automation in care scenarios', 'Smart health monitoring & assistance'] },
]

function prompt(ch) {
  const dir = ROOT + '/Challenges/' + ch.folder
  const tag = ch.code.toLowerCase()
  const dirs = ch.dirs.map((d, i) => ch.code + '.' + (i + 1) + ' ' + d)
  return `CONTEXT
Leukerbad Robotics Hackathon 2026 is running now (${TODAY} is day 1 of Nov 14–16) at Sportarena Leukerbad, Switzerland. About CHF 1M of robots on site from 20 companies. Tracks are OPEN: each team defines its own problem inside a theme. Judging: technical quality, innovation, real-world value, completeness; one champion per track goes to a final with pitch plus live robot demo. Teams of up to 5; build window about 47 hours. Personally operating high-value robots requires third-party liability insurance covering borrowed equipment; without it a team is limited to software, simulation, digital twins or low-value devices such as the LeRobot SO-101. Leukerbad is a small alpine thermal-spa resort with rehabilitation clinics, many elderly guests, tourism, steep terrain, snow and mountain hazards.
A knowledge base already exists under ${ROOT}/ . For every company there is a folder ${ROOT}/Companies/<Company>/${ch.folder}/ containing <Company>-${ch.code}-1-Brief.md (fit score, best hardware, fastest demo, risk), <Company>-${ch.code}-2-Products-and-Solutions.md and <Company>-${ch.code}-3-Playbook.md (3–4 build concepts with 48-hour plans, cross-vendor combos). Company folder names: ${SLUGS.join(', ')}.

YOUR TASK — CROSS-VENDOR SOLUTIONS for track ${ch.code} "${ch.title}"
Official tagline: ${ch.tagline}
Official directions:
${dirs.map(d => '  ' + d).join('\n')}

Write ONE file: ${dir}/${ch.code}-3-Cross-Vendor-Solutions.md
(Idempotency: first run: ls -la "${dir}" . If the file already exists and is larger than 4000 bytes, return immediately.)

STEP 1 — Read (no web research is needed; this is a synthesis of the knowledge base, web search allowance 0):
- ${dir}/${ch.code}-0-Track-Overview.md and ${dir}/${ch.code}-1-Solution-Patterns.md
- ${ROOT}/Event/Event-Intel.md (rules, judging, insurance, schedule)
- the Brief of ALL 20 companies for this track (20 files; read them in parallel batches)
- the Playbook of every company whose brief gives fit 3 or higher, plus the Playbooks of XREAL, SKYLANDX, D-Robotics and WUJI (add-on vendors) whatever their fit
- skim ${ROOT}/Companies/<Company>/<Company>-Developer-Guide.md for the 3–4 platforms you end up recommending most, to make sure your integration claims match what their SDKs allow

STEP 2 — Write the file. English, decision-oriented, scannable (tables, short bullets, bold key facts). Never invent capabilities: every claim about a product must come from the company docs you read; say "unconfirmed on site" where the docs say so. Use standard relative markdown links (no wikilinks): a company doc is linked as ../../Companies/<Company>/${ch.folder}/<Company>-${ch.code}-3-Playbook.md (or ...-1-Brief.md), a company profile as ../../Companies/<Company>/<Company>.md .

---
type: track-cross-vendor
challenge: ${ch.code}
challenge_title: "${ch.title}"
updated: ${TODAY}
tags: [leukerbad-hackathon, ${tag}, cross-vendor]
---
# ${ch.code} ${ch.title} — Cross-Vendor Solutions
First line under the title (navigation): [Start here](../../00-START-HERE.md) · [Track overview](${ch.code}-0-Track-Overview.md) · [Official directions: who has what](${ch.code}-6-Official-Directions-Who-Has-What.md) · [Hardware shortlist](${ch.code}-2-Hardware-Shortlist.md) · [Solution patterns](${ch.code}-1-Solution-Patterns.md)
## Choose in five minutes
(a Mermaid flowchart in a fenced code block with language "mermaid": from the team's constraints — insurance yes/no, hardware actually available, skills — to a recommended platform class and concept; keep node labels short and free of special characters; then 4–6 bullets explaining the branches)
## Team plays — the strongest solutions for this track
6–8 concrete solutions that combine vendors, ordered from most reliable to most ambitious. For each a "### Play N — <name>" section with: **Official direction(s) served** · **Problem → value in Leukerbad** · **Hardware** (company and model, with links to the company playbooks) · **Software stack** (which SDKs / models / open-source pieces, where compute runs) · **Why it can win** (one line each for technical quality, innovation, real-world value, completeness) · **48-hour outline** · **Main risk and fallback** · **Team profile it suits**.
## Best combination per official direction
(table with one row per official direction, in order: Direction | Strongest platform | Add-ons | One-line concept | Open)
## What pairs with what
(table: base platform (rows) × add-on vendors — XR glasses, 3D scanner, edge compute, dexterous hand, agent / AI software, EMG data capture — with a short note in each useful cell)
## If you have no insurance or no robot
(software, simulation, digital-twin and low-value-device concepts that still fit this track and still use the vendors' open SDKs, simulators, datasets or models; 4–6 concrete ideas with the repos or tools named in the company docs)
## If your first-choice hardware is taken
(table: first choice | plan B | plan C | what changes in the build)
## Approach comparison
(table: approach | technical depth | demo reliability | innovation | real-world value | completeness in 47 h — rate each low / medium / high with a few words)
## Sources
(the knowledge-base docs you used, as relative links)

RETURN: one line — the file written and the names of the plays.`
}

async function tryAgent(p, opts) {
  let r = await agent(p, opts)
  if (r == null) {
    log('retrying ' + opts.label)
    r = await agent(p + '\n\n(Second attempt: an earlier run was interrupted. Check whether the output file exists and finish or repair it.)', Object.assign({}, opts, { label: opts.label + ':retry' }))
  }
  return r
}

const out = await parallel(CH.map(ch => () => tryAgent(prompt(ch), { label: 'cross-vendor:' + ch.code, phase: 'Cross-vendor synthesis', agentType: 'general-purpose', effort: 'high' })))
return out.map((o, i) => CH[i].code + ': ' + (o ? String(o).slice(0, 400) : 'FAILED'))