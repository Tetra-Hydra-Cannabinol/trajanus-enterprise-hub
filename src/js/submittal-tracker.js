/**
 * Submittal Tracker - QCM Submittal Tracking System
 * TASK-019A: Track submittals through review lifecycle
 *
 * @author Trajanus USA
 * @location Jacksonville, Florida
 */

// ============================================
// SUBMITTAL DATABASE
// ============================================

const submittalDB = {
    submittals: [],
    listeners: [],

    /**
     * Generate unique ID for submittal
     */
    generateId() {
        return 'SUB-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).substr(2, 4).toUpperCase();
    },

    /**
     * Generate sequential submittal number
     */
    generateNumber() {
        const count = this.submittals.length + 1;
        return 'SUB-' + count.toString().padStart(3, '0');
    },

    /**
     * Add new submittal
     * @param {Object} submittal - Submittal data
     * @returns {Object} Created submittal
     */
    add(submittal) {
        const newSubmittal = {
            id: this.generateId(),
            number: submittal.number || this.generateNumber(),
            title: submittal.title || 'Untitled Submittal',
            description: submittal.description || '',
            category: submittal.category || 'General',
            priority: submittal.priority || 'normal', // low, normal, high, urgent
            status: 'submitted',
            submittedDate: new Date().toISOString(),
            submittedBy: submittal.submittedBy || 'System User',
            dueDate: submittal.dueDate || null,
            reviewedDate: null,
            reviewer: null,
            approvedDate: null,
            approvedBy: null,
            comments: [],
            attachments: submittal.attachments || [],
            checklist: submittal.checklist || {},
            history: [{
                action: 'created',
                date: new Date().toISOString(),
                user: submittal.submittedBy || 'System User',
                details: 'Submittal created'
            }],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };

        this.submittals.push(newSubmittal);
        this.save();
        this.notify('add', newSubmittal);
        return newSubmittal;
    },

    /**
     * Update submittal
     * @param {string} id - Submittal ID
     * @param {Object} changes - Changes to apply
     * @returns {Object} Updated submittal
     */
    update(id, changes) {
        const submittal = this.submittals.find(s => s.id === id);
        if (!submittal) {
            console.error('Submittal not found:', id);
            return null;
        }

        // Track status changes in history
        if (changes.status && changes.status !== submittal.status) {
            submittal.history.push({
                action: 'status_change',
                date: new Date().toISOString(),
                user: changes.changedBy || 'System User',
                details: `Status changed from "${submittal.status}" to "${changes.status}"`,
                oldStatus: submittal.status,
                newStatus: changes.status
            });

            // Update review/approval dates based on status
            if (changes.status === 'under-review' && !submittal.reviewedDate) {
                submittal.reviewedDate = new Date().toISOString();
            }
            if (changes.status === 'approved') {
                submittal.approvedDate = new Date().toISOString();
                submittal.approvedBy = changes.changedBy || 'System User';
            }
        }

        // Remove internal change tracking field
        delete changes.changedBy;

        Object.assign(submittal, changes);
        submittal.updatedAt = new Date().toISOString();

        this.save();
        this.notify('update', submittal);
        return submittal;
    },

    /**
     * Delete submittal
     * @param {string} id - Submittal ID
     */
    delete(id) {
        const index = this.submittals.findIndex(s => s.id === id);
        if (index !== -1) {
            const deleted = this.submittals.splice(index, 1)[0];
            this.save();
            this.notify('delete', deleted);
            return true;
        }
        return false;
    },

    /**
     * Get submittal by ID
     * @param {string} id - Submittal ID
     * @returns {Object} Submittal
     */
    get(id) {
        return this.submittals.find(s => s.id === id);
    },

    /**
     * Get submittals by status
     * @param {string} status - Status to filter by
     * @returns {Array} Filtered submittals
     */
    getByStatus(status) {
        return this.submittals.filter(s => s.status === status);
    },

    /**
     * Get submittals by category
     * @param {string} category - Category to filter by
     * @returns {Array} Filtered submittals
     */
    getByCategory(category) {
        return this.submittals.filter(s => s.category === category);
    },

    /**
     * Get all submittals with optional filters
     * @param {Object} filters - Filter options
     * @returns {Array} Filtered submittals
     */
    getAll(filters = {}) {
        let results = [...this.submittals];

        if (filters.status) {
            results = results.filter(s => s.status === filters.status);
        }
        if (filters.category) {
            results = results.filter(s => s.category === filters.category);
        }
        if (filters.priority) {
            results = results.filter(s => s.priority === filters.priority);
        }
        if (filters.search) {
            const search = filters.search.toLowerCase();
            results = results.filter(s =>
                s.title.toLowerCase().includes(search) ||
                s.number.toLowerCase().includes(search) ||
                s.description.toLowerCase().includes(search)
            );
        }

        // Sort by date (newest first by default)
        if (filters.sortBy === 'oldest') {
            results.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
        } else if (filters.sortBy === 'priority') {
            const priorityOrder = { urgent: 0, high: 1, normal: 2, low: 3 };
            results.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
        } else {
            results.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        }

        return results;
    },

    /**
     * Add comment to submittal
     * @param {string} id - Submittal ID
     * @param {string} comment - Comment text
     * @param {string} user - User name
     */
    addComment(id, comment, user = 'System User') {
        const submittal = this.get(id);
        if (submittal) {
            submittal.comments.push({
                id: Date.now().toString(36),
                text: comment,
                user: user,
                date: new Date().toISOString()
            });
            submittal.history.push({
                action: 'comment',
                date: new Date().toISOString(),
                user: user,
                details: 'Comment added'
            });
            submittal.updatedAt = new Date().toISOString();
            this.save();
            this.notify('update', submittal);
        }
    },

    /**
     * Get statistics
     * @returns {Object} Stats object
     */
    getStats() {
        return {
            total: this.submittals.length,
            submitted: this.getByStatus('submitted').length,
            underReview: this.getByStatus('under-review').length,
            approved: this.getByStatus('approved').length,
            rejected: this.getByStatus('rejected').length
        };
    },

    /**
     * Save to localStorage
     */
    save() {
        try {
            localStorage.setItem('qcm-submittals', JSON.stringify(this.submittals));
        } catch (e) {
            console.error('Failed to save submittals:', e);
        }
    },

    /**
     * Load from localStorage
     */
    load() {
        try {
            const data = localStorage.getItem('qcm-submittals');
            if (data) {
                this.submittals = JSON.parse(data);
            }
        } catch (e) {
            console.error('Failed to load submittals:', e);
            this.submittals = [];
        }
    },

    /**
     * Subscribe to changes
     * @param {Function} callback - Callback function
     */
    subscribe(callback) {
        this.listeners.push(callback);
    },

    /**
     * Notify listeners of changes
     * @param {string} action - Action type
     * @param {Object} data - Change data
     */
    notify(action, data) {
        this.listeners.forEach(cb => cb(action, data));
    },

    /**
     * Clear all submittals (for testing)
     */
    clear() {
        this.submittals = [];
        this.save();
        this.notify('clear', null);
    },

    /**
     * Add sample data for testing
     */
    addSampleData() {
        const samples = [
            { title: 'Structural Steel Drawings', category: 'Shop Drawings', priority: 'high' },
            { title: 'HVAC Equipment Specifications', category: 'Product Data', priority: 'normal' },
            { title: 'Concrete Mix Design', category: 'Mix Design', priority: 'urgent' },
            { title: 'Electrical Panel Schedule', category: 'Shop Drawings', priority: 'normal' },
            { title: 'Fire Sprinkler Layout', category: 'Shop Drawings', priority: 'high' },
            { title: 'Roofing Material Samples', category: 'Samples', priority: 'low' }
        ];

        samples.forEach((sample, i) => {
            const sub = this.add(sample);
            // Set different statuses for demo
            if (i === 1) this.update(sub.id, { status: 'under-review', reviewer: 'John Smith' });
            if (i === 2) this.update(sub.id, { status: 'under-review', reviewer: 'Jane Doe' });
            if (i === 3) this.update(sub.id, { status: 'approved' });
            if (i === 5) this.update(sub.id, { status: 'rejected', comments: [{ text: 'Does not meet specifications', user: 'QC Manager', date: new Date().toISOString() }] });
        });
    }
};

// ============================================
// SUBMITTAL TRACKER UI
// ============================================

class SubmittalTracker {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentView = 'kanban'; // kanban, list
        this.filters = {};
        this.selectedSubmittal = null;

        // Initialize database
        submittalDB.load();

        // Subscribe to changes
        submittalDB.subscribe((action, data) => {
            this.render();
        });

        // Initial render
        this.render();
    }

    /**
     * Render the tracker UI
     */
    render() {
        if (!this.container) return;

        const stats = submittalDB.getStats();

        this.container.innerHTML = `
            <div class="submittal-tracker">
                <!-- Header -->
                <div class="tracker-header">
                    <div class="tracker-title">
                        <h2>SUBMITTAL TRACKER</h2>
                        <div class="tracker-stats">
                            <span class="stat-item"><span class="stat-value">${stats.total}</span> Total</span>
                            <span class="stat-item pending"><span class="stat-value">${stats.submitted}</span> Pending</span>
                            <span class="stat-item review"><span class="stat-value">${stats.underReview}</span> In Review</span>
                            <span class="stat-item approved"><span class="stat-value">${stats.approved}</span> Approved</span>
                            <span class="stat-item rejected"><span class="stat-value">${stats.rejected}</span> Rejected</span>
                        </div>
                    </div>
                    <div class="tracker-actions">
                        <div class="view-toggle">
                            <button class="view-btn ${this.currentView === 'kanban' ? 'active' : ''}" data-view="kanban">
                                <span>📋</span> Kanban
                            </button>
                            <button class="view-btn ${this.currentView === 'list' ? 'active' : ''}" data-view="list">
                                <span>📃</span> List
                            </button>
                        </div>
                        <button class="add-submittal-btn">
                            <span>➕</span> New Submittal
                        </button>
                    </div>
                </div>

                <!-- Filters -->
                <div class="tracker-filters">
                    <input type="text" class="filter-search" placeholder="Search submittals..." value="${this.filters.search || ''}">
                    <select class="filter-category">
                        <option value="">All Categories</option>
                        <option value="Shop Drawings" ${this.filters.category === 'Shop Drawings' ? 'selected' : ''}>Shop Drawings</option>
                        <option value="Product Data" ${this.filters.category === 'Product Data' ? 'selected' : ''}>Product Data</option>
                        <option value="Samples" ${this.filters.category === 'Samples' ? 'selected' : ''}>Samples</option>
                        <option value="Mix Design" ${this.filters.category === 'Mix Design' ? 'selected' : ''}>Mix Design</option>
                        <option value="Certifications" ${this.filters.category === 'Certifications' ? 'selected' : ''}>Certifications</option>
                    </select>
                    <select class="filter-priority">
                        <option value="">All Priorities</option>
                        <option value="urgent" ${this.filters.priority === 'urgent' ? 'selected' : ''}>Urgent</option>
                        <option value="high" ${this.filters.priority === 'high' ? 'selected' : ''}>High</option>
                        <option value="normal" ${this.filters.priority === 'normal' ? 'selected' : ''}>Normal</option>
                        <option value="low" ${this.filters.priority === 'low' ? 'selected' : ''}>Low</option>
                    </select>
                </div>

                <!-- Content -->
                <div class="tracker-content">
                    ${this.currentView === 'kanban' ? this.renderKanban() : this.renderList()}
                </div>
            </div>
        `;

        this.attachEventListeners();
    }

    /**
     * Render Kanban board view
     */
    renderKanban() {
        const statuses = [
            { key: 'submitted', label: 'Submitted', icon: '📥' },
            { key: 'under-review', label: 'Under Review', icon: '🔍' },
            { key: 'approved', label: 'Approved', icon: '✅' },
            { key: 'rejected', label: 'Rejected', icon: '❌' }
        ];

        return `
            <div class="kanban-board">
                ${statuses.map(status => `
                    <div class="kanban-column" data-status="${status.key}">
                        <div class="column-header">
                            <span class="column-icon">${status.icon}</span>
                            <span class="column-title">${status.label}</span>
                            <span class="column-count">${submittalDB.getByStatus(status.key).length}</span>
                        </div>
                        <div class="column-content" data-status="${status.key}">
                            ${this.renderKanbanCards(status.key)}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    /**
     * Render cards for a Kanban column
     */
    renderKanbanCards(status) {
        const submittals = submittalDB.getAll({ ...this.filters, status });

        if (submittals.length === 0) {
            return '<div class="empty-column">No submittals</div>';
        }

        return submittals.map(sub => `
            <div class="kanban-card" draggable="true" data-id="${sub.id}">
                <div class="card-header">
                    <span class="card-number">${sub.number}</span>
                    <span class="card-priority priority-${sub.priority}">${sub.priority.toUpperCase()}</span>
                </div>
                <div class="card-title">${sub.title}</div>
                <div class="card-meta">
                    <span class="card-category">${sub.category}</span>
                    <span class="card-date">${this.formatDate(sub.submittedDate)}</span>
                </div>
                ${sub.comments.length > 0 ? `<div class="card-comments">💬 ${sub.comments.length}</div>` : ''}
            </div>
        `).join('');
    }

    /**
     * Render list view
     */
    renderList() {
        const submittals = submittalDB.getAll(this.filters);

        if (submittals.length === 0) {
            return `
                <div class="empty-list">
                    <span class="empty-icon">📋</span>
                    <p>No submittals found</p>
                    <button class="add-first-btn">Add Your First Submittal</button>
                </div>
            `;
        }

        return `
            <div class="submittal-list">
                <table class="list-table">
                    <thead>
                        <tr>
                            <th>Number</th>
                            <th>Title</th>
                            <th>Category</th>
                            <th>Priority</th>
                            <th>Status</th>
                            <th>Submitted</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${submittals.map(sub => `
                            <tr data-id="${sub.id}">
                                <td class="col-number">${sub.number}</td>
                                <td class="col-title">${sub.title}</td>
                                <td class="col-category">${sub.category}</td>
                                <td class="col-priority">
                                    <span class="priority-badge priority-${sub.priority}">${sub.priority}</span>
                                </td>
                                <td class="col-status">
                                    <span class="status-badge status-${sub.status}">${this.formatStatus(sub.status)}</span>
                                </td>
                                <td class="col-date">${this.formatDate(sub.submittedDate)}</td>
                                <td class="col-actions">
                                    <button class="action-btn view-btn" data-id="${sub.id}" title="View Details">👁️</button>
                                    <button class="action-btn edit-btn" data-id="${sub.id}" title="Edit">✏️</button>
                                    <button class="action-btn delete-btn" data-id="${sub.id}" title="Delete">🗑️</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // View toggle
        this.container.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.currentView = btn.dataset.view;
                this.render();
            });
        });

        // Add submittal button
        const addBtn = this.container.querySelector('.add-submittal-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.showAddModal());
        }

        // Add first submittal button
        const addFirstBtn = this.container.querySelector('.add-first-btn');
        if (addFirstBtn) {
            addFirstBtn.addEventListener('click', () => this.showAddModal());
        }

        // Filter inputs
        const searchInput = this.container.querySelector('.filter-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filters.search = e.target.value;
                this.render();
            });
        }

        const categoryFilter = this.container.querySelector('.filter-category');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', (e) => {
                this.filters.category = e.target.value || null;
                this.render();
            });
        }

        const priorityFilter = this.container.querySelector('.filter-priority');
        if (priorityFilter) {
            priorityFilter.addEventListener('change', (e) => {
                this.filters.priority = e.target.value || null;
                this.render();
            });
        }

        // Kanban card clicks
        this.container.querySelectorAll('.kanban-card').forEach(card => {
            card.addEventListener('click', () => {
                this.showDetailModal(card.dataset.id);
            });
        });

        // List row clicks
        this.container.querySelectorAll('.list-table tbody tr').forEach(row => {
            row.addEventListener('dblclick', () => {
                this.showDetailModal(row.dataset.id);
            });
        });

        // Action buttons in list
        this.container.querySelectorAll('.view-btn[data-id]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.showDetailModal(btn.dataset.id);
            });
        });

        this.container.querySelectorAll('.edit-btn[data-id]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.showEditModal(btn.dataset.id);
            });
        });

        this.container.querySelectorAll('.delete-btn[data-id]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.confirmDelete(btn.dataset.id);
            });
        });

        // Drag and drop
        this.setupDragAndDrop();
    }

    /**
     * Setup drag and drop for Kanban
     */
    setupDragAndDrop() {
        const cards = this.container.querySelectorAll('.kanban-card');
        const columns = this.container.querySelectorAll('.column-content');

        cards.forEach(card => {
            card.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', card.dataset.id);
                card.classList.add('dragging');
            });

            card.addEventListener('dragend', () => {
                card.classList.remove('dragging');
            });
        });

        columns.forEach(column => {
            column.addEventListener('dragover', (e) => {
                e.preventDefault();
                column.classList.add('drag-over');
            });

            column.addEventListener('dragleave', () => {
                column.classList.remove('drag-over');
            });

            column.addEventListener('drop', (e) => {
                e.preventDefault();
                column.classList.remove('drag-over');

                const id = e.dataTransfer.getData('text/plain');
                const newStatus = column.dataset.status;

                submittalDB.update(id, { status: newStatus });
            });
        });
    }

    /**
     * Show add submittal modal
     */
    showAddModal() {
        const modal = document.createElement('div');
        modal.className = 'submittal-modal-overlay';
        modal.innerHTML = `
            <div class="submittal-modal">
                <div class="modal-header">
                    <h3>➕ New Submittal</h3>
                    <button class="modal-close">✕</button>
                </div>
                <div class="modal-content">
                    <form class="submittal-form">
                        <div class="form-group">
                            <label>Title *</label>
                            <input type="text" name="title" required placeholder="Enter submittal title">
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>Category</label>
                                <select name="category">
                                    <option value="Shop Drawings">Shop Drawings</option>
                                    <option value="Product Data">Product Data</option>
                                    <option value="Samples">Samples</option>
                                    <option value="Mix Design">Mix Design</option>
                                    <option value="Certifications">Certifications</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Priority</label>
                                <select name="priority">
                                    <option value="normal">Normal</option>
                                    <option value="low">Low</option>
                                    <option value="high">High</option>
                                    <option value="urgent">Urgent</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Description</label>
                            <textarea name="description" rows="3" placeholder="Enter description (optional)"></textarea>
                        </div>
                        <div class="form-group">
                            <label>Due Date</label>
                            <input type="date" name="dueDate">
                        </div>
                        <div class="form-actions">
                            <button type="button" class="btn-cancel">Cancel</button>
                            <button type="submit" class="btn-submit">Create Submittal</button>
                        </div>
                    </form>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Close button
        modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
        modal.querySelector('.btn-cancel').addEventListener('click', () => modal.remove());

        // Close on overlay click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });

        // Form submit
        modal.querySelector('.submittal-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            submittalDB.add({
                title: formData.get('title'),
                category: formData.get('category'),
                priority: formData.get('priority'),
                description: formData.get('description'),
                dueDate: formData.get('dueDate') || null
            });
            modal.remove();
        });
    }

    /**
     * Show detail modal
     */
    showDetailModal(id) {
        const submittal = submittalDB.get(id);
        if (!submittal) return;

        const modal = document.createElement('div');
        modal.className = 'submittal-modal-overlay';
        modal.innerHTML = `
            <div class="submittal-modal detail-modal">
                <div class="modal-header">
                    <h3>${submittal.number}: ${submittal.title}</h3>
                    <button class="modal-close">✕</button>
                </div>
                <div class="modal-content">
                    <div class="detail-grid">
                        <div class="detail-main">
                            <div class="detail-section">
                                <h4>Details</h4>
                                <div class="detail-row">
                                    <span class="detail-label">Status:</span>
                                    <span class="status-badge status-${submittal.status}">${this.formatStatus(submittal.status)}</span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-label">Category:</span>
                                    <span>${submittal.category}</span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-label">Priority:</span>
                                    <span class="priority-badge priority-${submittal.priority}">${submittal.priority}</span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-label">Submitted:</span>
                                    <span>${this.formatDateTime(submittal.submittedDate)}</span>
                                </div>
                                ${submittal.dueDate ? `
                                    <div class="detail-row">
                                        <span class="detail-label">Due Date:</span>
                                        <span>${this.formatDate(submittal.dueDate)}</span>
                                    </div>
                                ` : ''}
                                ${submittal.reviewer ? `
                                    <div class="detail-row">
                                        <span class="detail-label">Reviewer:</span>
                                        <span>${submittal.reviewer}</span>
                                    </div>
                                ` : ''}
                            </div>

                            ${submittal.description ? `
                                <div class="detail-section">
                                    <h4>Description</h4>
                                    <p>${submittal.description}</p>
                                </div>
                            ` : ''}

                            <div class="detail-section">
                                <h4>Comments (${submittal.comments.length})</h4>
                                <div class="comments-list">
                                    ${submittal.comments.length === 0 ? '<p class="no-comments">No comments yet</p>' :
                                        submittal.comments.map(c => `
                                            <div class="comment">
                                                <div class="comment-header">
                                                    <span class="comment-user">${c.user}</span>
                                                    <span class="comment-date">${this.formatDateTime(c.date)}</span>
                                                </div>
                                                <div class="comment-text">${c.text}</div>
                                            </div>
                                        `).join('')
                                    }
                                </div>
                                <div class="add-comment">
                                    <textarea class="comment-input" placeholder="Add a comment..."></textarea>
                                    <button class="btn-add-comment">Add Comment</button>
                                </div>
                            </div>
                        </div>

                        <div class="detail-sidebar">
                            <div class="detail-section">
                                <h4>Actions</h4>
                                <div class="action-buttons">
                                    ${submittal.status === 'submitted' ?
                                        '<button class="action-btn-full" data-action="under-review">🔍 Start Review</button>' : ''}
                                    ${submittal.status === 'under-review' ? `
                                        <button class="action-btn-full approve" data-action="approved">✅ Approve</button>
                                        <button class="action-btn-full reject" data-action="rejected">❌ Reject</button>
                                    ` : ''}
                                    ${submittal.status === 'rejected' ?
                                        '<button class="action-btn-full" data-action="submitted">🔄 Resubmit</button>' : ''}
                                </div>
                            </div>

                            <div class="detail-section">
                                <h4>History</h4>
                                <div class="history-list">
                                    ${submittal.history.map(h => `
                                        <div class="history-item">
                                            <span class="history-action">${h.action.replace('_', ' ')}</span>
                                            <span class="history-date">${this.formatDateTime(h.date)}</span>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Close handlers
        modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });

        // Action buttons
        modal.querySelectorAll('[data-action]').forEach(btn => {
            btn.addEventListener('click', () => {
                submittalDB.update(id, { status: btn.dataset.action });
                modal.remove();
            });
        });

        // Add comment
        modal.querySelector('.btn-add-comment').addEventListener('click', () => {
            const input = modal.querySelector('.comment-input');
            if (input.value.trim()) {
                submittalDB.addComment(id, input.value.trim());
                modal.remove();
                this.showDetailModal(id); // Refresh
            }
        });
    }

    /**
     * Show edit modal
     */
    showEditModal(id) {
        const submittal = submittalDB.get(id);
        if (!submittal) return;

        const modal = document.createElement('div');
        modal.className = 'submittal-modal-overlay';
        modal.innerHTML = `
            <div class="submittal-modal">
                <div class="modal-header">
                    <h3>✏️ Edit ${submittal.number}</h3>
                    <button class="modal-close">✕</button>
                </div>
                <div class="modal-content">
                    <form class="submittal-form">
                        <div class="form-group">
                            <label>Title *</label>
                            <input type="text" name="title" required value="${submittal.title}">
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>Category</label>
                                <select name="category">
                                    ${['Shop Drawings', 'Product Data', 'Samples', 'Mix Design', 'Certifications', 'Other'].map(cat =>
                                        `<option value="${cat}" ${submittal.category === cat ? 'selected' : ''}>${cat}</option>`
                                    ).join('')}
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Priority</label>
                                <select name="priority">
                                    ${['low', 'normal', 'high', 'urgent'].map(p =>
                                        `<option value="${p}" ${submittal.priority === p ? 'selected' : ''}>${p.charAt(0).toUpperCase() + p.slice(1)}</option>`
                                    ).join('')}
                                </select>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Status</label>
                            <select name="status">
                                ${['submitted', 'under-review', 'approved', 'rejected'].map(s =>
                                    `<option value="${s}" ${submittal.status === s ? 'selected' : ''}>${this.formatStatus(s)}</option>`
                                ).join('')}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Description</label>
                            <textarea name="description" rows="3">${submittal.description || ''}</textarea>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="btn-cancel">Cancel</button>
                            <button type="submit" class="btn-submit">Save Changes</button>
                        </div>
                    </form>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Close handlers
        modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
        modal.querySelector('.btn-cancel').addEventListener('click', () => modal.remove());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });

        // Form submit
        modal.querySelector('.submittal-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            submittalDB.update(id, {
                title: formData.get('title'),
                category: formData.get('category'),
                priority: formData.get('priority'),
                status: formData.get('status'),
                description: formData.get('description')
            });
            modal.remove();
        });
    }

    /**
     * Confirm delete
     */
    confirmDelete(id) {
        const submittal = submittalDB.get(id);
        if (!submittal) return;

        if (confirm(`Are you sure you want to delete "${submittal.number}: ${submittal.title}"?`)) {
            submittalDB.delete(id);
        }
    }

    /**
     * Format date
     */
    formatDate(dateStr) {
        if (!dateStr) return 'N/A';
        return new Date(dateStr).toLocaleDateString();
    }

    /**
     * Format date and time
     */
    formatDateTime(dateStr) {
        if (!dateStr) return 'N/A';
        return new Date(dateStr).toLocaleString();
    }

    /**
     * Format status for display
     */
    formatStatus(status) {
        const labels = {
            'submitted': 'Submitted',
            'under-review': 'Under Review',
            'approved': 'Approved',
            'rejected': 'Rejected'
        };
        return labels[status] || status;
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { submittalDB, SubmittalTracker };
}
