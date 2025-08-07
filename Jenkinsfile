pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-v $HOME/.cache/pip:/root/.cache/pip'
        }
    }

    environment {
        PYTHONPATH = '.'
    }

    stages {

        stage('Устанавливаем зависимости') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('🚀 Запускаем тесты...') {
            steps {
                sh '''
                    pytest --alluredir=allure-results
                '''
            }
        }

        stage('📊 Генерируем Allure-отчёт') {
            steps {
                sh '''
                    mkdir -p allure-report
                    allure generate allure-results -o allure-report --clean
                '''
            }
        }

        stage('Публикуем Allure report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
        }
    }
}


