%define modname xcache
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 99_%{modname}.ini

Summary:	The XCache module for PHP
Name:		php-%{modname}
Version:	2.0.1
Release:	6
Group:		Development/PHP
License:	BSD-like
URL:		http://xcache.lighttpd.net/
Source0:	http://xcache.lighttpd.net/pub/Releases/%{version}/%{modname}-%{version}.tar.gz
Source1:	xcache.ini
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
install -d %{buildroot}/var/www/%{name}/coverager
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/%{soname}

install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf << EOF
Alias /%{name} /var/www/%{name}

<Directory "/var/www/%{name}">
    Require local granted
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>
EOF

install -m0644 admin/* %{buildroot}/var/www/%{name}/
install -m0644 coverager/* %{buildroot}/var/www/%{name}/coverager


%files
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

%files admin
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
/var/www/%{name}


%changelog
* Mon Jul 16 2012 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-1mdv2012.0
+ Revision: 809708
- 2.0.1

* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-0.0.rc1.1
+ Revision: 806418
- 2.0.1-rc1

* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-2
+ Revision: 795528
- rebuild for php-5.4.x

* Sat Apr 21 2012 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-1
+ Revision: 792624
- 2.0.0

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-4
+ Revision: 761343
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-3
+ Revision: 696488
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-2
+ Revision: 695489
- rebuilt for php-5.3.7

* Sat Jun 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-1
+ Revision: 682743
- 1.3.2

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-11
+ Revision: 646703
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-10mdv2011.0
+ Revision: 629899
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-9mdv2011.0
+ Revision: 628208
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-8mdv2011.0
+ Revision: 600548
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-7mdv2011.0
+ Revision: 588885
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-6mdv2010.1
+ Revision: 514716
- rebuilt for php-5.3.2

* Sun Feb 07 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.0-5mdv2010.1
+ Revision: 501751
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-4mdv2010.1
+ Revision: 485500
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-3mdv2010.1
+ Revision: 468271
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-2mdv2010.0
+ Revision: 451374
- rebuild

* Tue Aug 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-1mdv2010.0
+ Revision: 409238
- 1.3.0

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 2.0.0-0.0.r592.2mdv2010.0
+ Revision: 397295
- Rebuild

* Tue May 19 2009 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-0.0.r592.1mdv2010.0
+ Revision: 377675
- 2.0.0 (svn snap 592)
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-5mdv2009.1
+ Revision: 346705
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-4mdv2009.1
+ Revision: 341847
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-3mdv2009.1
+ Revision: 323136
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-2mdv2009.1
+ Revision: 310319
- rebuilt against php-5.2.7

* Fri Sep 26 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-1mdv2009.0
+ Revision: 288586
- import php-xcache

