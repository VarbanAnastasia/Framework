pipeline {
    agent any

    tools {
        // Название должно совпадать с тем, что указано в Global Tool Configuration
        python 'Python3.11'
    }

    environment {
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Install dependencies') {
            steps {
                withPythonEnv('Python3.11') {
                    sh '''
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run tests') {
            steps {
                withPythonEnv('Python3.11') {
                    sh '''
                        pytest tests/ --alluredir=${ALLURE_RESULTS}
                    '''
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: "${ALLURE_RESULTS}"]]
        }
    }
}
