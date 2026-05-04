// Use Railway backend (much faster and more reliable than serverless)
const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://life-tracker-backend.up.railway.app'; // UPDATE with your Railway URL

// View management
const views = ['today', 'week', 'goals', 'bucket'];
let currentView = 'today';
let allTasks = [];
let allGoals = [];

// Navigation
document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const view = tab.dataset.view;
        switchView(view);
    });
});

function switchView(view) {
    if (!views.includes(view)) return;

    currentView = view;

    // Update nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.view === view);
    });

    // Update views
    document.querySelectorAll('.view').forEach(v => {
        v.classList.toggle('active', v.id === `${view}-view`);
    });

    // Load data for the view
    loadViewData(view);
}

async function loadViewData(view) {
    switch(view) {
        case 'today':
            await loadTodayTasks();
            break;
        case 'week':
            await loadWeekTasks();
            break;
        case 'goals':
            await loadGoals();
            break;
        case 'bucket':
            await loadBucket();
            break;
    }
}

// Today View
async function loadTodayTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks?urgency_bucket=today&completed=false`);
        const tasks = await response.json();

        renderTodayTasks(tasks);
    } catch (error) {
        console.error('Error loading today tasks:', error);
        document.getElementById('today-tasks').innerHTML =
            '<div class="empty-state"><div class="empty-state-icon">⚠️</div><div class="empty-state-text">Unable to load tasks</div></div>';
    }
}

function renderTodayTasks(tasks) {
    const container = document.getElementById('today-tasks');

    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">✨</div>
                <div class="empty-state-text">No tasks for today yet!</div>
                <p style="margin-top: 12px; color: #6c757d;">Add tasks from the Week or Bucket views.</p>
            </div>
        `;
        return;
    }

    // Limit to 5 tasks
    const displayTasks = tasks.slice(0, 5);

    container.innerHTML = displayTasks.map(task => `
        <div class="task-card ${task.completed ? 'completed' : ''}" data-id="${task.id}">
            <div class="task-header">
                <div class="task-title">${task.title}</div>
            </div>
            <div class="task-meta">
                <span class="task-badge task-category">${task.category}</span>
                ${task.loose_deadline ? `<span class="task-deadline">⏰ ${task.loose_deadline}</span>` : ''}
            </div>
            <div class="task-actions" style="margin-top: 12px;">
                <button class="btn-small btn-complete" onclick="completeTask('${task.id}')">
                    ✓ Complete
                </button>
            </div>
        </div>
    `).join('');

    if (tasks.length > 5) {
        container.innerHTML += `
            <div style="text-align: center; padding: 20px; color: #6c757d; font-weight: 500;">
                + ${tasks.length - 5} more tasks in the queue
            </div>
        `;
    }
}

// Week View
async function loadWeekTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks?completed=false`);
        allTasks = await response.json();

        renderWeekTasks(allTasks);
    } catch (error) {
        console.error('Error loading week tasks:', error);
        document.getElementById('week-tasks').innerHTML =
            '<div class="empty-state"><div class="empty-state-icon">⚠️</div><div class="empty-state-text">Unable to load tasks</div></div>';
    }
}

function renderWeekTasks(tasks) {
    const container = document.getElementById('week-tasks');

    const urgencyBuckets = {
        'today': { icon: '🔥', title: 'Today', tasks: [] },
        'this_week': { icon: '📅', title: 'This Week', tasks: [] },
        'this_month': { icon: '📆', title: 'This Month', tasks: [] },
        'bucket': { icon: '🗂️', title: 'Someday', tasks: [] }
    };

    tasks.forEach(task => {
        if (urgencyBuckets[task.urgency_bucket]) {
            urgencyBuckets[task.urgency_bucket].tasks.push(task);
        }
    });

    container.innerHTML = Object.entries(urgencyBuckets)
        .filter(([_, data]) => data.tasks.length > 0)
        .map(([bucket, data]) => `
            <div class="urgency-section">
                <div class="urgency-header">
                    <span class="urgency-icon">${data.icon}</span>
                    <h2 class="urgency-title">${data.title}</h2>
                    <span class="urgency-count">${data.tasks.length}</span>
                </div>
                <div class="task-list">
                    ${data.tasks.map(task => `
                        <div class="task-card" data-id="${task.id}">
                            <div class="task-header">
                                <div class="task-title">${task.title}</div>
                            </div>
                            <div class="task-meta">
                                <span class="task-badge task-category">${task.category}</span>
                                ${task.loose_deadline ? `<span class="task-deadline">⏰ ${task.loose_deadline}</span>` : ''}
                            </div>
                            <div class="task-actions" style="margin-top: 12px;">
                                <button class="btn-small btn-complete" onclick="completeTask('${task.id}')">
                                    ✓ Complete
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');

    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🎉</div>
                <div class="empty-state-text">All caught up!</div>
                <p style="margin-top: 12px; color: #6c757d;">No tasks scheduled for the week.</p>
            </div>
        `;
    }
}

// Goals View
async function loadGoals() {
    try {
        const [goalsResponse, tasksResponse] = await Promise.all([
            fetch(`${API_BASE}/goals`),
            fetch(`${API_BASE}/tasks`)
        ]);

        allGoals = await goalsResponse.json();
        const allTasksData = await tasksResponse.json();

        renderGoals(allGoals, allTasksData);
    } catch (error) {
        console.error('Error loading goals:', error);
        document.getElementById('goals-grid').innerHTML =
            '<div class="empty-state"><div class="empty-state-icon">⚠️</div><div class="empty-state-text">Unable to load goals</div></div>';
    }
}

function renderGoals(goals, allTasksData) {
    const container = document.getElementById('goals-grid');

    if (goals.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <div class="empty-state-icon">🎯</div>
                <div class="empty-state-text">No goals yet</div>
                <p style="margin-top: 12px; color: #6c757d;">Capture a larger ambition to get started!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = goals.map(goal => {
        const linkedTasks = allTasksData.filter(t => t.linked_goal_id === goal.id);
        const incompleteTasks = linkedTasks.filter(t => !t.completed).slice(0, 3);

        return `
            <div class="goal-card">
                <div class="goal-header">
                    <h3 class="goal-title">${goal.title}</h3>
                    ${goal.description ? `<p class="goal-description">${goal.description}</p>` : ''}
                    <span class="task-badge task-category" style="margin-top: 8px;">${goal.category}</span>
                </div>

                <div class="progress-section">
                    <div class="progress-header">
                        <span>Progress</span>
                        <span>${Math.round(goal.progress)}%</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${goal.progress}%"></div>
                    </div>
                </div>

                ${incompleteTasks.length > 0 ? `
                    <div class="goal-tasks">
                        <div class="goal-tasks-title">Next Tasks</div>
                        ${incompleteTasks.map(task => `
                            <div class="mini-task">
                                <input type="checkbox" class="mini-task-checkbox"
                                    onchange="completeTask('${task.id}')"
                                    ${task.completed ? 'checked' : ''}>
                                <span>${task.title}</span>
                            </div>
                        `).join('')}
                    </div>
                ` : '<div style="margin-top: 20px; color: #6c757d; font-style: italic;">No tasks yet for this goal</div>'}
            </div>
        `;
    }).join('');
}

// Bucket View
async function loadBucket() {
    try {
        const response = await fetch(`${API_BASE}/tasks?urgency_bucket=bucket&completed=false`);
        const bucketTasks = await response.json();

        renderBucketFilters(bucketTasks);
        renderBucket(bucketTasks);
    } catch (error) {
        console.error('Error loading bucket:', error);
        document.getElementById('bucket-grid').innerHTML =
            '<div class="empty-state"><div class="empty-state-icon">⚠️</div><div class="empty-state-text">Unable to load bucket</div></div>';
    }
}

function renderBucketFilters(tasks) {
    const categories = [...new Set(tasks.map(t => t.category))];
    const container = document.getElementById('bucket-filters');

    container.innerHTML = `
        <button class="filter-btn active" data-filter="all">All (${tasks.length})</button>
        ${categories.map(cat => {
            const count = tasks.filter(t => t.category === cat).length;
            return `<button class="filter-btn" data-filter="${cat}">${cat} (${count})</button>`;
        }).join('')}
    `;

    container.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;
            const filteredTasks = filter === 'all' ? tasks : tasks.filter(t => t.category === filter);
            renderBucket(filteredTasks);
        });
    });
}

function renderBucket(tasks) {
    const container = document.getElementById('bucket-grid');

    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <div class="empty-state-icon">📦</div>
                <div class="empty-state-text">Bucket is empty</div>
                <p style="margin-top: 12px; color: #6c757d;">All your ideas are scheduled!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="bucket-item">
            <div class="bucket-item-title">${task.title}</div>
            <div class="task-meta">
                <span class="task-badge task-category">${task.category}</span>
            </div>
            <div class="bucket-item-actions">
                <button class="btn-promote" onclick="promoteTask('${task.id}', 'this_week')">
                    → This Week
                </button>
                <button class="btn-promote" onclick="promoteTask('${task.id}', 'today')">
                    🔥 Today
                </button>
            </div>
        </div>
    `).join('');
}

// Actions
async function completeTask(taskId) {
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}/complete`, {
            method: 'PATCH'
        });

        if (response.ok) {
            // Reload current view
            loadViewData(currentView);
        }
    } catch (error) {
        console.error('Error completing task:', error);
        alert('Failed to complete task');
    }
}

async function promoteTask(taskId, urgency) {
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ urgency_bucket: urgency })
        });

        if (response.ok) {
            loadViewData(currentView);
        }
    } catch (error) {
        console.error('Error promoting task:', error);
        alert('Failed to promote task');
    }
}

// Load initial view
loadViewData(currentView);

// Auto-refresh every 30 seconds
setInterval(() => {
    loadViewData(currentView);
}, 30000);
