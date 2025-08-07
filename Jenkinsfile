pipeline {
    agent any

    tools {
        // Название Python должно совпадать с тем, что ты указала в настройках Jenkins > Tools
        'jenkins.plugins.shiningpanda.tools.PythonInstallation' 'Python3.11'
    }

    environment {
        VENV_DIR = '.venv'
    }

    stages {
        stage('Create Virtual Env') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                source $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                source $VENV_DIR/bin/activate
                pytest --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
