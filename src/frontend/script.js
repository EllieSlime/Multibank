        // Функция для переключения между страницами
        function showPage(pageId) {
            const isLoggedIn = localStorage.getItem('authToken');

            // Защита: если не залогинен, а пытается открыть не login/registration — редирект на login
            if (!isLoggedIn && pageId !== 'login' && pageId !== 'registration') {
                alert('Требуется авторизация');
                showPage('login');
                return;
            }

            // Скрываем все страницы
            document.querySelectorAll('.page').forEach(page => {
                page.classList.remove('active');
            });

            // Показываем выбранную
            const page = document.getElementById(pageId);
            if (page) {
                page.classList.add('active');
            }

            // Обновляем активную ссылку в сайдбаре
            document.querySelectorAll('.sidebar-nav a').forEach(link => {
                link.classList.remove('active');
            });

            const currentLink = document.querySelector(`.sidebar-nav a[onclick="showPage('${pageId}')"]`);
            if (currentLink) {
                currentLink.classList.add('active');
            }

            // На мобильных закрываем сайдбар
            if (window.innerWidth <= 1024) {
                toggleSidebar();
            }

            window.scrollTo(0, 0);

            // Сохраняем текущую страницу
            localStorage.setItem('currentPage', pageId);
        }

        
        // Функция для переключения сайдбара
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const mainContent = document.getElementById('mainContent');
            
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('sidebar-open');
        }
        
        // Закрытие сайдбара при клике вне его на мобильных устройствах
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            const menuToggle = document.querySelector('.menu-toggle');
            
            if (window.innerWidth <= 1024 && 
                sidebar.classList.contains('active') && 
                !sidebar.contains(event.target) && 
                !menuToggle.contains(event.target)) {
                toggleSidebar();
            }
        });

        
        // Загрузка сохраненной страницы при загрузке
            document.addEventListener('DOMContentLoaded', function() {
                // Обработчик формы регистрации
                document.getElementById('registration-form')?.addEventListener('submit', async function(e) {
                    e.preventDefault();

                    const form = this;
                    const formData = new FormData(form);

                    const password = formData.get('password');
                    const confirmPassword = formData.get('confirmPassword');
                    if (password !== confirmPassword) {
                        alert('Пароли не совпадают');
                        return;
                    }

                    const data = {
                        email_address: formData.get('email'),
                        phone_number: formData.get('phone'),
                        first_name: formData.get('fio').split(' ')[1] || '',
                        last_name: formData.get('fio').split(' ')[0] || '',
                        middle_name: formData.get('fio').split(' ')[2] || '',
                        password: password
                    };

                    try {
                        const response = await fetch('/api/v1/auth/register', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(data)
                        });

                        const result = await response.json();

                        if (response.ok) {
                            alert('Регистрация успешна! Теперь войдите в систему.');
                            form.reset();
                            showPage('login');
                        } else {
                            alert(`Ошибка: ${result.detail || 'Неизвестная ошибка'}`);
                        }
                    } catch (error) {
                        console.error('Ошибка подключения к API:', error);
                        alert('Не удалось подключиться к серверу. Проверьте подключение.');
                    }
                });

                // Обработчик формы входа
                document.getElementById('login-form')?.addEventListener('submit', async function(e) {
                    e.preventDefault();

                    const form = this;
                    const formData = new FormData(form);
                    const identifier = formData.get('identifier');
                    const password = formData.get('password');

                    try {
                        const response = await fetch('/api/v1/auth/login', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ identifier, password })
                        });

                        const result = await response.json();

                        if (response.ok) {
                            // Сохраняем токен
                            localStorage.setItem('authToken', result.access_token.access_token || result.access_token);
                            localStorage.setItem('refreshToken', result.refresh_token);

                            alert('Вход выполнен! Добро пожаловать в MultiBank.');
                            showPage('home');
                            form.reset();
                        } else {
                            alert(`Ошибка: ${result.detail || 'Неверный логин или пароль'}`);
                        }
                    } catch (error) {
                        console.error('Ошибка подключения:', error);
                        alert('Не удалось подключиться к серверу');
                    }
                });

                // Проверяем, есть ли "токен" (условная авторизация)
                const isLoggedIn = localStorage.getItem('authToken');

                // Если залогинен — открываем главную
                if (isLoggedIn) {
                    showPage('home');
                } else {
                    // Иначе — вход
                    showPage('login');
                }
            
            // Инициализация чата с ИИ-помощником
            const chatMessagesModern = document.getElementById('chatMessagesModern');
            const chatInputModern = document.getElementById('chatInputModern');
            const sendBtnModern = document.getElementById('sendBtnModern');
            const voiceBtnModern = document.getElementById('voiceBtnModern');
            const suggestionsModern = document.querySelectorAll('.ai-suggestion-modern');
            
            // Функция добавления сообщения в чат
            function addMessageModern(text, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message-modern ${isUser ? 'user' : 'bot'}`;
                
                const now = new Date();
                const timeString = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
                
                if (isUser) {
                    messageDiv.innerHTML = `
                        <div class="message-content-modern">
                            <p>${text}</p>
                            <div class="message-time-modern">${timeString}</div>
                        </div>
                        <div class="message-avatar-modern">
                            <i class="fas fa-user"></i>
                        </div>
                    `;
                } else {
                    messageDiv.innerHTML = `
                        <div class="message-avatar-modern">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="message-content-modern">
                            <p>${text}</p>
                            <div class="message-time-modern">${timeString}</div>
                        </div>
                    `;
                }
                
                chatMessagesModern.appendChild(messageDiv);
                chatMessagesModern.scrollTop = chatMessagesModern.scrollHeight;
                
                // Автоответ от бота для пользовательских сообщений
                if (isUser) {
                    setTimeout(() => {
                        let response = "";
                        const lowerText = text.toLowerCase();
                        
                        if (lowerText.includes('баланс') || lowerText.includes('счет') || lowerText.includes('деньги')) {
                            response = "Ваш общий баланс составляет 245,680.50 рублей. Из них 124,560.75 рублей на основной карте, 85,340.20 рублей на накопительном счете и 3,450.25 долларов на валютном счете.";
                        } else if (lowerText.includes('трат') || lowerText.includes('расход') || lowerText.includes('потратил')) {
                            response = "За последний месяц вы потратили 45,200 рублей. Основные категории расходов: продукты (12,500 руб.), транспорт (8,300 руб.), развлечения (7,500 руб.).";
                        } else if (lowerText.includes('инвест') || lowerText.includes('акции') || lowerText.includes('портфель')) {
                            response = "Ваш инвестиционный портфель составляет 456,800 рублей с доходностью +12.5% за год. Рекомендую рассмотреть увеличение доли технологических компаний для диверсификации.";
                        } else if (lowerText.includes('сбереж') || lowerText.includes('накоп') || lowerText.includes('экономи')) {
                            response = "Для увеличения сбережений рекомендую откладывать 20% от дохода, что при вашей зарплате составит 17,000 рублей в месяц. Также рассмотрите вклад 'Накопительный' под 8.5% годовых.";
                        } else {
                            response = "Я понял ваш вопрос. Для более точного ответа мне нужно больше информации. Могу помочь с анализом расходов, планированием бюджета или инвестиционными рекомендациями.";
                        }
                        
                        addMessageModern(response, false);
                    }, 1000);
                }
            }
            
            // Обработчик отправки сообщения
            function sendMessageModern() {
                const message = chatInputModern.value.trim();
                if (message) {
                    addMessageModern(message, true);
                    chatInputModern.value = '';
                }
            }
            
            // Обработчики событий
            sendBtnModern.addEventListener('click', sendMessageModern);
            
            chatInputModern.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessageModern();
                }
            });
            
            voiceBtnModern.addEventListener('click', function() {
                alert('Голосовой ввод активирован. Говорите сейчас...');
                // В реальном приложении здесь будет интеграция с Web Speech API
                setTimeout(() => {
                    addMessageModern("Покажи мои последние транзакции", true);
                }, 1500);
            });
            
            function logoutUser() {
            localStorage.removeItem('authToken');
            localStorage.removeItem('refreshToken');
            alert('Вы вышли из аккаунта');
            showPage('login');
             }


            // Обработчики для предложений
            suggestionsModern.forEach(suggestion => {
                suggestion.addEventListener('click', function() {
                    addMessageModern(this.textContent, true);
                });
            });
        });
