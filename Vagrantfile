# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "wheezy64"

  config.vm.box_url = "http://vagrantbox-public.liip.ch/liip-wheezy64.box"

  config.vm.provider "lxc" do |lxc, override|
    override.vm.box_url = "http://vagrantbox-public.liip.ch/liip-wheezy64-lxc.box"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
    ansible.host_key_checking = false
  end

  config.vm.network :forwarded_port, host: 8000, guest: 8000
end

