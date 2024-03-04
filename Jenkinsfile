pipeline {
    agent any
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    docker.build("my_nginx_image_1", "-f Dockerfile .")
                }
            }
        }
        
        stage('Run Docker Container') {
            steps {
                script {
                    // Run Docker container with port mapping to 5656
                    docker.image('my_nginx_image_1').run('-p 5657:80 -d')
                }
            }
        }
    }
    
}
