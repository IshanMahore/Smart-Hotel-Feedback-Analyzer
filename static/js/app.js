// Global State and Chart Instances
let sentimentChart = null;
let serviceFeedbackChart = null;
let posNegChart = null;
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
        'dashboard': {
            title: 'Babuseth Guest House & Lodging',
            sub: 'Guest Feedback Intelligence Dashboard'
        },
        'analyze': {
            title: 'Analyze Guest Feedback',
            sub: 'Cognitive NLP processing for sentiment, aspect detection & recommendations'
        },
        'reviews': {
            title: 'Guest Reviews Database',
            sub: 'Verified guest feedback history and performance ratings'
        },
        'insights': {
            title: 'Hotel Management Insights',
            sub: 'Actionable summaries and prioritized operational intelligence'
        },
        'services': {
            title: 'Hotel Services & Amenities',
            sub: 'Babuseth Guest House & Lodging accommodation facilities'
        },
        'about': {
            title: 'About Babuseth Guest House & Lodging',
            sub: 'Property overview and Cognitive Computing architecture'
        }
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

            // Resize charts upon returning to dashboard
            if (targetView === 'dashboard') {
                if (sentimentChart) sentimentChart.resize();
                if (serviceFeedbackChart) serviceFeedbackChart.resize();
                if (posNegChart) posNegChart.resize();
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
        document.getElementById('metricRating').textContent = `${data.avg_rating} ★`;
        document.getElementById('metricPraised').textContent = data.most_praised_service;
        document.getElementById('metricComplaint').textContent = data.most_complained_service;

        // Render All 3 Required Charts
        renderSentimentChart(data.sentiment_distribution);
        renderServiceFeedbackChart(data.service_feedback);
        renderPosNegChart(data.service_pos_neg);
        renderDynamicInsights(data.insights);
    } catch (err) {
        console.error('Failed to load dashboard data:', err);
    }
}

// Chart 1: Guest Sentiment Distribution (Positive, Neutral, Negative)
function renderSentimentChart(dist) {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    if (sentimentChart) sentimentChart.destroy();

    sentimentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [dist.Positive || 0, dist.Neutral || 0, dist.Negative || 0],
                backgroundColor: ['#16a34a', '#d97706', '#dc2626'],
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
                    labels: { boxWidth: 12, font: { size: 12, family: 'system-ui', weight: '600' } }
                }
            },
            cutout: '68%'
        }
    });
}

// Chart 2: Service Feedback (Room, Cleanliness, Staff, AC, Wi-Fi, Parking, Breakfast, Service)
function renderServiceFeedbackChart(feedback) {
    const ctx = document.getElementById('serviceFeedbackChart').getContext('2d');
    if (serviceFeedbackChart) serviceFeedbackChart.destroy();

    const labels = Object.keys(feedback);
    const dataValues = Object.values(feedback);

    serviceFeedbackChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Guest Mentions',
                data: dataValues,
                backgroundColor: '#0b1b3d',
                hoverBackgroundColor: '#ea580c',
                borderRadius: 6,
                maxBarThickness: 34
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
                    ticks: { font: { size: 11, weight: '600' } }
                }
            }
        }
    });
}

// Chart 3: Positive vs Negative Feedback
function renderPosNegChart(posNegData) {
    const ctx = document.getElementById('posNegChart').getContext('2d');
    if (posNegChart) posNegChart.destroy();

    const services = Object.keys(posNegData);
    const posCounts = services.map(s => posNegData[s].positive);
    const negCounts = services.map(s => posNegData[s].negative);

    posNegChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: services,
            datasets: [
                {
                    label: 'Positive Feedback',
                    data: posCounts,
                    backgroundColor: '#16a34a',
                    borderRadius: 6,
                    maxBarThickness: 28
                },
                {
                    label: 'Negative Feedback',
                    data: negCounts,
                    backgroundColor: '#dc2626',
                    borderRadius: 6,
                    maxBarThickness: 28
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { boxWidth: 12, font: { size: 12, weight: '600' } }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0, font: { size: 11 } },
                    grid: { color: '#f1f5f9' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 11, weight: '600' } }
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
            alert('Please enter a guest review to analyze.');
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
        const aspectsContainer = document.getElementById('resAspectsContainer');
        const priorityBadge = document.getElementById('resPriority');
        const mainIssue = document.getElementById('resMainIssue');
        const recommendation = document.getElementById('resRecommendation');
        const timeline = document.getElementById('resPipeline');

        // Overall Sentiment styling
        badge.className = 'sentiment-badge-lg';
        if (res.sentiment === 'Positive') {
            badge.classList.add('badge-positive');
            badge.innerHTML = '<i class="fa-regular fa-face-smile"></i> Overall Sentiment: Positive';
        } else if (res.sentiment === 'Negative') {
            badge.classList.add('badge-negative');
            badge.innerHTML = '<i class="fa-regular fa-face-frown"></i> Overall Sentiment: Negative';
        } else {
            badge.classList.add('badge-neutral');
            badge.innerHTML = '<i class="fa-regular fa-face-meh"></i> Overall Sentiment: Neutral';
        }

        // Detected Aspects (Cleanliness -> Positive, Staff -> Positive, Wi-Fi -> Negative, etc.)
        aspectsContainer.innerHTML = '';
        res.aspect_sentiments.forEach(asp => {
            const item = document.createElement('div');
            const cls = asp.sentiment === 'Positive' ? 'pos' : (asp.sentiment === 'Negative' ? 'neg' : 'neu');
            const icon = asp.sentiment === 'Positive' ? 'fa-circle-check' : (asp.sentiment === 'Negative' ? 'fa-circle-xmark' : 'fa-circle-minus');
            item.className = `aspect-badge-item ${cls}`;
            item.innerHTML = `<span><strong>${asp.aspect}</strong> → ${asp.sentiment}</span> <i class="fa-solid ${icon}"></i>`;
            aspectsContainer.appendChild(item);
        });

        // Priority
        priorityBadge.className = `priority-pill priority-${res.priority.toLowerCase()}`;
        priorityBadge.textContent = res.priority;

        // Main Issue & Recommendation
        mainIssue.textContent = res.main_issue;
        recommendation.textContent = `"${res.recommendation}"`;

        // Cognitive Computing Pipeline Trace
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

// 3. GUEST REVIEWS TABLE & FILTERING
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
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:32px; color:#94a3b8;">No reviews found.</td></tr>`;
        return;
    }

    reviews.forEach(r => {
        const tr = document.createElement('tr');
        
        let pillClass = 'pill-neutral';
        if (r.sentiment === 'Positive') pillClass = 'pill-positive';
        if (r.sentiment === 'Negative') pillClass = 'pill-negative';

        const stars = '★'.repeat(Math.round(r.rating || 4));

        tr.innerHTML = `
            <td style="color:#64748b; font-weight:700;">#${r.id}</td>
            <td style="max-width: 440px; line-height: 1.45;">${escapeHtml(r.review)}</td>
            <td><span class="sentiment-pill ${pillClass}">${r.sentiment}</span></td>
            <td><span class="aspect-tag"><i class="fa-solid fa-tag"></i> ${r.aspect}</span></td>
            <td style="color:#ea580c; font-weight:700; white-space:nowrap;">${stars}</td>
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

// 4. INSIGHTS VIEW
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
                <h4>${ins.title}</h4>
                <p>"${ins.text}"</p>
            </div>
        `;
        container.appendChild(div);
    });
}

// Helper to escape HTML characters
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
