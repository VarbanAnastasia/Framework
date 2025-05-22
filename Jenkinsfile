pipeline {
    agent any

    environment {
        IMAGE_NAME = 'framework-tests'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo '🐳 Собираем Docker-образ...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🚀 Запускаем тесты...'
                sh 'rm -rf allure-results && mkdir -p allure-results'
                sh 'docker run --rm -v $PWD/allure-results:/app/allure-results $IMAGE_NAME'
            }
        }
    }

        post {
            always {
                echo '📊 Генерируем Allure-отчёт (даже если тесты упали)...'
                allure includeProperties: false, results: [[path: 'allure-results']], commandline: 'Allure_jenkins'
            }
        }
}



