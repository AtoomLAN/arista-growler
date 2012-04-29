Summary: arista-growler
Name: arista-growler
Version: 1.1.0
Release: 42
License: Rudy Hardeman <zarya@gigafreak.net>
Group: EOS/Extension
Source0: arista-growler.tar
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: Eos-release >= 2:4.9.0
%description
Growl extension for sending log notifications
%prep
%setup -q -n arista-growler
%build
%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/
mkdir -p $RPM_BUILD_ROOT/usr/local
mkdir -p $RPM_BUILD_ROOT/etc/ProcMgr.d/inst
cp -R CliPlugin $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/
cp -R growler $RPM_BUILD_ROOT/usr/local/
cp -R growler/gntp $RPM_BUILD_ROOT/usr/lib/python2.7/site-packages/
cp growler.init $RPM_BUILD_ROOT/etc/ProcMgr.d/inst/Growler
%files
%defattr(755,root,root,-)
/usr/lib/python2.7/site-packages/CliPlugin/Growl.py
/usr/local/growler/growler.py
/usr/local/growler/gntp/notifier.py
/usr/local/growler/gntp/__init__.py
/usr/lib/python2.7/site-packages/gntp/notifier.py
/usr/lib/python2.7/site-packages/gntp/__init__.py
/usr/lib/python2.7/site-packages/gntp/LICENSE
/usr/lib/python2.7/site-packages/gntp/cli.py
/usr/lib/python2.7/site-packages/gntp/config.py
/usr/lib/python2.7/site-packages/gntp/test/__init__.py
/usr/lib/python2.7/site-packages/gntp/test/basic_tests.py
/usr/lib/python2.7/site-packages/gntp/test/growl-icon.png
/usr/lib/python2.7/site-packages/gntp/test/test_config.py
/usr/lib/python2.7/site-packages/gntp/test/test_hash.py
/usr/local/growler/gntp/LICENSE
/usr/local/growler/gntp/cli.py
/usr/local/growler/gntp/config.py
/usr/local/growler/gntp/test/__init__.py
/usr/local/growler/gntp/test/basic_tests.py
/usr/local/growler/gntp/test/growl-icon.png
/usr/local/growler/gntp/test/test_config.py
/usr/local/growler/gntp/test/test_hash.py
/etc/ProcMgr.d/inst/Growler
%post
chkagent --add Growler
service ProcMgr reload
