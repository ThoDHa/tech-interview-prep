// Control-row filtering for the problem tables.
//
// Companion to tablesort-init.js: the problem tables on the two bank
// landings (docs/leetcode/index.md and docs/amazon/index.md) get a slim
// control row directly above the table - a funnel toggle and a reset-sort
// icon, right-aligned - and the funnel drops a compact filter panel between
// the row and the table:
// a case-insensitive problem-name search input, a Difficulty select (both
// landing tables carry a real Difficulty column), a Category select where
// that column exists (its options are the distinct tags the column's
// comma-separated cells contain, and a row matches on exact tag equality
// after split and trim), and a Tracks select where that column exists,
// plus a Clear button. Escape inside the panel empties every
// filter and closes it, and Escape on the funnel closes an open panel. The
// funnel carries a small dot badge while any
// filter is non-default. A table counts as filterable when its header row
// has a Problem column and a Difficulty column - the columns the
// filters can actually work on - so every other article table (pattern
// guides, sources) stays untouched. Like
// tablesort-init.js, per-page work subscribes to document$ for instant
// navigation: each swap delivers fresh tables, and the data attribute guard
// keeps repeat emissions from stacking duplicate control rows over the same
// DOM. The control row and the panel live in the article DOM next to the
// table, not inside it, so a swap replaces them together with the table: a
// fresh page always starts with the panel closed and the filters at their
// defaults.
//
// Because every control sits outside the table, header cells stay plain
// sortable text and Tablesort's header-click sort binding needs no
// cooperation from this file.
//
// Filterable tables supersede tablesort-init's standalone "Reset sort"
// button: at install time that button is still the table's previous sibling
// (the sort module's subscription runs first), so it is removed by its
// marker attribute and rebuilt as the control-row icon bound to the same
// resetTablesortState, gated on the default-order stamps as before (unstamped
// rows would be reordered into a scrambled, NaN-driven order). Tables
// without filters keep the standalone button, and both files degrade
// independently when the other is absent.
//
// Filtering only toggles row visibility, never row order, so Tablesort keeps
// working on the DOM it sees: hidden rows move with a sort but stay hidden,
// and Clear filters leaves sort state (aria-sort and row order) alone, while
// Reset sort leaves filter state alone.

const DIFFICULTY_OPTIONS = ["Easy", "Medium", "Hard"];
const TRACK_OPTIONS = ["Grind 75", "NeetCode 150", "Amazon OA"];
const ALL_OPTION_VALUE = "";
const ALL_OPTION_LABEL = "All";
const CONTROL_ROW_FONT_SIZE = "0.64rem";
const CONTROL_ROW_GAP = "0.6rem";
const BUTTON_GAP = "0.4rem";
const PROBLEM_INPUT_WIDTH = "12rem";
const PANEL_GAP = "0.6rem";
const PANEL_PADDING = "0.4rem 0.6rem";
const PANEL_MARGIN_TOP = "0.2rem";
const PANEL_BORDER = "1px solid currentColor";
const PANEL_BORDER_RADIUS = "0.2rem";
const PANEL_ROLE = "group";
const PANEL_LABEL = "Filters";
const BADGE_SIZE = "0.4em";
const BADGE_OFFSET = "-0.2em";
const SVG_NAMESPACE = "http://www.w3.org/2000/svg";

// Feather icon geometry (MIT-licensed set), drawn through createElementNS so
// the control row gains icons without an icon font dependency or CSP-hostile
// markup.
const FILTER_ICON = [
  ["polygon", { points: "22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" }],
];
const RESET_ICON = [
  ["polyline", { points: "1 4 1 10 7 10" }],
  ["path", { d: "M3.51 15a9 9 0 1 0 2.13-9.36L1 10" }],
];

// Module scope so panel ids survive instant navigation: a counter reset per
// document$ emission could hand out an id already held by a cached table on
// another page.
let filterPanelCount = 0;

/** First header row of a table, whether or not it has a thead. */
const headerRowOf = (table) => (table.tHead ? table.tHead.rows[0] : table.rows[0]);

/** Maps each filterable column's header text to its cell index. */
const columnMap = (table) => {
  const columns = {
    problem: -1,
    difficulty: -1,
    category: -1,
    tracks: -1,
  };
  Array.from(headerRowOf(table).cells).forEach((cell, index) => {
    const name = cell.textContent.trim().toLowerCase();
    if (name in columns) {
      columns[name] = index;
    }
  });
  return columns;
};

/** True when the column map has the problem-table shape: a Problem column plus a Difficulty column. */
const isFilterable = (columns) =>
  columns.problem !== -1 && columns.difficulty !== -1;

/** Indices applyFilters reads from a row; a short row missing any of them degrades to unfiltered. */
const requiredColumns = (columns) => {
  const indices = [columns.problem];
  if (columns.difficulty !== -1) {
    indices.push(columns.difficulty);
  }
  if (columns.tracks !== -1) {
    indices.push(columns.tracks);
  }
  if (columns.category !== -1) {
    indices.push(columns.category);
  }
  return indices;
};

/** True when the row has a cell at every index applyFilters reads. */
const rowCoversColumns = (row, requiredIndices) =>
  requiredIndices.every((index) => index < row.cells.length);

/** Trimmed text of the row's cell at the column index. */
const cellText = (row, columnIndex) => row.cells[columnIndex].textContent.trim();

/** Difficulty label for a row: its Difficulty cell. */
const difficultyOf = (row, columns) => cellText(row, columns.difficulty);

/** The row's Category cell split into its trimmed, non-empty tags. */
const categoryTagsOf = (row, columns) =>
  cellText(row, columns.category)
    .split(",")
    .map((tag) => tag.trim())
    .filter((tag) => tag !== "");

/** Distinct Category tags across the rows, sorted case-insensitively. */
const categoryOptionsOf = (table, columns) => {
  const tags = new Set();
  const requiredIndices = requiredColumns(columns);
  for (const body of table.tBodies) {
    for (const row of body.rows) {
      if (!rowCoversColumns(row, requiredIndices)) {
        continue;
      }
      for (const tag of categoryTagsOf(row, columns)) {
        tags.add(tag);
      }
    }
  }
  return [...tags].sort((left, right) =>
    left.localeCompare(right, undefined, { sensitivity: "base" })
  );
};

/** Builds an inline CSP-safe icon from Feather geometry via createElementNS. */
const buildIcon = (drawing) => {
  const svg = document.createElementNS(SVG_NAMESPACE, "svg");
  for (const [attribute, value] of Object.entries({
    viewBox: "0 0 24 24",
    width: "1em",
    height: "1em",
    fill: "none",
    stroke: "currentColor",
    "stroke-width": "2",
    "stroke-linecap": "round",
    "stroke-linejoin": "round",
    "aria-hidden": "true",
  })) {
    svg.setAttribute(attribute, value);
  }
  for (const [tag, attributes] of drawing) {
    const shape = document.createElementNS(SVG_NAMESPACE, tag);
    for (const [attribute, value] of Object.entries(attributes)) {
      shape.setAttribute(attribute, value);
    }
    svg.append(shape);
  }
  return svg;
};

/** Applies the borderless chrome-control look the control row and panel share; font: inherit because native buttons keep the browser default font otherwise. */
const styleAsChromeControl = (element) => {
  element.style.backgroundColor = "transparent";
  element.style.border = "none";
  element.style.color = "inherit";
  element.style.cursor = "pointer";
  element.style.padding = "0";
  element.style.font = "inherit";
};

/** Builds a borderless control-row icon button styled to inherit the theme colors. */
const buildIconButton = (label, drawing) => {
  const button = document.createElement("button");
  button.type = "button";
  button.setAttribute("aria-label", label);
  button.append(buildIcon(drawing));
  styleAsChromeControl(button);
  button.style.display = "inline-flex";
  button.style.alignItems = "center";
  return button;
};

/** Builds the hidden dot shown on the funnel while any filter is non-default. */
const buildActiveBadge = () => {
  const badge = document.createElement("span");
  badge.setAttribute("aria-hidden", "true");
  badge.style.position = "absolute";
  badge.style.top = BADGE_OFFSET;
  badge.style.right = BADGE_OFFSET;
  badge.style.width = BADGE_SIZE;
  badge.style.height = BADGE_SIZE;
  badge.style.borderRadius = "50%";
  badge.style.backgroundColor = "currentColor";
  badge.style.display = "none";
  return badge;
};

/** Builds the case-insensitive problem-name text input. */
const buildTextInput = () => {
  const input = document.createElement("input");
  input.type = "text";
  input.className = "md-input";
  input.placeholder = "Filter by problem";
  input.setAttribute("aria-label", "Filter problems by name");
  input.style.width = PROBLEM_INPUT_WIDTH;
  return input;
};

/** Builds a filter select: an all-option with an empty value followed by one option per label. */
const buildSelect = (label, allOptionLabel, optionLabels) => {
  const select = document.createElement("select");
  select.className = "md-input";
  select.setAttribute("aria-label", label);
  [allOptionLabel, ...optionLabels].forEach((optionLabel, index) => {
    const option = document.createElement("option");
    option.value = index === 0 ? ALL_OPTION_VALUE : optionLabel;
    option.textContent = optionLabel;
    select.append(option);
  });
  return select;
};

/** Builds the small clear button emptying every control without touching sort state. */
const buildClearButton = (table, controls) => {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = "Clear";
  button.setAttribute("aria-label", "Clear filters");
  styleAsChromeControl(button);
  button.addEventListener("click", () => clearFilters(table, controls));
  return button;
};

/** True when tablesort-init stamped every body's rows with their default order. */
const isDefaultOrderStamped = (table) =>
  table.tBodies.length > 0 &&
  Array.from(table.tBodies).every(
    (body) =>
      body.rows.length > 0 && body.rows[0].dataset.defaultIndex !== undefined
  );

/** Builds the reset-sort icon restoring default row order and sort state; null when the sort module is absent or the table carries no default-order stamps (unstamped rows would be reordered into a scrambled, NaN-driven order). */
const buildResetButton = (table) => {
  if (
    typeof resetTablesortState !== "function" ||
    !isDefaultOrderStamped(table)
  ) {
    return null;
  }
  const button = buildIconButton("Reset sort", RESET_ICON);
  button.setAttribute("aria-controls", table.id);
  button.addEventListener("click", () => resetTablesortState(table));
  return button;
};

/** Removes tablesort-init's standalone reset button; the control-row icon supersedes it here. */
const removeStandaloneReset = (table) => {
  const standalone = table.previousElementSibling;
  if (standalone?.matches("button[data-tablesort-reset]")) {
    standalone.remove();
  }
};

/** True when any control holds a non-default value, judged the way applyFilters judges it (trimmed). */
const isFilterActive = (controls) =>
  controls.text.value.trim() !== "" ||
  controls.selects.some((select) => select.value !== ALL_OPTION_VALUE);

/** Hides non-matching rows and mirrors the funnel badge. */
const applyFilters = (table, controls) => {
  const query = controls.text.value.trim().toLowerCase();
  const difficulty = controls.difficulty.value;
  const category = controls.category ? controls.category.value : "";
  const track = controls.tracks ? controls.tracks.value.toLowerCase() : "";
  const requiredIndices = requiredColumns(controls.columns);
  for (const body of table.tBodies) {
    for (const row of body.rows) {
      if (!rowCoversColumns(row, requiredIndices)) {
        continue;
      }
      const rowCategoryTags = category ? categoryTagsOf(row, controls.columns) : [];
      const matches =
        (!query ||
          cellText(row, controls.columns.problem).toLowerCase().includes(query)) &&
        (!difficulty || difficultyOf(row, controls.columns) === difficulty) &&
        (!category || rowCategoryTags.includes(category)) &&
        (!track ||
          cellText(row, controls.columns.tracks).toLowerCase().includes(track));
      row.style.display = matches ? "" : "none";
    }
  }
  controls.badge.style.display = isFilterActive(controls) ? "block" : "none";
};

/** Empties every filter control and reapplies, leaving sort state untouched. */
const clearFilters = (table, controls) => {
  controls.text.value = "";
  for (const select of controls.selects) {
    select.value = ALL_OPTION_VALUE;
  }
  applyFilters(table, controls);
};

/** True when the funnel reports its panel as open. */
const isPanelOpen = (controls) =>
  controls.funnelButton.getAttribute("aria-expanded") === "true";

/** Reveals the panel, marks the funnel expanded, and moves focus into the search input. */
const openPanel = (controls) => {
  controls.panel.style.display = "flex";
  controls.funnelButton.setAttribute("aria-expanded", "true");
  controls.text.focus();
};

/** Hides the panel, marks the funnel collapsed, and returns focus to the funnel. */
const closePanel = (controls) => {
  controls.panel.style.display = "none";
  controls.funnelButton.setAttribute("aria-expanded", "false");
  controls.funnelButton.focus();
};

/** Builds the compact card holding the filter controls, dropped under the control row. */
const buildFilterPanel = (table, controls) => {
  const panel = document.createElement("div");
  filterPanelCount += 1;
  panel.id = `filter-panel-${filterPanelCount}`;
  panel.setAttribute("role", PANEL_ROLE);
  panel.setAttribute("aria-label", PANEL_LABEL);
  panel.style.display = "none";
  panel.style.flexWrap = "wrap";
  panel.style.alignItems = "center";
  panel.style.gap = PANEL_GAP;
  panel.style.padding = PANEL_PADDING;
  panel.style.marginTop = PANEL_MARGIN_TOP;
  panel.style.border = PANEL_BORDER;
  panel.style.borderRadius = PANEL_BORDER_RADIUS;
  panel.append(controls.text, ...controls.selects, buildClearButton(table, controls));
  panel.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      clearFilters(table, controls);
      closePanel(controls);
    }
  });
  return panel;
};

/** Inserts the control row, the filter panel, and the event wiring above the table. */
const installFilterControls = (table, columns) => {
  const controls = {
    columns,
    text: buildTextInput(),
    difficulty: null,
    category: null,
    tracks: null,
    selects: [],
    funnelButton: null,
    badge: null,
    panel: null,
  };
  if (columns.difficulty !== -1) {
    controls.difficulty = buildSelect(
      "Filter by difficulty",
      ALL_OPTION_LABEL,
      DIFFICULTY_OPTIONS
    );
    controls.selects.push(controls.difficulty);
  }
  if (columns.category !== -1) {
    controls.category = buildSelect(
      "Filter by category",
      ALL_OPTION_LABEL,
      categoryOptionsOf(table, columns)
    );
    controls.selects.push(controls.category);
  }
  if (columns.tracks !== -1) {
    controls.tracks = buildSelect("Filter by tracks", ALL_OPTION_LABEL, TRACK_OPTIONS);
    controls.selects.push(controls.tracks);
  }
  controls.funnelButton = buildIconButton("Toggle filters", FILTER_ICON);
  controls.funnelButton.style.position = "relative";
  controls.funnelButton.setAttribute("aria-expanded", "false");
  controls.badge = buildActiveBadge();
  controls.funnelButton.append(controls.badge);
  controls.panel = buildFilterPanel(table, controls);
  controls.funnelButton.setAttribute("aria-controls", controls.panel.id);
  controls.funnelButton.addEventListener("click", () => {
    if (isPanelOpen(controls)) {
      closePanel(controls);
    } else {
      openPanel(controls);
    }
  });
  controls.funnelButton.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && isPanelOpen(controls)) {
      closePanel(controls);
    }
  });
  controls.text.addEventListener("input", () => applyFilters(table, controls));
  for (const select of controls.selects) {
    select.addEventListener("change", () => applyFilters(table, controls));
  }

  const buttons = document.createElement("span");
  buttons.style.display = "inline-flex";
  buttons.style.alignItems = "center";
  buttons.style.gap = BUTTON_GAP;
  const resetButton = buildResetButton(table);
  if (resetButton) {
    buttons.append(resetButton);
  }
  buttons.append(controls.funnelButton);

  const row = document.createElement("div");
  row.style.display = "flex";
  row.style.alignItems = "center";
  row.style.justifyContent = "flex-end";
  row.style.gap = CONTROL_ROW_GAP;
  row.style.fontSize = CONTROL_ROW_FONT_SIZE;
  row.append(buttons);

  removeStandaloneReset(table);
  table.before(row, controls.panel);
  applyFilters(table, controls);
};

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    for (const table of document.querySelectorAll(
      "article table:not([data-table-filter])"
    )) {
      const columns = columnMap(table);
      if (!isFilterable(columns)) {
        continue;
      }
      table.setAttribute("data-table-filter", "");
      installFilterControls(table, columns);
    }
  });
}
