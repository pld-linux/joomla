Summary:	Content management system
Summary(pl.UTF-8):	System zarządzania treścią
Name:		joomla
Version:	1.0.13
Release:	1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://joomlacode.org/gf/download/frsrelease/4508/13215/Joomla_%{version}-Stable-Full_Package.tar.bz2
#Source0:	Joomla_%{version}-Stable-Full_Package.tar.bz2
#Source0-md5:	ed01a4269faf3851a9f8320ac4de12fc
Source1:	Joomla_1.0.0_Polish_ISO-2.zip
# Source1-md5:	7e9075c6d7b9520898d56ee123d50484
# http://www.joomla.pl/index.php/component/option,com_remository/Itemid,15/func,select/id,6/
Source2:	%{name}-http.conf
Source3:	%{name}-lighttpd.conf
Patch0:		%{name}-config.patch
Patch1:		%{name}-install.patch
URL:		http://www.joomla.org/
# update to 1.5.7 is needed:
# http://securitytracker.com/alerts/2008/Sep/1020843.html
BuildRequires:	security(2008-September-7)
Requires:	php(gd)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(session)
Requires:	webapps
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_joomladir	%{_datadir}/%{name}
%define		_joomladata	/var/lib/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Joomla! is one of the most powerful Open Source Content Management
Systems on the planet. It is used all over the world for everything
from simple websites to complex corporate applications. Joomla! is
easy to install, simple to manage, and reliable.

%description -l pl.UTF-8
Joomla! to jeden z najpotężniejszych systemów zarządzania treścią z
otwartymi źródłami. Jest używana na całym świecie do wszystkiego od
prostych stron WWW do złożonych aplikacji korporacyjnych. Joomla! jest
łatwa w instalacji, prosta w zarządzaniu i niezawodna.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
unzip %{SOURCE1} -d language

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_joomladir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_joomladata}/{administrator,uploadfiles}

# Instalation:
cp -R * $RPM_BUILD_ROOT%{_joomladir}

mv -f $RPM_BUILD_ROOT%{_joomladir}/administrator/{backups,components,modules,templates} \
	$RPM_BUILD_ROOT%{_joomladata}/administrator
mv -f $RPM_BUILD_ROOT%{_joomladir}/{cache,components,images,language,mambots,media,modules,templates} \
	$RPM_BUILD_ROOT%{_joomladata}
ln -sf %{_joomladata}/administrator/{backups,components,modules,templates} $RPM_BUILD_ROOT%{_joomladir}/administrator
ln -sf %{_joomladata}/{cache,components,images,language,mambots,media,modules,templates} $RPM_BUILD_ROOT%{_joomladir}

# Play with configs:
sed -e 's|@JOOMLADIR@|%{_joomladir}|g' -e 's|@JOOMLADATA@|%{_joomladata}|g' \
	$RPM_BUILD_ROOT%{_joomladir}/configuration.php-dist > $RPM_BUILD_ROOT%{_sysconfdir}/configuration.php
ln -sf %{_sysconfdir}/configuration.php $RPM_BUILD_ROOT%{_joomladir}/configuration.php

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerun -- lighttpd 
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/configuration.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_joomladir}
%{_joomladir}/*
%defattr(644,root,http,775)
%dir %{_joomladata}
%{_joomladata}/*
