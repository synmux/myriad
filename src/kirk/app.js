// Application data
const quotesData = [
  {
    id: 1,
    text: "MLK was awful. He's not a good person",
    target_communities: ["Black Americans", "Civil Rights"],
    date: null,
    source: "Various media reports",
    severity: "extremely_harmful",
    context: "Attacking civil rights icon Martin Luther King Jr.",
  },
  {
    id: 2,
    text: "We made a huge mistake when we passed the Civil Rights Act in the 1960s",
    target_communities: ["Black Americans", "Civil Rights"],
    date: null,
    source: "Multiple sources",
    severity: "extremely_harmful",
    context: "Opposing fundamental civil rights legislation",
  },
  {
    id: 3,
    text: "If I see a Black pilot, I'm gonna be like 'boy, I hope he is qualified'",
    target_communities: ["Black Americans"],
    date: "2024-01-23",
    source: "Newsweek, USA Today",
    severity: "extremely_harmful",
    context: "Racist assumption about Black professionals",
  },
  {
    id: 4,
    text: "George Floyd was a scumbag unworthy of the attention",
    target_communities: ["Black Americans"],
    date: "2021",
    source: "Telegraph India",
    severity: "extremely_harmful",
    context: "Dehumanizing murder victim",
  },
  {
    id: 5,
    text: "Husbands should do everything he can to not force his wife into the workforce",
    target_communities: ["Women"],
    date: "2025-07-16",
    source: "Young Women's Leadership Summit",
    severity: "harmful",
    context: "Restricting women's economic independence",
  },
  {
    id: 6,
    text: "Women should submit to a godly man and raise more children than you can afford",
    target_communities: ["Women"],
    date: "2025-07-16",
    source: "Young Women's Leadership Summit",
    severity: "harmful",
    context: "Promoting women's subordination",
  },
  {
    id: 7,
    text: "Birth control makes women angry and bitter and screws up female brains",
    target_communities: ["Women"],
    date: null,
    source: "IMDB, Instagram",
    severity: "harmful",
    context: "Spreading medical misinformation about women's health",
  },
  {
    id: 8,
    text: "Women in their early 30s aren't attractive in the dating pool because they're not at their prime",
    target_communities: ["Women"],
    date: null,
    source: "Various reports",
    severity: "harmful",
    context: "Reducing women to their physical appearance and age",
  },
  {
    id: 9,
    text: "Called for 'Nuremberg-style trials' for providers of gender-affirming care",
    target_communities: ["LGBTQ+", "Transgender"],
    date: null,
    source: "Scene Magazine",
    severity: "extremely_harmful",
    context: "Calling for persecution of healthcare providers",
  },
  {
    id: 10,
    text: "Called transgender people 'groomers'",
    target_communities: ["LGBTQ+", "Transgender"],
    date: null,
    source: "Scene Magazine",
    severity: "extremely_harmful",
    context: "False and dangerous accusations",
  },
  {
    id: 11,
    text: "America does not need more visas for people from India. Perhaps no form of legal immigration has so displaced American workers as those from India. Enough already. We're full",
    target_communities: ["Immigrants", "Indian Americans"],
    date: "2025-09-02",
    source: "Money Control, Economic Times",
    severity: "harmful",
    context: "Anti-immigrant xenophobia targeting specific nationality",
  },
  {
    id: 12,
    text: "Jews control not just the colleges; it's the nonprofits, it's the movies, it's Hollywood, it's all of it",
    target_communities: ["Jewish people"],
    date: "October 2023",
    source: "Times of Israel",
    severity: "extremely_harmful",
    context: "Classic antisemitic conspiracy theory",
  },
  {
    id: 13,
    text: "Jewish communities have been pushing the exact kind of hatred against whites that they claim to want people to stop using against them",
    target_communities: ["Jewish people"],
    date: "November 2023",
    source: "Times of Israel, TRT Global",
    severity: "extremely_harmful",
    context: "Antisemitic victim-blaming rhetoric",
  },
  {
    id: 14,
    text: "Islam is not compatible with the West",
    target_communities: ["Muslims"],
    date: "May 2025",
    source: "5Pillars, Instagram",
    severity: "extremely_harmful",
    context: "Islamophobic generalization about 1.8 billion people",
  },
  {
    id: 15,
    text: "Muslims are commanded to take over the government in the land they live",
    target_communities: ["Muslims"],
    date: null,
    source: "5Pillars",
    severity: "extremely_harmful",
    context: "False conspiracy theory about Muslim Americans",
  },
  {
    id: 16,
    text: "Can we stop giving half the screen during these crisis briefings to sign language interpreters? I have nothing against the hearing impaired of course, but this is a joke",
    target_communities: ["Disabled people"],
    date: "2025-01-09",
    source: "Indy100, Reddit",
    severity: "harmful",
    context: "Ableist attack on accessibility accommodations",
  },
  {
    id: 17,
    text: "It's worth it to have a cost of, unfortunately, some gun deaths every single year, so that we can have the Second Amendment",
    target_communities: ["Gun violence victims", "Families"],
    date: null,
    source: "Multiple sources",
    severity: "extremely_harmful",
    context: "Dismissing lives lost to gun violence",
  },
  {
    id: 18,
    text: "That's awfully graphic. But the answer is yes, the baby would be delivered [if his 10-year-old daughter were raped and pregnant]",
    target_communities: ["Sexual assault victims", "Children"],
    date: null,
    source: "Hindustan Times",
    severity: "extremely_harmful",
    context: "Forcing child rape victims to give birth",
  },
  {
    id: 19,
    text: "We as conservatives believe that if you're in poverty it's largely because of values not because of lack of stuff",
    target_communities: ["Poor people"],
    date: "2024-09-19",
    source: "YouTube",
    severity: "harmful",
    context: "Victim-blaming people in poverty",
  },
  {
    id: 20,
    text: "The Biden administration's immigration policy is about bringing in voters that they like and, honestly, diminishing and decreasing white demographics in America",
    target_communities: ["Immigrants", "Non-white Americans"],
    date: null,
    source: "Immigration Forum",
    severity: "extremely_harmful",
    context: "Promoting 'Great Replacement' conspiracy theory",
  },
];

const communitiesData = [
  {
    name: "Black Americans",
    description:
      "African Americans have faced centuries of systemic racism, from slavery through Jim Crow to modern discrimination.",
    population: "47.9 million (14.4% of US population)",
    hate_crimes_2022:
      "2,430 incidents (64.5% of racially motivated hate crimes)",
  },
  {
    name: "Women",
    description:
      "Women make up approximately 51% of the US population and continue to face gender-based discrimination.",
    population: "167.5 million (51% of US population)",
    hate_crimes_2022:
      "Limited tracking, but domestic violence affects 1 in 3 women",
  },
  {
    name: "LGBTQ+",
    description:
      "LGBTQ+ Americans face discrimination in employment, housing, healthcare, and public accommodations.",
    population: "20.8 million adults (8.4% identify as LGBTQ+)",
    hate_crimes_2022: "1,402 incidents (15.8% of all hate crimes)",
  },
  {
    name: "Muslims",
    description:
      "Muslim Americans practice the second-largest religion in the world and face significant religious discrimination.",
    population: "3.45 million (1.05% of US population)",
    hate_crimes_2022: "158 incidents against Muslims",
  },
  {
    name: "Jewish people",
    description:
      "Jewish Americans are the largest religious minority in the US and face the most religious hate crimes.",
    population: "7.5 million (2.2% of US population)",
    hate_crimes_2022: "1,124 incidents (60% of religious hate crimes)",
  },
  {
    name: "Immigrants",
    description:
      "Foreign-born residents who have made America their home, contributing to economy and culture.",
    population: "46.2 million (13.9% of US population)",
    hate_crimes_2022: "247 incidents based on national origin",
  },
  {
    name: "Disabled people",
    description:
      "Americans with disabilities face barriers to employment, education, and public participation.",
    population: "42.5 million adults (13.7% have a disability)",
    hate_crimes_2022: "92 incidents based on disability",
  },
];

// Global variables
let filteredQuotes = [...quotesData];
let charts = {};

// Initialize app when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Small delay to ensure all elements are rendered
  setTimeout(() => {
    initializeApp();
  }, 100);
});

function initializeApp() {
  console.log("Initializing app...");
  setupNavigation();
  populateFilters();
  setupFilters();
  setupSearch();
  renderQuotes(quotesData);
  renderCommunities();
  // Initialize charts after a brief delay to ensure canvas elements are ready
  setTimeout(() => {
    initializeCharts();
  }, 200);
}

// Navigation
function setupNavigation() {
  console.log("Setting up navigation...");
  const navTabs = document.querySelectorAll(".nav-tab");
  const sections = document.querySelectorAll(".section");

  console.log(
    "Found tabs:",
    navTabs.length,
    "Found sections:",
    sections.length,
  );

  navTabs.forEach((tab, index) => {
    console.log(`Tab ${index}:`, tab.dataset.section);
    tab.addEventListener("click", (e) => {
      e.preventDefault();
      const targetSection = tab.dataset.section;
      console.log("Clicked tab for section:", targetSection);

      // Update active tab
      navTabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      // Update active section
      sections.forEach((s) => {
        s.classList.remove("active");
        console.log("Hiding section:", s.id);
      });

      const targetElement = document.getElementById(targetSection);
      if (targetElement) {
        targetElement.classList.add("active");
        console.log("Showing section:", targetSection);

        // Re-initialize charts when analysis section is shown
        if (targetSection === "analysis") {
          setTimeout(() => {
            console.log("Re-initializing charts...");
            initializeCharts();
          }, 100);
        }
      } else {
        console.error("Target section not found:", targetSection);
      }
    });
  });
}

// Search and Filter functionality
function setupSearch() {
  console.log("Setting up search...");
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", handleSearch);
    console.log("Search input event listener added");
  } else {
    console.error("Search input not found");
  }
}

function setupFilters() {
  console.log("Setting up filters...");
  const communityFilter = document.getElementById("communityFilter");
  const severityFilter = document.getElementById("severityFilter");

  if (communityFilter) {
    communityFilter.addEventListener("change", handleFilter);
    console.log("Community filter event listener added");
  } else {
    console.error("Community filter not found");
  }

  if (severityFilter) {
    severityFilter.addEventListener("change", handleFilter);
    console.log("Severity filter event listener added");
  } else {
    console.error("Severity filter not found");
  }
}

function populateFilters() {
  console.log("Populating filters...");
  const communityFilter = document.getElementById("communityFilter");
  if (!communityFilter) {
    console.error("Community filter element not found");
    return;
  }

  const communities = [
    ...new Set(quotesData.flatMap((quote) => quote.target_communities)),
  ];
  console.log("Found communities:", communities);

  communities.sort().forEach((community) => {
    const option = document.createElement("option");
    option.value = community;
    option.textContent = community;
    communityFilter.appendChild(option);
  });

  console.log("Community filter populated with", communities.length, "options");
}

function handleSearch(e) {
  console.log("Search triggered:", e.target.value);
  const searchTerm = e.target.value.toLowerCase();
  applyFilters(searchTerm);
}

function handleFilter(e) {
  console.log("Filter triggered:", e.target.value);
  const searchInput = document.getElementById("searchInput");
  const searchTerm = searchInput ? searchInput.value.toLowerCase() : "";
  applyFilters(searchTerm);
}

function applyFilters(searchTerm = "") {
  console.log("Applying filters with search term:", searchTerm);
  const communityFilter = document.getElementById("communityFilter");
  const severityFilter = document.getElementById("severityFilter");

  const communityValue = communityFilter ? communityFilter.value : "";
  const severityValue = severityFilter ? severityFilter.value : "";

  console.log(
    "Filter values - Community:",
    communityValue,
    "Severity:",
    severityValue,
  );

  filteredQuotes = quotesData.filter((quote) => {
    const matchesSearch =
      searchTerm === "" ||
      quote.text.toLowerCase().includes(searchTerm) ||
      quote.target_communities.some((community) =>
        community.toLowerCase().includes(searchTerm),
      ) ||
      quote.context.toLowerCase().includes(searchTerm);

    const matchesCommunity =
      communityValue === "" ||
      quote.target_communities.includes(communityValue);

    const matchesSeverity =
      severityValue === "" || quote.severity === severityValue;

    return matchesSearch && matchesCommunity && matchesSeverity;
  });

  console.log("Filtered quotes count:", filteredQuotes.length);
  renderQuotes(filteredQuotes);
}

// Quote rendering
function renderQuotes(quotes) {
  console.log("Rendering quotes:", quotes.length);
  const container = document.getElementById("quotesContainer");
  if (!container) {
    console.error("Quotes container not found");
    return;
  }

  if (quotes.length === 0) {
    container.innerHTML =
      '<p style="text-align: center; color: var(--color-gray-400); font-size: var(--font-size-lg);">No quotes match your search criteria.</p>';
    return;
  }

  container.innerHTML = quotes.map((quote) => createQuoteCard(quote)).join("");
  console.log("Quotes rendered successfully");
}

function createQuoteCard(quote) {
  const communityTags = quote.target_communities
    .map((community) => `<span class="community-tag">${community}</span>`)
    .join("");

  const severityClass = `severity-${quote.severity}`;
  const severityText = quote.severity
    .replace("_", " ")
    .replace(/\b\w/g, (l) => l.toUpperCase());

  return `
        <div class="quote-card" tabindex="0">
            <div class="quote-text">"${quote.text}"</div>
            <div class="quote-meta">
                ${communityTags}
                <span class="severity-tag ${severityClass}">${severityText}</span>
            </div>
            <div class="quote-details">
                <div class="quote-source"><strong>Source:</strong> ${quote.source}</div>
                ${quote.date ? `<div class="quote-date"><strong>Date:</strong> ${quote.date}</div>` : ""}
                <div class="quote-context"><strong>Context:</strong> ${quote.context}</div>
            </div>
        </div>
    `;
}

// Community rendering
function renderCommunities() {
  console.log("Rendering communities...");
  const container = document.getElementById("communitiesContainer");
  if (!container) {
    console.error("Communities container not found");
    return;
  }

  container.innerHTML = communitiesData
    .map((community) => createCommunityCard(community))
    .join("");
  console.log("Communities rendered successfully");
}

function createCommunityCard(community) {
  return `
        <div class="community-card">
            <h3>${community.name}</h3>
            <div class="community-description">${community.description}</div>
            <div class="community-stats">
                <div class="community-stat">
                    <span class="stat-key">Population:</span>
                    <span class="stat-value">${community.population}</span>
                </div>
                <div class="community-stat">
                    <span class="stat-key">Hate Crimes (2022):</span>
                    <span class="stat-value">${community.hate_crimes_2022}</span>
                </div>
            </div>
        </div>
    `;
}

// Chart initialization
function initializeCharts() {
  console.log("Initializing charts...");

  // Check if Chart.js is available
  if (typeof Chart === "undefined") {
    console.error("Chart.js not loaded");
    return;
  }

  // Destroy existing charts to avoid canvas reuse issues
  Object.values(charts).forEach((chart) => {
    if (chart && typeof chart.destroy === "function") {
      chart.destroy();
    }
  });
  charts = {};

  // Create charts with error handling
  try {
    createCommunityChart();
    createSeverityChart();
    createTimelineChart();
    createWordCloud();
    console.log("All charts initialized successfully");
  } catch (error) {
    console.error("Error initializing charts:", error);
  }
}

function createCommunityChart() {
  const canvas = document.getElementById("communityChart");
  if (!canvas) {
    console.error("Community chart canvas not found");
    return;
  }

  console.log("Creating community chart...");

  // Count quotes by community
  const communityCounts = {};
  quotesData.forEach((quote) => {
    quote.target_communities.forEach((community) => {
      communityCounts[community] = (communityCounts[community] || 0) + 1;
    });
  });

  const sortedCommunities = Object.entries(communityCounts).sort(
    (a, b) => b[1] - a[1],
  );

  const labels = sortedCommunities.map(([community]) => community);
  const data = sortedCommunities.map(([, count]) => count);
  const colors = [
    "#1FB8CD",
    "#FFC185",
    "#B4413C",
    "#ECEBD5",
    "#5D878F",
    "#DB4545",
    "#D2BA4C",
    "#964325",
    "#944454",
    "#13343B",
  ];

  charts.community = new Chart(canvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Number of Quotes",
          data: data,
          backgroundColor: colors.slice(0, labels.length),
          borderColor: colors
            .slice(0, labels.length)
            .map((color) => color + "80"),
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          ticks: {
            color: "#a7a9a9",
            maxRotation: 45,
          },
          grid: {
            color: "rgba(167, 169, 169, 0.2)",
          },
        },
        y: {
          ticks: {
            color: "#a7a9a9",
            stepSize: 1,
          },
          grid: {
            color: "rgba(167, 169, 169, 0.2)",
          },
        },
      },
      onClick: (event, elements) => {
        if (elements.length > 0) {
          const { index } = elements[0];
          const community = labels[index];
          filterByCommunity(community);
        }
      },
    },
  });

  console.log("Community chart created successfully");
}

function createSeverityChart() {
  const canvas = document.getElementById("severityChart");
  if (!canvas) {
    console.error("Severity chart canvas not found");
    return;
  }

  console.log("Creating severity chart...");

  const severityCounts = {};
  quotesData.forEach((quote) => {
    const severity = quote.severity
      .replace("_", " ")
      .replace(/\b\w/g, (l) => l.toUpperCase());
    severityCounts[severity] = (severityCounts[severity] || 0) + 1;
  });

  const labels = Object.keys(severityCounts);
  const data = Object.values(severityCounts);

  charts.severity = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          backgroundColor: ["#FFC185", "#B4413C"],
          borderColor: ["#FFC185", "#B4413C"],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: "#a7a9a9",
            padding: 20,
          },
        },
      },
    },
  });

  console.log("Severity chart created successfully");
}

function createTimelineChart() {
  const canvas = document.getElementById("timelineChart");
  if (!canvas) {
    console.error("Timeline chart canvas not found");
    return;
  }

  console.log("Creating timeline chart...");

  // Filter quotes with dates and group by year
  const yearCounts = {};
  quotesData.forEach((quote) => {
    if (quote.date) {
      const year = quote.date.includes("-")
        ? quote.date.split("-")[0]
        : quote.date;
      yearCounts[year] = (yearCounts[year] || 0) + 1;
    }
  });

  const sortedYears = Object.keys(yearCounts).sort();
  const data = sortedYears.map((year) => yearCounts[year]);

  if (sortedYears.length === 0) {
    // Create a simple message chart
    charts.timeline = new Chart(canvas, {
      type: "bar",
      data: {
        labels: ["No Data"],
        datasets: [
          {
            label: "Quotes per Year",
            data: [0],
            backgroundColor: ["#666"],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false },
        },
        scales: {
          x: { display: false },
          y: { display: false },
        },
      },
    });
    return;
  }

  charts.timeline = new Chart(canvas, {
    type: "line",
    data: {
      labels: sortedYears,
      datasets: [
        {
          label: "Quotes per Year",
          data: data,
          borderColor: "#1FB8CD",
          backgroundColor: "rgba(31, 184, 205, 0.1)",
          borderWidth: 2,
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: "#a7a9a9",
          },
        },
      },
      scales: {
        x: {
          ticks: {
            color: "#a7a9a9",
          },
          grid: {
            color: "rgba(167, 169, 169, 0.2)",
          },
        },
        y: {
          ticks: {
            color: "#a7a9a9",
            stepSize: 1,
          },
          grid: {
            color: "rgba(167, 169, 169, 0.2)",
          },
        },
      },
    },
  });

  console.log("Timeline chart created successfully");
}

function createWordCloud() {
  const container = document.getElementById("wordCloud");
  if (!container) {
    console.error("Word cloud container not found");
    return;
  }

  console.log("Creating word cloud...");

  // Extract common discriminatory terms
  const commonTerms = [
    "awful",
    "mistake",
    "unworthy",
    "scumbag",
    "control",
    "hatred",
    "incompatible",
    "commanded",
    "joke",
    "cost",
    "values",
    "diminishing",
    "displacement",
    "submission",
    "bitter",
    "trials",
    "groomers",
    "full",
  ];

  // Count frequency in quotes
  const wordFreq = {};
  quotesData.forEach((quote) => {
    const words = quote.text.toLowerCase().split(/\s+/);
    words.forEach((word) => {
      const cleanWord = word.replace(/[^\w]/g, "");
      if (commonTerms.includes(cleanWord) && cleanWord.length > 2) {
        wordFreq[cleanWord] = (wordFreq[cleanWord] || 0) + 1;
      }
    });
  });

  const sortedWords = Object.entries(wordFreq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15);

  container.innerHTML = sortedWords
    .map(
      ([word, freq]) => `
            <div class="word-item" style="font-size: ${Math.max(12, freq * 4)}px;">
                ${word} (${freq})
            </div>
        `,
    )
    .join("");

  console.log("Word cloud created successfully");
}

function filterByCommunity(community) {
  console.log("Filtering by community:", community);

  // Switch to quotes tab
  const quotesTab = document.querySelector('.nav-tab[data-section="quotes"]');
  if (quotesTab) {
    quotesTab.click();
  }

  // Set filter
  const communityFilter = document.getElementById("communityFilter");
  if (communityFilter) {
    communityFilter.value = community;
    handleFilter({ target: { value: community } });
  }

  // Scroll to quotes section
  const quotesSection = document.getElementById("quotes");
  if (quotesSection) {
    quotesSection.scrollIntoView({ behavior: "smooth" });
  }
}

// Keyboard navigation for quote cards
document.addEventListener("keydown", function (e) {
  if (e.target.classList.contains("quote-card") && e.key === "Enter") {
    e.target.click();
  }
});

// Add smooth scrolling for internal navigation
document.addEventListener("click", function (e) {
  if (e.target.matches('a[href^="#"]')) {
    e.preventDefault();
    const target = document.querySelector(e.target.getAttribute("href"));
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  }
});
