const tg = window.Telegram?.WebApp;

const SCREEN_META = {
  home: { titleKey: "screenHome", eyebrow: "ТГ Шевченко" },
  library: { titleKey: "screenLibrary", eyebrow: "cloud books" },
  reader: { titleKey: "screenReader", eyebrow: "classic reader" },
  progress: { titleKey: "screenProgress", eyebrow: "gentle pace" },
  settings: { titleKey: "screenSettings", eyebrow: "reading comfort" },
};

const I18N = {
  ru: {
    screenHome: "Домой",
    screenLibrary: "Библиотека",
    screenReader: "Чтение",
    screenProgress: "Прогресс",
    screenSettings: "Настройки",
    homeHeroTitle: "Вернемся к книге без рывка",
    homeHeroBody: "Один маленький фрагмент уже считается хорошей сессией.",
    welcomeDefault: "Добро пожаловать",
    greeting: "Привет, {name}",
    continueLabel: "Продолжить чтение",
    continueButton: "Читать",
    quickSessionButton: "3 минуты",
    noBookTitle: "Книга пока не выбрана",
    noBookMeta: "Загрузи книгу или выбери ее в библиотеке.",
    continueMeta: "{current} из {total} фрагментов",
    welcomeFallback: "Здесь будет короткое напоминание перед возвращением.",
    recentBooks: "Недавние книги",
    allBooks: "Все",
    importLabel: "Импорт",
    addBook: "Добавить книгу",
    importHint: "TXT, EPUB, FB2 или .fb2.zip. PDF отложим на потом.",
    chooseFile: "Выбрать файл",
    titlePlaceholder: "Название, если нужно",
    uploading: "Загрузка",
    uploadButton: "Загрузить",
    editBook: "Редактировать",
    editBookTitle: "Книга",
    editTitleLabel: "Название",
    editAuthorLabel: "Автор",
    editCoverLabel: "Обложка",
    removeCover: "Убрать обложку",
    cancel: "Отмена",
    saveChanges: "Сохранить",
    bookUpdated: "Книга обновлена.",
    loadingTitle: "Собираю тихое место для чтения",
    loadingLine1: "Проверяю книги",
    loadingLine2: "Вспоминаю прогресс",
    loadingLine3: "Готовлю мягкий вход",
    streakDone: "День засчитан",
    streakDays: "{count} дн.",
    libraryTitle: "Библиотека",
    readerLabel: "Книга",
    chooseBook: "Выбери книгу",
    searchPlaceholder: "Слово или номер фрагмента",
    searchButton: "Найти",
    readerEmpty: "Выбери книгу в библиотеке или загрузи новый файл.",
    readerInitial: "Здесь появится один небольшой абзац. Без гонки, без давления.",
    classicReadMode: "Читать в Classic Read Mode",
    classicReadModeHint: "Основной режим: страницы, главы, сноски и спокойное чтение",
    quickFragmentLabel: "Быстрый фрагмент",
    quickFragmentTitle: "Один смысловой кусок",
    quickFragmentPill: "ADHD tool",
    nextQuickFragment: "Ещё фрагмент",
    depthQuick: "Коротко",
    depthStory: "События",
    depthDeep: "Глубже",
    exitClassicReadMode: "Выйти из CRM",
    saveAndExit: "Сохранить и выйти",
    streakZero: "0 дней",
    streakOne: "1 день",
    streakHint: "Возвращение важнее идеальной серии.",
    sessionsLabel: "Сессии",
    sessionsHint: "Короткие заходы тоже считаются.",
    chunksLabel: "Фрагменты",
    chunksHint: "Маленькие шаги, меньше трения.",
    recentActivity: "Недавняя активность",
    languageLabel: "Язык",
    languageTitle: "Язык интерфейса",
    textSizeLabel: "Размер текста",
    comfortableText: "Комфортный",
    themeLabel: "Тема",
    themeAuto: "Системная / Telegram",
    chunkSizeLabel: "Размер фрагмента",
    oneParagraph: "Один абзац",
    focusHint: "Страницы, главы и спокойное чтение",
    soon: "Soon",
    navHome: "Home",
    navLibrary: "Library",
    navReader: "Reader",
    navProgress: "Progress",
    navSettings: "Settings",
    refresh: "Обновить",
    previousChunk: "Предыдущий фрагмент",
    nextChunk: "Следующий фрагмент",
    toggleReaderOverlay: "Показать настройки чтения",
    readerClose: "Закрыть",
    readerFontDown: "Уменьшить шрифт",
    readerFontUp: "Увеличить шрифт",
    readerThemeDark: "Dark",
    readerThemeBlack: "Black",
    readerThemeSepia: "Sepia",
    readerModePage: "Pages",
    readerModeChunk: "Chunks",
    readerZones: "Zones",
    readerZonesOff: "Hide zones",
    readerVisualProgress: "Стр. {page}/{loaded} · фрагм. {chunk}/{total}",
    recapDepth: "Глубина пересказа",
    closeRecap: "Закрыть пересказ",
    mainNav: "Главная навигация",
    weekDays: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    emptyLibrary: "Пока пусто. Добавь книгу, и она появится здесь.",
    authorUnknown: "Автор не указан",
    compactBookMeta: "{author} · {chunks} фрагм.",
    libraryBookMeta: "{author} · {words} слов",
    libraryCurrentMeta: "{author} · сейчас {current}/{total}",
    uploadNoFile: "Выбери TXT, EPUB или FB2 файл",
    selectedFile: "Выбран файл",
    selectedFileHint: "Нажми “Загрузить”, чтобы добавить книгу.",
    uploaded: "Загружено",
    addedBook: "Добавлена книга: {title}",
    chooseBookNotice: "Сначала выбери книгу",
    savedPlace: "Сохранено место: {title}, фрагмент {chunk}",
    finishedBook: "Ты дочитал(а) книгу! Это было не про скорость, а про возвращение.",
    savedNotice: "Сохранено. Можно спокойно вернуться позже.",
    sessionStarted: "Начата спокойная сессия на {minutes} минуты",
    sessionNotice: "{minutes} минуты. Один фрагмент уже достаточно.",
    progressChunk: "Фрагмент {page} · {words} слов",
    uploadFailed: "Upload failed",
    uploadAborted: "Upload aborted",
    invalidUploadResponse: "Upload response is not valid JSON",
    unnamedBook: "Без названия",
    languageSaved: "Язык сохранён.",
    activityEmpty: "Здесь появятся мягкие отметки: сессии, сохранения и возвращения к книге.",
  },
  uk: {
    screenHome: "Додому",
    screenLibrary: "Бібліотека",
    screenReader: "Читання",
    screenProgress: "Прогрес",
    screenSettings: "Налаштування",
    homeHeroTitle: "Повернімося до книжки без ривка",
    homeHeroBody: "Один маленький фрагмент вже рахується доброю сесією.",
    welcomeDefault: "Ласкаво просимо",
    greeting: "Привіт, {name}",
    continueLabel: "Продовжити читання",
    continueButton: "Читати",
    quickSessionButton: "3 хвилини",
    noBookTitle: "Книжку ще не вибрано",
    noBookMeta: "Завантаж книжку або вибери її в бібліотеці.",
    continueMeta: "{current} із {total} фрагментів",
    welcomeFallback: "Тут буде коротке нагадування перед поверненням.",
    recentBooks: "Нещодавні книжки",
    allBooks: "Усі",
    importLabel: "Імпорт",
    addBook: "Додати книжку",
    importHint: "TXT, EPUB, FB2 або .fb2.zip. PDF відкладемо на потім.",
    chooseFile: "Вибрати файл",
    titlePlaceholder: "Назва, якщо потрібно",
    uploading: "Завантаження",
    uploadButton: "Завантажити",
    editBook: "Редагувати",
    editBookTitle: "Книжка",
    editTitleLabel: "Назва",
    editAuthorLabel: "Автор",
    editCoverLabel: "Обкладинка",
    removeCover: "Прибрати обкладинку",
    cancel: "Скасувати",
    saveChanges: "Зберегти",
    bookUpdated: "Книжку оновлено.",
    loadingTitle: "Збираю тихе місце для читання",
    loadingLine1: "Перевіряю книжки",
    loadingLine2: "Згадую прогрес",
    loadingLine3: "Готую м'який вхід",
    streakDone: "День зараховано",
    streakDays: "{count} дн.",
    libraryTitle: "Бібліотека",
    readerLabel: "Книжка",
    chooseBook: "Вибери книжку",
    searchPlaceholder: "Слово або номер фрагмента",
    searchButton: "Знайти",
    readerEmpty: "Вибери книжку в бібліотеці або завантаж новий файл.",
    readerInitial: "Тут з'явиться один невеликий абзац. Без гонитви, без тиску.",
    classicReadMode: "Читати в Classic Read Mode",
    classicReadModeHint: "Основний режим: сторінки, розділи, примітки й спокійне читання",
    quickFragmentLabel: "Швидкий фрагмент",
    quickFragmentTitle: "Один смисловий шматок",
    quickFragmentPill: "ADHD tool",
    nextQuickFragment: "Ще фрагмент",
    depthQuick: "Коротко",
    depthStory: "Події",
    depthDeep: "Глибше",
    exitClassicReadMode: "Вийти з CRM",
    saveAndExit: "Зберегти й вийти",
    streakZero: "0 днів",
    streakOne: "1 день",
    streakHint: "Повернення важливіше за ідеальну серію.",
    sessionsLabel: "Сесії",
    sessionsHint: "Короткі підходи теж рахуються.",
    chunksLabel: "Фрагменти",
    chunksHint: "Малі кроки, менше тертя.",
    recentActivity: "Нещодавня активність",
    languageLabel: "Мова",
    languageTitle: "Мова інтерфейсу",
    textSizeLabel: "Розмір тексту",
    comfortableText: "Комфортний",
    themeLabel: "Тема",
    themeAuto: "Системна / Telegram",
    chunkSizeLabel: "Розмір фрагмента",
    oneParagraph: "Один абзац",
    focusHint: "Сторінки, розділи й спокійне читання",
    soon: "Скоро",
    navHome: "Додому",
    navLibrary: "Бібліотека",
    navReader: "Reader",
    navProgress: "Прогрес",
    navSettings: "Налаштування",
    refresh: "Оновити",
    previousChunk: "Попередній фрагмент",
    nextChunk: "Наступний фрагмент",
    toggleReaderOverlay: "Показати налаштування читання",
    readerClose: "Закрити",
    readerFontDown: "Зменшити шрифт",
    readerFontUp: "Збільшити шрифт",
    readerThemeDark: "Dark",
    readerThemeBlack: "Black",
    readerThemeSepia: "Sepia",
    readerModePage: "Pages",
    readerModeChunk: "Chunks",
    readerZones: "Зони",
    readerZonesOff: "Сховати зони",
    readerVisualProgress: "Стор. {page}/{loaded} · фрагм. {chunk}/{total}",
    recapDepth: "Глибина переказу",
    closeRecap: "Закрити переказ",
    mainNav: "Головна навігація",
    weekDays: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"],
    emptyLibrary: "Поки порожньо. Додай книжку, і вона з'явиться тут.",
    authorUnknown: "Автор не вказаний",
    compactBookMeta: "{author} · {chunks} фрагм.",
    libraryBookMeta: "{author} · {words} слів",
    libraryCurrentMeta: "{author} · зараз {current}/{total}",
    uploadNoFile: "Вибери TXT, EPUB або FB2 файл",
    selectedFile: "Вибрано файл",
    selectedFileHint: "Натисни “Завантажити”, щоб додати книжку.",
    uploaded: "Завантажено",
    addedBook: "Додано книжку: {title}",
    chooseBookNotice: "Спочатку вибери книжку",
    savedPlace: "Збережено місце: {title}, фрагмент {chunk}",
    finishedBook: "Ти дочитав(ла) книжку! Це було не про швидкість, а про повернення.",
    savedNotice: "Збережено. Можна спокійно повернутися пізніше.",
    sessionStarted: "Почато спокійну сесію на {minutes} хвилини",
    sessionNotice: "{minutes} хвилини. Один фрагмент уже достатньо.",
    progressChunk: "Фрагмент {page} · {words} слів",
    uploadFailed: "Завантаження не вдалося",
    uploadAborted: "Завантаження скасовано",
    invalidUploadResponse: "Відповідь upload не є валідним JSON",
    unnamedBook: "Без назви",
    languageSaved: "Мову збережено.",
    activityEmpty: "Тут з'являться м'які позначки: сесії, збереження й повернення до книжки.",
  },
};

const state = {
  screen: "home",
  language: "ru",
  currentUser: null,
  displayName: "Local Reader",
  books: [],
  activeBook: null,
  activeBookDetail: null,
  currentChunkIndex: 0,
  totalChunks: 0,
  currentChunk: null,
  welcomeBonus: "",
  recapDepth: "quick",
  activeSessionId: null,
  chunkCache: new Map(),
  searchResults: [],
  streakStatus: null,
  editBook: null,
  readerControlsVisible: false,
  readerOverlayTimer: null,
  readerSettings: {
    fontStep: 0,
    theme: "dark",
    mode: "page",
    showZones: false,
  },
  readerPages: [],
  readerLoadedChunks: [],
  readerPageCursor: 0,
  readerBufferedFromChunkIndex: null,
  readerBufferedUntilChunkIndex: -1,
  readerPrefetchPromise: null,
  readerReflowTimer: null,
  readerMeasure: null,
  readerLayoutVersion: 0,
  readerRangeSize: 32,
  readerPrefetchThreshold: 7,
  uploadProgress: 0,
  isUploading: false,
  isEditingBook: false,
  activity: [],
  stats: {
    sessions: 0,
    savedChunks: 0,
  },
};

const els = {
  appShell: document.querySelector(".app-shell"),
  topbar: document.querySelector(".app-topbar"),
  screenTitle: document.querySelector("#screenTitle"),
  topEyebrow: document.querySelector("#topEyebrow"),
  refreshBooks: document.querySelector("#refreshBooks"),
  homeGreeting: document.querySelector("#homeGreeting"),
  continueTitle: document.querySelector("#continueTitle"),
  continueMeta: document.querySelector("#continueMeta"),
  continueReading: document.querySelector("#continueReading"),
  quickSession: document.querySelector("#quickSession"),
  welcomePreviewCard: document.querySelector("#welcomePreviewCard"),
  welcomePreview: document.querySelector("#welcomePreview"),
  recentBooks: document.querySelector("#recentBooks"),
  bookFile: document.querySelector("#bookFile"),
  bookTitle: document.querySelector("#bookTitle"),
  appLoading: document.querySelector("#appLoading"),
  loadingLines: document.querySelectorAll(".loading-line"),
  uploadStatus: document.querySelector("#uploadStatus"),
  uploadProgress: document.querySelector("#uploadProgress"),
  uploadProgressFill: document.querySelector("#uploadProgressFill"),
  uploadProgressValue: document.querySelector("#uploadProgressValue"),
  uploadBook: document.querySelector("#uploadBook"),
  editBookDialog: document.querySelector("#editBookDialog"),
  editBookForm: document.querySelector("#editBookForm"),
  editBookHeading: document.querySelector("#editBookHeading"),
  editTitle: document.querySelector("#editTitle"),
  editAuthor: document.querySelector("#editAuthor"),
  editCover: document.querySelector("#editCover"),
  editRemoveCover: document.querySelector("#editRemoveCover"),
  closeEditBook: document.querySelector("#closeEditBook"),
  cancelEditBook: document.querySelector("#cancelEditBook"),
  saveBookEdit: document.querySelector("#saveBookEdit"),
  booksList: document.querySelector("#booksList"),
  bookCount: document.querySelector("#bookCount"),
  bookMeta: document.querySelector("#bookMeta"),
  progressMeta: document.querySelector("#progressMeta"),
  progressFill: document.querySelector("#progressFill"),
  readerSearchInput: document.querySelector("#readerSearchInput"),
  readerSearchButton: document.querySelector("#readerSearchButton"),
  readerSearchResults: document.querySelector("#readerSearchResults"),
  chunkText: document.querySelector("#chunkText"),
  chunkTextValue: document.querySelector("#chunkTextValue"),
  chunkPreviousButton: document.querySelector("#chunkPreviousButton"),
  chunkNextButton: document.querySelector("#chunkNextButton"),
  welcomeBonus: document.querySelector("#welcomeBonus"),
  welcomeBonusText: document.querySelector("#welcomeBonusText"),
  toggleWelcomeBonus: document.querySelector("#toggleWelcomeBonus"),
  closeWelcomeBonus: document.querySelector("#closeWelcomeBonus"),
  depthButtons: document.querySelectorAll(".depth-button"),
  tapPreviousChunk: document.querySelector("#tapPreviousChunk"),
  toggleReaderOverlay: document.querySelector("#toggleReaderOverlay"),
  tapNextChunk: document.querySelector("#tapNextChunk"),
  saveStop: document.querySelector("#saveStop"),
  exitFocusMode: document.querySelector("#exitFocusMode"),
  readerOverlay: document.querySelector("#readerOverlay"),
  overlayExit: document.querySelector("#overlayExit"),
  overlaySave: document.querySelector("#overlaySave"),
  readerProgressText: document.querySelector("#readerProgressText"),
  readerProgressMiniFill: document.querySelector("#readerProgressMiniFill"),
  readerFontDown: document.querySelector("#readerFontDown"),
  readerFontUp: document.querySelector("#readerFontUp"),
  readerThemeToggle: document.querySelector("#readerThemeToggle"),
  readerModeToggle: document.querySelector("#readerModeToggle"),
  readerZonesToggle: document.querySelector("#readerZonesToggle"),
  classicReadModeButton: document.querySelector("#classicReadModeButton"),
  streakValue: document.querySelector("#streakValue"),
  streakToast: document.querySelector("#streakToast"),
  streakToastText: document.querySelector("#streakToastText"),
  weekStreak: document.querySelector("#weekStreak"),
  sessionsValue: document.querySelector("#sessionsValue"),
  chunksValue: document.querySelector("#chunksValue"),
  activityList: document.querySelector("#activityList"),
  telegramUserInfo: document.querySelector("#telegramUserInfo"),
  languageOptions: document.querySelectorAll(".language-option"),
  navItems: document.querySelectorAll(".nav-item"),
  screens: document.querySelectorAll(".screen"),
  screenLinks: document.querySelectorAll("[data-go-screen]"),
};

function authHeaders() {
  if (tg?.initData) {
    return { Authorization: `Bearer ${tg.initData}` };
  }
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

async function apiForm(path, form, options = {}) {
  const response = await fetch(path, {
    method: options.method || "POST",
    body: form,
    headers: { ...authHeaders(), ...(options.headers || {}) },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }
  return response.json();
}

function t(key, params = {}) {
  const template = I18N[state.language]?.[key] ?? I18N.ru[key] ?? key;
  if (Array.isArray(template)) return template;
  return Object.entries(params).reduce((text, [name, value]) => text.replaceAll(`{${name}}`, value), template);
}

function setLanguage(language) {
  state.language = language === "uk" ? "uk" : "ru";
  document.documentElement.lang = state.language === "uk" ? "uk" : "ru";
  applyTranslations();
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  els.bookTitle.placeholder = t("titlePlaceholder");
  els.readerSearchInput.placeholder = t("searchPlaceholder");
  els.refreshBooks.title = t("refresh");
  els.refreshBooks.setAttribute("aria-label", t("refresh"));
  els.tapPreviousChunk.setAttribute("aria-label", t("previousChunk"));
  els.tapNextChunk.setAttribute("aria-label", t("nextChunk"));
  els.chunkPreviousButton.textContent = t("previousChunk");
  els.chunkNextButton.textContent = t("nextQuickFragment");
  els.toggleReaderOverlay.setAttribute("aria-label", t("toggleReaderOverlay"));
  els.readerFontDown.setAttribute("aria-label", t("readerFontDown"));
  els.readerFontUp.setAttribute("aria-label", t("readerFontUp"));
  document.querySelector(".depth-control")?.setAttribute("aria-label", t("recapDepth"));
  els.closeWelcomeBonus.setAttribute("aria-label", t("closeRecap"));
  document.querySelector(".bottom-nav")?.setAttribute("aria-label", t("mainNav"));
  els.homeGreeting.textContent = state.displayName ? t("greeting", { name: state.displayName }) : t("welcomeDefault");
  els.languageOptions.forEach((button) => {
    button.classList.toggle("active", button.dataset.language === state.language);
  });
  const meta = SCREEN_META[state.screen];
  els.screenTitle.textContent = t(meta.titleKey);
  renderAll();
  applyReaderSettings();
}

async function loadCurrentUser() {
  const user = await api("/users/me");
  state.currentUser = user;
  state.displayName = user.display_name || user.username || state.displayName;
  const language = user.preferences?.language || "ru";
  setLanguage(language);
}

async function loadStreak(options = {}) {
  try {
    const previousCompleted = state.streakStatus?.completed_today;
    const streak = await api("/users/me/streak");
    state.streakStatus = streak;
    renderProgress();
    if (options.celebrate && streak.completed_today && !previousCompleted) {
      showStreakCelebration(streak.streak_days);
    }
  } catch (error) {
    state.streakStatus = null;
  }
}

async function saveLanguage(language) {
  setLanguage(language);
  const user = await api("/users/me/preferences", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ language }),
  });
  state.currentUser = user;
  state.welcomeBonus = "";
  if (state.activeBook) {
    await loadWelcomeBonus(state.activeBook.id);
  }
  showNotice(t("languageSaved"));
}

function setupTelegram() {
  syncViewportHeight();
  syncSafeArea();
  applyTelegramTheme();
  setupZoomGuard();

  if (!tg) return;

  tg.ready();
  tg.expand();
  requestTelegramFullscreen();
  tg.disableVerticalSwipes?.();
  tg.setHeaderColor?.(tg.themeParams?.bg_color || "#0f1413");
  tg.setBackgroundColor?.(tg.themeParams?.bg_color || "#0f1413");
  tg.onEvent?.("themeChanged", applyTelegramTheme);
  tg.onEvent?.("viewportChanged", syncViewportHeight);
  tg.onEvent?.("fullscreenChanged", syncFullscreenState);
  tg.onEvent?.("fullscreenFailed", syncFullscreenState);
  tg.onEvent?.("safeAreaChanged", syncSafeArea);
  tg.onEvent?.("contentSafeAreaChanged", syncSafeArea);

  const user = tg.initDataUnsafe?.user;
  if (user) {
    const name = [user.first_name, user.last_name].filter(Boolean).join(" ") || user.username || `ID ${user.id}`;
    state.displayName = name;
    if (els.homeGreeting) els.homeGreeting.textContent = t("greeting", { name });
    if (els.telegramUserInfo) els.telegramUserInfo.textContent = name;
  }
}

function requestTelegramFullscreen() {
  if (!tg?.requestFullscreen) {
    document.body.classList.add("telegram-expanded");
    return;
  }

  try {
    tg.requestFullscreen();
    document.body.classList.add("telegram-fullscreen-requested");
  } catch (error) {
    document.body.classList.add("telegram-expanded");
  }
  syncFullscreenState();
}

function syncFullscreenState() {
  const isFullscreen = Boolean(tg?.isFullscreen);
  document.body.classList.toggle("telegram-fullscreen", isFullscreen);
  document.body.classList.toggle("telegram-expanded", !isFullscreen);
  document.documentElement.style.setProperty("--tg-chrome-top", isFullscreen ? "58px" : "0px");
  syncViewportHeight();
  syncSafeArea();
}

function setupZoomGuard() {
  const prevent = (event) => event.preventDefault();
  document.addEventListener("gesturestart", prevent, { passive: false });
  document.addEventListener("gesturechange", prevent, { passive: false });
  document.addEventListener("gestureend", prevent, { passive: false });
  document.addEventListener(
    "touchmove",
    (event) => {
      if (event.touches.length > 1) event.preventDefault();
    },
    { passive: false },
  );

  let lastTouchEnd = 0;
  document.addEventListener(
    "touchend",
    (event) => {
      const now = Date.now();
      if (now - lastTouchEnd <= 300) event.preventDefault();
      lastTouchEnd = now;
    },
    { passive: false },
  );
}

function syncViewportHeight() {
  const height = tg?.viewportStableHeight || tg?.viewportHeight || window.innerHeight;
  document.documentElement.style.setProperty("--app-height", `${height}px`);
  scheduleReaderRepagination();
}

function syncSafeArea() {
  const content = tg?.contentSafeAreaInset || {};
  const safe = tg?.safeAreaInset || {};
  const top = Math.max(content.top || 0, safe.top || 0);
  const bottom = Math.max(content.bottom || 0, safe.bottom || 0);
  const left = Math.max(content.left || 0, safe.left || 0);
  const right = Math.max(content.right || 0, safe.right || 0);

  document.documentElement.style.setProperty("--safe-top", `${top}px`);
  document.documentElement.style.setProperty("--safe-bottom", `${bottom}px`);
  document.documentElement.style.setProperty("--safe-left", `${left}px`);
  document.documentElement.style.setProperty("--safe-right", `${right}px`);
  scheduleReaderRepagination();
}

function applyTelegramTheme() {
  if (!tg?.themeParams) return;
  const params = tg.themeParams;
  const map = {
    bg_color: "--bg",
    secondary_bg_color: "--surface",
    section_bg_color: "--paper",
    text_color: "--text",
    hint_color: "--muted",
    button_color: "--accent",
  };
  for (const [telegramKey, cssVar] of Object.entries(map)) {
    if (params[telegramKey]) {
      document.documentElement.style.setProperty(cssVar, params[telegramKey]);
    }
  }
}

function navigate(screen) {
  if (screen !== "reader" && document.body.classList.contains("focus-mode")) {
    setFocusMode(false);
  }
  state.screen = screen;
  const meta = SCREEN_META[screen];
  els.screenTitle.textContent = t(meta.titleKey);
  els.topEyebrow.textContent = meta.eyebrow;

  els.screens.forEach((item) => {
    item.classList.toggle("active", item.dataset.screen === screen);
    if (item.dataset.screen === screen) item.scrollTop = 0;
  });
  els.navItems.forEach((item) => {
    item.classList.toggle("active", item.dataset.screenTarget === screen);
  });
  syncHeaderState();
}

async function loadBooks() {
  state.books = await api("/books");
  if (state.books.length && !state.activeBook) {
    await openBook(state.books[0].id, { switchToReader: false });
  }
  renderAll();
}

async function openBook(bookId, options = { switchToReader: true }) {
  const book = state.books.find((item) => item.id === bookId) || null;
  if (!book) return;

  state.activeBook = book;
  state.activeBookDetail = await api(`/books/${bookId}`);
  state.searchResults = [];
  resetReaderPages();
  if (els.readerSearchInput) els.readerSearchInput.value = "";
  state.currentChunkIndex = state.activeBookDetail.current_chunk_index || 0;
  state.totalChunks = state.activeBookDetail.total_chunks || book.total_chunks || 0;
  await loadWelcomeBonus(bookId);
  await readChunk(bookId, state.currentChunkIndex, { trackActivity: Boolean(options.switchToReader) });
  renderAll();

  if (options.switchToReader) {
    navigate("reader");
    if (options.openClassic !== false) {
      openClassicReadMode();
    }
  }
}

async function loadWelcomeBonus(bookId) {
  try {
    const bonus = await api(`/books/${bookId}/welcome-bonus?depth=${state.recapDepth}`);
    state.welcomeBonus = bonus.text;
  } catch (error) {
    state.welcomeBonus = "";
  }
}

async function readChunk(bookId, chunkIndex = state.currentChunkIndex, options = {}) {
  const safeIndex = Math.max(0, Math.min(chunkIndex, Math.max(0, state.totalChunks - 1)));
  const cacheKey = cacheKeyFor(bookId, safeIndex);
  const cached = options.trackActivity ? null : state.chunkCache.get(cacheKey);
  const activityParam = options.trackActivity ? "&track_activity=true" : "";
  const data = cached || (await api(`/books/${bookId}/read?chunk_index=${safeIndex}${activityParam}`));

  state.chunkCache.set(cacheKey, data);
  state.activeBook = data.book;
  state.currentChunk = data.chunk;
  state.currentChunkIndex = data.current_chunk_index;
  state.totalChunks = data.total_chunks;
  if (data.streak) handleStreakStatus(data.streak);

  if (!shouldUseVisualReaderPages()) {
    resetReaderPages();
  }
  renderReader();
  preloadAdjacentChunks(bookId, state.currentChunkIndex);
}

function resetReaderPages() {
  state.readerPages = [];
  state.readerLoadedChunks = [];
  state.readerPageCursor = 0;
  state.readerBufferedFromChunkIndex = null;
  state.readerBufferedUntilChunkIndex = -1;
  state.readerPrefetchPromise = null;
  state.readerLayoutVersion += 1;
}

function preloadAdjacentChunks(bookId, currentIndex) {
  [currentIndex - 1, currentIndex + 1].forEach((index) => {
    if (index < 0 || index >= state.totalChunks) return;
    const key = cacheKeyFor(bookId, index);
    if (state.chunkCache.has(key)) return;
    api(`/books/${bookId}/read?chunk_index=${index}`)
      .then((data) => state.chunkCache.set(key, data))
      .catch(() => {});
  });
}

function cacheKeyFor(bookId, index) {
  return `${bookId}:${index}`;
}

async function uploadBook() {
  if (state.isUploading) return;
  const file = els.bookFile.files?.[0];
  if (!file) {
    showNotice(t("uploadNoFile"));
    return;
  }

  const form = new FormData();
  form.append("file", file);
  if (els.bookTitle.value.trim()) {
    form.append("title", els.bookTitle.value.trim());
  }

  try {
    setUploadProgress(0, true);
    state.isUploading = true;
    els.uploadBook.disabled = true;
    const book = await uploadBookWithProgress(form);
    setUploadProgress(100, true);
    els.bookFile.value = "";
    els.bookTitle.value = "";
    showUploadedBook(book);
    state.chunkCache.clear();
    await loadBooks();
    await openBook(book.id, { switchToReader: true });
    addActivity(t("addedBook", { title: formatBookTitle(book.title) }));
  } finally {
    state.isUploading = false;
    els.uploadBook.disabled = false;
    window.setTimeout(() => setUploadProgress(0, false), 700);
  }
}

function uploadBookWithProgress(form) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();
    request.open("POST", "/books/upload");
    for (const [key, value] of Object.entries(authHeaders())) {
      request.setRequestHeader(key, value);
    }

    request.upload.addEventListener("progress", (event) => {
      if (!event.lengthComputable) {
        setUploadProgress(12, true);
        return;
      }
      const percent = Math.min(96, Math.round((event.loaded / event.total) * 100));
      setUploadProgress(percent, true);
    });

    request.addEventListener("load", () => {
      if (request.status >= 200 && request.status < 300) {
        try {
          resolve(JSON.parse(request.responseText));
        } catch (error) {
          reject(new Error(t("invalidUploadResponse")));
        }
        return;
      }
      reject(new Error(request.responseText || `Request failed: ${request.status}`));
    });
    request.addEventListener("error", () => reject(new Error(t("uploadFailed"))));
    request.addEventListener("abort", () => reject(new Error(t("uploadAborted"))));
    request.send(form);
  });
}

function setUploadProgress(percent, visible) {
  state.uploadProgress = Math.max(0, Math.min(100, percent));
  els.uploadProgress.classList.toggle("hidden", !visible);
  els.uploadProgressFill.style.width = `${state.uploadProgress}%`;
  els.uploadProgressValue.textContent = `${state.uploadProgress}%`;
}

function loadReaderSettings() {
  try {
    const saved = JSON.parse(localStorage.getItem("adhdReader.readerSettings") || "{}");
    state.readerSettings.fontStep = Number.isFinite(saved.fontStep) ? saved.fontStep : 0;
    state.readerSettings.theme = ["dark", "black", "sepia"].includes(saved.theme) ? saved.theme : "dark";
    state.readerSettings.mode = "page";
    state.readerSettings.showZones = Boolean(saved.showZones);
  } catch (error) {
    state.readerSettings = { fontStep: 0, theme: "dark", mode: "page", showZones: false };
  }
  applyReaderSettings();
}

function saveReaderSettings() {
  localStorage.setItem("adhdReader.readerSettings", JSON.stringify(state.readerSettings));
}

function applyReaderSettings() {
  const fontStep = Math.max(-2, Math.min(3, state.readerSettings.fontStep));
  state.readerSettings.fontStep = fontStep;
  state.readerSettings.mode = "page";
  document.documentElement.style.setProperty("--reader-font-adjust", `${fontStep}px`);
  document.body.classList.toggle("reader-theme-black", state.readerSettings.theme === "black");
  document.body.classList.toggle("reader-theme-sepia", state.readerSettings.theme === "sepia");
  document.body.classList.toggle("reader-theme-dark", state.readerSettings.theme === "dark");
  document.body.classList.toggle("reader-page-mode", state.readerSettings.mode === "page");
  document.body.classList.toggle("reader-chunk-mode", state.readerSettings.mode === "chunk");
  document.body.classList.toggle("reader-zones-visible", state.readerSettings.showZones);
  const themeKey = {
    dark: "readerThemeDark",
    black: "readerThemeBlack",
    sepia: "readerThemeSepia",
  }[state.readerSettings.theme];
  els.readerThemeToggle.textContent = t(themeKey);
  els.readerModeToggle.textContent = t(state.readerSettings.mode === "page" ? "readerModePage" : "readerModeChunk");
  els.readerZonesToggle.textContent = t(state.readerSettings.showZones ? "readerZonesOff" : "readerZones");
}

function changeReaderFont(delta) {
  state.readerSettings.fontStep = Math.max(-2, Math.min(3, state.readerSettings.fontStep + delta));
  applyReaderSettings();
  saveReaderSettings();
  resetReaderPages();
  updateImmersiveReaderText({ forceRebuild: true }).catch((error) => showNotice(error.message));
  revealReaderOverlay();
}

function cycleReaderTheme() {
  const themes = ["dark", "black", "sepia"];
  const index = themes.indexOf(state.readerSettings.theme);
  state.readerSettings.theme = themes[(index + 1) % themes.length];
  applyReaderSettings();
  saveReaderSettings();
  resetReaderPages();
  updateImmersiveReaderText({ forceRebuild: true }).catch((error) => showNotice(error.message));
  revealReaderOverlay();
}

async function toggleReaderMode() {
  state.readerSettings.mode = "page";
  applyReaderSettings();
  saveReaderSettings();
  resetReaderPages();
  if (state.activeBook) {
    await updateImmersiveReaderText();
    renderReaderProgressMini(state.totalChunks ? ((state.currentChunkIndex + 1) / state.totalChunks) * 100 : 0);
  }
  revealReaderOverlay();
}

function openClassicReadMode() {
  if (!state.activeBook) {
    showNotice(t("chooseBookNotice"));
    return;
  }
  state.readerSettings.mode = "page";
  applyReaderSettings();
  saveReaderSettings();
  setFocusMode(true);
}

function toggleReaderZones() {
  state.readerSettings.showZones = !state.readerSettings.showZones;
  applyReaderSettings();
  saveReaderSettings();
  revealReaderOverlay();
}

async function moveReaderPage(delta) {
  await ensureReaderPages();
  if (!state.readerPages.length) return;

  const nextCursor = state.readerPageCursor + delta;
  if (nextCursor < 0) {
    const firstLoadedChunk = state.readerBufferedFromChunkIndex ?? state.readerPages[0].startChunkIndex;
    const previousChunk = Math.max(0, firstLoadedChunk - state.readerRangeSize);
    if (previousChunk === firstLoadedChunk) return;
    const firstVisibleChunk = state.readerPages[0].startChunkIndex;
    await loadReaderPageRange(previousChunk);
    const oldFirstCursor = state.readerPages.findIndex((page) => page.startChunkIndex >= firstVisibleChunk);
    showReaderPage(Math.max(0, oldFirstCursor - 1));
    return;
  }

  if (nextCursor >= state.readerPages.length) {
    await prefetchReaderPages();
    if (nextCursor >= state.readerPages.length) return;
  }

  showReaderPage(nextCursor);
  if (state.readerPages.length - state.readerPageCursor <= state.readerPrefetchThreshold) {
    prefetchReaderPages().catch(() => {});
  }
}

async function ensureReaderPages() {
  if (state.readerSettings.mode !== "page" || !state.activeBook) return;
  await waitForReaderLayout();
  if (state.readerPages.length) {
    showReaderPage(state.readerPageCursor);
    return;
  }

  const startIndex = Math.max(0, state.currentChunkIndex);
  await loadReaderPageRange(startIndex);
  showReaderPage(state.readerPageCursor);
  prefetchReaderPages().catch(() => {});
}

async function prefetchReaderPages() {
  if (!state.activeBook || state.readerPrefetchPromise) {
    return state.readerPrefetchPromise;
  }
  if (state.readerBufferedFromChunkIndex === null || state.readerBufferedUntilChunkIndex < 0) return null;
  if (state.readerBufferedUntilChunkIndex >= state.totalChunks - 1) return null;
  const nextStart = Math.max(0, state.readerBufferedUntilChunkIndex + 1);
  state.readerPrefetchPromise = loadReaderPageRange(nextStart, { appendOnly: true }).finally(() => {
    state.readerPrefetchPromise = null;
  });
  return state.readerPrefetchPromise;
}

async function loadReaderPageRange(startChunkIndex, options = {}) {
  const anchor = getCurrentReaderPageAnchor();
  const layoutVersion = state.readerLayoutVersion;
  const data = await api(
    `/books/${state.activeBook.id}/read-range?start_chunk_index=${startChunkIndex}&limit=${state.readerRangeSize}`,
  );
  if (layoutVersion !== state.readerLayoutVersion) return;
  const chunks = data.chunks || [];
  if (!chunks.length) return;
  chunks.forEach((chunk) => {
    state.chunkCache.set(cacheKeyFor(state.activeBook.id, chunk.chunk_index), {
      book: data.book,
      chunk,
      current_chunk_index: chunk.chunk_index,
      total_chunks: data.total_chunks,
      has_previous: chunk.chunk_index > 0,
      has_next: chunk.chunk_index < data.total_chunks - 1,
    });
  });
  mergeReaderLoadedChunks(chunks);
  if (options.appendOnly && state.readerPages.length) {
    state.readerPages.push(...paginateReaderChunks(chunks));
    state.readerPageCursor = findReaderPageCursor(anchor);
  } else {
    rebuildReaderPages(anchor);
  }
  state.readerBufferedFromChunkIndex =
    state.readerBufferedFromChunkIndex === null
      ? data.start_chunk_index
      : Math.min(state.readerBufferedFromChunkIndex, data.start_chunk_index);
  state.readerBufferedUntilChunkIndex = Math.max(state.readerBufferedUntilChunkIndex, data.end_chunk_index);
}

function mergeReaderLoadedChunks(chunks) {
  const byIndex = new Map(state.readerLoadedChunks.map((chunk) => [chunk.chunk_index, chunk]));
  chunks.forEach((chunk) => byIndex.set(chunk.chunk_index, chunk));
  state.readerLoadedChunks = Array.from(byIndex.values()).sort((a, b) => a.chunk_index - b.chunk_index);
}

function rebuildReaderPages(anchor = getCurrentReaderPageAnchor()) {
  state.readerPages = paginateReaderChunks(state.readerLoadedChunks);
  state.readerPageCursor = findReaderPageCursor(anchor);
}

function paginateReaderChunks(chunks) {
  const metrics = getReaderVisualMetrics();
  const pages = [];
  const current = createEmptyReaderPage();

  chunks.forEach((chunk) => {
    getChunkParagraphs(chunk).forEach((block) => {
      appendParagraphToReaderPages(block, chunk.chunk_index, current, pages, metrics);
    });
  });

  commitReaderPage(current, pages);
  return pages;
}

function getChunkParagraphs(chunk) {
  const text = (chunk.text || "").replace(/\r\n?/g, "\n").trim();
  if (!text) return [];
  return text
    .split(/\n\s*\n/g)
    .flatMap((paragraph) => splitReaderStructuralBlocks(paragraph))
    .map((paragraph) => ({ text: paragraph, continuation: false, chapter: isReaderChapterHeading(paragraph) }));
}

function normalizeReaderParagraph(text) {
  return String(text || "")
    .replace(/[ \t]*\n[ \t]*/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function splitReaderStructuralBlocks(paragraph) {
  const blocks = [];
  const buffer = [];
  String(paragraph || "")
    .split(/\n+/g)
    .forEach((line) => {
      const clean = normalizeReaderParagraph(line);
      if (!clean) return;
      if (isReaderChapterHeading(clean)) {
        flushReaderLineBuffer(blocks, buffer);
        blocks.push(clean);
      } else {
        buffer.push(clean);
      }
    });
  flushReaderLineBuffer(blocks, buffer);
  return blocks;
}

function flushReaderLineBuffer(blocks, buffer) {
  if (!buffer.length) return;
  const value = normalizeReaderParagraph(buffer.join(" "));
  if (value) blocks.push(value);
  buffer.length = 0;
}

function createEmptyReaderPage() {
  return {
    blocks: [],
    startChunkIndex: null,
    endChunkIndex: null,
  };
}

function appendParagraphToReaderPages(block, chunkIndex, current, pages, metrics) {
  if (!block?.text) return;
  if (block.chapter && current.blocks.length) {
    commitReaderPage(current, pages);
  }

  const candidate = [...current.blocks, block];
  if (readerTextFits(candidate, metrics)) {
    addBlockToReaderPage(current, block, chunkIndex);
    return;
  }

  if (current.blocks.length) {
    if (isReaderHeadingOnlyPage(current)) {
      appendLongParagraphByWords(block.text, chunkIndex, current, pages, metrics);
      return;
    }
    commitReaderPage(current, pages);
  }

  if (readerTextFits([block], metrics)) {
    addBlockToReaderPage(current, block, chunkIndex);
    return;
  }

  appendLongParagraphByWords(block.text, chunkIndex, current, pages, metrics);
}

function appendLongParagraphByWords(paragraph, chunkIndex, current, pages, metrics) {
  let words = paragraph.split(/\s+/u).filter(Boolean);
  let isContinuation = false;
  while (words.length) {
    const count = findFittingWordCount(words, current.blocks, isContinuation, metrics);
    if (count === 0) {
      if (current.blocks.length) {
        commitReaderPage(current, pages);
        continue;
      }
      addBlockToReaderPage(current, { text: words.shift(), continuation: isContinuation }, chunkIndex);
      commitReaderPage(current, pages);
      isContinuation = true;
      continue;
    }

    addBlockToReaderPage(current, { text: words.slice(0, count).join(" "), continuation: isContinuation }, chunkIndex);
    words = words.slice(count);
    if (words.length) {
      commitReaderPage(current, pages);
      isContinuation = true;
    }
  }
}

function isReaderChapterHeading(text) {
  const value = normalizeReaderParagraph(text);
  if (!value) return false;
  const words = value.split(/\s+/u);
  if (words.length > 14 || value.length > 110) return false;
  if (
    /^(?:глава|розділ|раздел|част[ьи]?|частина|книга|chapter|part|book)(?:\s|$|[.:№-])/iu.test(value) ||
    /^(?:пролог|епілог|эпилог|вступ|передмова|предисловие|послесловие)(?:\s|$|[.:№-])/iu.test(value) ||
    /^(?:ch\.?|ч\.)\s*[\divxlcdm]+(?:\s|$|[.)])/iu.test(value)
  ) {
    return true;
  }
  if (words.length <= 2 && /^(?:[ivxlcdm]+|\d{1,4})(?:[.)])?$/iu.test(value)) {
    return true;
  }
  if (words.length <= 8 && !/[.!?…:;,]$/u.test(value)) {
    const letters = Array.from(value.matchAll(/[^\W\d_]/gu), (match) => match[0]);
    const uppercase = letters.filter((letter) => letter.toUpperCase() === letter && letter.toLowerCase() !== letter);
    return Boolean(letters.length && uppercase.length / letters.length >= 0.72);
  }
  return false;
}

function isReaderHeadingOnlyPage(page) {
  return page.blocks.length === 1 && page.blocks[0]?.chapter;
}

function findFittingWordCount(words, currentBlocks, continuation, metrics) {
  let low = 1;
  let high = words.length;
  let best = 0;

  while (low <= high) {
    const mid = Math.floor((low + high) / 2);
    const candidate = [...currentBlocks, { text: words.slice(0, mid).join(" "), continuation }];
    if (readerTextFits(candidate, metrics)) {
      best = mid;
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }

  return best;
}

function addBlockToReaderPage(page, block, chunkIndex) {
  if (page.startChunkIndex === null) page.startChunkIndex = chunkIndex;
  page.endChunkIndex = chunkIndex;
  page.blocks.push(block);
}

function commitReaderPage(page, pages) {
  if (!page.blocks.length) return;
  pages.push({
    blocks: page.blocks.map((block) => ({ ...block })),
    text: blocksToReaderText(page.blocks),
    startChunkIndex: page.startChunkIndex,
    endChunkIndex: page.endChunkIndex,
  });
  page.blocks = [];
  page.startChunkIndex = null;
  page.endChunkIndex = null;
}

function blocksToReaderText(blocks) {
  return blocks.map((block) => block.text).join("\n\n");
}

function getReaderVisualMetrics() {
  if (!els.chunkText || !els.chunkTextValue) {
    return { width: Math.max(260, window.innerWidth - 44), height: Math.max(320, window.innerHeight - 160) };
  }

  const containerStyle = window.getComputedStyle(els.chunkText);
  const textStyle = window.getComputedStyle(els.chunkTextValue);
  const paddingX = parseCssPixels(containerStyle.paddingLeft) + parseCssPixels(containerStyle.paddingRight);
  const paddingY = parseCssPixels(containerStyle.paddingTop) + parseCssPixels(containerStyle.paddingBottom);
  const contentWidth = Math.max(120, els.chunkText.clientWidth - paddingX);
  const contentHeight = Math.max(80, els.chunkText.clientHeight - paddingY);
  const maxTextWidth = parseCssPixels(textStyle.maxWidth, contentWidth);
  const width = Math.max(120, Math.min(contentWidth, maxTextWidth));

  return {
    width,
    height: contentHeight,
  };
}

function parseCssPixels(value, fallback = 0) {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function readerTextFits(text, metrics) {
  const measure = getReaderMeasure();
  measure.root.style.width = `${metrics.width}px`;
  measure.content.style.width = `${metrics.width}px`;
  renderReaderBlocks(measure.content, Array.isArray(text) ? text : [{ text: text || " ", continuation: false }]);
  return measure.content.scrollHeight <= metrics.height + 1;
}

function getReaderMeasure() {
  if (state.readerMeasure) return state.readerMeasure;

  const root = document.createElement("article");
  root.className = "chunk-text reader-pagination-measure";
  const content = document.createElement("div");
  content.className = "reader-page-content";
  root.append(content);
  document.body.append(root);
  state.readerMeasure = { root, content };
  return state.readerMeasure;
}

function getCurrentReaderPageAnchor() {
  const page = state.readerPages[state.readerPageCursor];
  if (!page) {
    return {
      chunkIndex: state.currentChunkIndex,
      textStart: "",
    };
  }
  return {
    chunkIndex: page.startChunkIndex,
    textStart: page.text.slice(0, 80),
  };
}

function findReaderPageCursor(anchor) {
  if (!state.readerPages.length) return 0;
  if (!anchor) return 0;

  const exact = state.readerPages.findIndex(
    (page) => page.startChunkIndex === anchor.chunkIndex && page.text.startsWith(anchor.textStart),
  );
  if (exact >= 0) return exact;

  const containing = state.readerPages.findIndex(
    (page) => page.startChunkIndex <= anchor.chunkIndex && page.endChunkIndex >= anchor.chunkIndex,
  );
  return containing >= 0 ? containing : 0;
}

function scheduleReaderRepagination(delay = 140) {
  if (state.readerReflowTimer) {
    window.clearTimeout(state.readerReflowTimer);
    state.readerReflowTimer = null;
  }
  if (!shouldUseVisualReaderPages()) return;

  state.readerReflowTimer = window.setTimeout(() => {
    state.readerReflowTimer = null;
    repaginateLoadedReaderPages().catch((error) => showNotice(error.message));
  }, delay);
}

async function repaginateLoadedReaderPages() {
  if (!shouldUseVisualReaderPages()) return;
  if (!state.readerLoadedChunks.length) {
    resetReaderPages();
    await ensureReaderPages();
    return;
  }

  const anchor = getCurrentReaderPageAnchor();
  rebuildReaderPages(anchor);
  showReaderPage(state.readerPageCursor);
}

function shouldUseVisualReaderPages() {
  return document.body.classList.contains("focus-mode") && state.readerSettings.mode === "page" && Boolean(state.activeBook);
}

function waitForReaderLayout() {
  return new Promise((resolve) => {
    window.requestAnimationFrame(() => window.requestAnimationFrame(resolve));
  });
}

function showReaderPage(cursor) {
  const page = state.readerPages[cursor];
  if (!page) return;
  state.readerPageCursor = cursor;
  state.currentChunkIndex = page.startChunkIndex;
  const cachedStart = state.chunkCache.get(cacheKeyFor(state.activeBook.id, page.startChunkIndex));
  if (cachedStart?.chunk) {
    state.currentChunk = cachedStart.chunk;
  }
  renderReaderBlocks(els.chunkTextValue, page.blocks || [{ text: page.text || "", continuation: false }]);
  const progress = state.totalChunks ? ((page.endChunkIndex + 1) / state.totalChunks) * 100 : 0;
  els.progressMeta.textContent = state.totalChunks ? `${page.startChunkIndex + 1} / ${state.totalChunks}` : "0 / 0";
  els.progressFill.style.width = `${Math.max(0, Math.min(100, progress))}%`;
  els.tapPreviousChunk.disabled = cursor <= 0 && (state.readerBufferedFromChunkIndex ?? 0) <= 0;
  els.tapNextChunk.disabled = cursor >= state.readerPages.length - 1 && state.readerBufferedUntilChunkIndex >= state.totalChunks - 1;
  renderReaderProgressMini(progress);
  preloadAdjacentChunks(state.activeBook.id, page.endChunkIndex);
}

function renderReaderBlocks(container, blocks) {
  container.replaceChildren();
  blocks.forEach((block) => {
    if (!block?.text) return;
    const paragraph = document.createElement("p");
    paragraph.className = "reader-paragraph";
    paragraph.classList.toggle("continuation", Boolean(block.continuation));
    paragraph.classList.toggle("chapter", Boolean(block.chapter));
    renderReaderInlineText(paragraph, block.text);
    container.append(paragraph);
  });
}

function renderReaderInlineText(container, text) {
  const value = String(text || "");
  const footnotePattern = /\[(\d{1,4})\]/gu;
  let cursor = 0;
  for (const match of value.matchAll(footnotePattern)) {
    if (match.index > cursor) {
      container.append(document.createTextNode(value.slice(cursor, match.index)));
    }
    const button = document.createElement("button");
    button.type = "button";
    button.className = "footnote-link";
    button.textContent = match[0];
    button.addEventListener("click", (event) => {
      event.stopPropagation();
      showBookNote(match[1]).catch((error) => showNotice(error.message));
    });
    container.append(button);
    cursor = match.index + match[0].length;
  }
  if (cursor < value.length) {
    container.append(document.createTextNode(value.slice(cursor)));
  }
}

async function showBookNote(marker) {
  if (!state.activeBook) return;
  const note = await api(`/books/${state.activeBook.id}/notes/${encodeURIComponent(marker)}`);
  showNotice(`Сноска [${note.marker}]\n\n${note.text}`);
}

function renderPlainReaderText(text) {
  const blocks = String(text || t("readerEmpty"))
    .replace(/\r\n?/g, "\n")
    .split(/\n\s*\n/g)
    .flatMap((paragraph) => splitReaderStructuralBlocks(paragraph))
    .map((paragraph) => ({ text: paragraph, continuation: false, chapter: isReaderChapterHeading(paragraph) }));
  renderReaderBlocks(els.chunkTextValue, blocks.length ? blocks : [{ text: t("readerEmpty"), continuation: false }]);
}

async function moveChunk(delta) {
  if (!state.activeBook) {
    navigate("library");
    return;
  }
  if (document.body.classList.contains("focus-mode") && state.readerSettings.mode === "page") {
    await moveReaderPage(delta);
    return;
  }
  const nextIndex = Math.max(0, Math.min(state.totalChunks - 1, state.currentChunkIndex + delta));
  if (nextIndex === state.currentChunkIndex) return;
  await readChunk(state.activeBook.id, nextIndex, { trackActivity: true });
}

async function saveProgress() {
  if (!state.activeBook) {
    showNotice(t("chooseBookNotice"));
    return;
  }

  await api(`/books/${state.activeBook.id}/progress`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      current_chunk_index: state.currentChunkIndex,
      chunks_read: 0,
      words_read: 0,
    }),
  });

  state.stats.savedChunks += 1;
  addActivity(t("savedPlace", { title: formatBookTitle(state.activeBook.title), chunk: state.currentChunkIndex + 1 }));
  renderProgress();

  if (isBookFinished()) {
    showNotice(t("finishedBook"));
  } else {
    showNotice(t("savedNotice"));
  }
  setFocusMode(false);
  navigate("home");
}

async function startSession(minutes = 3) {
  if (!state.activeBook) {
    navigate("library");
    showNotice(t("chooseBookNotice"));
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
  state.stats.sessions += 1;
  await loadStreak({ celebrate: true });
  addActivity(t("sessionStarted", { minutes }));
  navigate("reader");
  openClassicReadMode();
  renderProgress();
  showNotice(t("sessionNotice", { minutes }));
}

function handleStreakStatus(streak) {
  const previousCompleted = state.streakStatus?.completed_today;
  state.streakStatus = streak;
  renderProgress();
  if (streak.just_completed_today && !previousCompleted) {
    showStreakCelebration(streak.streak_days);
  }
}

function showStreakCelebration(days) {
  if (!els.streakToast) return;
  els.streakToastText.textContent = `${t("streakDone")} · ${t("streakDays", { count: days })}`;
  els.streakToast.classList.remove("hidden");
  els.streakToast.classList.remove("play");
  void els.streakToast.offsetWidth;
  els.streakToast.classList.add("play");
  window.setTimeout(() => els.streakToast.classList.add("hidden"), 2600);
}

function setLoadingVisible(visible) {
  if (!els.appLoading) return;
  els.appLoading.classList.toggle("is-hidden", !visible);
  if (!visible) {
    window.setTimeout(() => els.appLoading.classList.add("hidden"), 360);
  } else {
    els.appLoading.classList.remove("hidden");
  }
}

async function changeDepth(depth) {
  state.recapDepth = depth;
  els.depthButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.depth === depth);
  });
  if (state.activeBook) {
    await loadWelcomeBonus(state.activeBook.id);
    renderWelcome();
  }
}

function renderAll() {
  renderHome();
  renderLibrary();
  renderReader();
  renderProgress();
  renderSettings();
}

function renderHome() {
  const book = state.activeBook;
  els.continueTitle.textContent = book ? formatBookTitle(book.title) : t("noBookTitle");
  els.continueMeta.textContent = book
    ? t("continueMeta", { current: state.currentChunkIndex + 1, total: state.totalChunks || book.total_chunks })
    : t("noBookMeta");
  els.continueReading.disabled = !book;
  els.quickSession.disabled = !book;

  renderWelcome();
  renderBookCollection(els.recentBooks, state.books.slice(0, 6), true);
}

function renderWelcome() {
  const hasBonus = Boolean(state.welcomeBonus);
  els.welcomePreviewCard.classList.toggle("hidden", !hasBonus);
  if (!hasBonus) {
    els.welcomeBonus.classList.add("hidden");
  }
  els.toggleWelcomeBonus.disabled = !hasBonus;
  if (hasBonus) {
    els.welcomePreview.textContent = state.welcomeBonus;
    els.welcomeBonusText.textContent = state.welcomeBonus;
  }
}

function renderLibrary() {
  els.bookCount.textContent = String(state.books.length);
  renderBookCollection(els.booksList, state.books, false);
}

function renderBookCollection(container, books, compact) {
  container.innerHTML = "";
  if (!books.length) {
    const empty = document.createElement("div");
    empty.className = "activity-item";
    empty.textContent = t("emptyLibrary");
    container.append(empty);
    return;
  }

  books.forEach((book) => {
    const item = document.createElement(compact ? "button" : "article");
    item.className = `book-card ${state.activeBook?.id === book.id ? "active" : ""}`;
    const cover = document.createElement("span");
    cover.className = "book-cover";
    if (isRenderableCoverUrl(book.cover_image_data_url)) {
      const image = document.createElement("img");
      image.alt = "";
      image.addEventListener("error", () => {
        image.remove();
        cover.textContent = getBookCoverFallback(book);
      });
      try {
        image.src = book.cover_image_data_url;
      } catch (error) {
        cover.textContent = getBookCoverFallback(book);
      }
      cover.append(image);
    } else {
      cover.textContent = getBookCoverFallback(book);
    }

    const copy = document.createElement("span");
    copy.className = "book-copy";
    const title = document.createElement("span");
    title.className = "book-title";
    title.textContent = formatBookTitle(book.title);
    const subtitle = document.createElement("span");
    subtitle.className = "book-subtitle";
    subtitle.textContent = compact ? getCompactBookMeta(book) : getLibraryBookMeta(book);
    copy.append(title, subtitle);
    if (compact) {
      item.append(cover, copy);
      item.addEventListener("click", () => openBook(book.id, { switchToReader: true }).catch((error) => showNotice(error.message)));
    } else {
      const openButton = document.createElement("button");
      openButton.className = "book-card-main";
      openButton.type = "button";
      openButton.append(cover, copy);
      openButton.addEventListener("click", () => openBook(book.id, { switchToReader: true }).catch((error) => showNotice(error.message)));
      const editButton = document.createElement("button");
      editButton.className = "book-edit-button";
      editButton.type = "button";
      editButton.textContent = "✎";
      editButton.title = t("editBook");
      editButton.setAttribute("aria-label", t("editBook"));
      editButton.addEventListener("click", () => openEditBook(book));
      item.append(openButton, editButton);
    }
    container.append(item);
  });
}

function openEditBook(book) {
  state.editBook = book;
  els.editBookHeading.textContent = formatBookTitle(book.title);
  els.editTitle.value = book.title || "";
  els.editAuthor.value = book.author || "";
  els.editCover.value = "";
  els.editRemoveCover.checked = false;
  if (typeof els.editBookDialog.showModal === "function") {
    els.editBookDialog.showModal();
  } else {
    els.editBookDialog.setAttribute("open", "");
  }
}

function closeEditBook() {
  state.editBook = null;
  if (typeof els.editBookDialog.close === "function") {
    els.editBookDialog.close();
  } else {
    els.editBookDialog.removeAttribute("open");
  }
}

async function saveBookEdit(event) {
  event.preventDefault();
  if (!state.editBook || state.isEditingBook) return;
  const form = new FormData();
  form.append("title", els.editTitle.value.trim());
  form.append("author", els.editAuthor.value.trim());
  form.append("remove_cover", els.editRemoveCover.checked ? "true" : "false");
  if (els.editCover.files?.[0]) {
    form.append("cover", els.editCover.files[0]);
  }

  state.isEditingBook = true;
  els.saveBookEdit.disabled = true;
  try {
    const updated = await apiForm(`/books/${state.editBook.id}`, form, { method: "PATCH" });
    state.books = state.books.map((book) => (book.id === updated.id ? updated : book));
    if (state.activeBook?.id === updated.id) state.activeBook = updated;
    renderAll();
    closeEditBook();
    showNotice(t("bookUpdated"));
  } finally {
    state.isEditingBook = false;
    els.saveBookEdit.disabled = false;
  }
}

function getBookCoverFallback(book) {
  return formatBookTitle(book.title).slice(0, 1).toUpperCase() || "B";
}

function isRenderableCoverUrl(value) {
  if (!value || typeof value !== "string") return false;
  const trimmed = value.trim();
  if (trimmed.startsWith("data:image/")) {
    return /^data:image\/(?:png|jpe?g|webp|gif|svg\+xml);base64,[a-z0-9+/=\s]+$/i.test(trimmed);
  }
  if (trimmed.startsWith("https://")) {
    try {
      new URL(trimmed);
      return true;
    } catch (error) {
      return false;
    }
  }
  return false;
}

function renderReader() {
  const book = state.activeBook;
  els.bookMeta.textContent = book ? formatBookTitle(book.title) : t("chooseBook");
  els.progressMeta.textContent = state.totalChunks ? `${state.currentChunkIndex + 1} / ${state.totalChunks}` : "0 / 0";
  if (!shouldUseVisualReaderPages() || !state.readerPages.length) {
    renderPlainReaderText(state.currentChunk?.text || t("readerEmpty"));
  }

  const progress = state.totalChunks ? ((state.currentChunkIndex + 1) / state.totalChunks) * 100 : 0;
  els.progressFill.style.width = `${Math.max(0, Math.min(100, progress))}%`;
  renderReaderProgressMini(progress);
  els.tapPreviousChunk.disabled = !book || state.currentChunkIndex <= 0;
  els.tapNextChunk.disabled = !book || state.currentChunkIndex >= state.totalChunks - 1;
  els.chunkPreviousButton.disabled = !book || state.currentChunkIndex <= 0;
  els.chunkNextButton.disabled = !book || state.currentChunkIndex >= state.totalChunks - 1;
  els.saveStop.disabled = !book;
  els.readerSearchButton.disabled = !book;
  els.classicReadModeButton.disabled = !book;
  renderWelcome();
  renderSearchResults();
  if (document.body.classList.contains("focus-mode")) {
    updateImmersiveReaderText().catch((error) => showNotice(error.message));
  }
}

function renderReaderProgressMini(progress) {
  if (state.readerSettings.mode === "page" && state.totalChunks) {
    els.readerProgressText.textContent = t("readerVisualProgress", {
      page: state.readerPageCursor + 1,
      loaded: Math.max(1, state.readerPages.length),
      chunk: state.currentChunkIndex + 1,
      total: state.totalChunks,
    });
  } else {
    els.readerProgressText.textContent = state.totalChunks ? `${state.currentChunkIndex + 1} / ${state.totalChunks}` : "0 / 0";
  }
  els.readerProgressMiniFill.style.width = `${Math.max(0, Math.min(100, progress))}%`;
}

async function updateImmersiveReaderText(options = {}) {
  if (!document.body.classList.contains("focus-mode") || !state.activeBook || !state.currentChunk) return;
  if (state.readerSettings.mode === "chunk") {
    renderPlainReaderText(state.currentChunk.text || t("readerEmpty"));
    return;
  }

  if (options.forceRebuild) {
    resetReaderPages();
  }
  await ensureReaderPages();
}

function showUploadedBook(book) {
  if (!els.uploadStatus) return;
  els.uploadStatus.innerHTML = `
    <span>${t("uploaded")}</span>
    <strong></strong>
    <small></small>
  `;
  els.uploadStatus.querySelector("strong").textContent = formatBookTitle(book.title);
  els.uploadStatus.querySelector("small").textContent = t("compactBookMeta", {
    author: book.author || t("authorUnknown"),
    chunks: book.total_chunks,
  });
  els.uploadStatus.classList.remove("hidden");
}

function renderProgress() {
  const streakDays = state.streakStatus?.streak_days || state.currentUser?.gentle_streak_days || 0;
  els.streakValue.textContent = streakDays === 1 ? t("streakOne") : streakDays ? t("streakDays", { count: streakDays }) : t("streakZero");
  els.sessionsValue.textContent = String(state.stats.sessions);
  els.chunksValue.textContent = String(Math.max(state.currentChunkIndex + (state.activeBook ? 1 : 0), state.stats.savedChunks));
  renderWeekStreak();

  els.activityList.innerHTML = "";
  const activity = state.activity.slice(0, 5);
  if (!activity.length) {
    const empty = document.createElement("div");
    empty.className = "activity-item";
    empty.textContent = t("activityEmpty");
    els.activityList.append(empty);
    return;
  }
  activity.forEach((text) => {
    const item = document.createElement("div");
    item.className = "activity-item";
    item.textContent = text;
    els.activityList.append(item);
  });
}

function renderWeekStreak() {
  const labels = t("weekDays");
  const today = new Date();
  const mondayBasedDay = (today.getDay() + 6) % 7;
  els.weekStreak.innerHTML = "";
  labels.forEach((label, index) => {
    const item = document.createElement("span");
    item.className = "week-streak-day";
    item.classList.toggle("today", index === mondayBasedDay);
    item.classList.toggle("done", Boolean(state.streakStatus?.completed_today) && index === mondayBasedDay);
    item.textContent = label;
    els.weekStreak.append(item);
  });
}

function renderSettings() {
  if (!tg?.initDataUnsafe?.user) return;
  const user = tg.initDataUnsafe.user;
  els.telegramUserInfo.textContent = [user.first_name, user.last_name].filter(Boolean).join(" ") || user.username || `ID ${user.id}`;
}

function getCompactBookMeta(book) {
  return t("compactBookMeta", { author: book.author || t("authorUnknown"), chunks: book.total_chunks });
}

function getLibraryBookMeta(book) {
  if (state.activeBook?.id === book.id && state.totalChunks) {
    return t("libraryCurrentMeta", {
      author: book.author || t("authorUnknown"),
      current: state.currentChunkIndex + 1,
      total: state.totalChunks,
    });
  }
  return t("libraryBookMeta", { author: book.author || t("authorUnknown"), words: book.total_words });
}

function formatBookTitle(title) {
  let value = String(title || t("unnamedBook")).trim();
  value = value.replace(/\.(txt|epub|fb2|zip|docx?|rtf)$/gi, "");
  value = value.replace(/^microsoft\s+word\s*[-–—:]*\s*/i, "");
  value = value.replace(/_+/g, " ");
  value = value.replace(/^r[\s.-]+/i, "");
  value = value.replace(/\bfull\s*text\b/gi, "");
  value = value.replace(/\s+\d+\s*$/g, "");
  value = value.replace(/\s+/g, " ").trim().replace(/^[\s._-]+|[\s._-]+$/g, "");
  if (!value) return t("unnamedBook");
  if (/[A-Z]/.test(value) && value === value.toUpperCase()) {
    return value.toLowerCase().replace(/\b[a-z]/g, (letter) => letter.toUpperCase());
  }
  return value;
}

async function searchInBook() {
  if (!state.activeBook) {
    showNotice(t("chooseBookNotice"));
    return;
  }
  const query = els.readerSearchInput.value.trim();
  if (!query) {
    state.searchResults = [];
    renderSearchResults();
    return;
  }
  const data = await api(`/books/${state.activeBook.id}/search?q=${encodeURIComponent(query)}`);
  state.searchResults = data.results || [];
  renderSearchResults();
}

function renderSearchResults() {
  if (!els.readerSearchResults) return;
  els.readerSearchResults.innerHTML = "";
  if (!state.searchResults.length) {
    els.readerSearchResults.classList.add("hidden");
    return;
  }
  state.searchResults.forEach((result) => {
    const item = document.createElement("button");
    item.className = "search-result";
    const meta = document.createElement("span");
    meta.className = "search-result-meta";
    meta.textContent = t("progressChunk", { page: result.page_number, words: result.word_count });
    const snippet = document.createElement("span");
    snippet.className = "search-result-snippet";
    snippet.textContent = result.snippet;
    item.append(meta, snippet);
    item.addEventListener("click", () => {
      readChunk(state.activeBook.id, result.chunk_index, { trackActivity: true }).catch((error) => showNotice(error.message));
      state.searchResults = [];
      renderSearchResults();
    });
    els.readerSearchResults.append(item);
  });
  els.readerSearchResults.classList.remove("hidden");
}

function addActivity(text) {
  state.activity.unshift(text);
}

function isBookFinished() {
  return state.activeBook && state.totalChunks > 0 && state.currentChunkIndex >= state.totalChunks - 1;
}

function showNotice(message) {
  if (tg?.showAlert) {
    tg.showAlert(message);
  } else {
    window.alert(message);
  }
}

function bindEvents() {
  els.refreshBooks.addEventListener("click", () => loadBooks().catch((error) => showNotice(error.message)));
  els.uploadBook.addEventListener("click", () => uploadBook().catch((error) => showNotice(error.message)));
  els.bookFile.addEventListener("change", () => {
    if (els.bookFile.files?.[0]) {
      els.uploadStatus.innerHTML = `<span>${t("selectedFile")}</span><strong>${formatBookTitle(els.bookFile.files[0].name)}</strong><small>${t("selectedFileHint")}</small>`;
      els.uploadStatus.classList.remove("hidden");
    }
  });
  els.readerSearchButton.addEventListener("click", () => searchInBook().catch((error) => showNotice(error.message)));
  els.readerSearchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      searchInBook().catch((error) => showNotice(error.message));
    }
  });
  els.continueReading.addEventListener("click", () => {
    if (state.activeBook) {
      readChunk(state.activeBook.id, state.currentChunkIndex, { trackActivity: true })
        .then(() => {
          navigate("reader");
          openClassicReadMode();
        })
        .catch((error) => showNotice(error.message));
    }
  });
  els.quickSession.addEventListener("click", () => startSession(3).catch((error) => showNotice(error.message)));
  els.tapPreviousChunk.addEventListener("click", () => moveChunk(-1).catch((error) => showNotice(error.message)));
  els.tapNextChunk.addEventListener("click", () => moveChunk(1).catch((error) => showNotice(error.message)));
  els.chunkPreviousButton.addEventListener("click", () => moveChunk(-1).catch((error) => showNotice(error.message)));
  els.chunkNextButton.addEventListener("click", () => moveChunk(1).catch((error) => showNotice(error.message)));
  els.toggleReaderOverlay.addEventListener("click", () => toggleReaderOverlay());
  els.saveStop.addEventListener("click", () => saveProgress().catch((error) => showNotice(error.message)));
  els.classicReadModeButton.addEventListener("click", () => {
    openClassicReadMode();
  });
  els.exitFocusMode.addEventListener("click", () => {
    setFocusMode(false);
  });
  els.overlayExit.addEventListener("click", () => {
    setFocusMode(false);
  });
  els.overlaySave.addEventListener("click", () => saveProgress().catch((error) => showNotice(error.message)));
  els.readerFontDown.addEventListener("click", () => changeReaderFont(-1));
  els.readerFontUp.addEventListener("click", () => changeReaderFont(1));
  els.readerThemeToggle.addEventListener("click", () => cycleReaderTheme());
  els.readerModeToggle.addEventListener("click", () => toggleReaderMode().catch((error) => showNotice(error.message)));
  els.readerZonesToggle.addEventListener("click", () => toggleReaderZones());
  els.toggleWelcomeBonus.addEventListener("click", () => {
    if (state.welcomeBonus) els.welcomeBonus.classList.toggle("hidden");
  });
  els.closeWelcomeBonus.addEventListener("click", () => {
    els.welcomeBonus.classList.add("hidden");
  });
  els.editBookForm.addEventListener("submit", (event) => saveBookEdit(event).catch((error) => showNotice(error.message)));
  els.closeEditBook.addEventListener("click", closeEditBook);
  els.cancelEditBook.addEventListener("click", closeEditBook);
  els.editBookDialog.addEventListener("click", (event) => {
    if (event.target === els.editBookDialog) closeEditBook();
  });

  els.navItems.forEach((button) => {
    button.addEventListener("click", () => navigate(button.dataset.screenTarget));
  });
  els.screenLinks.forEach((button) => {
    button.addEventListener("click", () => navigate(button.dataset.goScreen));
  });
  els.depthButtons.forEach((button) => {
    button.addEventListener("click", () => changeDepth(button.dataset.depth).catch((error) => showNotice(error.message)));
  });
  els.languageOptions.forEach((button) => {
    button.addEventListener("click", () => saveLanguage(button.dataset.language).catch((error) => showNotice(error.message)));
  });

  window.addEventListener("resize", syncViewportHeight);
  window.addEventListener("orientationchange", () => scheduleReaderRepagination(240));
  window.addEventListener("keydown", (event) => {
    if (!document.body.classList.contains("focus-mode")) return;
    if (event.key === "ArrowLeft") moveChunk(-1).catch((error) => showNotice(error.message));
    if (event.key === "ArrowRight") moveChunk(1).catch((error) => showNotice(error.message));
    if (event.key === "Escape") setFocusMode(false);
  });
  els.screens.forEach((screen) => {
    screen.addEventListener("scroll", syncHeaderState, { passive: true });
  });
  bindReaderSwipe();
}

function syncHeaderState() {
  const activeScreen = document.querySelector(".screen.active");
  const scrolled = Boolean(activeScreen && activeScreen.scrollTop > 18);
  els.topbar.classList.toggle("is-condensed", scrolled);
}

function bindReaderSwipe() {
  let startX = 0;
  let startY = 0;
  els.chunkText.addEventListener(
    "touchstart",
    (event) => {
      if (!document.body.classList.contains("focus-mode")) return;
      const touch = event.changedTouches[0];
      startX = touch.clientX;
      startY = touch.clientY;
    },
    { passive: true },
  );
  els.chunkText.addEventListener(
    "touchend",
    (event) => {
      if (!document.body.classList.contains("focus-mode")) return;
      const touch = event.changedTouches[0];
      const deltaX = touch.clientX - startX;
      const deltaY = touch.clientY - startY;
      if (Math.abs(deltaX) < 48 || Math.abs(deltaX) < Math.abs(deltaY) * 1.4) return;
      moveChunk(deltaX < 0 ? 1 : -1).catch((error) => showNotice(error.message));
    },
    { passive: true },
  );
}

function toggleReaderOverlay() {
  if (!document.body.classList.contains("focus-mode")) return;
  setReaderOverlayVisible(!state.readerControlsVisible);
}

function revealReaderOverlay(delay = 2600) {
  if (!document.body.classList.contains("focus-mode")) return;
  setReaderOverlayVisible(true, delay);
}

function setReaderOverlayVisible(visible, delay = 0) {
  state.readerControlsVisible = visible;
  const inFocusMode = document.body.classList.contains("focus-mode");
  els.readerOverlay.classList.toggle("hidden", !inFocusMode && !visible);
  if (inFocusMode) {
    els.readerOverlay.classList.remove("hidden");
  }
  document.body.classList.toggle("reader-controls-visible", visible);
  if (state.readerOverlayTimer) {
    window.clearTimeout(state.readerOverlayTimer);
    state.readerOverlayTimer = null;
  }
  if (visible && delay) {
    state.readerOverlayTimer = window.setTimeout(() => setReaderOverlayVisible(false), delay);
  }
}

function setFocusMode(enabled) {
  els.classicReadModeButton.classList.toggle("active", enabled);
  els.classicReadModeButton.setAttribute("aria-pressed", enabled ? "true" : "false");
  document.body.classList.toggle("focus-mode", enabled);
  els.exitFocusMode.classList.toggle("hidden", !enabled);
  if (enabled) {
    navigate("reader");
    els.welcomeBonus.classList.add("hidden");
    applyReaderSettings();
    syncViewportHeight();
    syncSafeArea();
    updateImmersiveReaderText({ forceRebuild: true }).catch((error) => showNotice(error.message));
    revealReaderOverlay(2600);
  } else {
    setReaderOverlayVisible(false);
  }
  syncViewportHeight();
}

async function init() {
  setupTelegram();
  loadReaderSettings();
  bindEvents();
  setLoadingVisible(true);
  await loadCurrentUser();
  navigate("home");
  await loadStreak();
  await loadBooks();
}

init()
  .catch((error) => showNotice(error.message))
  .finally(() => setLoadingVisible(false));
