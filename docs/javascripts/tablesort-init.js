// Sortable problem tables, scoped to the bank landing pages.
//
// Material 9.7.6 free ships no table sorting, so the problem tables on the
// bank landing pages (docs/leetcode/index.md and docs/amazon/index.md) use
// tristen/tablesort, loaded from the unpkg entry above this file in
// mkdocs.yml. Per the theme's customization guidance, per-page JavaScript
// subscribes to the document$ observable so it re-runs on every page swap
// under navigation.instant. The subscription is gated on the current page
// being one of the landings themselves: the pathname check runs inside the
// subscription because instant navigation swaps the pathname per page, and
// other pages (pattern guides, write-ups, foundations, sources) keep plain,
// unsortable markdown tables.
//
// Tablesort's default comparator treats "-" as an ordinary string, so dash
// cells (an unknown Time or Difficulty) sort first ascending. The "minutes"
// sort registered below makes dash-only cells compare as +Infinity: last
// ascending, first descending. Its pattern only accepts "N minutes" cells
// and lone dashes, so every other column (dates, words) keeps Tablesort's
// default comparator.
//
// Tablesort.extend appends to module-level state, so it runs at load time
// instead of inside the document$ subscription, which re-runs per swap.
//
// The data attribute keeps repeat document$ emissions from re-initializing
// an already-sorted table, which would stack duplicate click handlers. The
// same guard keeps one reset control per table: the control is inserted
// into the article DOM next to the table, so it is cached and re-shown by
// instant navigation together with the stamped rows and its listener. The
// id assignment sits behind the same guard, so a cached table never gets a
// second content-table-N number after an instant-navigation round trip.
//
// Stamping and control installation run before the Tablesort constructor:
// a header carrying data-sort-default makes the constructor sort the rows
// immediately, and stamping afterwards would record that sorted order as
// the default.

const DASH_ONLY_CELL = /^[-\u2013\u2014]*$/;
const MINUTES_CELL = /^\d+\s*minutes?$/;

// Tablesort comparators use an inverted convention (positive when the first
// cell is smaller) and the ascending pass reverses after sorting, so
// subtracting in the opposite order yields value-ascending with +Infinity
// (dashes) last.
const timeCellValue = (text) => {
  const cell = text.trim();
  if (DASH_ONLY_CELL.test(cell)) {
    return Infinity;
  }
  const parsed = Number.parseFloat(cell);
  return Number.isNaN(parsed) ? Infinity : parsed;
};

if (typeof Tablesort !== "undefined") {
  Tablesort.extend(
    "minutes",
    (text) => MINUTES_CELL.test(text) || DASH_ONLY_CELL.test(text),
    (first, second) => timeCellValue(second) - timeCellValue(first)
  );
}

// Tablesort 5.x records sort state only as the aria-sort attribute on the
// sorted header cell, so removing it restarts the asc/desc cycle; the rows
// carry their default order as a data attribute stamped at init time.
const resetTablesortState = (table) => {
  for (const header of table.querySelectorAll("thead [aria-sort]")) {
    header.removeAttribute("aria-sort");
  }
  for (const body of table.tBodies) {
    const rows = Array.from(body.rows).sort(
      (first, second) =>
        Number(first.dataset.defaultIndex) - Number(second.dataset.defaultIndex)
    );
    for (const row of rows) {
      body.appendChild(row);
    }
  }
};

// Module scope so the numbering survives instant navigation: a counter
// reset per document$ emission could hand out an id already held by a
// cached table on another page.
let contentTableCount = 0;

const installResetControl = (table) => {
  let index = 0;
  for (const body of table.tBodies) {
    for (const row of body.rows) {
      row.dataset.defaultIndex = String(index);
      index += 1;
    }
  }
  const resetButton = document.createElement("button");
  resetButton.type = "button";
  resetButton.className = "md-button";
  resetButton.textContent = "Reset sort";
  resetButton.setAttribute("aria-controls", table.id);
  // Filterable tables fold this action into their control-row filter
  // panel and drop this standalone button; the marker is how the filter
  // module finds it.
  resetButton.setAttribute("data-tablesort-reset", "");
  resetButton.addEventListener("click", () => resetTablesortState(table));
  table.before(resetButton);
};

// True when the current page is a bank landing page: directory URLs end
// the path with /leetcode/ or /amazon/, while servers without them append
// index.html, and the deployed site prefixes a base path, so all three
// shapes pass.
const isBankLandingPage = () => {
  const pathname = window.location.pathname.replace(/index\.html$/, "");
  return pathname.endsWith("/leetcode/") || pathname.endsWith("/amazon/");
};

document$.subscribe(() => {
  if (typeof Tablesort === "undefined" || !isBankLandingPage()) {
    return;
  }
  for (const table of document.querySelectorAll("article table:not([data-tablesort])")) {
    table.setAttribute("data-tablesort", "");
    if (!table.id) {
      contentTableCount += 1;
      table.id = `content-table-${contentTableCount}`;
    }
    installResetControl(table);
    new Tablesort(table);
  }
});
