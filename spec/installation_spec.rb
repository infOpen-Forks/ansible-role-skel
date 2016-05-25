require 'serverspec'

if ENV['TRAVIS']
    set :backend, :exec
end

describe 'skel Ansible role' do

    describe 'first user home files' do

        describe file('/home/foo/.ssh') do
            it { should_not exist }
        end

        describe file('/home/foo/.bashrc') do
            it { should exist }
            it { should be_file }
        end

        describe file('/home/foo/foo') do
            it { should_not exist }
        end

        describe file('/home/foo/bar') do
            it { should_not exist }
        end
    end

    describe 'second user home files' do

        describe file('/home/bar/.ssh') do
            it { should exist }
            it { should be_directory }
            it { should be_mode 700 }
        end

        describe file('/home/bar/.bashrc') do
            it { should_not exist }
        end

        describe file('/home/bar/foo') do
            it { should exist }
            it { should be_directory }
            it { should be_mode 750 }
        end

        describe file('/home/bar/bar') do
            it { should exist }
            it { should be_directory }
            it { should be_mode 755 }
        end

        describe file('/home/bar/bar/foolink') do
            it { should exist }
            it { should be_symlink }
            it { should be_linked_to '/home/bar/foo' }
        end

        describe file('/home/bar/bar/foo.txt') do
            it { should exist }
            it { should be_file }
            it { should be_mode 640 }
        end

        describe file('/home/bar/bar/bar.txt') do
            it { should exist }
            it { should be_file }
            it { should be_mode 640 }
            its(:content) { should match /Ansible managed/ }
        end
    end
end

