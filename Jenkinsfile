#!groovy

def helmLint(String chart_dir) {
    sh "helm lint ${chart_dir}"
}

def helmDeploy(LinkedHashMap<String, Object> args) {
    if (args.dry_run) {
        echo "Running dry-run deployment"
        sh "helm upgrade --dry-run --debug --install ${args.name} ${args.chart_dir} --namespace=jenkins"
    } else {
        echo "Running deployment"
        sh "helm upgrade --install ${args.name} ${args.chart_dir} --namespace=jenkins"
        echo "Application ${args.name} successfully deployed"
        echo "Use helm status ${args.name} to check the deployment"
    }
}

String chart_dir = "charts/flask-api-chart"
String registry_url = "https://index.docker.io/v1/" // Docker Hub
String docker_credentials_id = "docker-hub" // name of the Jenkins" stored credentials ID
String docker_image = "sergiomartins8/flask-api-chart"

def chart

podTemplate(label: "jenkins-slave-base-pod", serviceAccount: "jenkins", containers: [
        containerTemplate(
                name: "base",
                image: "sergiomartins8/jenkins-slave-base:1.1",
                ttyEnabled: true,
                command: "cat"
        )
],
        volumes: [
                hostPathVolume(mountPath: "/var/run/docker.sock", hostPath: "/var/run/docker.sock")
        ]
) {
    node("jenkins-slave-base-pod") {
        container("base") {
            stage("Checkout") {
                checkout scm
            }
            stage("Setup configurations") {
                chart = readYaml(file: "${chart_dir}/Chart.yaml")
            }
            stage("PR Build and Test") {
                parallel(
                        "Unit Tests": {
                            sh 'python3 -m unittest discover tests/unit --buffer'
                        },
                        "SonarQube Alanysis": {
                            echo "sonarqube"
                        },
                        "Compile Integration Tests": {
                            echo "compile integration tests"
                        },
                        "Lint Helm Charts": {
                            helmLint(chart_dir)
                            helmDeploy(dry_run: true, name: chart.name, chart_dir: chart_dir)
                        }
                )
            }
            stage("Integration Testing") {
                sh 'python3 -m unittest discover tests/integration --buffer'
            }
            stage("Build && Push Image") {
                docker.withRegistry("${registry_url}", "${docker_credentials_id}") {
                    echo "Building service with docker.build(${docker_image}:${chart.version})"
                    container = docker.build("${docker_image}:${chart.version}", ".")
                    echo "Pushing to Docker Hub"
                    container.push()
                }
            }

            if (env.BRANCH_NAME == 'master') {
                stage("Deployment") {
                    helmDeploy(dry_run: false, name: chart.name, chart_dir: chart_dir)
                }
                stage("Tag build number") {
                    echo "tag"
                }
            }
        }
    }
}
