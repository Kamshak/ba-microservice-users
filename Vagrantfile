Vagrant.configure("2") do |config|
  # Settings for the VM
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "users-service.box"
  config.vm.network :private_network, ip: "192.168.10.11"

  # Use Docker-Compose to boot up development env
  config.vm.provision :docker
  config.vm.provision :docker_compose, yml: "/vagrant/docker-compose.yml", rebuild: true, run: "always"

  # Run DB Migrations on provisioning
  config.vm.provision "shell", privileged:true, inline: "docker exec vagrant_web_1 /usr/bin/python /opt/app/manager.py db upgrade"

  # To follow output: vagrant ssh -c "docker logs -f --tail 5 vagrant_web_1"
end
