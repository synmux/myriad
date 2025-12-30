// Tool data
const toolsData = [
  {
    name: "AI Label Assistant (Klart AI)",
    type: "Gmail Add-on",
    auto_labeling: "Yes - Primary Feature",
    labeling_method: "ChatGPT/GPT-5 powered AI analysis",
    draft_writing: "Limited",
    pricing_min: "Free plan available",
    pricing_paid: "Subscription required (details on website)",
    unusual_features:
      "Time-driven hourly triggers, Auto-archiving, DPA with OpenAI",
    platform: "Gmail only",
    team_features: "Scalable for enterprises",
    learning_curve: "Low",
    customization: "High - custom rules and labels",
  },
  {
    name: "Superhuman",
    type: "Email Client",
    auto_labeling: "Yes - Auto Labels & Custom Auto Labels with AI",
    labeling_method: "AI-powered automatic categorization",
    draft_writing: "Yes - Instant Reply, Auto Drafts, Write with AI",
    pricing_min: "$25/user/month (annual)",
    pricing_paid:
      "$30/month (Starter), $40/month (Business), Custom (Enterprise)",
    unusual_features:
      "Split Inbox, Read receipts, Recent Opens feed, Keyboard-first design, Collision detection",
    platform: "Gmail & Outlook",
    team_features: "Shared Conversations, Team Comments, Team Snippets",
    learning_curve: "Medium - requires onboarding",
    customization: "High - custom auto labels library",
  },
  {
    name: "Shortwave",
    type: "Email Client",
    auto_labeling: "Yes - AI filters & auto-apply labels",
    labeling_method: "AI-powered filters with custom prompts",
    draft_writing: "Yes - Personalized Ghostwriter, AI autocomplete",
    pricing_min: "Free (90 days history, basic AI)",
    pricing_paid:
      "$7/month (Personal), $14/month (Pro), $24/month (Business), $36/month (Premier)",
    unusual_features:
      "AI filters (3-50 depending on plan), Natural language search, AI inbox organization in one click, Bundles, Todos",
    platform: "Gmail only",
    team_features: "Thread sharing, Team comments, Assignees, Shared labels",
    learning_curve: "Low - self-serve",
    customization: "High - custom AI prompts for filters",
  },
  {
    name: "Clean Email",
    type: "Email Management Tool",
    auto_labeling: "Yes - Auto Clean rules",
    labeling_method: "Rule-based with sender/keyword/size criteria",
    draft_writing: "No",
    pricing_min: "Free trial available",
    pricing_paid: "Subscription tiers (check website)",
    unusual_features:
      "Smart Folders, Unsubscriber, Screener, Privacy Monitor, Keep Newest rule, Action History Summary",
    platform: "Multi-platform (Gmail, Outlook, etc.)",
    team_features: "Limited",
    learning_curve: "Low",
    customization: "High - multiple criteria combinations",
  },
  {
    name: "SaneBox",
    type: "Email Management Tool",
    auto_labeling: "Yes - AI-powered folder routing",
    labeling_method: "Advanced AI learns from behavior",
    draft_writing: "No",
    pricing_min: "$7/month (Snack - 1 account)",
    pricing_paid: "$7/month (Snack), $12/month (Lunch), $36/month (Dinner)",
    unusual_features:
      "SaneNoReply folder, Do Not Disturb, SaneBlackHole, Snooze with reminders, Digest summaries",
    platform: "Multi-platform (Gmail, Outlook, Apple Mail, etc.)",
    team_features: "Individual accounts only",
    learning_curve: "Low - automatic learning",
    customization: "Medium - folder-based system",
  },
  {
    name: "Gmelius",
    type: "Gmail Enhancement Suite",
    auto_labeling: "Yes - AI-powered auto-tagging",
    labeling_method: "AI analyzes first message for context",
    draft_writing: "Yes - AI Email Reply Assistant",
    pricing_min: "$10/user/month (Lite)",
    pricing_paid: "$10/month (Lite), $24/month (Growth), $36/month (Pro)",
    unusual_features:
      "Kanban boards in Gmail, Shared inbox management, Email sequences, Meeting scheduler, CRM integration",
    platform: "Gmail/Google Workspace",
    team_features: "Extensive - shared inboxes, collaboration tools",
    learning_curve: "Medium",
    customization: "High - workflow automation rules",
  },
  {
    name: "Gmail Gemini AI (Native)",
    type: "Built-in Feature",
    auto_labeling: "Yes - Tabbed Inbox with ML",
    labeling_method: "Neural network + heuristic algorithms",
    draft_writing: "Yes - Help me write, Smart Compose, Smart Reply",
    pricing_min: "Free (Basic)",
    pricing_paid: "Free basic, Advanced with Google Workspace",
    unusual_features:
      "Summary Cards, Nudging, Most Relevant search, Native Google integration",
    platform: "Gmail only",
    team_features: "Google Workspace features",
    learning_curve: "Very Low - built-in",
    customization: "Low - limited control",
  },
  {
    name: "Lindy AI",
    type: "AI Automation Platform",
    auto_labeling: "Yes - Custom AI workflows",
    labeling_method: "AI agents with natural language instructions",
    draft_writing: "Yes - Context-aware AI drafting",
    pricing_min: "Check website",
    pricing_paid: "Subscription-based",
    unusual_features:
      "Multi-agent collaboration, Email negotiation, CRM integration, Lead intent detection, No-code workflow builder",
    platform: "Gmail & multi-platform integrations",
    team_features: "Team workflows",
    learning_curve: "Medium - workflow setup",
    customization: "Very High - custom agent instructions",
  },
  {
    name: "n8n + AI (Self-hosted)",
    type: "Workflow Automation",
    auto_labeling: "Yes - Fully customizable AI labeling",
    labeling_method: "OpenAI/Gemini/Claude + custom prompts",
    draft_writing: "Yes - customizable",
    pricing_min: "Free (self-hosted)",
    pricing_paid: "Free (self-host) or Cloud plans",
    unusual_features:
      "Complete customization, Knowledge graph building, Self-hosted option, Multiple AI model support, Open source",
    platform: "Gmail + 400+ integrations",
    team_features: "Depends on setup",
    learning_curve: "High - technical setup required",
    customization: "Maximum - full code control",
  },
  {
    name: "Zapier + AI",
    type: "Automation Platform",
    auto_labeling: "Yes - AI-powered categorization",
    labeling_method: "ChatGPT integration with custom prompts",
    draft_writing: "Yes - AI-generated responses",
    pricing_min: "Free tier (limited)",
    pricing_paid: "Tiered pricing based on tasks",
    unusual_features:
      "5000+ app integrations, AI Email Assistant templates, Zapier Tables for logging",
    platform: "Gmail + massive ecosystem",
    team_features: "Team accounts available",
    learning_curve: "Medium - visual workflow builder",
    customization: "Very High - unlimited workflows",
  },
  {
    name: "GenFuse AI",
    type: "AI Workflow Builder",
    auto_labeling: "Yes - AI content-based labeling",
    labeling_method: "AI reads content and applies labels",
    draft_writing: "Yes - auto-reply/draft generation",
    pricing_min: "Check website",
    pricing_paid: "Subscription-based",
    unusual_features:
      "AI Copilot for workflow creation, Multi-step workflows, LLM calls, PDF OCR, Image analysis nodes",
    platform: "Gmail + multi-app integration",
    team_features: "Available",
    learning_curve: "Medium",
    customization: "Very High - AI nodes",
  },
  {
    name: "Hey Email",
    type: "Email Service",
    auto_labeling: "Yes - The Screener, Feed, Paper Trail",
    labeling_method: "Manual screening + automatic categorization",
    draft_writing: "Limited",
    pricing_min: "$99/year",
    pricing_paid: "$99/year (personal), $12/user/month (business)",
    unusual_features:
      "The Screener (email approval), Paper Trail for receipts, The Feed for newsletters, Spy tracker blocking, Built-in workflows",
    platform: "Standalone (@hey.com domain)",
    team_features: "Thread sharing, Private team comments",
    learning_curve: "Medium - different paradigm",
    customization: "Low - opinionated design",
  },
  {
    name: "Canary Mail",
    type: "Email Client",
    auto_labeling: "Yes - AI Smart Filters",
    labeling_method: "Machine learning based on user behavior",
    draft_writing: "Yes - Generative AI Email Writer",
    pricing_min: "Free plan available",
    pricing_paid: "Subscription tiers",
    unusual_features:
      "End-to-end encryption, On-device AI processing, Smart Bulk Cleaner, Privacy-focused, Unified inbox",
    platform: "Multi-platform (iOS, Android, Mac, Windows)",
    team_features: "Limited",
    learning_curve: "Low",
    customization: "High - learns from usage",
  },
  {
    name: "Jeeva Smart Inbox AI",
    type: "AI Inbox Assistant",
    auto_labeling: "Yes - Auto-categorization",
    labeling_method: "AI intent detection and lead scoring",
    draft_writing: "Yes - Context-aware replies",
    pricing_min: "Check website",
    pricing_paid: "Business-focused pricing",
    unusual_features:
      "Lead intent detection, Follow-up automation, CRM integration (HubSpot, Zoho, Salesforce), Auto-folder creation",
    platform: "Gmail & Outlook",
    team_features: "Yes - unified inbox",
    learning_curve: "Low",
    customization: "High - smart rules",
  },
  {
    name: "Mailmeteor AI Writer",
    type: "Gmail Add-on",
    auto_labeling: "No - Focus on sending",
    labeling_method: "N/A",
    draft_writing: "Yes - Primary feature",
    pricing_min: "Free (50 emails/day)",
    pricing_paid:
      "$9.99/month (Premium), $24.99/month (Pro), $49.99/month (Business)",
    unusual_features:
      "Mass personalized campaigns, Mail merge, Email tracking, Analytics",
    platform: "Gmail",
    team_features: "Team features in higher tiers",
    learning_curve: "Low",
    customization: "High for campaigns",
  },
];

// State management
const state = {
  tools: toolsData,
  filteredTools: toolsData,
  selectedTools: [],
  filters: {
    search: "",
    autoLabeling: "all",
    price: "all",
    platform: "all",
    learningCurve: "all",
    draft: "all",
    team: "all",
    customization: "all",
  },
  sortBy: "name-asc",
  viewMode: "cards",
};

// Initialize app
function init() {
  setupEventListeners();
  updateStats();
  applyFilters();
  renderView();
  initializeDarkMode();
}

// Dark mode
function initializeDarkMode() {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  const savedTheme = prefersDark ? "dark" : "light";
  document.documentElement.setAttribute("data-color-scheme", savedTheme);
  updateDarkModeIcon(savedTheme === "dark");

  darkModeToggle.addEventListener("click", () => {
    const currentTheme =
      document.documentElement.getAttribute("data-color-scheme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-color-scheme", newTheme);
    updateDarkModeIcon(newTheme === "dark");
  });
}

function updateDarkModeIcon(isDark) {
  const icon = document.querySelector("#darkModeToggle .icon");
  icon.textContent = isDark ? "☀️" : "🌙";
}

// Event listeners
function setupEventListeners() {
  // Search
  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", (e) => {
    state.filters.search = e.target.value;
    document
      .querySelector(".search-wrapper")
      .classList.toggle("has-value", e.target.value.length > 0);
    applyFilters();
    renderView();
  });

  document.getElementById("clearSearch").addEventListener("click", () => {
    searchInput.value = "";
    state.filters.search = "";
    document.querySelector(".search-wrapper").classList.remove("has-value");
    applyFilters();
    renderView();
  });

  // Filters
  document
    .getElementById("autoLabelingFilter")
    .addEventListener("change", (e) => {
      state.filters.autoLabeling = e.target.value;
      applyFilters();
      renderView();
    });

  document.getElementById("priceFilter").addEventListener("change", (e) => {
    state.filters.price = e.target.value;
    applyFilters();
    renderView();
  });

  document.getElementById("platformFilter").addEventListener("change", (e) => {
    state.filters.platform = e.target.value;
    applyFilters();
    renderView();
  });

  document
    .getElementById("learningCurveFilter")
    .addEventListener("change", (e) => {
      state.filters.learningCurve = e.target.value;
      applyFilters();
      renderView();
    });

  document
    .getElementById("customizationFilter")
    .addEventListener("change", (e) => {
      state.filters.customization = e.target.value;
      applyFilters();
      renderView();
    });

  // Toggle buttons
  document.querySelectorAll(".toggle-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const filter = e.target.dataset.filter;
      const value = e.target.dataset.value;

      // Update active state
      e.target.parentElement
        .querySelectorAll(".toggle-btn")
        .forEach((b) => b.classList.remove("active"));
      e.target.classList.add("active");

      state.filters[filter] = value;
      applyFilters();
      renderView();
    });
  });

  // Set initial active state for toggle buttons
  document.querySelectorAll('.toggle-btn[data-value="all"]').forEach((btn) => {
    btn.classList.add("active");
  });

  // Reset filters
  document
    .getElementById("resetFilters")
    .addEventListener("click", resetFilters);
  document
    .getElementById("resetFromEmpty")
    .addEventListener("click", resetFilters);

  // Sort
  document.getElementById("sortBy").addEventListener("change", (e) => {
    state.sortBy = e.target.value;
    sortTools();
    renderView();
  });

  // View toggle
  document.querySelectorAll(".view-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      document
        .querySelectorAll(".view-btn")
        .forEach((b) => b.classList.remove("active"));
      e.target.classList.add("active");
      state.viewMode = e.target.dataset.view;
      renderView();
    });
  });

  // Export
  document.getElementById("exportBtn").addEventListener("click", exportResults);

  // Comparison
  document
    .getElementById("compareBtn")
    .addEventListener("click", showComparison);
  document
    .getElementById("clearComparison")
    .addEventListener("click", clearComparison);

  // Quick links
  document.querySelectorAll(".quick-link-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const filter = e.target.dataset.filter;
      applyQuickFilter(filter);
    });
  });

  // Modal close
  document.querySelectorAll(".modal-close").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.closest(".modal").classList.add("hidden");
    });
  });

  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", () => {
      overlay.closest(".modal").classList.add("hidden");
    });
  });
}

// Filter and sort functions
function applyFilters() {
  let filtered = [...state.tools];

  // Search
  if (state.filters.search) {
    const search = state.filters.search.toLowerCase();
    filtered = filtered.filter(
      (tool) =>
        tool.name.toLowerCase().includes(search) ||
        tool.type.toLowerCase().includes(search) ||
        tool.auto_labeling.toLowerCase().includes(search) ||
        tool.unusual_features.toLowerCase().includes(search) ||
        tool.platform.toLowerCase().includes(search),
    );
  }

  // Auto-labeling
  if (state.filters.autoLabeling !== "all") {
    filtered = filtered.filter((tool) => {
      const labeling = tool.auto_labeling.toLowerCase();
      if (state.filters.autoLabeling === "primary") {
        return labeling.includes("primary");
      } else if (state.filters.autoLabeling === "yes") {
        return labeling.startsWith("yes") && !labeling.includes("primary");
      } else if (state.filters.autoLabeling === "limited") {
        return labeling.includes("limited");
      } else if (state.filters.autoLabeling === "no") {
        return labeling.toLowerCase().startsWith("no");
      }
      return true;
    });
  }

  // Price
  if (state.filters.price !== "all") {
    filtered = filtered.filter((tool) => {
      const price = extractPrice(tool.pricing_min);
      if (state.filters.price === "free") {
        return price === 0;
      } else if (state.filters.price === "under10") {
        return price > 0 && price < 10;
      } else if (state.filters.price === "10-25") {
        return price >= 10 && price <= 25;
      } else if (state.filters.price === "25-40") {
        return price > 25 && price <= 40;
      } else if (state.filters.price === "40plus") {
        return price > 40;
      }
      return true;
    });
  }

  // Platform
  if (state.filters.platform !== "all") {
    filtered = filtered.filter((tool) => {
      const platform = tool.platform.toLowerCase();
      if (state.filters.platform === "gmail-only") {
        return (
          platform.includes("gmail") &&
          !platform.includes("multi") &&
          !platform.includes("&")
        );
      } else if (state.filters.platform === "multi-platform") {
        return (
          platform.includes("multi") ||
          platform.includes("&") ||
          platform.includes("+")
        );
      } else if (state.filters.platform === "standalone") {
        return platform.includes("standalone") || platform.includes("@hey.com");
      }
      return true;
    });
  }

  // Learning curve
  if (state.filters.learningCurve !== "all") {
    filtered = filtered.filter((tool) => {
      const curve = tool.learning_curve.toLowerCase();
      return curve.includes(state.filters.learningCurve.replace("-", " "));
    });
  }

  // Draft writing
  if (state.filters.draft !== "all") {
    filtered = filtered.filter((tool) => {
      const draft = tool.draft_writing.toLowerCase();
      if (state.filters.draft === "yes") {
        return draft.startsWith("yes");
      } else if (state.filters.draft === "limited") {
        return draft.includes("limited");
      } else if (state.filters.draft === "no") {
        return draft === "no";
      }
      return true;
    });
  }

  // Team features
  if (state.filters.team !== "all") {
    filtered = filtered.filter((tool) => {
      const team = tool.team_features.toLowerCase();
      if (state.filters.team === "yes") {
        return (
          team.includes("extensive") ||
          team.includes("shared") ||
          team.includes("team") ||
          team.includes("collaboration") ||
          team.includes("unified")
        );
      } else if (state.filters.team === "limited") {
        return team.includes("limited") || team.includes("individual");
      } else if (state.filters.team === "no") {
        return team === "no";
      }
      return true;
    });
  }

  // Customization
  if (state.filters.customization !== "all") {
    filtered = filtered.filter((tool) => {
      const custom = tool.customization.toLowerCase();
      return custom.includes(state.filters.customization.replace("-", " "));
    });
  }

  state.filteredTools = filtered;
  sortTools();
  updateResultsCount();
}

function sortTools() {
  const sorted = [...state.filteredTools];

  switch (state.sortBy) {
    case "name-asc":
      sorted.sort((a, b) => a.name.localeCompare(b.name));
      break;
    case "name-desc":
      sorted.sort((a, b) => b.name.localeCompare(a.name));
      break;
    case "price-asc":
      sorted.sort(
        (a, b) => extractPrice(a.pricing_min) - extractPrice(b.pricing_min),
      );
      break;
    case "price-desc":
      sorted.sort(
        (a, b) => extractPrice(b.pricing_min) - extractPrice(a.pricing_min),
      );
      break;
    case "best-labeling":
      sorted.sort((a, b) => {
        const scoreA = a.auto_labeling.includes("Primary")
          ? 3
          : a.auto_labeling.startsWith("Yes")
            ? 2
            : 1;
        const scoreB = b.auto_labeling.includes("Primary")
          ? 3
          : b.auto_labeling.startsWith("Yes")
            ? 2
            : 1;
        return scoreB - scoreA;
      });
      break;
    case "easiest":
      sorted.sort((a, b) => {
        const order = { "very low": 1, low: 2, medium: 3, high: 4 };
        const scoreA =
          order[a.learning_curve.toLowerCase().split("-")[0].trim()] || 5;
        const scoreB =
          order[b.learning_curve.toLowerCase().split("-")[0].trim()] || 5;
        return scoreA - scoreB;
      });
      break;
    case "most-customizable":
      sorted.sort((a, b) => {
        const order = {
          maximum: 5,
          "very high": 4,
          high: 3,
          medium: 2,
          low: 1,
        };
        const scoreA =
          order[a.customization.toLowerCase().split("-")[0].trim()] || 0;
        const scoreB =
          order[b.customization.toLowerCase().split("-")[0].trim()] || 0;
        return scoreB - scoreA;
      });
      break;
  }

  state.filteredTools = sorted;
}

function extractPrice(priceString) {
  if (
    !priceString ||
    priceString.toLowerCase().includes("free") ||
    priceString.toLowerCase().includes("check website")
  ) {
    return 0;
  }
  const match = priceString.match(/\$(\d+)/);
  return match ? parseInt(match[1]) : 999;
}

function resetFilters() {
  state.filters = {
    search: "",
    autoLabeling: "all",
    price: "all",
    platform: "all",
    learningCurve: "all",
    draft: "all",
    team: "all",
    customization: "all",
  };

  document.getElementById("searchInput").value = "";
  document.querySelector(".search-wrapper").classList.remove("has-value");
  document.getElementById("autoLabelingFilter").value = "all";
  document.getElementById("priceFilter").value = "all";
  document.getElementById("platformFilter").value = "all";
  document.getElementById("learningCurveFilter").value = "all";
  document.getElementById("customizationFilter").value = "all";

  document.querySelectorAll(".toggle-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.value === "all");
  });

  applyFilters();
  renderView();
}

function applyQuickFilter(filter) {
  resetFilters();

  if (filter === "best-labeling") {
    state.filters.autoLabeling = "primary";
    document.getElementById("autoLabelingFilter").value = "primary";
  } else if (filter === "best-value") {
    state.filters.price = "10-25";
    document.getElementById("priceFilter").value = "10-25";
    state.filters.autoLabeling = "yes";
    document.getElementById("autoLabelingFilter").value = "yes";
  } else if (filter === "unusual") {
    state.sortBy = "best-labeling";
    document.getElementById("sortBy").value = "best-labeling";
  }

  applyFilters();
  renderView();
}

// Render functions
function renderView() {
  if (state.filteredTools.length === 0) {
    showEmptyState();
  } else {
    hideEmptyState();
    if (state.viewMode === "cards") {
      renderCards();
    } else {
      renderTable();
    }
  }
  updateComparisonBar();
}

function showEmptyState() {
  document.getElementById("emptyState").classList.remove("hidden");
  document.getElementById("cardsView").classList.add("hidden");
  document.getElementById("tableView").classList.add("hidden");
}

function hideEmptyState() {
  document.getElementById("emptyState").classList.add("hidden");
}

function renderCards() {
  document.getElementById("cardsView").classList.remove("hidden");
  document.getElementById("tableView").classList.add("hidden");

  const container = document.getElementById("cardsView");
  container.innerHTML = state.filteredTools
    .map((tool) => createToolCard(tool))
    .join("");

  // Add event listeners
  container.querySelectorAll(".compare-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", (e) => {
      const toolName = e.target.dataset.tool;
      handleToolSelection(toolName, e.target.checked);
    });
  });

  container.querySelectorAll(".btn-details").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const toolName = e.target.dataset.tool;
      showToolDetails(toolName);
    });
  });
}

function renderTable() {
  document.getElementById("cardsView").classList.add("hidden");
  document.getElementById("tableView").classList.remove("hidden");

  const tbody = document.getElementById("tableBody");
  tbody.innerHTML = state.filteredTools
    .map((tool) => createTableRow(tool))
    .join("");

  // Add event listeners
  tbody.querySelectorAll(".compare-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", (e) => {
      const toolName = e.target.dataset.tool;
      handleToolSelection(toolName, e.target.checked);
    });
  });

  tbody.querySelectorAll(".btn-details").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const toolName = e.target.dataset.tool;
      showToolDetails(toolName);
    });
  });
}

function createToolCard(tool) {
  const features = tool.unusual_features.split(",").slice(0, 3);
  const isSelected = state.selectedTools.includes(tool.name);

  return `
    <div class="tool-card ${isSelected ? "selected" : ""}">
      <div class="card-header">
        <div class="card-title-row">
          <h3 class="tool-name">${tool.name}</h3>
          <input type="checkbox" class="compare-checkbox" data-tool="${tool.name}" ${isSelected ? "checked" : ""}>
        </div>
        <span class="type-badge">${tool.type}</span>
      </div>
      
      <div class="card-info">
        <div class="info-row">
          <span class="info-label">Auto-Labeling:</span>
          <span class="info-value ${getStatusClass(tool.auto_labeling)}">
            ${tool.auto_labeling.includes("Yes") ? "✓" : tool.auto_labeling.includes("No") ? "✗" : "~"} 
            ${tool.auto_labeling.replace("Yes - ", "")}
          </span>
        </div>
        <div class="info-row">
          <span class="info-label">Draft Writing:</span>
          <span class="info-value ${getStatusClass(tool.draft_writing)}">
            ${tool.draft_writing.startsWith("Yes") ? "✓" : tool.draft_writing === "No" ? "✗" : "~"} 
            ${tool.draft_writing}
          </span>
        </div>
        <div class="info-row">
          <span class="info-label">Starting Price:</span>
          <span class="price-tag">${formatPrice(tool.pricing_min)}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Learning Curve:</span>
          <span class="info-value">${tool.learning_curve}</span>
        </div>
      </div>
      
      <div class="unusual-features">
        <h4>Key Features</h4>
        <ul class="features-list">
          ${features.map((f) => `<li>${f.trim()}</li>`).join("")}
        </ul>
      </div>
      
      <div class="card-actions">
        <button class="btn-details" data-tool="${tool.name}">View Details</button>
      </div>
    </div>
  `;
}

function createTableRow(tool) {
  const isSelected = state.selectedTools.includes(tool.name);

  return `
    <tr class="${isSelected ? "selected" : ""}">
      <td><input type="checkbox" class="compare-checkbox" data-tool="${tool.name}" ${isSelected ? "checked" : ""}></td>
      <td><strong>${tool.name}</strong></td>
      <td>${tool.type}</td>
      <td class="${getStatusClass(tool.auto_labeling)}">${tool.auto_labeling}</td>
      <td class="${getStatusClass(tool.draft_writing)}">${tool.draft_writing}</td>
      <td>${formatPrice(tool.pricing_min)}</td>
      <td>${tool.platform}</td>
      <td>${tool.learning_curve}</td>
      <td><button class="btn-details" data-tool="${tool.name}">Details</button></td>
    </tr>
  `;
}

function getStatusClass(status) {
  if (
    status.toLowerCase().startsWith("yes") ||
    status.toLowerCase().includes("primary")
  ) {
    return "status-yes";
  } else if (status.toLowerCase().includes("limited")) {
    return "status-limited";
  } else {
    return "status-no";
  }
}

function formatPrice(priceString) {
  if (priceString.toLowerCase().includes("free")) {
    return "Free";
  } else if (priceString.toLowerCase().includes("check website")) {
    return "See Website";
  }
  return priceString;
}

// Tool selection
function handleToolSelection(toolName, isSelected) {
  if (isSelected) {
    if (!state.selectedTools.includes(toolName)) {
      state.selectedTools.push(toolName);
    }
  } else {
    state.selectedTools = state.selectedTools.filter((t) => t !== toolName);
  }

  updateComparisonBar();
  renderView();
}

function updateComparisonBar() {
  const bar = document.getElementById("comparisonBar");
  const count = document.getElementById("comparisonCount");

  if (state.selectedTools.length > 0) {
    bar.classList.remove("hidden");
    count.textContent = `${state.selectedTools.length} tool${state.selectedTools.length > 1 ? "s" : ""} selected`;
  } else {
    bar.classList.add("hidden");
  }
}

function clearComparison() {
  state.selectedTools = [];
  document
    .querySelectorAll(".compare-checkbox")
    .forEach((cb) => (cb.checked = false));
  updateComparisonBar();
  renderView();
}

// Details modal
function showToolDetails(toolName) {
  const tool = state.tools.find((t) => t.name === toolName);
  if (!tool) return;

  const modal = document.getElementById("detailModal");
  const content = document.getElementById("detailContent");

  const features = tool.unusual_features.split(",");

  content.innerHTML = `
    <div class="detail-header">
      <h2 class="detail-title">${tool.name}</h2>
      <span class="type-badge">${tool.type}</span>
    </div>
    
    <div class="detail-section">
      <h3>Overview</h3>
      <div class="detail-grid">
        <div class="detail-item">
          <div class="detail-item-label">Platform</div>
          <div class="detail-item-value">${tool.platform}</div>
        </div>
        <div class="detail-item">
          <div class="detail-item-label">Learning Curve</div>
          <div class="detail-item-value">${tool.learning_curve}</div>
        </div>
        <div class="detail-item">
          <div class="detail-item-label">Customization</div>
          <div class="detail-item-value">${tool.customization}</div>
        </div>
      </div>
    </div>
    
    <div class="detail-section">
      <h3>Auto-Labeling</h3>
      <div class="detail-grid">
        <div class="detail-item">
          <div class="detail-item-label">Capability</div>
          <div class="detail-item-value ${getStatusClass(tool.auto_labeling)}">${tool.auto_labeling}</div>
        </div>
        <div class="detail-item">
          <div class="detail-item-label">Method</div>
          <div class="detail-item-value">${tool.labeling_method}</div>
        </div>
      </div>
    </div>
    
    <div class="detail-section">
      <h3>Draft Writing</h3>
      <div class="detail-item">
        <div class="detail-item-label">Capability</div>
        <div class="detail-item-value ${getStatusClass(tool.draft_writing)}">${tool.draft_writing}</div>
      </div>
    </div>
    
    <div class="detail-section">
      <h3>Pricing</h3>
      <div class="detail-grid">
        <div class="detail-item">
          <div class="detail-item-label">Starting Price</div>
          <div class="detail-item-value">${tool.pricing_min}</div>
        </div>
        <div class="detail-item">
          <div class="detail-item-label">Paid Plans</div>
          <div class="detail-item-value">${tool.pricing_paid}</div>
        </div>
      </div>
    </div>
    
    <div class="detail-section">
      <h3>Team Features</h3>
      <div class="detail-item">
        <div class="detail-item-value">${tool.team_features}</div>
      </div>
    </div>
    
    <div class="detail-section">
      <h3>Unusual &amp; Special Features</h3>
      <ul class="features-list">
        ${features.map((f) => `<li>${f.trim()}</li>`).join("")}
      </ul>
    </div>
  `;

  modal.classList.remove("hidden");
}

// Comparison modal
function showComparison() {
  if (state.selectedTools.length < 2) {
    alert("Please select at least 2 tools to compare");
    return;
  }

  const tools = state.selectedTools.map((name) =>
    state.tools.find((t) => t.name === name),
  );
  const modal = document.getElementById("comparisonModal");
  const content = document.getElementById("comparisonContent");

  content.innerHTML = `
    <h2>Tool Comparison</h2>
    <table class="comparison-table">
      <thead>
        <tr>
          <th>Feature</th>
          ${tools.map((t) => `<th>${t.name}</th>`).join("")}
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Type</strong></td>
          ${tools.map((t) => `<td>${t.type}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Auto-Labeling</strong></td>
          ${tools.map((t) => `<td class="${getStatusClass(t.auto_labeling)}">${t.auto_labeling}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Labeling Method</strong></td>
          ${tools.map((t) => `<td>${t.labeling_method}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Draft Writing</strong></td>
          ${tools.map((t) => `<td class="${getStatusClass(t.draft_writing)}">${t.draft_writing}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Starting Price</strong></td>
          ${tools.map((t) => `<td>${t.pricing_min}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Paid Plans</strong></td>
          ${tools.map((t) => `<td>${t.pricing_paid}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Platform</strong></td>
          ${tools.map((t) => `<td>${t.platform}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Team Features</strong></td>
          ${tools.map((t) => `<td>${t.team_features}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Learning Curve</strong></td>
          ${tools.map((t) => `<td>${t.learning_curve}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Customization</strong></td>
          ${tools.map((t) => `<td>${t.customization}</td>`).join("")}
        </tr>
        <tr>
          <td><strong>Unusual Features</strong></td>
          ${tools.map((t) => `<td>${t.unusual_features}</td>`).join("")}
        </tr>
      </tbody>
    </table>
  `;

  modal.classList.remove("hidden");
}

// Stats
function updateStats() {
  const total = state.tools.length;
  const withLabeling = state.tools.filter((t) =>
    t.auto_labeling.toLowerCase().startsWith("yes"),
  ).length;
  const percentage = Math.round((withLabeling / total) * 100);

  // Price range
  const prices = state.tools
    .map((t) => extractPrice(t.pricing_min))
    .filter((p) => p > 0);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices.filter((p) => p < 999));

  // Most common type
  const types = {};
  state.tools.forEach((t) => {
    types[t.type] = (types[t.type] || 0) + 1;
  });
  const topType = Object.keys(types).reduce((a, b) =>
    types[a] > types[b] ? a : b,
  );

  document.getElementById("totalTools").textContent = total;
  document.getElementById("autoLabelTools").textContent = `${percentage}%`;
  document.getElementById("avgPrice").textContent = `$${minPrice}-$${maxPrice}`;
  document.getElementById("topFeature").textContent = topType;
}

function updateResultsCount() {
  const count = document.getElementById("resultsCount");
  count.textContent = `Showing ${state.filteredTools.length} of ${state.tools.length} tools`;
}

// Export
function exportResults() {
  let text = `Gmail AI Tools Comparison\n`;
  text += `Generated on ${new Date().toLocaleDateString()}\n`;
  text += `\nShowing ${state.filteredTools.length} of ${state.tools.length} tools\n`;
  text += `\n${"=".repeat(80)}\n\n`;

  state.filteredTools.forEach((tool, index) => {
    text += `${index + 1}. ${tool.name}\n`;
    text += `   Type: ${tool.type}\n`;
    text += `   Auto-Labeling: ${tool.auto_labeling}\n`;
    text += `   Labeling Method: ${tool.labeling_method}\n`;
    text += `   Draft Writing: ${tool.draft_writing}\n`;
    text += `   Starting Price: ${tool.pricing_min}\n`;
    text += `   Paid Plans: ${tool.pricing_paid}\n`;
    text += `   Platform: ${tool.platform}\n`;
    text += `   Team Features: ${tool.team_features}\n`;
    text += `   Learning Curve: ${tool.learning_curve}\n`;
    text += `   Customization: ${tool.customization}\n`;
    text += `   Unusual Features: ${tool.unusual_features}\n`;
    text += `\n${"-".repeat(80)}\n\n`;
  });

  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `gmail-ai-tools-comparison-${new Date().toISOString().split("T")[0]}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Initialize on load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
