pipeline {
    agent any
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    docker.build("my_nginx_image", "-f Dockerfile .")
                }
            }
        }
        
        stage('Run Docker Container') {
            steps {
                script {
                    // Run Docker container with port mapping to 5656
                    docker.image('my_nginx_image').run('-p 5656:80 -d')
                }
            }
        }
    }
    
}
