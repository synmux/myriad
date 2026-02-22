# You're Wrong About AI Water Use

(but only in that you don't go far enough)

---

> Include concrete numbers where possible, intuitive comparisons, and a section on what is worth focusing on.

- Why water usage is not the most important or urgent concern in AI, compared to other impacts (e.g. labour, power concentration, surveillance, safety)
- The actual issue is datacentres at all.
  - Certain types of compute run exponentially more quickly on GPUs.
    - Yes, that's right, graphics cards.
    - They're fast.
    - **They also run exceptionally hot**.
  - Yesterday, the heat-generating compute was cryptocurrency mining.
  - Today, the heat-generating compute is AI
  - Tomorrow, it'll be something we can't even envision right now.
  - What they have in common is **heat**.
  - That heat has to be dealt with - ie, taken away from the heat-generating components.
    - It's then dumped somewhere - the outside air, the ocean, a glacier, whatever.
    - This is why datacentres in space will never work. They can't dump their heat.
    - The most common technology - one which works in dry, hot climates - is **evaporative cooling.**
    - This uses water. The heat energy is used to evaporate the water, and the water is lost.
- But it doesn't have to be that way!
  - There are alternatives to evaporative cooling.
    - One, which I still don't understand why we don't do, is... build datacentres in cold places.
      - The heat can literally be dumped to the outside air.
      - No evaporation required.
      - Even better thermodynamics can be achieved by dumping the heat into the sea or a glacier.
    - In Malmo in Sweden, they simply dump heat into the ambient air.
      - There's a closed loop of water or some other fluid circulating around the system.
      - The water's temperature just changes as it circulates around the cooling loop.
      - When it reaches the outside, heat exchangers dump it in the atmosphere.
      - When it reaches the inside, it absorbs heat from the datacentre equipment such as servers and routers.
      - Consider that you're not going to make any impact on the atmosphere's temperature by pointing a hot air blower out the window.
    - One idea - which is a bit pie in the sky - is datacentres at sea.
      - These have major power issues.
        - To be viable they would need onsite nuclear or **massive** solar and/or wind.
      - However, their heat management strategy is sound.
        - Just dump it into the ocean.
    - [Claude: other ideas?]
- So it really isn't about AI. AI is just the workload right now.
  - We need to rethink where and how we build datacentres.
  - Maybe don't build something which is like 70% heat management in the desert?
- Pun: "hot take"
  - What can I say, I couldn’t resist.

---

## Expanded Plan (Self-Sufficient)

This is the fully fleshed-out plan for a ~3,000–4,000 word blog post. It is designed to be self-sufficient: anyone reading this section alone should have everything they need to write the final article. All statistics have been independently verified against primary sources. Corrections to the original outline are noted inline.

### Thesis

People who criticise AI for water usage are pointing at the right problem but framing it too narrowly. The real issue is datacenter cooling infrastructure choices — not AI specifically — and water isn’t even the most urgent AI concern compared to labour exploitation, power concentration, surveillance, safety, and energy/carbon.

### Voice and Style

- **British English** throughout (centre, labour, colour, defence, minimise)
- Short declarative sentences for emphasis
- Parenthetical asides and self-aware humour
- Technical accuracy without jargon — explain everything, don’t talk down
- Let numbers do the emotional heavy lifting in Section 6
- The "hot take" pun is pre-committed; lean into it

### Estimated Word Count

| Section                                          | Target Words |
| ------------------------------------------------ | ------------ |
| 1. The Number Everyone Quotes                    | ~400         |
| 2. It’s Not AI. It’s Heat.                       | ~500         |
| 3. The Dumbest Possible Way to Cool a Datacenter | ~700         |
| 4. Just Build Them in Cold Places                | ~500         |
| 5. No, You Can’t Put Them in Space               | ~200         |
| 6. What You Should Actually Be Worried About     | ~800         |
| 7. The Actual Hot Take (Conclusion)              | ~300         |
| **Total**                                        | **~3,400**   |

### Argument Arc

1. The viral number is unreliable → **destabilise**
2. The real variable is heat, not AI → **reframe**
3. We cool heat in the dumbest way possible → **indict**
4. Better ways exist and are proven → **construct**
5. Space won’t save us → **entertain and reinforce**
6. Bigger problems deserve your outrage → **redirect**
7. Stop being distracted → **synthesise**

---

### Section 1: "The Number Everyone Quotes (and Gets Wrong)" (~400 words)

**Purpose:** Hook reader with the viral "bottle of water per query" stat, then destabilise it.

**Content to cover:**

Open with the headline claim everyone has seen: "every ChatGPT query uses a bottle of water." It’s viral, it’s shareable, and it’s wrong — or right — depending on whom you ask and what you count.

The actual range spans three orders of magnitude:

- **Industry claims (direct on-site cooling only):** Sam Altman stated an average ChatGPT query uses approximately **0.32ml** of water — about five drops, or one-fifteenth of a teaspoon. Google published a similar figure for Gemini: **0.26ml** per median text prompt (August 2025 technical report). These figures count only water physically consumed in datacenter cooling systems.
  - _Source: DatacenterDynamics, reporting Altman’s statement; Google Cloud Blog, "Measuring the environmental impact of AI inference" (August 2025)_

- **Academic estimates (full lifecycle):** The peer-reviewed paper "Making AI Less ‘Thirsty’" by Li, Yang, Islam, and Ren (UC Riverside, 2023) found that **20 to 50 ChatGPT queries** consume roughly **500ml** (one bottle) of water — approximately **10–25ml per query** when accounting for direct cooling, indirect water from electricity generation, and manufacturing. This is the study that spawned the "bottle of water" headline, but the headline misrepresents it: the paper says 500ml per 20-50 queries, not per single query.
  - _Source: arXiv:2304.03271; published in Communications of the ACM (2025)_

- **Independent energy-based estimates** (accounting for both direct and indirect water) place the figure at roughly **3.5–5ml per query** for GPT-4o-class models.
  - _Source: Sean Goedecke’s analysis (2025)_

The key point: the spread from 0.26ml to 25ml is roughly a **100x range**. That variance is the tell. It means the problem isn’t AI. It’s _where and how you cool the thing_.

**Note:** The original plan cited "519ml per query" as a worst-case figure. This is a misreading of the Li & Ren paper. The correct figure is ~500ml per 20-50 queries (~10-25ml per individual query at full lifecycle). The plan also cited a "1,600x spread" — the corrected spread (0.26ml to ~25ml) is approximately 100x, which is still dramatic enough to make the point.

**Transition:** "So which is it? That depends entirely on something that has nothing to do with artificial intelligence."

---

### Section 2: "It’s Not AI. It’s Heat." (~500 words)

**Purpose:** Reframe from "AI uses water" to "GPUs generate heat, heat must go somewhere." Water is a cooling problem, not a compute problem.

**Content to cover:**

GPUs are fast. They also run exceptionally hot. The power consumption progression for datacenter GPUs:

- **NVIDIA V100/A100 (2017–2020):** 250–400W TDP depending on form factor
- **NVIDIA H100 (2023):** 700W TDP (SXM5 variant)
- **NVIDIA B200 (2024–2025):** 1,000–1,200W TDP
- **NVIDIA GB200 Superchip:** 2,700W total (2× B200 at 1,200W each + 1× Grace CPU at 300W)
- _Sources: NVIDIA datasheets; TRG Datacenters; TweakTown; Introl deployment guides_

**Correction from original plan:** The plan stated "150–200W traditional" as the starting point. This is too low for datacenter GPUs (it’s closer to consumer/workstation GPUs). The correct baseline for datacenter-grade GPUs is 250–400W.

Rack density has followed the same trajectory:

- **~5 kW per rack** (2010s average enterprise) — verified via Ramboll, Enconnex, and industry surveys showing 2.4–6 kW averages between 2008–2014
- **132 kW per rack** (2025) — specifically the NVIDIA GB200 NVL72, per Schneider Electric’s reference architecture
- **250–900 kW per rack** projected for 2026–2027 (Blackwell Ultra / Rubin generation with 576 GPUs per rack). NVIDIA showed 1 MW rack designs at OCP 2025.
- _Sources: Ramboll; Schneider Electric / DatacenterDynamics; Introl; Axautik Group_

The workload changes; the heat doesn’t. Yesterday: cryptocurrency mining. Today: AI training and inference. Tomorrow: something we can’t envision. This isn’t hypothetical — crypto miners are literally pivoting their infrastructure to AI. By October 2025, public Bitcoin miners had signed over **$65 billion** in AI and high-performance computing contracts with hyperscalers including Amazon and Microsoft, with approximately 70% of mining companies pivoting to include AI infrastructure.

- _Source: CoinShares (October 2025); DatacenterDynamics; ETF Trends_

Cooling accounts for approximately **40% of a datacenter’s total electricity** on average, with a range from 7% (efficient hyperscale) to 55% (older enterprise facilities).

- _Sources: National Renewable Energy Laboratory; Congressional Research Service report R48646; Stanford analysis_

This is the "hot take" pun insertion point. "What can I say, I couldn’t resist."

**Transition:** "If the problem is heat, the question becomes: how do we deal with it? And the answer, far too often, is the dumbest possible way."

---

### Section 3: "The Dumbest Possible Way to Cool a Datacenter" (~700 words)

**Purpose:** Explain evaporative cooling, then build indignation at the absurdity of desert datacenters. This is where the concrete water numbers land.

**Content to cover:**

**Explain evaporative cooling simply:** Spray water onto something hot. The water absorbs heat as it evaporates. The heat goes into the atmosphere. The water is gone forever. It works brilliantly in dry, hot climates — which is precisely where you shouldn’t be using a technology that consumes water.

**The scandal:** According to Bloomberg’s 2025 analysis (using data from World Resources Institute and DC Byte), approximately **two-thirds of new datacenters** built or in development since 2022 are in areas already experiencing high levels of water stress. More than 160 new AI datacenters have been built in the US in the past three years in water-stressed locations — a 70% increase from the prior three-year period.

- _Source: Bloomberg, "The AI Boom Is Draining Water From the Areas That Need It Most" (2025)_

**Case studies as a litany of poor decisions:**

- **The Dalles, Oregon:** In 2021, Google’s three datacenter sites used 355 million gallons of water — approximately **29% (roughly one-third) of the town’s entire water supply**. Usage tripled between 2017 (124.2 million gallons) and 2021. Google initially fought to keep these figures secret: the city sued The Oregonian newspaper to prevent disclosure, claiming trade secret status. A district attorney ruled against the city. Google has continued expanding, with additional facilities built in 2025 and more planned.
  - _Sources: IT Pro; OPB (January 2026); DatacenterDynamics; Fortune longform investigation_

- **Uruguay:** Google’s original plan for a datacenter called for cooling towers consuming **7.6 million litres (2 million gallons) of potable water per day** — equivalent to the daily domestic use of 55,000 people. This plan emerged during Uruguay’s **worst drought in 74 years**, during which a state of emergency was declared in Montevideo and authorities diluted public drinking water with salty water. Protests erupted: "It’s not drought, it’s pillage." After public outcry, Google redesigned the project to use air cooling instead.
  - _Sources: The Guardian; Mongabay; DatacenterDynamics; TechTimes_

- **Mesa/Phoenix, Arizona:** Datacenters in the desert requiring millions of gallons daily. In Arizona, agriculture already takes approximately **72–74%** of water withdrawals. One council member: "data centres are an irresponsible use of our water."
  - _Sources: MAP Arizona Dashboard; Arizona Department of Water Resources; CLIMAS (University of Arizona)_

**Correction from original plan:** The plan cited Arizona agriculture at 86% of water withdrawals. Current official data (University of Arizona MAP Dashboard, USGS) shows approximately 72–74%. The lower figure is still striking enough to make the point.

**Aggregate numbers:**

- US datacenters consumed approximately **17 billion gallons** of water directly through cooling in 2023, projected to **double or quadruple by 2028**.
- Indirect water consumption (from the electricity that powers datacenters): an additional **211 billion gallons** — roughly **12× the direct cooling figure**.
- _Source: Lawrence Berkeley National Laboratory, 2024 report on 2023 data_

**Perspective — putting it in context:**

- US datacenters account for approximately **0.04% of total US freshwater consumption** (direct on-site only). This is small in absolute terms.
- For comparison: thermoelectric power withdraws approximately **133 billion gallons per day** (**~48.5 trillion gallons annually**) — dwarfing datacenters by orders of magnitude.
  - _Source: USGS Circular 1441, "Estimated use of water in the United States in 2015"_
- The textile industry uses approximately **200 tonnes of water per tonne of fabric** and generates **20% of global industrial wastewater**.
  - _Sources: OECD Environment Working Papers No. 253; CNN; Geneva Environment Network_

**The point:** Datacenter water use matters _locally and specifically_ — Google using a third of The Dalles’ water is a real problem for The Dalles — but the per-query number fixation misses the structural issue entirely. The 0.04% national figure tells you the problem isn’t the total volume; it’s the concentration of demand in water-stressed locations.

"Maybe don’t build something which is 70% heat management in the desert?"

**Transition:** "If evaporative cooling in deserts is so clearly mad, is there an alternative? Yes. Several. Some startlingly obvious."

---

### Section 4: "Just Build Them in Cold Places (and Other Apparently Radical Ideas)" (~500 words)

**Purpose:** Show proven alternatives exist and are deployed at scale. The water problem is a _choice_, not an inevitability.

**Content to cover:**

**Cold-climate free cooling:**

- **Verne Global (now Verne), Iceland:** Free cooling from subarctic climate for virtually the entire year, eliminating mechanical refrigeration. 100% renewable power (geothermal + hydro). PUE 1.21. Housed on the site of a former NATO base. Operational since 2012; 15MW Nscale AI deployment announced 2025.
  - _Sources: Data Center Knowledge; Verne Global website; Nortek Air Solutions_

- **Green Mountain, Stavanger, Norway:** Inside a former NATO ammunition storage bunker carved into a mountainside. Fjord water at a constant 8°C drawn from 100-metre depth by gravity. 100% renewable hydropower. PUE 1.18. Operational since 2013.
  - _Sources: Green Mountain website; Data Center Knowledge; Conyx Cloud Solutions_

- **AQ Compute, near Oslo, Norway:** Closed-loop rear-door heat exchangers, immersion cooling, and direct-to-chip cooling. PUE 1.07–1.2. Operational since February 2024.
  - _Sources: AQ Compute website; Datacenter Forum; DatacenterDynamics_

**District heating reuse** — the heat isn’t waste, it’s a resource in the wrong place:

- **Stockholm Data Parks, Sweden:** By 2022, Stockholm Exergi’s Open District Heating initiative had recovered enough heat from datacenters to warm **30,000 modern apartments** annually. Target: 10% of Stockholm’s heating from recovered datacenter waste heat. Network spans ~3,000 km of pipes.
  - _Sources: EU Covenant of Mayors; Stockholm Exergi; Stockholm Data Parks_

- **Odense, Denmark:** Meta’s hyperscale Tietgenbyen datacenter provides up to **165,000 MWh annually** via Fjernvarme Fyn, warming **11,000 homes and businesses**. Denmark’s biggest heat pump plant (~45 MW), part of their coal phase-out.
  - _Sources: Ramboll; Munters case study; Alfa Laval_

- **Google Hamina, Finland:** In partnership with city-owned Haminan Energia, provides heat covering **80% of the local district heating demand**. Heat provided free of charge to households, schools, and public service buildings. Operates at 97% carbon-free energy. Operational late 2025.
  - _Sources: Google Blog; The Energy Mix; DatacenterDynamics_

- **Microsoft Espoo, Finland:** In partnership with Fortum, will supply zero-emission district heating to approximately **250,000 users** across Espoo, Kauniainen, and Kirkkonummi. Described as the world’s largest datacenter waste heat recovery scheme. At full capacity, covers approximately 40% of those users’ heat demand.
  - _Sources: Microsoft News Centre Europe (2022); Fortum; City of Espoo; Enter Espoo_

**Correction from original plan:** The plan stated Microsoft Espoo would heat "an entire city and two neighbouring municipalities." This overstates the capacity — it serves those areas but covers approximately 40% of demand, not 100%.

**Deep lake water cooling:** Toronto’s Enwave system draws 4°C water from Lake Ontario via a 3 km pipe. **75% electricity reduction** compared to traditional air conditioning, saves **832 million litres of water annually**, serves over 100 downtown buildings, avoids over 60 MW of peak electrical demand. Operational since 2004; expanded ~2024.

- _Sources: Enwave website; Washington Post (2021); CBC News_

**Immersion cooling:** Submerge servers in dielectric fluid. Zero water consumption. Real-world PUE as low as **1.02–1.07** (Alibaba, BitFury).

- _Sources: Energy Informatics / SpringerOpen (2023); various deployment reports_

**Closed-loop systems:** Fill once, circulate forever, no ongoing water consumption.

- **Microsoft:** All new datacenter designs since August 2024 use closed-loop, chip-level cooling with zero water evaporation. Saves 125+ million litres per datacenter annually. Pilots in Phoenix, AZ and Mount Pleasant, WI in 2026; online from late 2027.
- **Oracle:** Direct-to-chip, closed-loop, non-evaporative liquid cooling. Only needs filling once. Planned for sites in New Mexico, Michigan, Texas, and Wisconsin (announced February 2026).
- _Sources: Microsoft Cloud Blog (December 2024); Oracle Blog (February 2026); DatacenterDynamics; GeekWire_

Microsoft has committed to **zero-water datacenters from 2027**. If Microsoft can do it, it’s clearly feasible.

**Transition:** "At this point, someone in the comments is going to suggest putting datacenters in space. Let me save us all some time."

---

### Section 5: "No, You Can’t Put Them in Space" (~200 words, brief aside)

**Purpose:** Entertaining digression that reinforces the heat thesis. Physics makes the problem vivid.

**Content to cover:**

The only heat dissipation method in vacuum is thermal radiation. No air. No water. No convection. Just photons leaving a hot surface — slowly.

Multiple technical analyses of orbital datacenter feasibility cite approximately **~1,200 square metres of radiator surface per megawatt** of waste heat as a key constraint.

- _Sources: Exellyn ("From sci-fi to reality"); EE Times ("The Hidden Physics of Running Data Centers in Orbit"); Chaotropy analysis_

A 100 MW datacenter (modest by modern standards) would need **120,000 square metres** (~**12 hectares**) of radiators — roughly **17 football pitches**.

The ISS External Active Thermal Control System (EATCS) can reject a total of **70 kW** of heat (two independent ammonia loops at 35 kW each), using 24 radiator panels measuring approximately 3.12m × 13.6m each.

- _Source: NASA ISS ATCS Overview; Wikipedia — External Active Thermal Control System_

**Correction from original plan:** The plan stated the ISS can only dissipate 16 kW. The correct figure is **70 kW** (EATCS full capacity). The 16 kW figure may refer to the Early EATCS or a subsystem. A single modern GPU rack (132 kW for a GB200 NVL72) produces nearly **twice** the heat the ISS’s entire thermal control system can handle. This is an even more dramatic comparison than the original.

"Space is not cold. Space is a vacuum flask. It keeps things hot."

**Transition:** "The water problem is real, it’s a choice, and the solutions exist. Which brings us to the part where I annoy the other half of the room."

---

### Section 6: "What You Should Actually Be Worried About" (~800 words)

**Purpose:** The "don’t go far enough" payoff. Redirect to genuinely structural, harder-to-solve AI concerns.

**Opening:** "If you’ve spent your outrage budget on water, you’ve been shortchanged."

#### 6a — Labour Exploitation

- Kenyan content moderation workers employed by Sama on behalf of OpenAI earned take-home pay of **$1.32–$2.00 per hour** for traumatic work (child abuse, murder, torture, self-harm content). Workers on nine-hour shifts described being mentally scarred.
  - _Source: TIME exclusive investigation, January 2023_
- OpenAI paid Sama **$12.50/hr per worker** — between 6× and 9× what workers actually received.
  - _Source: TIME; WeeTracker_
- In May 2024, **97 African data labellers** (working for Meta, OpenAI, and Scale AI) published an open letter to President Biden describing conditions as **"modern-day slavery"**, demanding US tech companies stop "systemically abusing and exploiting African workers." Facilitated by the advocacy group Foxglove.
  - _Sources: The Hill; Foxglove open letter; Futurism_
- In July 2023, Kenyan content moderators filed a petition with the Kenyan parliament calling for an investigation into Big Tech outsourcing of content moderation and AI work — an inquiry into "outsourced ethics" that remains ongoing as of February 2026.
  - _Sources: TechCrunch (July 2023); Citizen Digital; Cedra.ai (February 2026)_
- "Every ‘safe’ AI output is built on human suffering at the bottom of the supply chain."

#### 6b — Power Concentration

- The Magnificent Seven (Apple, Microsoft, Alphabet, Amazon, NVIDIA, Meta, Tesla) account for approximately **33% of the S&P 500** market cap as of early 2026, having ranged between 31–37% over the past year.
  - _Sources: The Motley Fool; Nasdaq_
- Big Tech AI capital expenditure: approximately **$427 billion** in 2025, projected to reach **$562 billion** in 2026.
  - _Sources: Goldman Sachs; io-fund.com; IEEE ComSoc_
- A super PAC called "Leading the Future" launched in mid-2025 with over **$100 million** in initial funding from a16z, OpenAI, Perplexity, and Palantir to advocate against strict AI regulation. Separately, registered lobbying firms earned over **$90 million** from AI-related issues in the first three quarters of 2025.
  - _Sources: Axios (January 2026); CNBC; Issue One_
- **451 organisations** lobbied on AI issues in 2023, up from **6 in 2016** — a roughly **7,400% increase**. The eight largest tech/AI companies spent a combined $36 million on federal lobbying in the first half of 2025 alone.
  - _Sources: OpenSecrets (January 2024); CNBC (February 2024)_
- On **December 11, 2025**, President Trump signed an Executive Order directing the Attorney General to establish an AI Litigation Task Force to challenge state AI laws, directing the Secretary of Commerce to identify conflicting state laws within 90 days, and threatening states that enact "onerous" AI laws with loss of federal funding.
  - _Sources: White House official text; DLA Piper analysis; Sidley Austin analysis; Skadden analysis_

#### 6c — Surveillance

- China: an estimated **600–700 million** surveillance cameras, approximately 432 per 1,000 people, increasingly integrated with AI facial recognition.
  - _Sources: CNN; Comparitech; Chinascope_
- Clearview AI: scraped approximately **50–70 billion+** face images from social media (up from 30 billion in 2023, per Clearview’s own claims and US government contract documents).
  - _Sources: Engadget (2023); PetaPixel; Wikipedia; Clearview AI website_
- Israel’s Lavender system: identified **37,000 Palestinians** as potential targets for military action. Human review of each target amounted to approximately **20 seconds** — essentially a rubber stamp to verify the target was male. The system had an approximately 10% error rate. The army determined that for each junior operative, up to 15–20 civilians as collateral damage was permissible.
  - _Sources: +972 Magazine investigation (April 2024); Al Jazeera_
- "AI doesn’t create the surveillance impulse. It makes it cheap, fast, and scalable."

#### 6d — Safety

- **Biden robocalls (January 2024):** An AI-generated deepfake robocall using a synthetic voice mimicking President Biden was sent to 5,000–25,000 New Hampshire voters, telling them not to vote in the primary. Political consultant Steven Kramer was indicted on 26 criminal charges. The FCC imposed a $6 million fine and ruled AI-generated voices in robocalls illegal.
  - _Sources: NPR; PBS; New Hampshire DOJ_
- **Harris deepfake (July 2024):** Elon Musk shared a manipulated video with AI-generated audio making Kamala Harris appear to describe herself as "the ultimate diversity hire." The repost received **128+ million views** on X. Musk violated X’s own synthetic media policy.
  - _Sources: Rolling Stone; Bloomberg; CBC; Council on Foreign Relations_
- **Canadian PM deepfake (May 2025):** A deepfake of PM Mark Carney falsely announcing a ban on pre-2000 vehicles appeared on TikTok the day before the federal election. It reached **1 million+ views** on TikTok and **2.4 million+ views** on X before removal.
  - _Sources: DFRLab (June 2025); PolitiFact; The Journal.ie_
- Autonomous weapons deployed in active conflicts.

**Note from research:** The original plan cited "105,000+ deepfake incidents in the US in 2024" and "$200M+ damages in Q1." This figure could not be traced to a verifiable primary source. Substitute with: businesses lost an average of ~$500,000 per deepfake incident in 2024; North America saw a **1,740% increase** in deepfake fraud between 2022 and 2023. (_Source: Keepnet Labs; Security Magazine_)

#### 6e — Energy and Carbon

- Datacenters consumed approximately **415 TWh** globally in 2024 (**1.5% of global electricity**). The IEA projects this will roughly double to ~945 TWh by 2030 (~3% of global electricity).
  - _Source: IEA "Energy and AI" report (2025)_
- **ChatGPT energy comparison:** The widely cited "10× the energy of a Google search" claim originated from 2023 analysis and a 2024 Goldman Sachs report (ChatGPT at ~3 Wh vs Google search at ~0.3 Wh). However, both figures are now outdated: Altman stated GPT-4o uses approximately 0.3 Wh per query, and Google search is now estimated at ~0.04 Wh. AI inference remains more energy-intensive than traditional search, but the gap has narrowed significantly due to efficiency improvements.
  - _Sources: ZME Science; Washington Post (August 2025); Goldman Sachs (2024)_
- Microsoft total emissions (Scope 1, 2, and 3) have increased **23.4%** compared to their 2020 baseline, despite pledging to be carbon negative by 2030. Scope 3 (supply chain) emissions make up 97% of total. (FY2024 data, published May 2025.)
  - _Sources: Sustainability Magazine; Microsoft blog (May 2025); Newsweek_
- Google total emissions have increased **51%** compared to their 2019 baseline year, driven primarily by datacenter energy consumption for AI workloads (which grew 27% in 2024). Google has not abandoned its 2030 net-zero goal.
  - _Sources: Google 2025 Environmental Report (June 2025); Yale E360; ESG Dive_
- Of new generation capacity being built to meet rising datacenter electricity demand, approximately **60% will come from natural gas** (fossil fuels) and 40% from renewables (27.5% solar, 12.5% wind). Goldman Sachs estimates natural gas will meet 60% of datacenter power needs by 2030 (~28 GW).
  - _Sources: Goldman Sachs Research (2024); Goldman Sachs "6 Ps" report_
- "The energy problem is the water problem’s older, meaner sibling. And unlike water, you can’t solve it by moving to Norway."

**Correction from original plan:** The "ChatGPT uses roughly 10× the energy of a Google search" claim is flagged as outdated. The section should present it as a historically cited comparison that no longer holds cleanly, rather than as current fact.

---

### Section 7: "The Actual Hot Take" (Conclusion, ~300 words)

**Purpose:** Synthesise. Leave the reader with a clear, memorable thesis.

**Content to cover:**

- Water criticism points at the right problem (corporate irresponsibility in infrastructure) but uses the wrong frame (AI bad).
- The workload is irrelevant. Crypto yesterday, AI today, something else tomorrow. The constant: we build heat-intensive infrastructure in the worst possible places using the most water-intensive cooling because land is cheap and regulations are weak.
- The solutions exist, are proven, are deployed. The barrier is economic and political, not technical. Microsoft’s zero-water commitment from 2027, Norway’s fjord-cooled bunkers, Stockholm heating 30,000 homes with waste heat — these aren’t prototypes. They’re operational.
- Meanwhile, genuinely hard problems — labour, power, surveillance, safety, energy — get less airtime because "AI drinks water" fits in a headline and "the entire AI supply chain is built on exploited labour in the Global South" does not.
- Closing line: "You’re right that AI water use is a problem. You’re wrong that it’s _the_ problem. And until we stop being distracted by the solvable issues, the unsolvable ones will keep getting worse."

---

### Sources / Further Reading

Sources are grouped here by topic for reference. In the final post, they should appear as inline citations or a flat list.

**Water usage data:**

- Li, Yang, Islam, Ren (UC Riverside): "Making AI Less ‘Thirsty’" — arXiv:2304.03271 (2023); Communications of the ACM (2025)
- Sam Altman on ChatGPT water usage — DatacenterDynamics
- Google Cloud Blog: "Measuring the environmental impact of AI inference" (August 2025)
- Sean Goedecke: independent energy-based water usage analysis (2025)
- Lawrence Berkeley National Laboratory: 2024 datacenter water report (17B gal direct, 211B gal indirect)
- Bloomberg: "The AI Boom Is Draining Water From the Areas That Need It Most" (2025)
- USGS Circular 1441: "Estimated use of water in the United States in 2015" (thermoelectric withdrawals)
- Google 2024 Water Stewardship Report
- OECD Environment Working Papers No. 253 (textile industry water usage)

**Datacenter locations and water conflicts:**

- OPB: Google water demands and The Dalles (January 2026)
- Fortune: Google datacenter / The Dalles water dispute (longform investigation)
- DatacenterDynamics: disclosure lawsuit and water figures
- The Guardian: Google datacenter plan in Uruguay (2023)
- Mongabay: data centers and drought in Latin America (2023)
- MAP Arizona Dashboard / University of Arizona CLIMAS: Arizona water usage by sector

**Cooling alternatives:**

- Green Mountain, Norway — fjord cooling (greenmountain.no)
- Verne Global (now Verne), Iceland — free air cooling (verneglobal.com)
- AQ Compute, Norway — rear-door heat exchangers (aq-compute.com)
- Stockholm Data Parks / Stockholm Exergi — district heating (stockholmdataparks.com)
- Ramboll: Meta surplus heat in Odense, Denmark
- Google Blog: Hamina, Finland heat recovery (late 2025)
- Microsoft News Centre Europe: Espoo, Finland waste heat scheme (2022)
- Enwave Toronto — deep lake water cooling (enwave.com)
- Microsoft Cloud Blog: zero-water datacenter design (December 2024)
- Oracle Blog: closed-loop cooling (February 2026)

**GPU power and rack density:**

- NVIDIA datasheets (V100, A100, H100, B200, GB200)
- TRG Datacenters: H100 power consumption guide
- Ramboll: rack density evolution
- Schneider Electric / DatacenterDynamics: GB200 NVL72 reference architecture
- Introl: high-density rack analysis; deployment guides

**Crypto-to-AI pivot:**

- CoinShares (October 2025): $65B in AI contracts from Bitcoin miners
- DatacenterDynamics: crypto pivot to AI analysis
- ETF Trends: Bitcoin miners shift to AI data centres

**Space datacenter infeasibility:**

- Exellyn: "From sci-fi to reality" — orbital datacenter analysis
- EE Times: "The Hidden Physics of Running Data Centers in Orbit"
- Chaotropy: "Why Jeff Bezos is probably wrong"
- NASA ISS ATCS Overview (EATCS: 70 kW capacity, 24 radiator panels)

**Labour exploitation:**

- TIME: exclusive investigation into OpenAI / Sama / Kenya (January 2023)
- WeeTracker: OpenAI-Sama controversy analysis
- The Hill: 97 data labellers’ open letter to Biden (May 2024)
- Foxglove: original open letter text
- TechCrunch: Kenyan moderators’ petition to parliament (July 2023)
- Cedra.ai: "Outsourced Ethics" inquiry update (February 2026)

**Power concentration:**

- The Motley Fool / Nasdaq: Magnificent Seven S&P 500 market cap share
- Goldman Sachs / io-fund.com / IEEE ComSoc: Big Tech AI capex figures
- Axios (January 2026): AI lobbying spending
- CNBC: "Leading the Future" super PAC
- OpenSecrets (January 2024): AI lobbying organisation count
- White House: Executive Order text (December 11, 2025)
- DLA Piper / Sidley Austin / Skadden: EO legal analyses

**Surveillance:**

- CNN / Comparitech / Chinascope: China surveillance camera estimates
- Engadget / PetaPixel / Clearview AI: facial image database size
- +972 Magazine (April 2024): Lavender investigation
- Al Jazeera: Lavender and Gospel systems

**Safety (deepfakes and elections):**

- NPR / PBS / New Hampshire DOJ: Biden robocall incident (January 2024)
- Rolling Stone / Bloomberg / CBC / CFR: Harris deepfake shared by Musk (July 2024)
- DFRLab / PolitiFact / The Journal.ie: Carney deepfake (May 2025)
- Security Magazine / Keepnet Labs: deepfake fraud statistics

**Energy and carbon:**

- IEA: "Energy and AI" report (2025) — 415 TWh, projections to 2030
- Goldman Sachs Research: data center power demand (2024)
- Sustainability Magazine / Microsoft blog: Microsoft emissions +23.4% (FY2024)
- Google 2025 Environmental Report / Yale E360: Google emissions +51%
- Washington Post (August 2025): AI efficiency improvements

---

### Corrections Summary

All corrections from the original outline, identified during fact-checking:

| Original Claim                                 | Correction                                                              | Impact                                                              |
| ---------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------- |
| "519ml per query" worst case                   | ~500ml per 20-50 queries (~10-25ml per query full lifecycle)            | Narrows the spread but still dramatic (~100×)                       |
| "1,600× spread"                                | ~100× spread (0.26ml to ~25ml)                                          | Still makes the point effectively                                   |
| "150-200W traditional GPU"                     | 250-400W for datacenter GPUs (V100/A100)                                | Minor — adjust starting point                                       |
| "ISS can only dissipate 16 kW"                 | ISS EATCS dissipates **70 kW**                                          | Makes the space argument _stronger_ (132 kW rack ≈ 2× ISS capacity) |
| "86% of Arizona water = agriculture"           | ~72-74% (current official data)                                         | Still striking; adjust figure                                       |
| "Clearview AI: 30 billion images"              | Now 50-70 billion+ (30B was 2023 figure)                                | Update to current figure                                            |
| "105,000+ deepfake incidents, $200M+ damages"  | Unverifiable — no traceable primary source                              | Replace with 1,740% increase in deepfake fraud (2022-2023)          |
| "ChatGPT uses 10× the energy of Google search" | Outdated as of 2025 due to efficiency improvements                      | Present as historical claim, note it no longer holds                |
| "Mag Seven = 31% of S&P 500"                   | ~33% as of early 2026 (ranged 31-37%)                                   | Minor adjustment                                                    |
| Microsoft Espoo heats "entire city"            | Covers ~40% of demand for 250,000 users across Espoo + 2 municipalities | Clarify scope                                                       |
| "0.26-0.32ml" framed as ChatGPT range          | 0.26ml is Gemini (Google), 0.32ml is ChatGPT (Altman)                   | Separate the two figures                                            |

---
