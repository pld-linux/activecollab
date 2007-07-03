Summary:	activeCollab
Name:		activecollab
Version:	0.7.1
Release:	0.7
License:	HPL
Group:		Applications/WWW
Source0:	http://www.activecollab.com/files/0.7.1/activeCollab.tar.gz
# Source0-md5:	7cf254743083243202e9d1152240ea1a
URL:		http://www.activecollab.com/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-gd
Requires:	php-mysql
Requires:	php-simplexml
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
ctiveCollab is an easy to use, web based, open source collaboration
and project management tool. Set up an environment where you, your
team and your clients can collaborate on active projects using a set
of simple, functional tools.

%prep
%setup -q -n activecollab

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
	AddDefaultCharset utf-8
</Directory>
EOF
rm -f .htaccess

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a . $RPM_BUILD_ROOT%{_appdir}
rm -f $RPM_BUILD_ROOT%{_appdir}/apache.conf

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc license.txt readme.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%{_appdir}
