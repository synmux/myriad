// Data structure - stored in memory (not using localStorage due to sandbox restrictions)
const data = {
  positive: [
    {
      title: "Hate Crime Legislation Strengthened",
      date: "June 2025",
      dateSort: "2025-06",
      description:
        "Government committed to making anti-LGBTQ+ hate crimes aggravated offences with tougher sentences, putting them on equal footing with racial and religious hate crimes.",
      sources: "Official government statements, Crime Bill announcements",
      impact: "Enhanced legal protections and deterrent effect",
    },
    {
      title: "Gender Clinic Waiting List Support Pilot",
      date: "September 2025",
      dateSort: "2025-09",
      description:
        "£125,000 pilot providing mental health and wellbeing support for adults waiting for gender services (some wait 8+ years)",
      sources: "NHS England announcements",
      impact: "Addresses mental health crisis during long waits",
    },
    {
      title: "Adult Gender Services Review",
      date: "2025",
      dateSort: "2025-01",
      description:
        "NHS commissioned independent review (Levy Review) into operation and delivery of adult gender dysphoria clinics",
      sources: "NHS England, Health Department statements",
      impact: "Potential for service improvements, though concerns about scope",
    },
    {
      title: "Conversion Therapy Ban Promised",
      date: "July 2024 (ongoing)",
      dateSort: "2024-07",
      description:
        "Reaffirmed commitment to full trans-inclusive ban on conversion therapy in King's Speech",
      sources: "King's Speech, government statements",
      impact: "Not yet implemented - draft bill not published after 15+ months",
    },
  ],
  negative: [
    {
      title: "Permanent Puberty Blockers Ban",
      date: "December 2024",
      dateSort: "2024-12",
      description:
        "Health Secretary Wes Streeting made temporary ban permanent for under-18s outside clinical trials",
      sources: "Department of Health announcements, parliamentary records",
      impact:
        "Restricts access to treatment, criticized by LGBT+ Labour and medical organizations",
    },
    {
      title: "Endorsement of Supreme Court Ruling",
      date: "April 2025",
      dateSort: "2025-04",
      description:
        'PM Starmer welcomed ruling defining "sex" as biological sex, reversing previous position that "trans women are women"',
      sources: "Prime Minister's statements, government communications",
      impact: "Enables exclusion of trans people from single-sex spaces",
    },
    {
      title: "Position Shifts on Trans Women",
      date: "April 2025",
      dateSort: "2025-04-15",
      description:
        'Starmer\'s spokesperson stated PM no longer believes "trans women are women", reversing 2022 position',
      sources: "Official spokesperson statements, press briefings",
      impact: "Perceived as abandoning trans community, internal party dissent",
    },
  ],
  delayed: [
    {
      title: "Gender Recognition Reform",
      date: "Pre-election promise - no progress",
      dateSort: "2024-07-01",
      description:
        'Pledged to "modernise and simplify" GRC process, but no legislation introduced',
      sources: "Labour manifesto, government statements",
      impact: "No change to current system requiring medical diagnosis",
    },
    {
      title: "Conversion Therapy Ban",
      date: "Promised July 2024 - still pending",
      dateSort: "2024-07-02",
      description:
        "Draft bill promised but not published 15+ months after King's Speech",
      sources: "King's Speech, parliamentary records",
      impact: "Conversion therapy remains legal despite repeated promises",
    },
    {
      title: "Single-Sex Spaces Guidance",
      date: "October 2025 - delayed",
      dateSort: "2025-10",
      description:
        "Minister Bridget Phillipson has not approved EHRC's 300-page code of practice on single-sex spaces",
      sources: "EHRC statements, ministerial communications",
      impact:
        "Organizations continue using potentially unlawful guidance; creates uncertainty",
    },
  ],
  external: [
    {
      title: "Supreme Court Ruling",
      date: "April 2025",
      dateSort: "2025-04-01",
      description:
        'Court ruled "sex" in Equality Act means biological sex, not gender identity (Not a government action)',
      sources: "Supreme Court judgment",
      impact: "Major legal shift enabling exclusion from single-sex spaces",
    },
    {
      title: "NHS Cass Review Implementation",
      date: "August 2024",
      dateSort: "2024-08",
      description:
        "NHS England began implementing Cass Review recommendations on children's gender services",
      sources: "NHS England announcements",
      impact:
        "Closure of Tavistock, opening of regional centers, restricted treatments",
    },
  ],
};

const policyAreas = {
  healthcare: {
    name: "Healthcare",
    promise: "Improve services and waiting times, implement Cass Review",
    status: "mixed",
    statusText: "Mixed - some improvements, major restrictions",
    actions: [
      "Permanent puberty blockers ban (December 2024)",
      "Waiting list support pilot (September 2025)",
      "Adult services review launched (2025)",
    ],
    assessment:
      "Mixed outcome - While the government has introduced a waiting list support pilot and commissioned a review of adult services, these positive steps are counterbalanced by the permanent ban on puberty blockers for under-18s. The ban has been criticized by medical organizations and LGBT+ Labour members as restricting access to necessary treatment.",
  },
  legal: {
    name: "Legal Recognition",
    promise: "Simplify GRC process while keeping medical diagnosis requirement",
    status: "not-implemented",
    statusText: "Not Implemented",
    actions: [
      "No legislation introduced",
      "No government action taken on this manifesto promise",
    ],
    assessment:
      "No progress has been made on this pre-election promise. The Gender Recognition Certificate process remains unchanged, still requiring medical diagnosis and lengthy bureaucratic procedures. This represents an unfulfilled manifesto commitment.",
  },
  hateCrime: {
    name: "Hate Crime Protection",
    promise: "Make LGBTQ+ hate crimes aggravated offences",
    status: "implemented",
    statusText: "In Progress - Being Fulfilled",
    actions: [
      "Committed in Crime Bill (June 2025)",
      "Will give LGBTQ+ hate crimes equal status with racial and religious hate crimes",
    ],
    assessment:
      "Positive development - The government is fulfilling this manifesto promise by including provisions in the Crime Bill to make anti-LGBTQ+ hate crimes aggravated offences with tougher sentences. This represents enhanced legal protections and a deterrent effect.",
  },
  conversion: {
    name: "Conversion Therapy",
    promise: "Full trans-inclusive ban",
    status: "delayed",
    statusText: "Delayed",
    actions: [
      "Promised in King's Speech (July 2024)",
      "Draft bill not published (15+ months later)",
      "Conversion therapy remains legal",
    ],
    assessment:
      "Negative outcome - Despite being promised in the King's Speech in July 2024 and being a repeated government commitment, the draft bill has not been published after more than 15 months. Conversion therapy practices targeting trans people remain legal in the UK.",
  },
  spaces: {
    name: "Single-Sex Spaces",
    promise: "Protect spaces while respecting trans rights",
    status: "mixed",
    statusText: "Unclear/Delayed",
    actions: [
      "PM endorsed Supreme Court ruling (April 2025)",
      "EHRC guidance approval delayed (October 2025)",
      "Creates legal uncertainty for organizations",
    ],
    assessment:
      "Unclear outcome - The government's endorsement of the Supreme Court ruling defining sex as biological sex has been seen as restrictive by trans advocates. Meanwhile, the delay in approving EHRC guidance creates uncertainty, with organizations potentially using unlawful guidance.",
  },
  equality: {
    name: "Equality Act",
    promise: "Protect and maintain",
    status: "implemented",
    statusText: "Maintained",
    actions: [
      "Supported Supreme Court interpretation",
      "No changes proposed to the Act itself",
    ],
    assessment:
      "Neutral outcome - The Equality Act itself remains unchanged. The government has supported the Supreme Court's interpretation of the Act, but has not proposed any legislative amendments. The Act's protections remain in place, though their interpretation has shifted.",
  },
};

// State management
let currentView = "summary";
let currentFilter = "all";
let currentTab = "healthcare";

// Initialize app
function initApp() {
  setupNavigation();
  setupTimeline();
  setupPolicyTabs();
  setupActionCards();
  setupFilters();
  setupSearch();
}

// Navigation
function setupNavigation() {
  const navButtons = document.querySelectorAll(".nav-btn");
  navButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const view = btn.dataset.view;
      navigateToView(view);
    });
  });
}

function navigateToView(view) {
  // Update current view
  currentView = view;

  // Update active states
  document
    .querySelectorAll(".view")
    .forEach((v) => v.classList.remove("active"));
  document
    .querySelectorAll(".nav-btn")
    .forEach((btn) => btn.classList.remove("active"));

  document.getElementById(`view-${view}`).classList.add("active");
  document.querySelector(`[data-view="${view}"]`).classList.add("active");

  // Scroll to top
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Timeline
function setupTimeline() {
  const container = document.getElementById("timeline");
  const allActions = getAllActionsSorted();

  allActions.forEach((action) => {
    const item = createTimelineItem(action);
    container.appendChild(item);
  });
}

function getAllActionsSorted() {
  const allActions = [];

  data.positive.forEach((action) => {
    allActions.push({ ...action, category: "positive" });
  });
  data.negative.forEach((action) => {
    allActions.push({ ...action, category: "negative" });
  });
  data.delayed.forEach((action) => {
    allActions.push({ ...action, category: "delayed" });
  });
  data.external.forEach((action) => {
    allActions.push({ ...action, category: "external" });
  });

  return allActions.sort((a, b) => a.dateSort.localeCompare(b.dateSort));
}

function createTimelineItem(action) {
  const item = document.createElement("div");
  item.className = `timeline-item ${action.category}`;
  item.dataset.category = action.category;

  const markerSymbol = {
    positive: "+",
    negative: "−",
    delayed: "⏸",
    external: "i",
  }[action.category];

  const categoryLabel = {
    positive: "Positive Action",
    negative: "Restrictive Action",
    delayed: "Delayed/Stalled",
    external: "External Context (NOT GOVERNMENT)",
  }[action.category];

  item.innerHTML = `
    <div class="timeline-marker ${action.category}">${markerSymbol}</div>
    <div class="timeline-content">
      <div class="timeline-date">${action.date}</div>
      <div class="timeline-badge ${action.category}">${categoryLabel}</div>
      <div class="timeline-title">${action.title}</div>
      <div class="timeline-description">${action.description}</div>
      <div class="timeline-details">
        <div class="timeline-impact"><strong>Impact:</strong> ${action.impact}</div>
        <div class="timeline-sources"><strong>Sources:</strong> ${action.sources}</div>
      </div>
    </div>
  `;

  item.querySelector(".timeline-content").addEventListener("click", () => {
    item.classList.toggle("expanded");
  });

  return item;
}

// Policy Tabs
function setupPolicyTabs() {
  const tabButtons = document.querySelectorAll(".tab-btn");
  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.dataset.tab;
      switchTab(tab);
    });
  });

  // Load initial tab
  switchTab("healthcare");
}

function switchTab(tabName) {
  currentTab = tabName;

  // Update active states
  document
    .querySelectorAll(".tab-btn")
    .forEach((btn) => btn.classList.remove("active"));
  document.querySelector(`[data-tab="${tabName}"]`).classList.add("active");

  // Render content
  const content = document.getElementById("policy-content");
  const policy = policyAreas[tabName];

  if (policy) {
    content.innerHTML = `
      <div class="policy-tab-content">
        <div class="policy-header">
          <h3>${policy.name}</h3>
          <div class="policy-status ${policy.status}">${policy.statusText}</div>
        </div>
        <div class="policy-section">
          <h4>Pre-Election Promise</h4>
          <p>${policy.promise}</p>
        </div>
        <div class="policy-section">
          <h4>Actions Taken</h4>
          <ul>
            ${policy.actions.map((action) => `<li>${action}</li>`).join("")}
          </ul>
        </div>
        <div class="policy-section">
          <h4>Assessment</h4>
          <p>${policy.assessment}</p>
        </div>
      </div>
    `;
  }
}

// Action Cards
function setupActionCards() {
  const container = document.getElementById("actions-list");
  const allActions = getAllActionsSorted().reverse(); // Most recent first

  allActions.forEach((action) => {
    const card = createActionCard(action);
    container.appendChild(card);
  });
}

function createActionCard(action) {
  const card = document.createElement("div");
  card.className = `action-card ${action.category}`;
  card.dataset.category = action.category;
  card.dataset.title = action.title.toLowerCase();
  card.dataset.description = action.description.toLowerCase();

  const categoryLabel = {
    positive: "Positive Action",
    negative: "Restrictive Action",
    delayed: "Delayed/Stalled",
    external: "External Context (NOT GOVERNMENT)",
  }[action.category];

  card.innerHTML = `
    <div class="action-header">
      <div class="action-title">${action.title}</div>
      <div class="action-date">${action.date}</div>
    </div>
    <div class="action-category ${action.category}">${categoryLabel}</div>
    <div class="action-description">${action.description}</div>
    <div class="action-expanded">
      <div class="action-impact">
        <h5>Impact Assessment</h5>
        <p>${action.impact}</p>
      </div>
      <div class="action-sources"><strong>Sources:</strong> ${action.sources}</div>
    </div>
  `;

  card.addEventListener("click", () => {
    card.classList.toggle("expanded");
  });

  return card;
}

// Filters
function setupFilters() {
  const filterButtons = document.querySelectorAll(".filter-btn");
  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const filter = btn.dataset.filter;
      applyFilter(filter, btn);
    });
  });
}

function applyFilter(filter, button) {
  currentFilter = filter;

  // Update active state for this filter group
  const filterGroup = button.parentElement;
  filterGroup
    .querySelectorAll(".filter-btn")
    .forEach((btn) => btn.classList.remove("active"));
  button.classList.add("active");

  // Apply filter to timeline items
  const timelineItems = document.querySelectorAll(".timeline-item");
  timelineItems.forEach((item) => {
    if (filter === "all" || item.dataset.category === filter) {
      item.classList.remove("hidden");
    } else {
      item.classList.add("hidden");
    }
  });

  // Apply filter to action cards
  const actionCards = document.querySelectorAll(".action-card");
  actionCards.forEach((card) => {
    if (filter === "all" || card.dataset.category === filter) {
      card.classList.remove("hidden");
    } else {
      card.classList.add("hidden");
    }
  });
}

// Search
function setupSearch() {
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const searchTerm = e.target.value.toLowerCase();
      filterActionsBySearch(searchTerm);
    });
  }
}

function filterActionsBySearch(searchTerm) {
  const actionCards = document.querySelectorAll(".action-card");
  actionCards.forEach((card) => {
    const title = card.dataset.title;
    const description = card.dataset.description;

    // Only apply search if not already hidden by category filter
    if (currentFilter === "all" || card.dataset.category === currentFilter) {
      if (
        searchTerm === "" ||
        title.includes(searchTerm) ||
        description.includes(searchTerm)
      ) {
        card.classList.remove("hidden");
      } else {
        card.classList.add("hidden");
      }
    }
  });
}

// Initialize when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initApp);
} else {
  initApp();
}
