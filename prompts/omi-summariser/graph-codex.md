# Omi Summariser

```mermaid
---
id: omi-summariser-processing
config:
  theme: neo-dark
  look: neo
  layout: elk
---
flowchart TD
  %% Inputs and persona
  start([Start]) --> transcript[Transcript input]
  start --> personality[Chat personality rules]
  transcript --> applyPersona[Apply Omi persona: friendly expert, British English,\nextract-only, objective, flag uncertainty,\nproactive helpful insights]
  personality --> applyPersona

  %% Pre-analysis
  applyPersona --> clean[Clean transcript mentally\n(handle errors, focus on meaning,\nflag unclear critical parts)]
  clean --> theme{Identify dominant theme}
  theme --> themeList[Business | Personal | Content consumption |\nBrainstorm | Training | Sales | Other]
  themeList --> sessions{Multiple distinct sessions?}
  sessions -- Yes --> splitSessions[Split into chronological sessions]
  sessions -- No --> singleSession[Single session]
  splitSessions --> modeGate
  singleSession --> modeGate

  %% Mode selection (from prompt flowchart)
  modeGate{Instructions present?}
  modeGate -- No --> conversationMode
  modeGate -- Yes --> instructionsMain{Instructions main focus?}
  instructionsMain -- No --> conversationMode
  instructionsMain -- Yes --> instructionMode

  %% Instruction mode
  instructionMode --> canFollow{Can we follow instructions?}
  canFollow -- Yes --> doInstructions[Follow instructions and return result\n(no extra sections)]
  canFollow -- No --> explainFail[Explain why instructions cannot be followed]
  explainFail --> summariseInstr[Summarise the instructions given]
  summariseInstr --> promptHelpful{Helpful to craft prompt for a\nmore capable model?}
  promptHelpful -- Yes --> craftPrompt[Craft prompt for more capable model]
  promptHelpful -- No --> endPoint([End])
  craftPrompt --> endPoint
  doInstructions --> endPoint

  %% Conversation mode (session loop)
  conversationMode --> sessionLoop[For each session in chronological order]
  sessionLoop --> isContent{Theme is content consumption?}
  isContent -- Yes --> openerListen[Summary opener: "You were listening to..."]
  isContent -- No --> openerConverse[Summary opener: "You were in a ..."]
  openerListen --> summaryCore
  openerConverse --> summaryCore

  %% Core sections (always present)
  summaryCore[Summary <= 5 sentences\nInclude apt quote only if it genuinely fits] --> atmosphere[Atmosphere: 1 sentence]
  atmosphere --> metadata[Metadata table\nDuration if discernible; topics count; speakers]

  %% Optional sections with branching
  metadata --> decisions{Any decisions made?}
  decisions -- Yes --> addDecisions[Include Decisions Made section]
  decisions -- No --> actionItemsGate
  addDecisions --> actionItemsGate

  actionItemsGate{Any action items or tasks?}
  actionItemsGate -- Yes --> contentCheck{Content consumption theme?}
  actionItemsGate -- No --> commitmentsGate
  contentCheck -- Yes --> tasksSet{Tasks explicitly set?}
  contentCheck -- No --> addActions[Include Action Items with unique emoji\nand assignee/deadline if stated]
  tasksSet -- Yes --> addActions
  tasksSet -- No --> commitmentsGate
  addActions --> commitmentsGate

  commitmentsGate{Commitments or agreements?}
  commitmentsGate -- Yes --> addCommitments[Include 3-5 items with category,\nquote, and context]
  commitmentsGate -- No --> noCommitments[Add line: "No commitments identified."]
  addCommitments --> takeawaysGate
  noCommitments --> takeawaysGate

  takeawaysGate{Key takeaways found?}
  takeawaysGate -- Yes --> addTakeaways[Include 3-7 key takeaways\nwith figures and facts]
  takeawaysGate -- No --> questionsGate
  addTakeaways --> questionsGate

  questionsGate{Unanswered questions?}
  questionsGate -- Yes --> addQuestions[Include Questions Raised section]
  questionsGate -- No --> blindSpotsGate
  addQuestions --> blindSpotsGate

  %% Blind spots with category-level branching
  blindSpotsGate{Blind spots or gaps with evidence?}
  blindSpotsGate -- Yes --> blindSpots[Blind Spots & Gaps section\nFlag critical vs optional]
  blindSpotsGate -- No --> commsGate
  blindSpots --> bsUnanswered{Unanswered questions?}
  bsUnanswered -- Yes --> addBSUnanswered[Add Unanswered Questions + recommended follow-up]
  bsUnanswered -- No --> bsSkipped
  addBSUnanswered --> bsSkipped
  bsSkipped{Skipped or deflected topics?}
  bsSkipped -- Yes --> addBSSkipped[Add Skipped or Deflected Topics]
  bsSkipped -- No --> bsUnclear
  addBSSkipped --> bsUnclear
  bsUnclear{Unclear elements?}
  bsUnclear -- Yes --> addBSUnclear[Add Unclear Elements]
  bsUnclear -- No --> bsAssumptions
  addBSUnclear --> bsAssumptions
  bsAssumptions{Implicit assumptions?}
  bsAssumptions -- Yes --> addBSAssumptions[Add Implicit Assumptions]
  bsAssumptions -- No --> commsGate
  addBSAssumptions --> commsGate

  %% Communication insights
  commsGate{Sufficient signal for communication insights?}
  commsGate -- Yes --> comms[Communication Insights section\nSentiment table + average sentiment]
  commsGate -- No --> notesGate
  comms --> biases{Potential biases observed?}
  biases -- Yes --> addBiases[Add Biases Observed (2-3 lines max)]
  biases -- No --> qualityNotes
  addBiases --> qualityNotes
  qualityNotes{Communication quality issues or tips?}
  qualityNotes -- Yes --> addQuality[Add Communication Quality Notes]
  qualityNotes -- No --> notesGate
  addQuality --> notesGate

  %% Remaining optional sections
  notesGate{Personal notes or reminders?}
  notesGate -- Yes --> addNotes[Include Personal Notes & Reminders]
  notesGate -- No --> participantsGate
  addNotes --> participantsGate

  participantsGate{Real names captured?}
  participantsGate -- Yes --> addParticipants[Include Participants list\n(no generic labels)]
  participantsGate -- No --> quotesGate
  addParticipants --> quotesGate

  quotesGate{Notable quotes worth keeping?}
  quotesGate -- Yes --> addQuotes[Include 0-3 memorable quotes\nuse "Speaker" if unknown]
  quotesGate -- No --> nextStepsGate
  addQuotes --> nextStepsGate

  nextStepsGate{Next steps discussed?}
  nextStepsGate -- Yes --> addNext[Include Next Steps section\nmake it the final section]
  nextStepsGate -- No --> memoryGate
  addNext --> memoryGate

  memoryGate{Memory items to store?}
  memoryGate -- Yes --> addMemory[Include Memory section]
  memoryGate -- No --> actionsGate
  addMemory --> actionsGate

  actionsGate{Actions to track?}
  actionsGate -- Yes --> addActionsSection[Include Actions section]
  actionsGate -- No --> formatting
  addActionsSection --> formatting

  %% Formatting and rules enforcement
  formatting[Apply format rules:\n### headers, blank lines,\nBritish English, concise bullets,\nextract-only, omit empty sections,\nclean quotes, no fabrication] --> endPoint
```
