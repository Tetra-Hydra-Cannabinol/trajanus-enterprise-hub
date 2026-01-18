import { useState, useEffect } from 'react'

function Feedback() {
    const [comments, setComments] = useState([])
    const [newComment, setNewComment] = useState('')
    const [userName, setUserName] = useState('')
    const [category, setCategory] = useState('general')
    const [showForm, setShowForm] = useState(false)

    const categories = [
        { value: 'general', label: 'General Feedback' },
        { value: 'bug', label: 'Bug Report' },
        { value: 'feature', label: 'Feature Request' },
        { value: 'ui', label: 'UI/UX Suggestion' },
        { value: 'integration', label: 'Integration Issue' }
    ]

    // Load comments from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('healthcare-feedback')
        if (saved) {
            try {
                setComments(JSON.parse(saved))
            } catch (e) {
                console.error('Failed to load feedback:', e)
            }
        }
    }, [])

    // Save comments to localStorage
    useEffect(() => {
        localStorage.setItem('healthcare-feedback', JSON.stringify(comments))
    }, [comments])

    const handleSubmit = (e) => {
        e.preventDefault()
        if (!newComment.trim() || !userName.trim()) return

        const comment = {
            id: Date.now(),
            user: userName.trim(),
            category,
            text: newComment.trim(),
            timestamp: new Date().toISOString(),
            status: 'new'
        }

        setComments(prev => [comment, ...prev])
        setNewComment('')
        setShowForm(false)
    }

    const updateStatus = (id, status) => {
        setComments(prev => prev.map(c =>
            c.id === id ? { ...c, status } : c
        ))
    }

    const deleteComment = (id) => {
        if (confirm('Delete this feedback?')) {
            setComments(prev => prev.filter(c => c.id !== id))
        }
    }

    const getCategoryColor = (cat) => {
        const colors = {
            general: '#00AAFF',
            bug: '#f87171',
            feature: '#4ade80',
            ui: '#fbbf24',
            integration: '#a78bfa'
        }
        return colors[cat] || '#00AAFF'
    }

    const getStatusBadge = (status) => {
        const badges = {
            new: { label: 'New', color: '#00AAFF' },
            reviewed: { label: 'Reviewed', color: '#fbbf24' },
            implemented: { label: 'Done', color: '#4ade80' },
            declined: { label: 'Declined', color: '#808080' }
        }
        return badges[status] || badges.new
    }

    const formatDate = (iso) => {
        const date = new Date(iso)
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    return (
        <div className="feedback-panel">
            <div className="feedback-header">
                <h2>Team Feedback</h2>
                <button
                    className="add-feedback-btn"
                    onClick={() => setShowForm(!showForm)}
                >
                    {showForm ? '✕ Cancel' : '+ Add Feedback'}
                </button>
            </div>

            {showForm && (
                <form className="feedback-form" onSubmit={handleSubmit}>
                    <div className="form-row">
                        <input
                            type="text"
                            placeholder="Your name"
                            value={userName}
                            onChange={(e) => setUserName(e.target.value)}
                            className="feedback-input"
                            required
                        />
                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            className="feedback-select"
                        >
                            {categories.map(cat => (
                                <option key={cat.value} value={cat.value}>
                                    {cat.label}
                                </option>
                            ))}
                        </select>
                    </div>
                    <textarea
                        placeholder="Enter your feedback, suggestions, or bug reports..."
                        value={newComment}
                        onChange={(e) => setNewComment(e.target.value)}
                        className="feedback-textarea"
                        rows={4}
                        required
                    />
                    <button type="submit" className="submit-feedback-btn">
                        Submit Feedback
                    </button>
                </form>
            )}

            <div className="feedback-list">
                {comments.length === 0 ? (
                    <div className="no-feedback">
                        <span className="no-feedback-icon">💬</span>
                        <p>No feedback yet. Be the first to share your thoughts!</p>
                    </div>
                ) : (
                    comments.map(comment => (
                        <div key={comment.id} className="feedback-item">
                            <div className="feedback-item-header">
                                <div className="feedback-meta">
                                    <span className="feedback-user">{comment.user}</span>
                                    <span
                                        className="feedback-category"
                                        style={{ backgroundColor: getCategoryColor(comment.category) + '20', color: getCategoryColor(comment.category) }}
                                    >
                                        {categories.find(c => c.value === comment.category)?.label}
                                    </span>
                                </div>
                                <div className="feedback-actions">
                                    <select
                                        value={comment.status}
                                        onChange={(e) => updateStatus(comment.id, e.target.value)}
                                        className="status-select"
                                        style={{ color: getStatusBadge(comment.status).color }}
                                    >
                                        <option value="new">New</option>
                                        <option value="reviewed">Reviewed</option>
                                        <option value="implemented">Done</option>
                                        <option value="declined">Declined</option>
                                    </select>
                                    <button
                                        className="delete-btn"
                                        onClick={() => deleteComment(comment.id)}
                                    >
                                        🗑
                                    </button>
                                </div>
                            </div>
                            <p className="feedback-text">{comment.text}</p>
                            <span className="feedback-time">{formatDate(comment.timestamp)}</span>
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}

export default Feedback
