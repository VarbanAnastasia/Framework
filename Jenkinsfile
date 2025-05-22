pipeline {
    agent any

    environment {
        IMAGE_NAME = 'framework-tests'
        PROJECT_DIR = '/home/jenkins/framework' // путь внутри Jenkins-контейнера
    }

    stages {
        stage('Build Docker Image') {
            steps {
                dir("${PROJECT_DIR}") {
                    echo '🐳 Собираем Docker-образ из исходников...'
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir("${PROJECT_DIR}") {
                    echo '🚀 Запускаем тесты...'
                    sh "mkdir -p allure-results"
                    sh "docker run --rm -v \$PWD/allure-results:/app/allure-results ${IMAGE_NAME}"
                }
            }
        }

        stage('Allure Report') {
            steps {
                dir("${PROJECT_DIR}") {
                    echo '📊 Генерируем отчёт Allure...'
                    allure includeProperties: false, results: [[path: 'allure-results']]
                }
            }
        }
    }
}
