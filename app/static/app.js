const tg = window.Telegram?.WebApp;

const state = {
  books: [],
  activeBook: null,
  currentChunkIndex: 0,
  totalChunks: 0,
  activeSessionId: null,
  recapDepth: "quick",
  celebratedBookIds: new Set(),
};

const els = {
  authNotice: document.querySelector("#authNotice"),
  refreshBooks: document.querySelector("#refreshBooks"),
  bookFile: document.querySelector("#bookFile"),
  bookTitle: document.querySelector("#bookTitle"),
  uploadBook: document.querySelector("#uploadBook"),
  booksList: document.querySelector("#booksList"),
  bookCount: document.querySelector("#bookCount"),
  welcomeBonus: document.querySelector("#welcomeBonus"),
  depthButtons: document.querySelectorAll(".depth-button"),
  bookMeta: document.querySelector("#bookMeta"),
  progressMeta: document.querySelector("#progressMeta"),
  chunkText: document.querySelector("#chunkText"),
  previousChunk: document.querySelector("#previousChunk"),
  nextChunk: document.querySelector("#nextChunk"),
  saveStop: document.querySelector("#saveStop"),
  sessionButtons: document.querySelectorAll(".session-button"),
};

function authHeaders() {
  if (tg?.initData) {
    return { Authorization: `Bearer ${tg.initData}` };
  }
  els.authNotice.classList.remove("hidden");
  return {
    "X-Telegram-User-Id": "dev-user-1",
    "X-Telegram-Username": "local_reader",
    "X-Telegram-Display-Name": "Local Reader",
  };
}

async function api(path, options = {}) {
  const headers = { ...authHeaders(), ...(options.headers || {}) };
  const response = await fetch(path, { ...options, headers });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }
  return response.json();
}

async function loadBooks() {
  state.books = await api("/books");
  renderBooks();
}

function renderBooks() {
  els.bookCount.textContent = String(state.books.length);
  els.booksList.innerHTML = "";

  if (!state.books.length) {
    const empty = document.createElement("p");
    empty.className = "book-subtitle";
    empty.textContent = "Пока пусто. Загрузи небольшой TXT и попробуй один абзац.";
    els.booksList.append(empty);
    return;
  }

  for (const book of state.books) {
    const item = document.createElement("button");
    item.className = `book-item ${state.activeBook?.id === book.id ? "active" : ""}`;
    item.innerHTML = `
      <span class="book-title"></span>
      <span class="book-subtitle">${book.total_chunks} фрагм. · ${book.total_words} слов</span>
    `;
    item.querySelector(".book-title").textContent = book.title;
    item.addEventListener("click", () => openBook(book.id));
    els.booksList.append(item);
  }
}

async function uploadBook() {
  const file = els.bookFile.files?.[0];
  if (!file) {
    showTelegramAlert("Выбери TXT, EPUB или FB2 файл");
    return;
  }

  const form = new FormData();
  form.append("file", file);
  if (els.bookTitle.value.trim()) {
    form.append("title", els.bookTitle.value.trim());
  }

  const book = await api("/books/upload", { method: "POST", body: form });
  els.bookFile.value = "";
  els.bookTitle.value = "";
  await loadBooks();
  await openBook(book.id);
}

async function openBook(bookId) {
  state.activeBook = state.books.find((book) => book.id === bookId) || null;
  state.currentChunkIndex = 0;
  await showWelcomeBonus(bookId);
  await readChunk(bookId);
  renderBooks();
}

async function showWelcomeBonus(bookId) {
  const bonus = await api(`/books/${bookId}/welcome-bonus?depth=${state.recapDepth}`);
  els.welcomeBonus.textContent = bonus.text;
  els.welcomeBonus.classList.remove("hidden");
}

async function readChunk(bookId, chunkIndex = null) {
  const suffix = chunkIndex === null ? "" : `?chunk_index=${chunkIndex}`;
  const data = await api(`/books/${bookId}/read${suffix}`);
  state.activeBook = data.book;
  state.currentChunkIndex = data.current_chunk_index;
  state.totalChunks = data.total_chunks;

  els.bookMeta.textContent = data.book.title;
  els.progressMeta.textContent = `${data.current_chunk_index + 1} / ${data.total_chunks}`;
  els.chunkText.textContent = data.chunk?.text || "Текст не найден.";
  els.previousChunk.disabled = !data.has_previous;
  els.nextChunk.disabled = !data.has_next;
}

async function saveProgress() {
  if (!state.activeBook) return;
  const words = countWords(els.chunkText.textContent);
  await api(`/books/${state.activeBook.id}/progress`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      current_chunk_index: state.currentChunkIndex,
      chunks_read: 1,
      words_read: words,
    }),
  });
  if (isBookFinished()) {
    showCompletion();
    return;
  }
  showTelegramAlert("Сохранено. Можно спокойно вернуться позже.");
}

async function move(delta) {
  if (!state.activeBook) return;
  const nextIndex = Math.max(0, Math.min(state.totalChunks - 1, state.currentChunkIndex + delta));
  await readChunk(state.activeBook.id, nextIndex);
  await saveProgressSilently();
  if (delta > 0 && isBookFinished()) {
    showCompletion();
  }
}

async function saveProgressSilently() {
  if (!state.activeBook) return;
  await api(`/books/${state.activeBook.id}/progress`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      current_chunk_index: state.currentChunkIndex,
      chunks_read: 1,
      words_read: countWords(els.chunkText.textContent),
    }),
  });
}

async function startSession(minutes) {
  if (!state.activeBook) {
    showTelegramAlert("Сначала выбери книгу");
    return;
  }

  const session = await api("/sessions/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      book_id: state.activeBook.id,
      planned_minutes: minutes,
      start_chunk_index: state.currentChunkIndex,
    }),
  });
  state.activeSessionId = session.id;
  showTelegramAlert(`${minutes} минут. Один абзац уже считается хорошим стартом.`);
}

function countWords(text) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function showTelegramAlert(message) {
  if (tg?.showAlert) {
    tg.showAlert(message);
  } else {
    alert(message);
  }
}

async function changeDepth(depth) {
  state.recapDepth = depth;
  els.depthButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.depth === depth);
  });
  if (state.activeBook) {
    await showWelcomeBonus(state.activeBook.id);
  }
}

function isBookFinished() {
  return state.activeBook && state.totalChunks > 0 && state.currentChunkIndex >= state.totalChunks - 1;
}

function showCompletion() {
  if (!state.activeBook || state.celebratedBookIds.has(state.activeBook.id)) return;
  state.celebratedBookIds.add(state.activeBook.id);
  showTelegramAlert("Ты дочитал(а) книгу! 🎉✨ Это было не про скорость, а про возвращение. Мягко, красиво, победа.");
}

function applyTelegramTheme() {
  if (!tg?.themeParams) return;
  const map = {
    bg_color: "--bg",
    secondary_bg_color: "--surface",
    section_bg_color: "--paper",
    text_color: "--text",
    hint_color: "--muted",
    button_color: "--accent",
    button_text_color: "--button-text",
  };
  for (const [telegramKey, cssVar] of Object.entries(map)) {
    const value = tg.themeParams[telegramKey];
    if (value) {
      document.documentElement.style.setProperty(cssVar, value);
    }
  }
}

els.refreshBooks.addEventListener("click", loadBooks);
els.uploadBook.addEventListener("click", () => uploadBook().catch((error) => showTelegramAlert(error.message)));
els.previousChunk.addEventListener("click", () => move(-1).catch((error) => showTelegramAlert(error.message)));
els.nextChunk.addEventListener("click", () => move(1).catch((error) => showTelegramAlert(error.message)));
els.saveStop.addEventListener("click", () => saveProgress().catch((error) => showTelegramAlert(error.message)));
els.sessionButtons.forEach((button) => {
  button.addEventListener("click", () => startSession(Number(button.dataset.minutes)).catch((error) => showTelegramAlert(error.message)));
});
els.depthButtons.forEach((button) => {
  button.addEventListener("click", () => changeDepth(button.dataset.depth).catch((error) => showTelegramAlert(error.message)));
});

if (tg) {
  applyTelegramTheme();
  tg.ready();
  tg.expand();
}

loadBooks().catch((error) => showTelegramAlert(error.message));
