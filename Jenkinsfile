pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                echo '🐳 Собираем Docker-образ...'
                sh 'docker build -t framework-tests .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🚀 Запускаем автотесты...'
                sh 'docker run --rm -v $PWD/allure-results:/app/allure-results framework-tests'
            }
        }

        stage('Allure Report') {
            steps {
                echo '📊 Показываем отчёт...'
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**', fingerprint: true
        }
    }
}
