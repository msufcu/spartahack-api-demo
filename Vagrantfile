Vagrant.configure("2") do |config|
	#config.vm.box = "rasmus/php7dev"
	#config.vm.box_url = "https://vagrantcloud.com/rasmus/php7dev"
	#config.vm.box = "generic/debian9"
	#config.vm.box_url = "https://vagrantcloud.com/generic/debian9"
	config.vm.box = "ubuntu/trusty64"
	config.vm.box_url = "https://vagrantcloud.com/ubuntu/trusty64cd "
	
	config.vm.box_download_insecure = true
	
	config.vm.network "forwarded_port", guest:80, host:8080
	#config.vm.network "forwarded_port", guest:8000, host:8000
	
	config.vm.synced_folder "php/", "/var/www/html/php/"
	config.vm.provision :shell, path: "provisioners/wsgi.sh"
	#config.vm.provision :shell, inline: "apt-get install -y apache2 python"
end