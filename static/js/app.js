// Global State and Chart Instances
let sentimentChart = null;
let aspectChart = null;
let currentReviews = [];
let activeFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadDashboardData();
    loadReviewsData();
    setupAnalyzeForm();
    setupTableSearch();
});

// Sidebar Navigation
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const pageViews = document.querySelectorAll('.page-view');
    const pageHeading = document.getElementById('pageHeading');
    const pageSubheading = document.getElementById('pageSubheading');

    const headings = {
        'dashboard': { title: 'Hotel Feedback Dashboard', sub: 'Real-time overview of guest sentiments and service performance' },
        'analyze': { title: 'Analyze Guest Feedback', sub: 'Cognitive NLP processing for sentiment, aspect detection & suggestions' },
        'aspects': { title: 'Hotel Service Aspects', sub: 'Granular classification into 10 key operational categories' },
        'reviews': { title: 'Guest Reviews Database', sub: 'Browse, search, and filter historical guest feedback' },
        'insights': { title: 'Management Insights', sub: 'Actionable summaries and prioritized operational recommendations' },
        'about': { title: 'Cognitive Computing Architecture', sub: 'How human feedback is transformed into actionable intelligence' }
    };

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetView = item.getAttribute('data-view');

            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');

            pageViews.forEach(view => {
                view.classList.remove('active');
                if (view.id === `view-${targetView}`) {
                    view.classList.add('active');
                }
            });

            if (headings[targetView]) {
                pageHeading.textContent = headings[targetView].title;
                pageSubheading.textContent = headings[targetView].sub;
            }

            // Trigger chart resize if navigating to dashboard
            if (targetView === 'dashboard') {
                if (sentimentChart) sentimentChart.resize();
                if (aspectChart) aspectChart.resize();
            }
        });
    });
}

// 1. DASHBOARD & CHARTS
async function loadDashboardData() {
    try {
        const res = await fetch('/api/dashboard');
        const data = await res.json();

        // Update KPI Cards
        document.getElementById('metricTotal').textContent = data.total;
        document.getElementById('metricPositive').textContent = data.positive;
        document.getElementById('metricNegative').textContent = data.negative;
        document.getElementById('metricNeutral').textContent = data.neutral;
        document.getElementById('metricComplaint').textContent = data.most_common_complaint;
        document.getElementById('metricPraised').textContent = data.most_liked_service;

        // Render Charts
        renderSentimentChart(data.sentiment_distribution);
        renderAspectChart(data.aspect_distribution);
        renderDynamicInsights(data.insights);
    } catch (err) {
        console.error('Failed to load dashboard data:', err);
    }
}

function renderSentimentChart(dist) {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    if (sentimentChart) sentimentChart.destroy();

    sentimentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                data: [dist.Positive || 0, dist.Negative || 0, dist.Neutral || 0],
                backgroundColor: ['#10b981', '#ef4444', '#f59e0b'],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { boxWidth: 14, font: { size: 12, family: 'system-ui' } }
                }
            },
            cutout: '70%'
        }
    });
}

function renderAspectChart(dist) {
    const ctx = document.getElementById('aspectChart').getContext('2d');
    if (aspectChart) aspectChart.destroy();

    const labels = Object.keys(dist);
    const counts = Object.values(dist);

    aspectChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mention Count',
                data: counts,
                backgroundColor: '#0284c7',
                borderRadius: 6,
                maxBarThickness: 32
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0, font: { size: 11 } },
                    grid: { color: '#f1f5f9' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 11 } }
                }
            }
        }
    });
}

// 2. ANALYZE FEEDBACK FORM & COGNITIVE LOGIC
function setupAnalyzeForm() {
    const analyzeBtn = document.getElementById('btnAnalyze');
    const inputArea = document.getElementById('feedbackInput');
    const saveCheckbox = document.getElementById('saveToDataset');
    const emptyState = document.getElementById('resultEmpty');
    const resultBox = document.getElementById('resultBox');

    // Preset button handlers
    const presetButtons = document.querySelectorAll('.preset-chip');
    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            inputArea.value = btn.getAttribute('data-text');
            triggerAnalysis();
        });
    });

    analyzeBtn.addEventListener('click', triggerAnalysis);

    async function triggerAnalysis() {
        const text = inputArea.value.trim();
        if (!text) {
            alert('Please enter a guest feedback comment to analyze.');
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

        try {
            const res = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    save: saveCheckbox.checked
                })
            });

            if (!res.ok) throw new Error('Analysis failed');

            const result = await res.json();
            displayAnalysisResult(result);

            // If saved, refresh dashboard and review tables
            if (saveCheckbox.checked) {
                loadDashboardData();
                loadReviewsData();
            }
        } catch (err) {
            alert('Error running NLP analysis: ' + err.message);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Analyze Feedback';
        }
    }

    function displayAnalysisResult(res) {
        emptyState.style.display = 'none';
        resultBox.style.display = 'block';

        const badge = document.getElementById('resSentimentBadge');
        const aspectVal = document.getElementById('resAspect');
        const polarityVal = document.getElementById('resPolarity');
        const suggestionVal = document.getElementById('resSuggestion');
        const timeline = document.getElementById('resPipeline');

        // Sentiment badge styling
        badge.className = 'sentiment-badge-lg';
        if (res.sentiment === 'Positive') {
            badge.classList.add('badge-positive');
            badge.innerHTML = '<i class="fa-regular fa-face-smile"></i> Sentiment: Positive';
        } else if (res.sentiment === 'Negative') {
            badge.classList.add('badge-negative');
            badge.innerHTML = '<i class="fa-regular fa-face-frown"></i> Sentiment: Negative';
        } else {
            badge.classList.add('badge-neutral');
            badge.innerHTML = '<i class="fa-regular fa-face-meh"></i> Sentiment: Neutral';
        }

        aspectVal.textContent = res.aspect;
        polarityVal.textContent = `Polarity Score: ${res.polarity}`;
        suggestionVal.textContent = res.suggestion;

        // Populate Cognitive Timeline
        timeline.innerHTML = '';
        res.pipeline_steps.forEach((step, index) => {
            const item = document.createElement('div');
            item.className = 'timeline-item active';
            item.innerHTML = `
                <div class="timeline-dot">${index + 1}</div>
                <div class="timeline-content">
                    <h5>${step.step}</h5>
                    <p>${step.desc}</p>
                </div>
            `;
            timeline.appendChild(item);
        });
    }
}

// 5. REVIEWS PAGE & FILTERING
async function loadReviewsData(filter = 'all') {
    try {
        const url = filter === 'all' ? '/api/reviews' : `/api/reviews?sentiment=${filter}`;
        const res = await fetch(url);
        currentReviews = await res.json();
        renderReviewsTable(currentReviews);
    } catch (err) {
        console.error('Failed to load reviews:', err);
    }
}

function renderReviewsTable(reviews) {
    const tbody = document.getElementById('reviewsTableBody');
    tbody.innerHTML = '';

    if (reviews.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:32px; color:#94a3b8;">No reviews found.</td></tr>`;
        return;
    }

    reviews.forEach(r => {
        const tr = document.createElement('tr');
        
        let pillClass = 'pill-neutral';
        if (r.sentiment === 'Positive') pillClass = 'pill-positive';
        if (r.sentiment === 'Negative') pillClass = 'pill-negative';

        tr.innerHTML = `
            <td style="color:#64748b; font-weight:600;">#${r.id}</td>
            <td style="max-width: 450px; line-height: 1.4;">${escapeHtml(r.review)}</td>
            <td><span class="sentiment-pill ${pillClass}">${r.sentiment}</span></td>
            <td><span class="aspect-tag"><i class="fa-solid fa-tag"></i> ${r.aspect}</span></td>
            <td style="color:#64748b; white-space:nowrap;">${r.date}</td>
        `;
        tbody.appendChild(tr);
    });
}

function filterReviews(sentiment, btnElement) {
    activeFilter = sentiment;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btnElement.classList.add('active');
    loadReviewsData(sentiment);
}

function setupTableSearch() {
    const searchInput = document.getElementById('reviewSearch');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = currentReviews.filter(r => 
            r.review.toLowerCase().includes(term) || 
            r.aspect.toLowerCase().includes(term) ||
            r.sentiment.toLowerCase().includes(term)
        );
        renderReviewsTable(filtered);
    });
}

// 6. INSIGHTS VIEW
function renderDynamicInsights(insights) {
    const container = document.getElementById('insightsContainer');
    if (!container) return;

    container.innerHTML = '';
    insights.forEach(ins => {
        const div = document.createElement('div');
        div.className = `insight-card type-${ins.type}`;
        div.innerHTML = `
            <div class="insight-icon">
                <i class="fa-solid ${ins.icon}"></i>
            </div>
            <div class="insight-content">
                <h4>Operational Insight</h4>
                <p>"${ins.text}"</p>
            </div>
        `;
        container.appendChild(div);
    });
}

// Helper to sanitize HTML strings
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
