pipeline {
    agent any

    environment {
        IMAGE_NAME = 'framework-tests'
    }

    stages {
        stage('Prepare Workspace') {
            steps {
                echo '📁 Готовим директорию для отчётов...'
                sh 'mkdir -p allure-results'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Собираем Docker-образ...'
                sh "docker build -t $IMAGE_NAME ."
            }
        }

        stage('Run Tests') {
            steps {
                echo '🚀 Запускаем тесты внутри контейнера...'
                sh "docker run --rm -v $WORKSPACE/allure-results:/app/allure-results $IMAGE_NAME"
            }
        }

        stage('Allure Report') {
            steps {
                echo '📊 Генерируем отчёт Allure...'
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            echo '📦 Архивируем результаты...'
            archiveArtifacts artifacts: 'allure-results/**/*', fingerprint: true
        }
    }
}
