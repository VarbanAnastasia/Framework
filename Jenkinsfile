pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                echo '🐳 Собираем Docker-образ...'
                sh 'docker build -t framework-tests .'
            }
        }
//
//         stage('Run Tests') {
//             steps {
//                 echo '🚀 Запускаем тесты...'
//                 sh 'docker run --rm framework-tests | tee result.log'
//             }
//         }
//
//         stage('Show Logs') {
//             steps {
//                 echo '📄 Вывод логов:'
//                 sh 'cat result.log'
//             }
//         }
//     }
}
