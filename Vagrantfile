# -*- mode: ruby -*-
# # vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

CONFIG = File.join(File.dirname(__FILE__), "config.rb")

require 'fileutils'

# Defaults for config options defined in CONFIG
$vb_gui = false
$vb_memory = 512
$vb_cpus = 1
$vb_name = "dev-vm"

if File.exist?(CONFIG)
  require CONFIG
end

Vagrant.configure(VAGRANTFILE_API_VERSION) do |c|
  c.vm.define vm_name = "dev-vm" do |config|
    config.vm.hostname = vm_name

    config.vm.box = "ubuntu/trusty64"

    # InfluxDB
    config.vm.network "forwarded_port", guest: 8083, host: 9083, auto_correct: true
    config.vm.network "forwarded_port", guest: 8086, host: 9086, auto_correct: true

    ip = "10.10.10.10"
    config.vm.network :private_network, ip: ip

    config.vm.provider :virtualbox do |vb|
      vb.gui = $vb_gui
      vb.memory = $vb_memory
      vb.cpus = $vb_cpus
      vb.name = $vb_name
    end

    config.vm.provision "shell", inline: "/vagrant/setup.sh"
    config.vm.provision "file", source: "./config.js", destination: "/tmp/config.js"
  end
end
