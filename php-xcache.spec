%define modname xcache
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 99_%{modname}.ini

Summary:	The XCache module for PHP
Name:		php-%{modname}
Version:	3.1.0
Release:	7
Group:		Development/PHP
License:	BSD-like
URL:		http://xcache.lighttpd.net/
Source0:	http://xcache.lighttpd.net/pub/Releases/%{version}/%{modname}-%{version}.tar.gz
Source1:	xcache.ini
Patch0:         xcache-3.1.0-config.diff
BuildRequires:  php-devel >= 3:5.2.0
Conflicts:	php-afterburner php-mmcache php-eaccelerator php-apc

%description
XCache is a fast, stable PHP opcode cacher that has been tested and is now
running on production servers under high load. It overcomes a lot of problems
that has been with other competing opcachers such as being able to be used with
new PHP versions.

%package	admin
Summary:	Web admin GUI for XCache
Group:		Development/PHP
Requires:	apache-mod_php
Requires:	%{name}

%description	admin
This package contains a Web admin GUI for XCache.

%prep
%setup -q -n %{modname}-%{version}
%patch0 -p1

cp %{SOURCE1} %{inifile}
perl -pi -e "s|\@libdir\@|%{_libdir}|g" %{inifile}

%build
%serverbuild

phpize

%configure2_5x \
    --enable-%{modname} \
    --enable-xcache-constant \
    --enable-xcache-optimizer \
    --enable-xcache-coverager \
    --enable-xcache-assembler \
    --enable-xcache-disassembler \
    --enable-xcache-encoder \
    --enable-xcache-decoder \
    --enable-xcache-test \
    --enable-xcache-dprint

%make

%install
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}/srv/www/%{name}/coverager
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/%{soname}

install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf << EOF
Alias /%{name} /srv/www/%{name}

<Directory "/srv/www/%{name}">
    Require local granted
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>
EOF

cp -rP htdocs/* %{buildroot}/srv/www/%{name}/
install -d %{buildroot}%{_sysconfdir}/%{name}/cacher
install -d %{buildroot}%{_sysconfdir}/%{name}/coverager
mv %{buildroot}/srv/www/%{name}/config.example.php \
   %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}/srv/www/%{name}/cacher/config.example.php \
   %{buildroot}%{_sysconfdir}/%{name}/cacher
mv %{buildroot}/srv/www/%{name}/coverager/config.example.php \
   %{buildroot}%{_sysconfdir}/%{name}/coverager

%files
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

%files admin
%attr(0644,root,root) %config(noreplace) %{_webappconfdir}/%{name}.conf
/srv/www/%{name}
%{_sysconfdir}/%{name}
