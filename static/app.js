const GEMINI_CONFIG = {
    apiEndpoint: '/chat',
    maxTokens: 1000,
    temperature: 0.7
};

const appState = {
    currentSection: 'chat',

    currentConversation: {
        messages: [],
        sentiment: 'neutral',
        topics: [],
        startTime: Date.now()
    },

    analytics: {
        totalConversations: 1,
        totalMessages: 0,
        responseTimes: [],
        apiCalls: {
            successful: 0,
            failed: 0
        },
        sentimentCounts: {
            positive: 0,
            negative: 0,
            neutral: 0
        }
    },

    settings: {
        theme: 'auto',
        language: 'en',
        temperature: 0.7,
        showTimestamps: true,
        enableSentiment: true,
        contextMemory: true
    }
};

const fallbackResponses = {
    apiError: [
        "I'm having trouble connecting to my AI brain right now. Please try again in a moment!",
        "Oops! I'm experiencing some technical difficulties. Please try again shortly.",
        "I'm temporarily unable to process that request. Please try again."
    ],

    networkError: [
        "It seems there is a network issue. Please check your connection and try again.",
        "I can't reach the AI server right now. Please try again."
    ],

    genericError: [
        "Something unexpected happened. Please try again.",
        "I encountered an error while processing your request. Please try again."
    ]
};

const elements = {
    messageInput: null,
    sendBtn: null,
    chatMessages: null,
    typingIndicator: null,
    charCount: null,
    quickReplies: [],
    navItems: [],
    mobileNavItems: [],
    contentSections: [],
    themeToggle: null,
    themeSelect: null,
    apiStatus: null,
    sessionMessages: null,
    sessionSentiment: null,
    sessionDuration: null,
    apiCalls: null,
    recentTopics: null
};

document.addEventListener('DOMContentLoaded', function () {
    console.log('AI Chatbot: Initializing...');

    initializeElements();
    initializeApp();
    setupEventListeners();
    updateAnalytics();
    updateSessionInfo();
    startSessionTimer();
    updateApiStatus(true);

    console.log('AI Chatbot: Ready');
});

function initializeElements() {
    elements.messageInput = document.getElementById('messageInput');
    elements.sendBtn = document.getElementById('sendBtn');
    elements.chatMessages = document.getElementById('chatMessages');
    elements.typingIndicator = document.getElementById('typingIndicator');
    elements.charCount = document.getElementById('charCount');

    elements.quickReplies = document.querySelectorAll('.quick-reply');
    elements.navItems = document.querySelectorAll('.nav-item');
    elements.mobileNavItems = document.querySelectorAll('.mobile-nav-item');
    elements.contentSections = document.querySelectorAll('.content-section');

    elements.themeToggle = document.getElementById('themeToggle');
    elements.themeSelect = document.getElementById('themeSelect');

    elements.apiStatus = document.getElementById('apiStatus');

    elements.sessionMessages = document.getElementById('sessionMessages');
    elements.sessionSentiment = document.getElementById('sessionSentiment');
    elements.sessionDuration = document.getElementById('sessionDuration');
    elements.apiCalls = document.getElementById('apiCalls');
    elements.recentTopics = document.getElementById('recentTopics');
}

function initializeApp() {
    if (!elements.chatMessages) {
        console.error('chatMessages element not found');
        return;
    }

    const welcomeMessage = {
        id: Date.now(),
        text: "Hello! I'm your AI Assistant. I can help you with any questions, provide detailed explanations, assist with problems, and engage in meaningful conversations. How can I help you today?",
        sender: 'bot',
        timestamp: new Date(),
        sentiment: 'positive',
        isWelcome: true
    };

    appState.currentConversation.messages = [welcomeMessage];

    renderMessage(welcomeMessage);
    updateAnalytics();
    updateSessionInfo();
}

function setupEventListeners() {
    if (elements.messageInput) {
        elements.messageInput.addEventListener('input', handleInputChange);
        elements.messageInput.addEventListener('keydown', handleKeyPress);
    }

    if (elements.sendBtn) {
        elements.sendBtn.addEventListener('click', sendMessage);
    }

    elements.quickReplies.forEach(function (button) {
        button.addEventListener('click', function () {
            const message = button.getAttribute('data-message');

            if (!message || !elements.messageInput) {
                return;
            }

            elements.messageInput.value = message;

            handleInputChange({
                target: elements.messageInput
            });

            sendMessage();
        });
    });

    elements.navItems.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const section = button.getAttribute('data-section');

            if (section) {
                switchSection(section);
            }
        });
    });

    elements.mobileNavItems.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const section = button.getAttribute('data-section');

            if (section) {
                switchSection(section);
            }
        });
    });

    if (elements.themeToggle) {
        elements.themeToggle.addEventListener('click', toggleTheme);
    }

    if (elements.themeSelect) {
        elements.themeSelect.addEventListener('change', function (event) {
            appState.settings.theme = event.target.value;
            applyTheme();
        });
    }

    setupSettingsListeners();
}

function setupSettingsListeners() {
    const languageSelect = document.getElementById('languageSelect');
    const temperatureSlider = document.getElementById('temperatureSlider');
    const temperatureValue = document.getElementById('temperatureValue');

    const showTimestamps = document.getElementById('showTimestamps');
    const enableSentiment = document.getElementById('enableSentiment');
    const contextMemory = document.getElementById('contextMemory');

    const exportChat = document.getElementById('exportChat');
    const clearChat = document.getElementById('clearChat');

    if (languageSelect) {
        languageSelect.addEventListener('change', function (event) {
            appState.settings.language = event.target.value;
        });
    }

    if (temperatureSlider) {
        temperatureSlider.addEventListener('input', function (event) {
            const value = parseFloat(event.target.value);

            if (!Number.isNaN(value)) {
                appState.settings.temperature = value;
                GEMINI_CONFIG.temperature = value;

                if (temperatureValue) {
                    temperatureValue.textContent = value.toFixed(1);
                }
            }
        });
    }

    if (showTimestamps) {
        showTimestamps.addEventListener('change', function (event) {
            appState.settings.showTimestamps = event.target.checked;
            rerenderMessages();
        });
    }

    if (enableSentiment) {
        enableSentiment.addEventListener('change', function (event) {
            appState.settings.enableSentiment = event.target.checked;
            rerenderMessages();
        });
    }

    if (contextMemory) {
        contextMemory.addEventListener('change', function (event) {
            appState.settings.contextMemory = event.target.checked;
        });
    }

    if (exportChat) {
        exportChat.addEventListener('click', exportChatHistory);
    }

    if (clearChat) {
        clearChat.addEventListener('click', clearChatHistory);
    }
}

function handleInputChange(event) {
    const input = event.target;

    if (!input || !elements.charCount) {
        return;
    }

    let length = input.value.length;

    if (length > 1000) {
        input.value = input.value.substring(0, 1000);
        length = 1000;
    }

    elements.charCount.textContent = length + '/1000';
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    if (!elements.messageInput) {
        return;
    }

    const messageText = elements.messageInput.value.trim();

    if (!messageText) {
        return;
    }

    if (elements.sendBtn) {
        elements.sendBtn.disabled = true;
    }

    const userMessage = {
        id: Date.now(),
        text: messageText,
        sender: 'user',
        timestamp: new Date(),
        sentiment: analyzeSentiment(messageText)
    };

    appState.currentConversation.messages.push(userMessage);

    elements.messageInput.value = '';

    if (elements.charCount) {
        elements.charCount.textContent = '0/1000';
    }

    renderMessage(userMessage);

    updateAnalytics();
    updateSessionInfo();
    updateTopics(messageText);

    showTypingIndicator();

    const startTime = Date.now();

    try {
        const botResponse = await generateAIResponse(messageText);

        const responseTime = Date.now() - startTime;

        const botMessage = {
            id: Date.now() + 1,
            text: botResponse,
            sender: 'bot',
            timestamp: new Date(),
            sentiment: 'positive',
            responseTime: responseTime
        };

        appState.currentConversation.messages.push(botMessage);

        appState.analytics.responseTimes.push(responseTime);
        appState.analytics.apiCalls.successful++;

        hideTypingIndicator();

        renderMessage(botMessage);

        updateApiStatus(true);
        updateAnalytics();
        updateSessionInfo();

    } catch (error) {
        console.error('Chat error:', error);

        appState.analytics.apiCalls.failed++;

        const errorResponse = getRandomFallbackResponse(error);

        const botMessage = {
            id: Date.now() + 1,
            text: errorResponse,
            sender: 'bot',
            timestamp: new Date(),
            sentiment: 'neutral',
            isError: true
        };

        appState.currentConversation.messages.push(botMessage);

        hideTypingIndicator();

        renderMessage(botMessage);

        updateApiStatus(false);
        updateAnalytics();
        updateSessionInfo();
    }

    if (elements.sendBtn) {
        elements.sendBtn.disabled = false;
    }

    if (elements.messageInput) {
        elements.messageInput.focus();
    }

    scrollToBottom();
}

async function generateAIResponse(userMessage) {
    const response = await fetch(GEMINI_CONFIG.apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: userMessage,
            contextMemory: appState.settings.contextMemory,
            language: appState.settings.language,
            temperature: appState.settings.temperature
        })
    });

    let data;

    try {
        data = await response.json();
    } catch (error) {
        throw new Error('Invalid server response');
    }

    if (!response.ok) {
        const serverMessage =
            data && data.reply
                ? data.reply
                : 'HTTP ' + response.status;

        throw new Error(serverMessage);
    }

    if (!data || typeof data.reply !== 'string') {
        throw new Error('Invalid response from server');
    }

    return data.reply;
}

function getRandomFallbackResponse(error) {
    const message = error && error.message
        ? error.message.toLowerCase()
        : '';

    let responses;

    if (
        message.includes('failed to fetch') ||
        message.includes('network') ||
        message.includes('connection')
    ) {
        responses = fallbackResponses.networkError;
    } else if (
        message.includes('http') ||
        message.includes('api') ||
        message.includes('gemini')
    ) {
        responses = fallbackResponses.apiError;
    } else {
        responses = fallbackResponses.genericError;
    }

    return responses[
        Math.floor(Math.random() * responses.length)
    ];
}

function analyzeSentiment(text) {
    const lowerText = text.toLowerCase();

    const positiveWords = [
        'good',
        'great',
        'awesome',
        'excellent',
        'amazing',
        'wonderful',
        'love',
        'like',
        'happy',
        'fantastic',
        'perfect',
        'thank',
        'thanks',
        'glad',
        'nice'
    ];

    const negativeWords = [
        'bad',
        'terrible',
        'awful',
        'horrible',
        'hate',
        'dislike',
        'sad',
        'angry',
        'frustrated',
        'disappointed',
        'problem',
        'issue',
        'wrong',
        'upset',
        'annoyed'
    ];

    let positiveCount = 0;
    let negativeCount = 0;

    positiveWords.forEach(function (word) {
        if (lowerText.includes(word)) {
            positiveCount++;
        }
    });

    negativeWords.forEach(function (word) {
        if (lowerText.includes(word)) {
            negativeCount++;
        }
    });

    if (positiveCount > negativeCount) {
        return 'positive';
    }

    if (negativeCount > positiveCount) {
        return 'negative';
    }

    return 'neutral';
}

function renderMessage(message) {
    if (!elements.chatMessages) {
        return;
    }

    const messageDiv = document.createElement('div');
    messageDiv.className =
        'message ' + message.sender + '-message';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent =
        message.sender === 'bot'
            ? '🤖'
            : '👤';

    const content = document.createElement('div');
    content.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';

    textDiv.textContent = message.text;

    if (message.isError) {
        textDiv.classList.add('error-message');
    }

    content.appendChild(textDiv);

    if (appState.settings.showTimestamps) {
        const timeDiv = document.createElement('div');

        timeDiv.className = 'message-time';

        timeDiv.textContent =
            formatTime(message.timestamp);

        content.appendChild(timeDiv);
    }

    if (
        appState.settings.enableSentiment &&
        message.sender === 'user' &&
        message.sentiment
    ) {
        const sentimentDiv =
            document.createElement('div');

        sentimentDiv.className =
            'sentiment-indicator ' +
            message.sentiment;

        sentimentDiv.textContent =
            getSentimentIcon(message.sentiment) +
            ' ' +
            message.sentiment;

        content.appendChild(sentimentDiv);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    elements.chatMessages.appendChild(messageDiv);

    scrollToBottom();
}

function getSentimentIcon(sentiment) {
    if (sentiment === 'positive') {
        return '😊';
    }

    if (sentiment === 'negative') {
        return '😔';
    }

    return '😐';
}

function showTypingIndicator() {
    if (elements.typingIndicator) {
        elements.typingIndicator.classList.remove('hidden');
        scrollToBottom();
    }
}

function hideTypingIndicator() {
    if (elements.typingIndicator) {
        elements.typingIndicator.classList.add('hidden');
    }
}

function scrollToBottom() {
    if (elements.chatMessages) {
        elements.chatMessages.scrollTop =
            elements.chatMessages.scrollHeight;
    }
}

function formatTime(date) {
    const validDate =
        date instanceof Date
            ? date
            : new Date(date);

    return validDate.toLocaleTimeString(
        'en-US',
        {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        }
    );
}

function switchSection(sectionName) {
    elements.navItems.forEach(function (nav) {
        nav.classList.remove('active');

        if (
            nav.getAttribute('data-section') ===
            sectionName
        ) {
            nav.classList.add('active');
        }
    });

    elements.mobileNavItems.forEach(function (nav) {
        nav.classList.remove('active');

        if (
            nav.getAttribute('data-section') ===
            sectionName
        ) {
            nav.classList.add('active');
        }
    });

    elements.contentSections.forEach(function (section) {
        section.classList.remove('active');

        if (
            section.id ===
            sectionName + '-section'
        ) {
            section.classList.add('active');
        }
    });

    appState.currentSection = sectionName;

    if (sectionName === 'analytics') {
        setTimeout(function () {
            initializeCharts();
        }, 100);
    }
}

function toggleTheme() {
    const currentTheme =
        document.documentElement.getAttribute(
            'data-color-scheme'
        );

    const newTheme =
        currentTheme === 'dark'
            ? 'light'
            : 'dark';

    document.documentElement.setAttribute(
        'data-color-scheme',
        newTheme
    );

    appState.settings.theme = newTheme;

    if (elements.themeSelect) {
        elements.themeSelect.value = newTheme;
    }

    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    if (!elements.themeToggle) {
        return;
    }

    const icon =
        elements.themeToggle.querySelector('i');

    if (!icon) {
        return;
    }

    icon.className =
        theme === 'dark'
            ? 'fas fa-sun'
            : 'fas fa-moon';
}

function applyTheme() {
    const theme = appState.settings.theme;

    if (theme === 'auto') {
        document.documentElement.removeAttribute(
            'data-color-scheme'
        );
    } else {
        document.documentElement.setAttribute(
            'data-color-scheme',
            theme
        );
    }

    updateThemeIcon(theme);
}

function updateAnalytics() {
    appState.analytics.totalMessages =
        appState.currentConversation.messages.length;

    appState.analytics.sentimentCounts = {
        positive: 0,
        negative: 0,
        neutral: 0
    };

    appState.currentConversation.messages.forEach(
        function (message) {
            if (
                message.sentiment &&
                appState.analytics.sentimentCounts[
                    message.sentiment
                ] !== undefined
            ) {
                appState.analytics.sentimentCounts[
                    message.sentiment
                ]++;
            }
        }
    );

    const totalConversations =
        document.getElementById('totalConversations');

    const totalMessages =
        document.getElementById('totalMessages');

    const avgResponseTime =
        document.getElementById('avgResponseTime');

    const apiSuccessRate =
        document.getElementById('apiSuccessRate');

    if (totalConversations) {
        totalConversations.textContent =
            appState.analytics.totalConversations;
    }

    if (totalMessages) {
        totalMessages.textContent =
            appState.analytics.totalMessages;
    }

    if (
        avgResponseTime &&
        appState.analytics.responseTimes.length > 0
    ) {
        const total =
            appState.analytics.responseTimes.reduce(
                function (a, b) {
                    return a + b;
                },
                0
            );

        const average =
            total /
            appState.analytics.responseTimes.length;

        avgResponseTime.textContent =
            (average / 1000).toFixed(1) + 's';
    }

    if (apiSuccessRate) {
        const successful =
            appState.analytics.apiCalls.successful;

        const failed =
            appState.analytics.apiCalls.failed;

        const total =
            successful + failed;

        const rate =
            total > 0
                ? Math.round(
                    (successful / total) * 100
                )
                : 100;

        apiSuccessRate.textContent =
            rate + '%';
    }

    updateCharts();
}

function initializeCharts() {
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js is not loaded.');
        return;
    }

    const sentimentCanvas =
        document.getElementById('sentimentChart');

    if (
        sentimentCanvas &&
        !sentimentCanvas.chartInstance
    ) {
        const data =
            appState.analytics.sentimentCounts;

        sentimentCanvas.chartInstance =
            new Chart(
                sentimentCanvas,
                {
                    type: 'doughnut',

                    data: {
                        labels: [
                            'Positive',
                            'Negative',
                            'Neutral'
                        ],

                        datasets: [
                            {
                                data: [
                                    data.positive,
                                    data.negative,
                                    data.neutral
                                ],

                                backgroundColor: [
                                    '#1FB8CD',
                                    '#B4413C',
                                    '#5D878F'
                                ],

                                borderWidth: 0
                            }
                        ]
                    },

                    options: {
                        responsive: true,
                        maintainAspectRatio: true,

                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                }
            );
    }

    const responseCanvas =
        document.getElementById('responseTimeChart');

    if (
        responseCanvas &&
        !responseCanvas.chartInstance
    ) {
        const responseTimes =
            appState.analytics.responseTimes
                .slice(-10)
                .map(function (time) {
                    return time / 1000;
                });

        const labels =
            responseTimes.map(function (_, index) {
                return 'Msg ' + (index + 1);
            });

        responseCanvas.chartInstance =
            new Chart(
                responseCanvas,
                {
                    type: 'line',

                    data: {
                        labels: labels,

                        datasets: [
                            {
                                label:
                                    'Response Time (seconds)',

                                data:
                                    responseTimes,

                                borderColor:
                                    '#1FB8CD',

                                backgroundColor:
                                    '#FFC185',

                                borderWidth: 2,

                                fill: false,

                                tension: 0.4
                            }
                        ]
                    },

                    options: {
                        responsive: true,
                        maintainAspectRatio: true,

                        plugins: {
                            legend: {
                                display: false
                            }
                        },

                        scales: {
                            y: {
                                beginAtZero: true,

                                title: {
                                    display: true,
                                    text: 'Seconds'
                                }
                            }
                        }
                    }
                }
            );
    }
}

function updateCharts() {
    if (typeof Chart === 'undefined') {
        return;
    }

    const sentimentCanvas =
        document.getElementById('sentimentChart');

    if (
        sentimentCanvas &&
        sentimentCanvas.chartInstance
    ) {
        const data =
            appState.analytics.sentimentCounts;

        sentimentCanvas
            .chartInstance
            .data
            .datasets[0]
            .data = [
                data.positive,
                data.negative,
                data.neutral
            ];

        sentimentCanvas
            .chartInstance
            .update();
    }

    const responseCanvas =
        document.getElementById('responseTimeChart');

    if (
        responseCanvas &&
        responseCanvas.chartInstance
    ) {
        const responseTimes =
            appState.analytics.responseTimes
                .slice(-10)
                .map(function (time) {
                    return time / 1000;
                });

        responseCanvas
            .chartInstance
            .data
            .labels =
            responseTimes.map(function (_, index) {
                return 'Msg ' + (index + 1);
            });

        responseCanvas
            .chartInstance
            .data
            .datasets[0]
            .data = responseTimes;

        responseCanvas
            .chartInstance
            .update();
    }
}

function updateSessionInfo() {
    if (elements.sessionMessages) {
        elements.sessionMessages.textContent =
            appState.currentConversation.messages.length;
    }

    if (elements.apiCalls) {
        elements.apiCalls.textContent =
            appState.analytics.apiCalls.successful +
            appState.analytics.apiCalls.failed;
    }

    const userMessages =
        appState.currentConversation.messages
            .filter(function (message) {
                return message.sender === 'user';
            })
            .slice(-3);

    if (userMessages.length === 0) {
        if (elements.sessionSentiment) {
            elements.sessionSentiment.textContent =
                'Neutral';
        }

        return;
    }

    const counts = {
        positive: 0,
        negative: 0,
        neutral: 0
    };

    userMessages.forEach(function (message) {
        if (
            counts[message.sentiment] !== undefined
        ) {
            counts[message.sentiment]++;
        }
    });

    let dominant = 'neutral';

    if (
        counts.positive > counts.negative &&
        counts.positive >= counts.neutral
    ) {
        dominant = 'positive';
    } else if (
        counts.negative > counts.positive &&
        counts.negative >= counts.neutral
    ) {
        dominant = 'negative';
    }

    if (elements.sessionSentiment) {
        elements.sessionSentiment.textContent =
            dominant.charAt(0).toUpperCase() +
            dominant.slice(1);

        elements.sessionSentiment.className =
            'stat-value sentiment ' +
            dominant;
    }
}

function updateTopics(message) {
    const topics =
        extractTopics(message);

    topics.forEach(function (topic) {
        if (
            !appState.currentConversation
                .topics
                .includes(topic)
        ) {
            appState.currentConversation
                .topics
                .push(topic);

            if (elements.recentTopics) {
                const topicDiv =
                    document.createElement('div');

                topicDiv.className =
                    'topic-item';

                topicDiv.textContent =
                    topic;

                elements.recentTopics
                    .appendChild(topicDiv);

                while (
                    elements.recentTopics
                        .children
                        .length > 5
                ) {
                    elements.recentTopics
                        .removeChild(
                            elements.recentTopics
                                .firstChild
                        );
                }
            }
        }
    });
}

function extractTopics(text) {
    const lowerText =
        text.toLowerCase();

    const keywords = [
        'ai',
        'artificial intelligence',
        'machine learning',
        'deep learning',
        'technology',
        'coding',
        'programming',
        'python',
        'sql',
        'data science',
        'data analysis',
        'job',
        'jobs',
        'career',
        'help',
        'question',
        'problem',
        'explain'
    ];

    const topics = [];

    keywords.forEach(function (keyword) {
        if (lowerText.includes(keyword)) {
            topics.push(
                keyword.charAt(0).toUpperCase() +
                keyword.slice(1)
            );
        }
    });

    return topics.length > 0
        ? topics
        : ['General'];
}

function updateApiStatus(isOnline) {
    const indicators =
        document.querySelectorAll(
            '.status-indicator'
        );

    indicators.forEach(function (indicator) {
        if (isOnline) {
            indicator.classList.add('online');
            indicator.classList.remove('offline');
        } else {
            indicator.classList.remove('online');
            indicator.classList.add('offline');
        }
    });

    if (elements.apiStatus) {
        const statusText =
            elements.apiStatus.querySelector(
                'span:last-child'
            );

        if (statusText) {
            statusText.textContent =
                isOnline
                    ? 'AI Online'
                    : 'AI Offline';
        }
    }
}

function startSessionTimer() {
    setInterval(function () {
        const minutes =
            Math.floor(
                (
                    Date.now() -
                    appState.currentConversation.startTime
                ) / 60000
            );

        if (elements.sessionDuration) {
            elements.sessionDuration.textContent =
                minutes + 'm';
        }
    }, 60000);
}

function rerenderMessages() {
    if (!elements.chatMessages) {
        return;
    }

    elements.chatMessages.innerHTML = '';

    appState.currentConversation
        .messages
        .forEach(function (message) {
            renderMessage(message);
        });

    scrollToBottom();
}

function exportChatHistory() {
    const chatData = {
        conversation:
            appState.currentConversation,

        analytics:
            appState.analytics,

        settings:
            appState.settings,

        exportDate:
            new Date().toISOString(),

        messageCount:
            appState.currentConversation
                .messages
                .length
    };

    const dataString =
        JSON.stringify(
            chatData,
            null,
            2
        );

    const blob =
        new Blob(
            [dataString],
            {
                type: 'application/json'
            }
        );

    const url =
        URL.createObjectURL(blob);

    const link =
        document.createElement('a');

    link.href = url;

    link.download =
        'chat-history-' +
        new Date()
            .toISOString()
            .split('T')[0] +
        '.json';

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);
}

async function clearChatHistory() {
    const confirmed =
        confirm(
            'Are you sure you want to clear the chat history? This will also clear the chatbot memory.'
        );

    if (!confirmed) {
        return;
    }

    try {
        const response =
            await fetch(
                '/clear-memory',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type':
                            'application/json'
                    }
                }
            );

        if (!response.ok) {
            console.warn(
                'Server memory could not be cleared.'
            );
        }
    } catch (error) {
        console.warn(
            'Could not clear server memory:',
            error
        );
    }

    appState.currentConversation = {
        messages: [],
        sentiment: 'neutral',
        topics: [],
        startTime: Date.now()
    };

    appState.analytics = {
        totalConversations: 1,
        totalMessages: 0,
        responseTimes: [],
        apiCalls: {
            successful: 0,
            failed: 0
        },
        sentimentCounts: {
            positive: 0,
            negative: 0,
            neutral: 0
        }
    };

    if (elements.chatMessages) {
        elements.chatMessages.innerHTML = '';
    }

    if (elements.recentTopics) {
        elements.recentTopics.innerHTML =
            '<div class="topic-item">General</div>';
    }

    initializeApp();

    updateAnalytics();
    updateSessionInfo();
    updateApiStatus(true);
}

console.log('AI Chatbot app.js loaded successfully.');