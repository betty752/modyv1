// Initialize Vue application
new Vue({
    el: '#app',
    data: {
        // Authentication
        authMode: 'login',
        loginForm: {
            username: '',
            password: ''
        },
        registerForm: {
            username: '',
            email: '',
            password: '',
            confirmPassword: '',
            gender: 'M',
            menstrualDate: ''
        },
        
        // User data
        user: null,
        
        // UI states
        currentPage: 'dashboard',
        isLoading: false,
        errorMessage: '',
        successMessage: '',
        
        // Mood tracking
        moodForm: {
            question1: 0,
            question2: 0,
            question3: 0,
            emoji: '',
            notes: ''
        },
        emojis: {
            'very_happy': '😄',
            'happy': '🙂',
            'neutral': '😐',
            'sad': '😔',
            'very_sad': '😢',
            'angry': '😡',
            'tired': '😴',
            'anxious': '😰'
        },
        
        // Analysis
        analysisPeriod: '30',
        moodHistory: [],
        newMenstrualDate: '',
        
        // Charts
        timelineChart: null,
        distributionChart: null,
        questionsChart: null,
        cycleChart: null,
        
        // Current mood for suggestions
        currentMood: null,
        
        // Suggestion content
        positiveQuotes: [
            "Le bonheur n'est pas quelque chose de prêt à l'emploi. Il découle de vos propres actions. - Dalaï Lama",
            "La plus perdue des journées est celle où l'on n'a pas ri. - E.E. Cummings",
            "Le bonheur, c'est lorsque vos actes sont en accord avec vos paroles. - Gandhi",
            "Le bonheur de votre vie dépend de la qualité de vos pensées. - Marc Aurèle",
            "Compte ton âge en amis, pas en années. Compte ta vie en sourires, pas en larmes. - John Lennon"
        ],
        neutralQuotes: [
            "La vie n'est pas de se découvrir soi-même, mais de se créer soi-même. - George Bernard Shaw",
            "La seule façon de faire du bon travail est d'aimer ce que vous faites. - Steve Jobs",
            "Le but de notre vie est d'être heureux. - Dalaï Lama",
            "Un voyage de mille lieues commence toujours par un premier pas. - Lao Tseu",
            "Crois en toi-même et tu es déjà à mi-chemin. - Theodore Roosevelt"
        ],
        negativeQuotes: [
            "Cela aussi passera. - Proverbe persan",
            "Tu n'es pas seul dans tes difficultés. Chaque fleur doit pousser à travers la terre. - Laurie Jean Sennott",
            "Le fond du gouffre est devenu la fondation solide sur laquelle j'ai rebâti ma vie. - J.K. Rowling",
            "Au milieu de la difficulté se trouve l'opportunité. - Albert Einstein",
            "L'heure la plus sombre est juste avant l'aube. - Thomas Fuller"
        ],
        
        positiveMusicSuggestions: [
            { title: "Happy - Pharrell Williams", url: "https://www.youtube.com/watch?v=ZbZSe6N_BXs" },
            { title: "Good Feeling - Flo Rida", url: "https://www.youtube.com/watch?v=3OnnDqH6Wj8" },
            { title: "Walking on Sunshine - Katrina & The Waves", url: "https://www.youtube.com/watch?v=iPUmE-tne5U" },
            { title: "Can't Stop the Feeling - Justin Timberlake", url: "https://www.youtube.com/watch?v=ru0K8uYEZWw" },
            { title: "Uptown Funk - Mark Ronson ft. Bruno Mars", url: "https://www.youtube.com/watch?v=OPf0YbXqDm0" }
        ],
        neutralMusicSuggestions: [
            { title: "Here Comes the Sun - The Beatles", url: "https://www.youtube.com/watch?v=KQetemT1sWc" },
            { title: "Weightless - Marconi Union", url: "https://www.youtube.com/watch?v=UfcAVejslrU" },
            { title: "Lovely Day - Bill Withers", url: "https://www.youtube.com/watch?v=bEeaS6fuUoA" },
            { title: "Three Little Birds - Bob Marley", url: "https://www.youtube.com/watch?v=zaGUr6wzyT8" },
            { title: "Views - Drake", url: "https://www.youtube.com/watch?v=uxpDa-c-4Mc" }
        ],
        negativeMusicSuggestions: [
            { title: "Weightless - Marconi Union", url: "https://www.youtube.com/watch?v=UfcAVejslrU" },
            { title: "Claire de Lune - Debussy", url: "https://www.youtube.com/watch?v=CvFH_6DNRCY" },
            { title: "Breathe Me - Sia", url: "https://www.youtube.com/watch?v=ghPcYqn0p4Y" },
            { title: "Peaceful Piano Playlist", url: "https://www.youtube.com/watch?v=2OEL4P1Rz04" },
            { title: "Ambient Music for Stress Relief", url: "https://www.youtube.com/watch?v=lFcSrYw-ARY" }
        ],
        
        positiveActivities: [
            "Partagez votre énergie positive avec un ami ou un membre de votre famille",
            "Tenez un journal sur ce qui vous a rendu heureux aujourd'hui",
            "Essayez une nouvelle activité ou un nouveau passe-temps qui vous intéresse",
            "Exprimez votre gratitude pour trois choses dans votre vie",
            "Planifiez quelque chose d'excitant pour l'avenir"
        ],
        neutralActivities: [
            "Faites une courte promenade à l'extérieur et remarquez 5 belles choses",
            "Créez une liste de tâches pour organiser vos pensées",
            "Essayez une nouvelle recette ou commandez votre plat préféré",
            "Appelez un ami pour une conversation rapide",
            "Pratiquez la pleine conscience ou la respiration profonde pendant 5 minutes"
        ],
        negativeActivities: [
            "Prenez un bain chaud ou une douche relaxante",
            "Écrivez vos sentiments dans un journal",
            "Faites une activité créative simple comme dessiner ou colorier",
            "Pratiquez 5 minutes de méditation guidée",
            "Respirez profondément pendant 2 minutes en comptant jusqu'à 4 à l'inspiration et 6 à l'expiration"
        ],
        
        positiveVideos: [
            { title: "Yoga matinal rapide - 10 min", url: "https://www.youtube.com/watch?v=VaoV1PrYft4" },
            { title: "Séance d'entraînement dansante de 10 minutes", url: "https://www.youtube.com/watch?v=Rw9S2wb0UxI" },
            { title: "Méditation guidée pour l'énergie positive", url: "https://www.youtube.com/watch?v=86m4RC_ADEY" }
        ],
        neutralVideos: [
            { title: "Méditation de 5 minutes pour l'équilibre", url: "https://www.youtube.com/watch?v=inpok4MKVLM" },
            { title: "Étirement de yoga doux", url: "https://www.youtube.com/watch?v=4pKly2JojMw" },
            { title: "Sons de la nature pour la relaxation", url: "https://www.youtube.com/watch?v=eKFTSSKCzWA" }
        ],
        negativeVideos: [
            { title: "Méditation guidée pour l'anxiété", url: "https://www.youtube.com/watch?v=O-6f5wQXSu8" },
            { title: "Respiration profonde pour le stress", url: "https://www.youtube.com/watch?v=aNXKjGFUlMs" },
            { title: "Sons de pluie apaisants pour dormir", url: "https://www.youtube.com/watch?v=yIQd2Ya0Ziw" }
        ],
        
        // Profile
        profileForm: {
            full_name: '',
            age: '',
            occupation: '',
            interests: '',
            goals: '',
            additional_notes: ''
        }
    },
    
    mounted() {
        // Check if user is already logged in (e.g., from localStorage)
        const savedUser = localStorage.getItem('moody_user');
        if (savedUser) {
            try {
                this.user = JSON.parse(savedUser);
                this.loadInitialData();
            } catch (e) {
                localStorage.removeItem('moody_user');
            }
        }
    },
    
    methods: {
        // Authentication
        async login() {
            if (!this.loginForm.username || !this.loginForm.password) {
                this.errorMessage = "Veuillez remplir tous les champs";
                return;
            }
            
            this.isLoading = true;
            this.errorMessage = '';
            
            try {
                const response = await axios.post('/api/login', {
                    username: this.loginForm.username,
                    password: this.loginForm.password
                });
                
                if (response.data.success) {
                    this.user = response.data.user;
                    localStorage.setItem('moody_user', JSON.stringify(this.user));
                    this.loadInitialData();
                } else {
                    this.errorMessage = response.data.message || "Échec de la connexion";
                }
            } catch (error) {
                this.errorMessage = "Erreur de connexion au serveur";
                console.error(error);
            }
            
            this.isLoading = false;
        },
        
        async register() {
            // Validate inputs
            if (!this.registerForm.username || !this.registerForm.email || 
                !this.registerForm.password || !this.registerForm.confirmPassword) {
                this.errorMessage = "Veuillez remplir tous les champs";
                return;
            }
            
            if (this.registerForm.password !== this.registerForm.confirmPassword) {
                this.errorMessage = "Les mots de passe ne correspondent pas";
                return;
            }
            
            if (this.registerForm.password.length < 6) {
                this.errorMessage = "Le mot de passe doit comporter au moins 6 caractères";
                return;
            }
            
            // Email validation
            const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailPattern.test(this.registerForm.email)) {
                this.errorMessage = "Format d'email invalide";
                return;
            }
            
            // Check menstrual date for female users
            if (this.registerForm.gender === 'F' && !this.registerForm.menstrualDate) {
                this.errorMessage = "Veuillez entrer la date de vos dernières règles";
                return;
            }
            
            this.isLoading = true;
            this.errorMessage = '';
            
            try {
                const response = await axios.post('/api/register', {
                    username: this.registerForm.username,
                    email: this.registerForm.email,
                    password: this.registerForm.password,
                    gender: this.registerForm.gender,
                    menstrual_date: this.registerForm.menstrualDate
                });
                
                if (response.data.success) {
                    this.user = response.data.user;
                    localStorage.setItem('moody_user', JSON.stringify(this.user));
                    this.loadInitialData();
                } else {
                    this.errorMessage = response.data.message || "Échec de l'inscription";
                }
            } catch (error) {
                this.errorMessage = "Erreur de connexion au serveur";
                console.error(error);
            }
            
            this.isLoading = false;
        },
        
        async logout() {
            try {
                await axios.post('/api/logout');
                this.user = null;
                localStorage.removeItem('moody_user');
                this.resetAllForms();
            } catch (error) {
                console.error(error);
            }
        },
        
        // Initial data loading
        async loadInitialData() {
            // Set gender-specific theme
            document.documentElement.style.setProperty(
                '--primary-color', 
                this.user.gender === 'F' ? 'var(--female-color)' : 'var(--male-color)'
            );
            
            // Load profile data
            await this.loadProfile();
            
            // Load latest mood data
            await this.loadLatestMood();
            
            // Load mood history for analysis
            if (this.currentPage === 'analysis') {
                await this.loadMoodHistory();
            }
        },
        
        // Profile
        async loadProfile() {
            try {
                const response = await axios.get('/api/profile');
                
                if (response.data.success) {
                    const profile = response.data.profile;
                    this.profileForm = {
                        full_name: profile.full_name || '',
                        age: profile.age || '',
                        occupation: profile.occupation || '',
                        interests: profile.interests || '',
                        goals: profile.goals || '',
                        additional_notes: profile.additional_notes || ''
                    };
                    
                    // Update user data if any changes
                    if (response.data.user) {
                        this.user = response.data.user;
                        localStorage.setItem('moody_user', JSON.stringify(this.user));
                    }
                    
                    if (this.user.gender === 'F' && this.user.last_menstrual_date) {
                        this.newMenstrualDate = this.user.last_menstrual_date;
                    }
                }
            } catch (error) {
                console.error(error);
            }
        },
        
        async updateProfile() {
            // Validate age if provided
            if (this.profileForm.age) {
                const age = parseInt(this.profileForm.age);
                if (isNaN(age) || age < 0 || age > 120) {
                    this.errorMessage = "Veuillez entrer un âge valide entre 0 et 120";
                    return;
                }
            }
            
            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';
            
            try {
                const response = await axios.post('/api/update_profile', this.profileForm);
                
                if (response.data.success) {
                    this.successMessage = "Profil mis à jour avec succès";
                } else {
                    this.errorMessage = response.data.message || "Échec de la mise à jour du profil";
                }
            } catch (error) {
                this.errorMessage = "Erreur de connexion au serveur";
                console.error(error);
            }
            
            this.isLoading = false;
        },
        
        async updateMenstrualDate() {
            if (!this.newMenstrualDate) {
                this.errorMessage = "Veuillez sélectionner une date";
                return;
            }
            
            this.isLoading = true;
            this.errorMessage = '';
            
            try {
                const response = await axios.post('/api/update_menstrual_date', {
                    date: this.newMenstrualDate
                });
                
                if (response.data.success) {
                    this.user.last_menstrual_date = this.newMenstrualDate;
                    localStorage.setItem('moody_user', JSON.stringify(this.user));
                    
                    // Redraw cycle chart if on analysis page
                    if (this.currentPage === 'analysis') {
                        this.loadMoodHistory();
                    }
                } else {
                    this.errorMessage = response.data.message || "Échec de la mise à jour de la date";
                }
            } catch (error) {
                this.errorMessage = "Erreur de connexion au serveur";
                console.error(error);
            }
            
            this.isLoading = false;
        },
        
        // Mood tracking
        async saveMood() {
            // Validate inputs
            if (this.moodForm.question1 === 0 || this.moodForm.question2 === 0 || this.moodForm.question3 === 0) {
                this.errorMessage = "Veuillez répondre à toutes les questions";
                return;
            }
            
            if (!this.moodForm.emoji) {
                this.errorMessage = "Veuillez sélectionner une émotion";
                return;
            }
            
            this.isLoading = true;
            this.errorMessage = '';
            
            try {
                const response = await axios.post('/api/save_mood', this.moodForm);
                
                if (response.data.success) {
                    // Update current mood
                    this.currentMood = {
                        date: new Date().toISOString().split('T')[0],
                        ...this.moodForm
                    };
                    
                    // Navigate to suggestions
                    this.currentPage = 'suggestions';
                    
                    // Reset mood form
                    this.resetMoodForm();
                } else {
                    this.errorMessage = response.data.message || "Échec de l'enregistrement de l'humeur";
                }
            } catch (error) {
                this.errorMessage = "Erreur de connexion au serveur";
                console.error(error);
            }
            
            this.isLoading = false;
        },
        
        async loadLatestMood() {
            try {
                const response = await axios.get('/api/mood_history', {
                    params: { days: 1 }
                });
                
                if (response.data.success && response.data.entries.length > 0) {
                    this.currentMood = response.data.entries[0];
                }
            } catch (error) {
                console.error(error);
            }
        },
        
        // Analysis
        async loadMoodHistory() {
            try {
                const response = await axios.get('/api/mood_history', {
                    params: { days: parseInt(this.analysisPeriod) || 0 }
                });
                
                if (response.data.success) {
                    this.moodHistory = response.data.entries;
                    
                    if (this.moodHistory.length > 0) {
                        this.$nextTick(() => {
                            this.renderCharts();
                        });
                    }
                }
            } catch (error) {
                console.error(error);
            }
        },
        
        renderCharts() {
            this.renderTimelineChart();
            this.renderDistributionChart();
            this.renderQuestionsChart();
            
            if (this.user.gender === 'F' && this.user.last_menstrual_date) {
                this.renderCycleChart();
            }
        },
        
        renderTimelineChart() {
            const ctx = document.getElementById('timelineChart');
            if (!ctx) return;
            
            // Destroy existing chart if it exists
            if (this.timelineChart) {
                this.timelineChart.destroy();
            }
            
            // Prepare data
            const dates = this.moodHistory.map(entry => entry.date);
            
            // Convert emoji choice to numeric values
            const emojiValues = {
                'very_happy': 5,
                'happy': 4,
                'neutral': 3,
                'sad': 2,
                'very_sad': 1,
                'angry': 1.5,
                'tired': 2.5,
                'anxious': 2
            };
            
            const values = this.moodHistory.map(entry => emojiValues[entry.emoji] || 3);
            
            // Create chart
            this.timelineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Humeur',
                        data: values,
                        borderColor: this.user.gender === 'F' ? '#FFB6C1' : '#ADD8E6',
                        backgroundColor: this.user.gender === 'F' ? 'rgba(255, 182, 193, 0.2)' : 'rgba(173, 216, 230, 0.2)',
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    }]
                },
                options: {
                    scales: {
                        y: {
                            min: 0.5,
                            max: 5.5,
                            ticks: {
                                callback: function(value) {
                                    const labels = ["", "Très Triste", "Triste", "Neutre", "Heureux", "Très Heureux"];
                                    return labels[value] || "";
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        },
        
        renderDistributionChart() {
            const ctx = document.getElementById('distributionChart');
            if (!ctx) return;
            
            // Destroy existing chart if it exists
            if (this.distributionChart) {
                this.distributionChart.destroy();
            }
            
            // Count occurrences of each emoji
            const emojiCounts = {};
            this.moodHistory.forEach(entry => {
                emojiCounts[entry.emoji] = (emojiCounts[entry.emoji] || 0) + 1;
            });
            
            // Prepare data
            const labels = Object.keys(emojiCounts).map(emoji => {
                const labelMap = {
                    'very_happy': 'Très Heureux 😄',
                    'happy': 'Heureux 🙂',
                    'neutral': 'Neutre 😐',
                    'sad': 'Triste 😔',
                    'very_sad': 'Très Triste 😢',
                    'angry': 'En colère 😡',
                    'tired': 'Fatigué 😴',
                    'anxious': 'Anxieux 😰'
                };
                return labelMap[emoji] || emoji;
            });
            
            const data = Object.values(emojiCounts);
            
            // Create chart
            this.distributionChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            '#FFB6C1', // Pink
                            '#ADD8E6', // Light blue
                            '#A5D6A7', // Light green
                            '#FFCC80', // Light orange
                            '#EF9A9A', // Light red
                            '#CE93D8', // Light purple
                            '#B0BEC5', // Light blue-grey
                            '#F48FB1'  // Light pink
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right'
                        }
                    }
                }
            });
        },
        
        renderQuestionsChart() {
            const ctx = document.getElementById('questionsChart');
            if (!ctx) return;
            
            // Destroy existing chart if it exists
            if (this.questionsChart) {
                this.questionsChart.destroy();
            }
            
            // Calculate averages
            let q1Sum = 0, q2Sum = 0, q3Sum = 0;
            this.moodHistory.forEach(entry => {
                q1Sum += entry.question1;
                q2Sum += entry.question2;
                q3Sum += entry.question3;
            });
            
            const count = this.moodHistory.length;
            const q1Avg = q1Sum / count;
            const q2Avg = q2Sum / count;
            const q3Avg = q3Sum / count;
            
            // Create chart
            this.questionsChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Énergie', 'Stress', 'Satisfaction'],
                    datasets: [{
                        label: 'Moyenne',
                        data: [q1Avg, q2Avg, q3Avg],
                        backgroundColor: this.user.gender === 'F' ? '#FFB6C1' : '#ADD8E6',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 3.5,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        },
        
        renderCycleChart() {
            const ctx = document.getElementById('cycleChart');
            if (!ctx || !this.user.last_menstrual_date) return;
            
            // Destroy existing chart if it exists
            if (this.cycleChart) {
                this.cycleChart.destroy();
            }
            
            try {
                // Parse the last menstrual date
                const lastPeriod = new Date(this.user.last_menstrual_date);
                
                // Prepare data
                const emojiValues = {
                    'very_happy': 5,
                    'happy': 4,
                    'neutral': 3,
                    'sad': 2,
                    'very_sad': 1,
                    'angry': 1.5,
                    'tired': 2.5,
                    'anxious': 2
                };
                
                const chartData = this.moodHistory.map(entry => {
                    const entryDate = new Date(entry.date);
                    const daysDiff = Math.floor((entryDate - lastPeriod) / (24 * 60 * 60 * 1000));
                    const cycleDay = (daysDiff % 28) + 1; // Assuming 28-day cycle
                    
                    return {
                        x: cycleDay,
                        y: emojiValues[entry.emoji] || 3
                    };
                });
                
                // Create chart
                this.cycleChart = new Chart(ctx, {
                    type: 'scatter',
                    data: {
                        datasets: [{
                            label: 'Humeur',
                            data: chartData,
                            backgroundColor: '#FFB6C1',
                            pointRadius: 6,
                            pointHoverRadius: 8
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                min: 1,
                                max: 28,
                                title: {
                                    display: true,
                                    text: 'Jour du cycle'
                                }
                            },
                            y: {
                                min: 0.5,
                                max: 5.5,
                                ticks: {
                                    callback: function(value) {
                                        const labels = ["", "Très Triste", "Triste", "Neutre", "Heureux", "Très Heureux"];
                                        return labels[value] || "";
                                    }
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: false
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return `Jour ${context.parsed.x}: ${context.parsed.y}`;
                                    }
                                }
                            }
                        }
                    }
                });
            } catch (error) {
                console.error('Erreur lors du rendu du graphique du cycle:', error);
            }
        },
        
        // Utility functions
        resetMoodForm() {
            this.moodForm = {
                question1: 0,
                question2: 0,
                question3: 0,
                emoji: '',
                notes: ''
            };
        },
        
        resetAllForms() {
            this.resetMoodForm();
            
            this.loginForm = {
                username: '',
                password: ''
            };
            
            this.registerForm = {
                username: '',
                email: '',
                password: '',
                confirmPassword: '',
                gender: 'M',
                menstrualDate: ''
            };
            
            this.profileForm = {
                full_name: '',
                age: '',
                occupation: '',
                interests: '',
                goals: '',
                additional_notes: ''
            };
            
            this.errorMessage = '';
            this.successMessage = '';
            this.currentPage = 'dashboard';
            this.authMode = 'login';
        },
        
        getCurrentDate() {
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            return new Date().toLocaleDateString('fr-FR', options);
        },
        
        formatDate(dateStr) {
            if (!dateStr) return "Non définie";
            
            try {
                const options = { year: 'numeric', month: 'long', day: 'numeric' };
                return new Date(dateStr).toLocaleDateString('fr-FR', options);
            } catch (e) {
                return dateStr;
            }
        },
        
        getEmojiLabel(emojiValue) {
            const labels = {
                'very_happy': 'Très Heureux',
                'happy': 'Heureux',
                'neutral': 'Neutre',
                'sad': 'Triste',
                'very_sad': 'Très Triste',
                'angry': 'En colère',
                'tired': 'Fatigué',
                'anxious': 'Anxieux'
            };
            return labels[emojiValue] || '';
        },
        
        getRandomQuote(type) {
            let quotes = [];
            
            if (type === 'positive') {
                quotes = this.positiveQuotes;
            } else if (type === 'neutral') {
                quotes = this.neutralQuotes;
            } else {
                quotes = this.negativeQuotes;
            }
            
            const randomIndex = Math.floor(Math.random() * quotes.length);
            return quotes[randomIndex];
        },
        
        isPositiveMood(emoji) {
            return emoji === 'very_happy' || emoji === 'happy';
        },
        
        isNeutralMood(emoji) {
            return emoji === 'neutral';
        },
        
        isNegativeMood(emoji) {
            return emoji === 'sad' || emoji === 'very_sad' || 
                   emoji === 'angry' || emoji === 'tired' || emoji === 'anxious';
        }
    },
    
    watch: {
        // Reset error message when auth mode changes
        authMode() {
            this.errorMessage = '';
        },
        
        // Load appropriate data when page changes
        currentPage(newPage) {
            if (newPage === 'analysis') {
                this.loadMoodHistory();
            } else if (newPage === 'profile') {
                this.loadProfile();
            } else if (newPage === 'suggestions') {
                this.loadLatestMood();
            }
            
            this.errorMessage = '';
            this.successMessage = '';
        }
    }
});