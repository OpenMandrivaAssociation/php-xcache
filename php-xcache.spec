%define modname xcache
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 99_%{modname}.ini

Summary:	The XCache module for PHP
Name:		php-%{modname}
Version:	1.2.2
Release:	%mkrel 4
Group:		Development/PHP
License:	BSD-like
URL:		http://xcache.lighttpd.net/
Source0:	http://xcache.lighttpd.net/pub/Releases/%{version}/%{modname}-%{version}.tar.gz
Source1:	xcache.ini
BuildRequires:  php-devel >= 3:5.2.0
Conflicts:	php-afterburner php-mmcache php-eaccelerator php-apc
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
XCache is a fast, stable PHP opcode cacher that has been tested and is now
running on production servers under high load. It overcomes a lot of problems
that has been with other competing opcachers such as being able to be used with
new PHP versions.

%package	admin
Summary:	Web admin GUI for XCache
Group:		Development/PHP
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache-mod_php
Requires:	%{name}

%description	admin
This package contains a Web admin GUI for XCache.

To access the web GUI please open up your favourite web browser and point to:

http://localhost/%{name}/

%prep

%setup -q -n %{modname}-%{version}

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
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}/var/www/%{name}/coverager
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/%{soname}

cat > %{name}.conf << EOF
Alias /%{name} /var/www/%{name}

<Directory "/var/www/%{name}">
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>
EOF

install -m0644 %{name}.conf %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/

install -m0644 admin/* %{buildroot}/var/www/%{name}/
install -m0644 coverager/* %{buildroot}/var/www/%{name}/coverager

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%post admin
%_post_webapp

%postun admin
%_postun_webapp

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

%files admin
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
/var/www/%{name}
