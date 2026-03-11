const activeList = document.getElementById('activeTasks');
const doneList = document.getElementById('doneTasks');
const newInput = document.getElementById('newTaskInput');
const newDueDate = document.getElementById('newDueDate');
const addBtn = document.getElementById('addBtn');
const searchInput = document.getElementById('searchInput');
const sortButtons = document.querySelectorAll('[data-sort]');
const statusMessage = document.getElementById('statusMessage');

let tasks = [];
let searchQuery = '';
let currentSort = 'all';

const escapeHtml = value =>
  String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

function formatDueDate(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return '';
  const now = new Date();
  const diffDays = Math.ceil((date - now) / (1000 * 60 * 60 * 24));
  let badgeText = '';
  let badgeClass = 'future';

  if (diffDays < 0) {
    badgeText = 'Просрочено';
    badgeClass = 'overdue';
  } else if (diffDays === 0) {
    badgeText = 'Сегодня';
    badgeClass = 'today';
  } else if (diffDays <= 2) {
    badgeText = `Через ${diffDays} дн.`;
    badgeClass = 'soon';
  }

  const timeStr = date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return `
    <span class="due-badge ${badgeClass}">${badgeText}</span>
    <span class="due-date">${timeStr}</span>
  `;
}

function showStatus(text, isError = true) {
  if (!statusMessage) return;
  statusMessage.textContent = text;
  statusMessage.hidden = false;
  statusMessage.dataset.error = isError ? 'true' : 'false';
}

function hideStatus() {
  if (!statusMessage) return;
  statusMessage.hidden = true;
  statusMessage.textContent = '';
  delete statusMessage.dataset.error;
}

function lockUI() {
  addBtn.disabled = true;
  newInput.disabled = true;
  newDueDate.disabled = true;
  searchInput.disabled = true;
  sortButtons.forEach(button => {
    button.disabled = true;
  });
}

function unlockUI() {
  addBtn.disabled = false;
  newInput.disabled = false;
  newDueDate.disabled = false;
  searchInput.disabled = false;
  sortButtons.forEach(button => {
    button.disabled = false;
  });
}

async function authFetch(url, options = {}) {
  const response = await fetch(url, {
    credentials: 'include',
    ...options,
    headers: {
      ...(options.headers || {}),
    },
  });

  if (response.status === 401) {
    lockUI();
    showStatus('Авторизуйтесь через Google, чтобы управлять задачами');
    throw new Error('Unauthorized');
  }

  return response;
}

async function fetchTasks() {
  try {
    const response = await authFetch('/task/all');
    const data = await response.json();
    tasks = data;
    hideStatus();
    unlockUI();
    render();
  } catch (error) {
    console.error(error);
  }
}

function filterAndSortTasks() {
  const filtered = tasks.filter(task => {
    if (!searchQuery) return true;
    return task.name.toLowerCase().includes(searchQuery);
  });
  const sorted = [...filtered];

  if (currentSort === 'alpha') {
    sorted.sort((a, b) => a.name.localeCompare(b.name));
  } else if (currentSort === 'due') {
    sorted.sort((a, b) => {
      const aTime = a.due ? new Date(a.due).getTime() : Infinity;
      const bTime = b.due ? new Date(b.due).getTime() : Infinity;
      return aTime - bTime;
    });
  } else if (currentSort === 'date') {
    sorted.sort((a, b) => b.id - a.id);
  }

  return sorted;
}

function render() {
  const sorted = filterAndSortTasks();
  const active = sorted.filter(task => !task.done);
  const done = sorted.filter(task => task.done);

  activeList.innerHTML = '';
  doneList.innerHTML = '';

  if (active.length === 0) {
    activeList.innerHTML = '<div class="empty-message">Нет активных задач</div>';
  } else {
    active.forEach(task => activeList.appendChild(createTaskElement(task)));
  }

  if (done.length === 0) {
    doneList.innerHTML = '<div class="empty-message">Нет завершённых задач</div>';
  } else {
    done.forEach(task => doneList.appendChild(createTaskElement(task)));
  }
}

function createTaskElement(task) {
  const div = document.createElement('div');
  div.className = `task ${task.done ? 'done' : ''}`;
  div.dataset.id = task.id;
  const notesPreview = escapeHtml(task.notes_preview || 'Нет заметок').replace(/\n/g, '<br>');
  const dueHtml = task.due ? `<div class="due-wrapper">${formatDueDate(task.due)}</div>` : '';

  div.innerHTML = `
    <input type="checkbox" ${task.done ? 'checked' : ''}>
    <div class="task-content">
      <span class="task-text">${escapeHtml(task.name)}</span>
      ${dueHtml}
      <div class="notes-preview">${notesPreview}</div>
    </div>
    <span class="star ${task.favorite ? 'favorite' : ''}">★</span>
    <span class="delete">×</span>
  `;

  const checkbox = div.querySelector('input[type="checkbox"]');
  const content = div.querySelector('.task-content');
  const star = div.querySelector('.star');
  const deleteBtn = div.querySelector('.delete');
  const textSpan = div.querySelector('.task-text');

  checkbox.addEventListener('change', async () => {
    await updateTaskState(task.id, { done: checkbox.checked });
  });

  star.addEventListener('click', async () => {
    await updateTaskState(task.id, { favorite: !task.favorite });
  });

  deleteBtn.addEventListener('click', async () => {
    if (!confirm('Удалить задачу?')) return;
    await deleteTask(task.id);
  });

  content.addEventListener('click', e => {
    if (e.target.closest('.star') || e.target.closest('.delete')) return;
    window.location.href = `/notes/${task.id}`;
  });

  textSpan.addEventListener('dblclick', () => {
    if (div.classList.contains('editing-title')) return;
    div.classList.add('editing-title');
    const input = document.createElement('input');
    input.type = 'text';
    input.value = task.name;
    input.className = 'edit-input';
    textSpan.replaceWith(input);
    input.focus();
    input.select();

    const save = async () => {
      const newValue = input.value.trim();
      div.classList.remove('editing-title');
      input.replaceWith(textSpan);
      if (!newValue || newValue === task.name) {
        textSpan.textContent = task.name;
        return;
      }
      await updateTaskName(task.id, newValue);
    };

    input.onblur = save;
    input.onkeydown = event => {
      if (event.key === 'Enter') {
        event.preventDefault();
        save();
      }
      if (event.key === 'Escape') {
        div.classList.remove('editing-title');
        input.replaceWith(textSpan);
        textSpan.textContent = task.name;
      }
    };
  });

  return div;
}

async function addNewTask() {
  const text = newInput.value.trim();
  if (!text) return;
  const due = newDueDate.value ? new Date(newDueDate.value).toISOString() : null;

  try {
    const response = await authFetch('/task/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: text, due }),
    });
    const created = await response.json();
    tasks.unshift(created);
    newInput.value = '';
    newDueDate.value = '';
    hideStatus();
    render();
  } catch (error) {
    console.error(error);
    showStatus('Не удалось добавить задачу');
  }
}

async function updateTaskState(taskId, payload) {
  try {
    const response = await authFetch(`/task/${taskId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const updated = await response.json();
    tasks = tasks.map(task => (task.id === updated.id ? updated : task));
    hideStatus();
    render();
  } catch (error) {
    console.error(error);
    showStatus('Не удалось обновить задачу');
  }
}

async function deleteTask(taskId) {
  try {
    await authFetch(`/task/${taskId}`, {
      method: 'DELETE',
    });
    tasks = tasks.filter(task => task.id !== taskId);
    hideStatus();
    render();
  } catch (error) {
    console.error(error);
    showStatus('Не удалось удалить задачу');
  }
}

async function updateTaskName(taskId, name) {
  try {
    const response = await authFetch(`/task/${taskId}?name=${encodeURIComponent(name)}`, {
      method: 'PATCH',
    });
    const updated = await response.json();
    tasks = tasks.map(task => (task.id === updated.id ? updated : task));
    hideStatus();
    render();
  } catch (error) {
    console.error(error);
    showStatus('Не удалось переименовать задачу');
  }
}

addBtn.addEventListener('click', addNewTask);
newInput.addEventListener('keypress', event => {
  if (event.key === 'Enter') {
    event.preventDefault();
    addNewTask();
  }
});

searchInput.addEventListener('input', event => {
  searchQuery = event.target.value.toLowerCase();
  render();
});

sortButtons.forEach(button => {
  button.addEventListener('click', () => {
    currentSort = button.dataset.sort;
    sortButtons.forEach(btn => btn.classList.toggle('active', btn === button));
    render();
  });
});

lockUI();
fetchTasks();
