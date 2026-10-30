(() => {
  "use strict";

  const root = document.documentElement;
  const themeToggle = document.querySelector(".theme-toggle");
  const themeColor = document.getElementById("theme-color");
  const searchInput = document.getElementById("search");
  const clearButton = document.getElementById("clear-filters");
  const resultCount = document.getElementById("result-count");
  const typeButtons = [...document.querySelectorAll(".segmented-button[data-type]")];
  const tagButtons = [...document.querySelectorAll(".tag-chip[data-tag]")];
  const cards = [...document.querySelectorAll(".item-card")];
  const lanes = [...document.querySelectorAll(".lane")];

  const state = {
    type: "all",
    tags: new Set(),
    query: "",
  };

  const normalize = (value) =>
    String(value)
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim();

  const itemLabel = (count) => `${count} ${count === 1 ? "item" : "itens"}`;

  const isFiltering = () =>
    state.type !== "all" || state.tags.size > 0 || state.query.trim() !== "";

  function applyFilters() {
    const query = normalize(state.query);
    let visible = 0;

    cards.forEach((card) => {
      const matchesType = state.type === "all" || card.dataset.type === state.type;
      const cardTags = (card.dataset.tags || "").split(/\s+/).filter(Boolean);
      const matchesTags =
        state.tags.size === 0 ||
        [...state.tags].some((tag) => cardTags.includes(tag));
      const matchesQuery =
        !query || normalize(card.dataset.search || "").includes(query);
      const show = matchesType && matchesTags && matchesQuery;
      card.classList.toggle("is-hidden", !show);
      if (show) visible += 1;
    });

    lanes.forEach((lane) => {
      const laneCards = [...lane.querySelectorAll(".item-card")];
      const laneVisible = laneCards.filter(
        (card) => !card.classList.contains("is-hidden")
      ).length;
      const empty = lane.querySelector(".lane-empty");
      if (empty) empty.hidden = laneVisible !== 0;
      lane.classList.toggle("is-empty", laneVisible === 0);
    });

    if (resultCount) {
      resultCount.textContent = isFiltering()
        ? `${visible} de ${cards.length} ${cards.length === 1 ? "item" : "itens"}`
        : itemLabel(cards.length);
    }

    if (clearButton) clearButton.hidden = !isFiltering();
    syncURL();
  }

  function syncControls() {
    typeButtons.forEach((button) => {
      const active = button.dataset.type === state.type;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    tagButtons.forEach((button) => {
      const active = state.tags.has(button.dataset.tag);
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    if (searchInput) searchInput.value = state.query;
  }

  function syncURL() {
    const url = new URL(window.location.href);
    const params = new URLSearchParams();
    if (state.type !== "all") params.set("tipo", state.type);
    if (state.tags.size) params.set("tag", [...state.tags].join(","));
    if (state.query.trim()) params.set("q", state.query.trim());
    url.search = params.toString();
    try {
      window.history.replaceState(null, "", url);
    } catch (error) {
      /* file:// ou ambientes sem histórico */
    }
  }

  function readURL() {
    const params = new URLSearchParams(window.location.search);
    const type = params.get("tipo");
    if (type && typeButtons.some((button) => button.dataset.type === type)) {
      state.type = type;
    }
    const tags = (params.get("tag") || "")
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean);
    state.tags = new Set(
      tags.filter((tag) => tagButtons.some((button) => button.dataset.tag === tag))
    );
    state.query = params.get("q") || "";
  }

  typeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      state.type = button.dataset.type || "all";
      syncControls();
      applyFilters();
    });
  });

  tagButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const tag = button.dataset.tag;
      if (!tag) return;
      if (state.tags.has(tag)) state.tags.delete(tag);
      else state.tags.add(tag);
      syncControls();
      applyFilters();
    });
  });

  searchInput?.addEventListener("input", (event) => {
    state.query = event.target.value;
    applyFilters();
  });

  clearButton?.addEventListener("click", () => {
    state.type = "all";
    state.tags.clear();
    state.query = "";
    syncControls();
    applyFilters();
    searchInput?.focus();
  });

  function updateThemeUI() {
    const isDark = root.dataset.theme === "dark";
    if (themeToggle) {
      themeToggle.setAttribute(
        "aria-label",
        isDark ? "Ativar tema claro" : "Ativar tema escuro"
      );
      themeToggle.setAttribute(
        "title",
        isDark ? "Ativar tema claro" : "Ativar tema escuro"
      );
      themeToggle.setAttribute("aria-pressed", String(isDark));
    }
    if (themeColor) {
      themeColor.setAttribute("content", isDark ? "#000000" : "#f5f5f7");
    }
  }

  themeToggle?.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try {
      localStorage.setItem("career-theme", next);
    } catch (error) {
      /* localStorage pode estar indisponível */
    }
    updateThemeUI();
  });

  document.querySelectorAll(".print-button").forEach((button) => {
    button.addEventListener("click", () => window.print());
  });

  readURL();
  syncControls();
  applyFilters();
  updateThemeUI();
})();
