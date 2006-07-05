Summary:	Content management system
Summary(pl):	System zarz±dzania tre¶ci±
Name:		joomla
Version:	1.0.10
Release:	1
License:	GPL v2
Group:		Applications/Databases/Interfaces
# http://developer.joomla.org/sf/frs/do/downloadFile/projects.joomla/frs.joomla_1_0.1_0_10/frs5789
Source0:	Joomla_%{version}-Stable-Full_Package.tar.bz2
# Source0-md5:	4c608dc14fe8952bd35803e5cc8f56cc
# http://www.joomla.pl/index.php/component/option,com_remository/Itemid,15/func,select/id,6/
Source2:	%{name}-http.conf
Patch0:		%{name}-config.patch
Patch1:		%{name}-install.patch
URL:		http://www.joomla.org/
Requires:	php
Requires:	php-gd
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-session
Requires:	apache >= 2.0
Requires:	webapps
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
from simple websites to complex corporate applications.
Joomla! is easy to install, simple to manage, and reliable. 

%description -l pl
Joomla! to jeden z najpotê¿niejszych systemów zarz±dzania tre¶ci± z
otwartymi ¼ród³ami. Jest u¿ywana na ca³ym ¶wiecie do wszystkiego od
prostych stron WWW do z³o¿onych aplikacji korporacyjnych. Joomla!
jest ³atwa w instalacji, prosta w zarz±dzaniu i niezawodna.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1

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

install %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/configuration.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%dir %{_joomladir}
%{_joomladir}/*
%defattr(644,root,http,775)
%dir %{_joomladata}
%{_joomladata}/*
