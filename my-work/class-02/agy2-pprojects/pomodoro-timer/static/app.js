/* ==========================================================================
   ZenFlow Pomodoro - Client Application Script
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  // ------------------------------------------------------------------------
  // State Management
  // ------------------------------------------------------------------------
  const state = {
    mode: "work", // 'work', 'short_break', 'long_break'
    timeLeft: 25 * 60,
    totalTime: 25 * 60,
    isRunning: false,
    timerId: null,
    workSessionCount: 0,
    activeTaskId: null,
    taskFilter: "all",
    
    // User Settings (defaults)
    settings: {
      work_duration: 25,
      short_break_duration: 5,
      long_break_duration: 15,
      auto_start_breaks: false,
      auto_start_pomodoros: false,
      theme: "sage"
    },

    // Audio Engine State
    audioCtx: null,
    activeSounds: {
      rain: { node: null, gain: null, playing: false, vol: 0.5 },
      waves: { node: null, gain: null, playing: false, vol: 0.5 },
      wind: { node: null, gain: null, playing: false, vol: 0.5 }
    }
  };

  // ------------------------------------------------------------------------
  // DOM Elements
  // ------------------------------------------------------------------------
  const el = {
    // Theme & Header
    html: document.documentElement,
    themeBtns: document.querySelectorAll(".theme-btn"),
    openStatsBtn: document.getElementById("open-stats-btn"),
    openSettingsBtn: document.getElementById("open-settings-btn"),

    // Timer Card
    tabWork: document.getElementById("tab-work"),
    tabShortBreak: document.getElementById("tab-short-break"),
    tabLongBreak: document.getElementById("tab-long-break"),
    timeDisplay: document.getElementById("time-display"),
    sessionTag: document.getElementById("session-tag"),
    progressCircle: document.getElementById("timer-progress-circle"),
    toggleBtn: document.getElementById("toggle-btn"),
    toggleBtnLabel: document.getElementById("toggle-btn-label"),
    playIcon: document.getElementById("play-icon"),
    pauseIcon: document.getElementById("pause-icon"),
    resetBtn: document.getElementById("reset-btn"),
    skipBtn: document.getElementById("skip-btn"),

    // Active Task Ribbon
    activeTaskRibbon: document.getElementById("active-task-ribbon"),
    activeTaskTitle: document.getElementById("active-task-title"),
    clearActiveTaskBtn: document.getElementById("clear-active-task"),

    // Ambient Sounds
    testChimeBtn: document.getElementById("test-chime-btn"),
    soundRainBtn: document.getElementById("sound-rain-btn"),
    soundRainVol: document.getElementById("sound-rain-vol"),
    soundWavesBtn: document.getElementById("sound-waves-btn"),
    soundWavesVol: document.getElementById("sound-waves-vol"),
    soundWindBtn: document.getElementById("sound-wind-btn"),
    soundWindVol: document.getElementById("sound-wind-vol"),

    // Stats Overview
    statTodayMins: document.getElementById("stat-today-mins"),
    statTodaySessions: document.getElementById("stat-today-sessions"),
    statCompletedTasks: document.getElementById("stat-completed-tasks"),

    // Task Manager
    addTaskForm: document.getElementById("add-task-form"),
    taskInputTitle: document.getElementById("task-input-title"),
    taskInputCategory: document.getElementById("task-input-category"),
    taskInputEst: document.getElementById("task-input-est"),
    taskList: document.getElementById("task-list"),
    filterBtns: document.querySelectorAll(".filter-btn"),

    // Modals
    settingsDialog: document.getElementById("settings-dialog"),
    closeSettingsBtn: document.getElementById("close-settings-btn"),
    cancelSettingsBtn: document.getElementById("cancel-settings-btn"),
    settingsForm: document.getElementById("settings-form"),
    settingWork: document.getElementById("setting-work"),
    settingShortBreak: document.getElementById("setting-short-break"),
    settingLongBreak: document.getElementById("setting-long-break"),
    settingAutoBreaks: document.getElementById("setting-auto-breaks"),
    settingAutoPomo: document.getElementById("setting-auto-pomo"),

    statsDialog: document.getElementById("stats-dialog"),
    closeStatsBtn: document.getElementById("close-stats-btn"),
    modalTodayMins: document.getElementById("modal-stat-today-mins"),
    modalTodaySessions: document.getElementById("modal-stat-today-sessions"),
    modalTotalMins: document.getElementById("modal-stat-total-mins"),
    modalCompletedTasks: document.getElementById("modal-stat-completed-tasks"),
    weeklyChart: document.getElementById("weekly-chart")
  };

  // Circle circumference: 2 * PI * 120 = ~753.98
  const CIRCUMFERENCE = 2 * Math.PI * 120;

  // ------------------------------------------------------------------------
  // Web Audio API Ambient Sound Generator
  // ------------------------------------------------------------------------
  function getAudioContext() {
    if (!state.audioCtx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      state.audioCtx = new AudioCtx();
    }
    if (state.audioCtx.state === "suspended") {
      state.audioCtx.resume();
    }
    return state.audioCtx;
  }

  // Tibetan Bell Chime Notification
  function playBellChime() {
    try {
      const ctx = getAudioContext();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(528, ctx.currentTime); // 528 Hz Solfeggio frequency

      gain.gain.setValueAtTime(0, ctx.currentTime);
      gain.gain.linearRampToValueAtTime(0.4, ctx.currentTime + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 3.0);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 3.1);
    } catch (e) {
      console.warn("Audio chime playback error:", e);
    }
  }

  // Generates 5 seconds of pink noise buffer
  function createNoiseBuffer(ctx) {
    const bufferSize = ctx.sampleRate * 5;
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      b3 = 0.86650 * b3 + white * 0.3104856;
      b4 = 0.55000 * b4 + white * 0.5329522;
      b5 = -0.7616 * b5 - white * 0.0168980;
      data[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362;
      data[i] *= 0.11; // scale
      b6 = white * 0.115926;
    }
    return buffer;
  }

  function toggleSound(soundName) {
    const ctx = getAudioContext();
    const sound = state.activeSounds[soundName];

    if (sound.playing) {
      // Stop sound
      if (sound.gain) {
        sound.gain.gain.linearRampToValueAtTime(0.001, ctx.currentTime + 0.4);
        setTimeout(() => {
          if (sound.node) sound.node.stop();
          sound.playing = false;
          updateSoundUI(soundName);
        }, 400);
      }
    } else {
      // Start sound
      const buffer = createNoiseBuffer(ctx);
      const source = ctx.createBufferSource();
      source.buffer = buffer;
      source.loop = true;

      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();

      if (soundName === "rain") {
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(1000, ctx.currentTime);
      } else if (soundName === "waves") {
        filter.type = "bandpass";
        filter.frequency.setValueAtTime(400, ctx.currentTime);
        filter.Q.setValueAtTime(1.0, ctx.currentTime);
        // LFO for wave modulation
        const lfo = ctx.createOscillator();
        lfo.frequency.setValueAtTime(0.12, ctx.currentTime);
        const lfoGain = ctx.createGain();
        lfoGain.gain.setValueAtTime(250, ctx.currentTime);
        lfo.connect(lfoGain);
        lfoGain.connect(filter.frequency);
        lfo.start();
      } else if (soundName === "wind") {
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(600, ctx.currentTime);
      }

      gain.gain.setValueAtTime(0.001, ctx.currentTime);
      gain.gain.linearRampToValueAtTime(sound.vol, ctx.currentTime + 0.6);

      source.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);

      source.start();
      sound.node = source;
      sound.gain = gain;
      sound.playing = true;
      updateSoundUI(soundName);
    }
  }

  function updateSoundUI(soundName) {
    const btn = document.querySelector(`.sound-toggle-btn[data-sound="${soundName}"]`);
    if (btn) {
      if (state.activeSounds[soundName].playing) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    }
  }

  function setSoundVolume(soundName, val) {
    const vol = val / 100;
    state.activeSounds[soundName].vol = vol;
    if (state.activeSounds[soundName].playing && state.activeSounds[soundName].gain) {
      const ctx = getAudioContext();
      state.activeSounds[soundName].gain.gain.setValueAtTime(vol, ctx.currentTime);
    }
  }

  // ------------------------------------------------------------------------
  // Timer Logic
  // ------------------------------------------------------------------------
  function setMode(mode) {
    state.mode = mode;
    state.isRunning = false;
    clearInterval(state.timerId);

    // Update Mode Tab UI
    [el.tabWork, el.tabShortBreak, el.tabLongBreak].forEach(tab => tab.classList.remove("active"));
    if (mode === "work") el.tabWork.classList.add("active");
    if (mode === "short_break") el.tabShortBreak.classList.add("active");
    if (mode === "long_break") el.tabLongBreak.classList.add("active");

    // Set duration
    if (mode === "work") {
      state.totalTime = parseInt(state.settings.work_duration, 10) * 60;
      el.sessionTag.textContent = `Focus Session #${state.workSessionCount + 1}`;
    } else if (mode === "short_break") {
      state.totalTime = parseInt(state.settings.short_break_duration, 10) * 60;
      el.sessionTag.textContent = "Short Break";
    } else if (mode === "long_break") {
      state.totalTime = parseInt(state.settings.long_break_duration, 10) * 60;
      el.sessionTag.textContent = "Long Break";
    }

    state.timeLeft = state.totalTime;
    updateTimerUI();
  }

  function toggleTimer() {
    if (state.isRunning) {
      pauseTimer();
    } else {
      startTimer();
    }
  }

  function startTimer() {
    state.isRunning = true;
    updateControlsUI();
    getAudioContext(); // Resume audio context if needed

    state.timerId = setInterval(() => {
      state.timeLeft--;
      updateTimerUI();

      if (state.timeLeft <= 0) {
        onTimerComplete();
      }
    }, 1000);
  }

  function pauseTimer() {
    state.isRunning = false;
    clearInterval(state.timerId);
    updateControlsUI();
  }

  function resetTimer() {
    pauseTimer();
    state.timeLeft = state.totalTime;
    updateTimerUI();
  }

  function skipTimer() {
    pauseTimer();
    if (confirm("Skip this current session?")) {
      advanceSessionMode();
    }
  }

  function onTimerComplete() {
    pauseTimer();
    playBellChime();

    // Log session to backend
    const durationMinutes = Math.round(state.totalTime / 60);
    const activeTask = state.activeTaskId;

    fetch("/api/sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode: state.mode,
        duration_minutes: durationMinutes,
        task_id: activeTask
      })
    }).then(() => {
      loadStats();
      loadTasks();
    });

    if (state.mode === "work") {
      state.workSessionCount++;
    }

    advanceSessionMode(true);
  }

  function advanceSessionMode(autoStartTriggered = false) {
    if (state.mode === "work") {
      if (state.workSessionCount % 4 === 0 && state.workSessionCount > 0) {
        setMode("long_break");
      } else {
        setMode("short_break");
      }
      if (autoStartTriggered && state.settings.auto_start_breaks) {
        startTimer();
      }
    } else {
      setMode("work");
      if (autoStartTriggered && state.settings.auto_start_pomodoros) {
        startTimer();
      }
    }
  }

  function updateTimerUI() {
    const minutes = Math.floor(state.timeLeft / 60);
    const seconds = state.timeLeft % 60;
    const formatted = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

    el.timeDisplay.textContent = formatted;
    document.title = `${formatted} - ${state.mode === "work" ? "Focus" : "Break"} | ZenFlow`;

    // SVG Ring Progress
    const progressFraction = state.timeLeft / state.totalTime;
    const offset = CIRCUMFERENCE * (1 - progressFraction);
    el.progressCircle.style.strokeDasharray = CIRCUMFERENCE;
    el.progressCircle.style.strokeDashoffset = offset;
  }

  function updateControlsUI() {
    if (state.isRunning) {
      el.playIcon.classList.add("hidden");
      el.pauseIcon.classList.remove("hidden");
      el.toggleBtnLabel.textContent = "Pause";
      el.toggleBtn.classList.remove("btn-primary");
      el.toggleBtn.classList.add("btn-secondary");
    } else {
      el.playIcon.classList.remove("hidden");
      el.pauseIcon.classList.add("hidden");
      el.toggleBtnLabel.textContent = state.mode === "work" ? "Start Focus" : "Start Break";
      el.toggleBtn.classList.remove("btn-secondary");
      el.toggleBtn.classList.add("btn-primary");
    }
  }

  // ------------------------------------------------------------------------
  // Task Manager REST API Integration
  // ------------------------------------------------------------------------
  function loadTasks() {
    fetch("/api/tasks")
      .then(res => res.json())
      .then(tasks => renderTaskList(tasks))
      .catch(err => console.error("Error fetching tasks:", err));
  }

  function renderTaskList(tasks) {
    el.taskList.innerHTML = "";

    const filtered = tasks.filter(task => {
      if (state.taskFilter === "pending") return task.status !== "completed";
      if (state.taskFilter === "completed") return task.status === "completed";
      return true;
    });

    if (filtered.length === 0) {
      el.taskList.innerHTML = `<li class="task-item" style="justify-content: center; color: var(--text-secondary); font-size: 0.88rem;">No objectives found. Add one above!</li>`;
      return;
    }

    filtered.forEach(task => {
      const li = document.createElement("li");
      li.className = `task-item ${task.status === "completed" ? "completed" : ""}`;

      const isCurrentActive = state.activeTaskId === task.id;

      li.innerHTML = `
        <div class="task-item-left">
          <input type="checkbox" class="task-checkbox" ${task.status === "completed" ? "checked" : ""} data-id="${task.id}" />
          <div class="task-details">
            <span class="task-title">${escapeHtml(task.title)}</span>
            <div class="task-meta">
              <span class="category-tag">${escapeHtml(task.category)}</span>
              <span>🍅 ${task.completed_pomodoros}/${task.est_pomodoros}</span>
            </div>
          </div>
        </div>
        <div class="task-actions">
          ${
            task.status !== "completed"
              ? `<button class="btn btn-secondary btn-activate-task ${isCurrentActive ? "btn-primary" : ""}" data-id="${task.id}">
                  ${isCurrentActive ? "Active" : "Set Active"}
                </button>`
              : ""
          }
          <button class="btn-delete-task" data-id="${task.id}" title="Delete task">&times;</button>
        </div>
      `;

      el.taskList.appendChild(li);
    });
  }

  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
  }

  el.addTaskForm.addEventListener("submit", e => {
    e.preventDefault();
    const title = el.taskInputTitle.value.trim();
    const category = el.taskInputCategory.value;
    const est = parseInt(el.taskInputEst.value, 10) || 1;

    if (!title) return;

    fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, category, est_pomodoros: est })
    })
      .then(res => res.json())
      .then(newTask => {
        el.taskInputTitle.value = "";
        loadTasks();
      });
  });

  el.taskList.addEventListener("click", e => {
    const target = e.target;
    
    // Toggle completion
    if (target.classList.contains("task-checkbox")) {
      const id = target.dataset.id;
      const status = target.checked ? "completed" : "pending";
      fetch(`/api/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
      }).then(() => {
        loadTasks();
        loadStats();
      });
    }

    // Activate task for timer
    if (target.classList.contains("btn-activate-task")) {
      const id = parseInt(target.dataset.id, 10);
      setActiveTask(id);
    }

    // Delete task
    if (target.classList.contains("btn-delete-task")) {
      const id = target.dataset.id;
      fetch(`/api/tasks/${id}`, { method: "DELETE" }).then(() => {
        if (state.activeTaskId === parseInt(id, 10)) {
          clearActiveTask();
        }
        loadTasks();
      });
    }
  });

  function setActiveTask(taskId) {
    fetch("/api/tasks")
      .then(res => res.json())
      .then(tasks => {
        const task = tasks.find(t => t.id === taskId);
        if (task) {
          state.activeTaskId = task.id;
          el.activeTaskTitle.textContent = `Focusing on: ${task.title}`;
          el.activeTaskRibbon.classList.remove("hidden");
          loadTasks();
        }
      });
  }

  function clearActiveTask() {
    state.activeTaskId = null;
    el.activeTaskRibbon.classList.add("hidden");
    loadTasks();
  }

  el.clearActiveTaskBtn.addEventListener("click", clearActiveTask);

  // Filter Buttons
  el.filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      el.filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.taskFilter = btn.dataset.filter;
      loadTasks();
    });
  });

  // ------------------------------------------------------------------------
  // Stats & Analytics
  // ------------------------------------------------------------------------
  function loadStats() {
    fetch("/api/stats")
      .then(res => res.json())
      .then(stats => {
        el.statTodayMins.textContent = `${stats.today_minutes}m`;
        el.statTodaySessions.textContent = stats.today_sessions;
        el.statCompletedTasks.textContent = stats.completed_tasks;

        el.modalTodayMins.textContent = stats.today_minutes;
        el.modalTodaySessions.textContent = stats.today_sessions;
        el.modalTotalMins.textContent = stats.total_minutes;
        el.modalCompletedTasks.textContent = stats.completed_tasks;

        renderWeeklyChart(stats.weekly_history);
      });
  }

  function renderWeeklyChart(weeklyHistory) {
    el.weeklyChart.innerHTML = "";

    // Generate last 7 days labels
    const days = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];
      const dayLabel = d.toLocaleDateString("en-US", { weekday: "short" });
      days.push({ dateStr, dayLabel, minutes: 0 });
    }

    // Merge history
    weeklyHistory.forEach(h => {
      const found = days.find(d => d.dateStr === h.date);
      if (found) found.minutes = h.minutes;
    });

    const maxMins = Math.max(60, ...days.map(d => d.minutes));

    days.forEach(d => {
      const heightPercent = (d.minutes / maxMins) * 100;
      const col = document.createElement("div");
      col.className = "chart-bar-col";
      col.innerHTML = `
        <div class="chart-bar" style="height: ${Math.max(4, heightPercent)}%;" title="${d.minutes} mins"></div>
        <span class="chart-label">${d.dayLabel}</span>
      `;
      el.weeklyChart.appendChild(col);
    });
  }

  // ------------------------------------------------------------------------
  // Settings & Theme
  // ------------------------------------------------------------------------
  function loadSettings() {
    fetch("/api/settings")
      .then(res => res.json())
      .then(settings => {
        state.settings = { ...state.settings, ...settings };
        
        // Theme
        setTheme(state.settings.theme || "sage");

        // Form fields
        el.settingWork.value = state.settings.work_duration;
        el.settingShortBreak.value = state.settings.short_break_duration;
        el.settingLongBreak.value = state.settings.long_break_duration;
        el.settingAutoBreaks.checked = state.settings.auto_start_breaks === "true" || state.settings.auto_start_breaks === true;
        el.settingAutoPomo.checked = state.settings.auto_start_pomodoros === "true" || state.settings.auto_start_pomodoros === true;

        setMode(state.mode);
      });
  }

  function setTheme(themeName) {
    state.settings.theme = themeName;
    el.html.setAttribute("data-theme", themeName);
    el.themeBtns.forEach(btn => {
      btn.classList.toggle("active", btn.dataset.theme === themeName);
    });
  }

  el.themeBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const theme = btn.dataset.theme;
      setTheme(theme);
      saveSettingsToServer({ theme });
    });
  });

  function saveSettingsToServer(newSettings) {
    state.settings = { ...state.settings, ...newSettings };
    fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ settings: newSettings })
    });
  }

  // ------------------------------------------------------------------------
  // Modal Handlers
  // ------------------------------------------------------------------------
  el.openSettingsBtn.addEventListener("click", () => el.settingsDialog.showModal());
  el.closeSettingsBtn.addEventListener("click", () => el.settingsDialog.close());
  el.cancelSettingsBtn.addEventListener("click", () => el.settingsDialog.close());

  el.settingsForm.addEventListener("submit", e => {
    e.preventDefault();
    const updated = {
      work_duration: el.settingWork.value,
      short_break_duration: el.settingShortBreak.value,
      long_break_duration: el.settingLongBreak.value,
      auto_start_breaks: el.settingAutoBreaks.checked ? "true" : "false",
      auto_start_pomodoros: el.settingAutoPomo.checked ? "true" : "false"
    };

    saveSettingsToServer(updated);
    el.settingsDialog.close();
    setMode(state.mode);
  });

  el.openStatsBtn.addEventListener("click", () => {
    loadStats();
    el.statsDialog.showModal();
  });
  el.closeStatsBtn.addEventListener("click", () => el.statsDialog.close());

  // ------------------------------------------------------------------------
  // Event Listeners Initialization
  // ------------------------------------------------------------------------
  el.tabWork.addEventListener("click", () => setMode("work"));
  el.tabShortBreak.addEventListener("click", () => setMode("short_break"));
  el.tabLongBreak.addEventListener("click", () => setMode("long_break"));

  el.toggleBtn.addEventListener("click", toggleTimer);
  el.resetBtn.addEventListener("click", resetTimer);
  el.skipBtn.addEventListener("click", skipTimer);

  // Sound listeners
  el.testChimeBtn.addEventListener("click", playBellChime);
  
  [
    { btn: el.soundRainBtn, vol: el.soundRainVol, name: "rain" },
    { btn: el.soundWavesBtn, vol: el.soundWavesVol, name: "waves" },
    { btn: el.soundWindBtn, vol: el.soundWindVol, name: "wind" }
  ].forEach(item => {
    item.btn.addEventListener("click", () => toggleSound(item.name));
    item.vol.addEventListener("input", e => setSoundVolume(item.name, e.target.value));
  });

  // Initial Load
  loadSettings();
  loadTasks();
  loadStats();
});
