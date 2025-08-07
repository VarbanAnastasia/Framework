pipeline {
    agent {
        docker {
            image 'python:3.11'  // Используем Docker-образ с Python
        }
    }

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install allure-pytest'
            }
        }

        stage('Run tests') {
            steps {
                sh 'pytest tests/ --alluredir=allure-results'
            }
        }

        stage('Allure Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }
    }
}
