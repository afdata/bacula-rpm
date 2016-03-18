%global uid 133
%global username bacula

Name:               bacula
Version:            7.4.0
Release:            8%{?dist}
Summary:            Cross platform network backup for Linux, Unix, Mac and Windows
# See LICENSE for details
License:            AGPLv3 with exceptions
Group:              System Environment/Daemons
URL:                http://www.bacula.org
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:            http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Source2:            quickstart_postgresql.txt
Source3:            quickstart_mysql.txt
Source4:            quickstart_sqlite3.txt
Source5:            README.Redhat
Source6:            %{name}.logrotate
Source7:            %{name}-fd.init
Source8:            %{name}-dir.init
Source9:            %{name}-sd.init
Source10:           %{name}-fd.service
Source11:           %{name}-dir.service
Source12:           %{name}-sd.service
Source13:           %{name}-bat.desktop
Source14:           %{name}-traymonitor.desktop
Source15:           %{name}-fd.sysconfig
Source16:           %{name}-dir.sysconfig
Source17:           %{name}-sd.sysconfig
Source18:           %{name}-sd.sysconfig.el5

Patch1:             %{name}-7.0.3-openssl.patch
Patch2:             %{name}-7.4.0-queryfile.patch
Patch3:             %{name}-7.0.3-sqlite-priv.patch
Patch4:             %{name}-7.4.0-bat-build.patch
Patch5:             %{name}-7.4.0-seg-fault.patch
Patch6:             %{name}-5.2.13-logwatch.patch
Patch7:             %{name}-7.0.3-non-free-code.patch
Patch8:             %{name}-7.0.3-tray-monitor-configure.patch

# Original patch removed by mistake, upstream is not willing to add it again:
# http://www.bacula.org/git/cgit.cgi/bacula/commit/?h=Branch-7.0&id=51b3b98fb77ab3c0decee455cc6c4d2eb3c5303a
# Without this, there is no library providing the correct shared object name
# required by the daemons.
# http://bugs.bacula.org/view.php?id=2084
Patch9:             %{name}-7.0.4-autoconf.patch

BuildRequires:      desktop-file-utils
BuildRequires:      perl
BuildRequires:      sed
BuildRequires:      gcc-c++

BuildRequires:      glibc-devel
BuildRequires:      libacl-devel
BuildRequires:      libstdc++-devel
BuildRequires:      libxml2-devel
BuildRequires:      libcap-devel
BuildRequires:      lzo-devel
BuildRequires:      mysql-devel
BuildRequires:      ncurses-devel
BuildRequires:      openssl-devel
BuildRequires:      postgresql-devel
BuildRequires:      readline-devel
BuildRequires:      sqlite-devel
BuildRequires:      zlib-devel

%if 0%{?fedora} || 0%{?rhel} >= 6
BuildRequires:      qt4-devel >= 4.6.2
BuildRequires:      tcp_wrappers-devel
%else
BuildRequires:      tcp_wrappers
%endif

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:      systemd
%endif

%description
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture and is efficient and relatively easy to
use, while offering many advanced storage management features that make it easy
to find and recover lost or damaged files.

%package libs
Summary:            Bacula libraries
Group:              System Environment/Daemons
Obsoletes:          bacula-sysconfdir <= 2.4

%description libs
Bacula is a set of programs that allow you to manage the backup,
recovery, and verification of computer data across a network of
different computers. It is based on a client/server architecture.

This package contains basic Bacula libraries, which are used by all
Bacula programs.

%package libs-sql
Summary:            Bacula SQL libraries
Group:              System Environment/Daemons
Obsoletes:          bacula-libs-mysql <= 5.0.3
Obsoletes:          bacula-libs-sqlite <= 5.0.3
Obsoletes:          bacula-libs-postgresql <= 5.0.3
Provides:           bacula-libs-mysql = %{version}-%{release}
Provides:           bacula-libs-sqlite = %{version}-%{release}
Provides:           bacula-libs-postgresql = %{version}-%{release}

%description libs-sql
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the SQL Bacula libraries, which are used by Director and
Storage daemons. You have to select your preferred catalog library through the
alternatives system.

%package common
Summary:            Common Bacula files
Group:              System Environment/Daemons
Obsoletes:          bacula-sysconfdir <= 2.4
Provides:           group(%username) = %uid
Provides:           user(%username) = %uid
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires(pre):      shadow-utils
Requires(postun):   shadow-utils

%description common
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains files common to all Bacula daemons.

%package director
Summary:            Bacula Director files
Group:              System Environment/Daemons
Requires:           bacula-common%{?_isa} = %{version}-%{release}
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           bacula-libs-sql%{?_isa} = %{version}-%{release}
# Director backends merged into core.
Provides:           bacula-director-common = %{version}-%{release}
Obsoletes:          bacula-director-common < 5.2.3-5
Provides:           bacula-director-mysql = %{version}-%{release}
Obsoletes:          bacula-director-mysql < 5.2.3-5
Provides:           bacula-director-sqlite = %{version}-%{release}
Obsoletes:          bacula-director-sqlite < 5.2.3-5
Provides:           bacula-director-postgresql = %{version}-%{release}
Obsoletes:          bacula-director-postgresql < 5.2.3-5

%if 0%{?fedora} || 0%{?rhel} >= 7
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%if 0%{?rhel} == 5 || 0%{?rhel} == 6
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service
%endif

%description director
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the director files.

%package logwatch
Summary:            Bacula Director logwatch scripts
Group:              System Environment/Daemons
# RHEL 5 does not support noarch subpackages
%if 0%{?fedora} || 0%{?rhel} >= 6
BuildArch:          noarch
%endif
Requires:           bacula-director = %{version}-%{release}
Requires:           logwatch

%description logwatch
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains logwatch scripts for Bacula Director.

%package storage
Summary:            Bacula storage daemon files
Group:              System Environment/Daemons
Requires:           bacula-common%{?_isa} = %{version}-%{release}
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           bacula-libs-sql%{?_isa} = %{version}-%{release}
Requires:           mt-st
# Storage backends merged into core.
Provides:           bacula-storage-common = %{version}-%{release}
Obsoletes:          bacula-storage-common < 5.2.2-2
Provides:           bacula-storage-mysql = %{version}-%{release}
Obsoletes:          bacula-storage-mysql < 5.2.0
Provides:           bacula-storage-sqlite = %{version}-%{release}
Obsoletes:          bacula-storage-sqlite < 5.2.0
Provides:           bacula-storage-postgresql = %{version}-%{release}
Obsoletes:          bacula-storage-postgresql < 5.2.0

%if 0%{?fedora} || 0%{?rhel} >= 7
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%if 0%{?rhel} == 5 || 0%{?rhel} == 6
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service
%endif

%description storage
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the storage daemon, the daemon responsible for writing
the data received from the clients onto tape drives or other mass storage
devices.

%package client
Summary:            Bacula backup client
Group:              System Environment/Daemons
Requires:           bacula-common%{?_isa} = %{version}-%{release}
Requires:           bacula-libs%{?_isa} = %{version}-%{release}

%if 0%{?fedora} || 0%{?rhel} >= 7
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%if 0%{?rhel} == 5 || 0%{?rhel} == 6
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service
%endif

%description client
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the bacula client, the daemon running on the system to be
backed up.

%package console
Summary:            Bacula management console
Group:              System Environment/Daemons
Obsoletes:          bacula-console-gnome <= 2.4
Obsoletes:          bacula-console-wxwidgets <= 5.0.3
Requires:           bacula-libs%{?_isa} = %{version}-%{release}

%description console
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the command-line management console for the bacula backup
system.

%if 0%{?fedora} || 0%{?rhel} >= 6
%package console-bat
Summary:            Bacula bat console
Group:              System Environment/Daemons
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           dejavu-lgc-sans-fonts

%description console-bat
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the bat version of the bacula management console.

%package traymonitor
Summary:            Bacula system tray monitor
Group:              System Environment/Daemons
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           dejavu-lgc-sans-fonts

%description traymonitor
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the Gnome and KDE compatible tray monitor to monitor your
bacula server.
%endif

%package devel
Summary:            Bacula development files
Group:              Development/Libraries
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           bacula-libs-sql%{?_isa} = %{version}-%{release}

%description devel
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This development package contains static libraries and header files.

%package -n nagios-plugins-bacula
Summary:            Nagios Plugin - check_bacula
Group:              Applications/System
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           nagios-common%{?_isa}

%description -n nagios-plugins-bacula
Provides check_bacula support for Nagios.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
#%patch7 -p1
#%patch8 -p1
%patch9 -p1
cp %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} .

# Remove execution permissions from files we're packaging as docs later on
find updatedb -type f | xargs chmod -x

%build
build() {
export CFLAGS="$RPM_OPT_FLAGS -I%{_includedir}/ncurses"
export CPPFLAGS="$RPM_OPT_FLAGS -I%{_includedir}/ncurses"
%configure \
        --disable-conio \
        --disable-rpath \
        --docdir=%{_datadir}/bacula \
        --enable-batch-insert \
        --enable-build-dird \
        --enable-build-stored \
        --enable-includes \
        --enable-largefile \
        --enable-readline \
        --enable-smartalloc \
        --sysconfdir=%{_sysconfdir}/bacula \
        --with-basename=bacula \
        --with-bsrdir=%{_localstatedir}/spool/bacula \
        --with-dir-password=@@DIR_PASSWORD@@ \
        --with-fd-password=@@FD_PASSWORD@@ \
        --with-hostname=localhost \
        --with-logdir=%{_localstatedir}/log/bacula \
        --with-mon-dir-password=@@MON_DIR_PASSWORD@@ \
        --with-mon-fd-password=@@MON_FD_PASSWORD@@ \
        --with-mon-sd-password=@@MON_SD_PASSWORD@@ \
        --with-mysql \
        --with-openssl \
        --with-pid-dir=%{_localstatedir}/run \
        --with-plugindir=%{_libdir}/bacula \
        --with-postgresql \
        --with-scriptdir=%{_libexecdir}/bacula \
        --with-sd-password=@@SD_PASSWORD@@ \
        --with-smtp-host=localhost \
        --with-sqlite3 \
        --with-subsys-dir=%{_localstatedir}/lock/subsys \
        --with-tcp-wrappers \
        --with-working-dir=%{_localstatedir}/spool/bacula \
        --with-x \
        $*
}

%if 0%{?fedora} || 0%{?rhel} >= 6
export QMAKE=/usr/bin/qmake-qt4
build --enable-bat
%else
build --disable-bat
%endif

# Remove RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}
make -C examples/nagios/check_bacula

%if 0%{?fedora} || 0%{?rhel} >= 6
pushd src/qt-console/tray-monitor
    $QMAKE tray-monitor.pro
    make %{?_smp_mflags}
    cp -f .libs/bacula-tray-monitor .
popd
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Nagios plugin
install -p -m 755 -D examples/nagios/check_bacula/.libs/check_bacula %{buildroot}%{_libdir}/nagios/plugins/check_bacula

# Remove catalogue backend symlinks
rm -f %{buildroot}%{_libdir}/libbaccats.so
rm -f %{buildroot}%{_libdir}/libbaccats-%{version}.so

%if 0%{?fedora} || 0%{?rhel} >= 6
# Bat
install -p -m 644 -D src/qt-console/images/bat_icon.png %{buildroot}%{_datadir}/pixmaps/bat.png
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE13}

# QT Tray monitor
install -p -m 755 -D src/qt-console/tray-monitor/bacula-tray-monitor %{buildroot}%{_sbindir}/bacula-tray-monitor
install -p -m 644 -D src/qt-console/tray-monitor/tray-monitor.conf %{buildroot}%{_sysconfdir}/bacula/tray-monitor.conf
install -p -m 644 -D src/qt-console/images/bat_icon.png %{buildroot}%{_datadir}/pixmaps/bacula-tray-monitor.png
install -p -m 644 -D manpages/bacula-tray-monitor.1 %{buildroot}%{_mandir}/man1/bacula-tray-monitor.1
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE14}

%else
rm -f %{buildroot}%{_mandir}/man1/bat.1*
%endif

# Logrotate
mkdir -p %{buildroot}%{_localstatedir}/log/bacula
install -p -m 644 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/bacula

# Logwatch
install -p -m 755 -D scripts/logwatch/bacula %{buildroot}%{_sysconfdir}/logwatch/scripts/services/bacula
install -p -m 755 -D scripts/logwatch/applybaculadate %{buildroot}%{_sysconfdir}/logwatch/scripts/shared/applybaculadate
install -p -m 644 -D scripts/logwatch/logfile.bacula.conf %{buildroot}%{_sysconfdir}/logwatch/conf/logfiles/bacula.conf
install -p -m 644 -D scripts/logwatch/services.bacula.conf %{buildroot}%{_sysconfdir}/logwatch/conf/services/bacula.conf

%if 0%{?fedora} || 0%{?rhel} >= 7
# Systemd unit files
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 -D %{SOURCE10} %{buildroot}%{_unitdir}/bacula-fd.service
install -p -m 644 -D %{SOURCE11} %{buildroot}%{_unitdir}/bacula-dir.service
install -p -m 644 -D %{SOURCE12} %{buildroot}%{_unitdir}/bacula-sd.service
%else
# Initscripts
install -p -m 755 -D %{SOURCE7} %{buildroot}%{_initrddir}/bacula-fd
install -p -m 755 -D %{SOURCE8} %{buildroot}%{_initrddir}/bacula-dir
install -p -m 755 -D %{SOURCE9} %{buildroot}%{_initrddir}/bacula-sd
%endif

# Sysconfig
install -p -m 644 -D %{SOURCE15} %{buildroot}%{_sysconfdir}/sysconfig/bacula-fd
install -p -m 644 -D %{SOURCE16} %{buildroot}%{_sysconfdir}/sysconfig/bacula-dir
%if 0%{?fedora} || 0%{?rhel} >= 6
install -p -m 644 -D %{SOURCE17} %{buildroot}%{_sysconfdir}/sysconfig/bacula-sd
%else
install -p -m 644 -D %{SOURCE18} %{buildroot}%{_sysconfdir}/sysconfig/bacula-sd
%endif

# Spool directory
mkdir -p %{buildroot}%{_localstatedir}/spool/bacula

# Remove stuff we do not need
rm -f %{buildroot}%{_libexecdir}/bacula/{bacula,bacula-ctl-*,startmysql,stopmysql,bconsole,make_catalog_backup}
rm -f %{buildroot}%{_sbindir}/bacula
rm -f %{buildroot}%{_mandir}/man8/bacula.8.gz
rm -f %{buildroot}%{_libdir}/*.la
%if 0%{?fedora} || 0%{?rhel} >= 6
rm -f %{buildroot}%{_datadir}/bacula/{ChangeLog,INSTALL,LICENSE,LICENSE-FAQ,LICENSE-FOSS,README,ReleaseNotes,VERIFYING,technotes}
%else
rm -rf %{buildroot}%{_datadir}/bacula
%endif

# Fix up some perms so rpmlint does not complain too much
chmod 755 %{buildroot}%{_sbindir}/*
chmod 755 %{buildroot}%{_libdir}/bacula/*
chmod 755 %{buildroot}%{_libexecdir}/bacula/*
chmod 644 %{buildroot}%{_libexecdir}/bacula/btraceback.*

%clean
rm -rf %{buildroot}

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig
exit 0

%post libs-sql
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-mysql.so 50
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-sqlite3.so 40
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-postgresql.so 60

# Fix for automatic selection of backends during upgrades
if readlink /etc/alternatives/libbaccats.so | grep --silent mysql || \
   readlink /etc/alternatives/bacula-dir | grep --silent mysql || \
   readlink /etc/alternatives/bacula-sd | grep --silent mysql; then
        /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-mysql.so
elif readlink /etc/alternatives/libbaccats.so | grep --silent sqlite || \
   readlink /etc/alternatives/bacula-dir | grep --silent sqlite || \
   readlink /etc/alternatives/bacula-sd | grep --silent sqlite; then
        /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-sqlite3.so
else
        /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-postgresql.so
fi
/sbin/ldconfig

%preun libs-sql
if [ "$1" = 0 ]; then
        /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-mysql.so
        /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-sqlite3.so
        /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-postgresql.so
fi

%postun libs-sql
/sbin/ldconfig
exit 0

%pre common
getent group %username >/dev/null || groupadd -g %uid -r %username &>/dev/null || :
getent passwd %username >/dev/null || useradd -u %uid -r -s /sbin/nologin \
    -d /var/spool/bacula -M -c 'Bacula Backup System' -g %username %username &>/dev/null || :
exit 0

%if 0%{?fedora} || 0%{?rhel} >= 7

%post client
%systemd_post %{name}-fd.service

%preun client
%systemd_preun %{name}-fd.service

%postun client
%systemd_postun_with_restart %{name}-fd.service

%post director
%systemd_post %{name}-dir.service

%preun director
%systemd_preun %{name}-dir.service

%postun director
%systemd_postun_with_restart %{name}-dir.service

%post storage
%systemd_post %{name}-sd.service

%preun storage
%systemd_preun %{name}-sd.service

%postun storage
%systemd_postun_with_restart %{name}-sd.service

%endif

%if 0%{?rhel} == 5 || 0%{?rhel} == 6

%post client
/sbin/chkconfig --add bacula-fd

%preun client
if [ "$1" = 0 ]; then
        /sbin/service bacula-fd stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del bacula-fd
fi

%postun client
if [ "$1" -ge "1" ]; then
        /sbin/service bacula-fd condrestart >/dev/null 2>&1 || :
fi

%post director
/sbin/chkconfig --add bacula-dir

%preun director
if [ "$1" = 0 ]; then
        /sbin/service bacula-dir stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del bacula-dir
fi

%postun director
if [ "$1" -ge "1" ]; then
        /sbin/service bacula-dir condrestart >/dev/null 2>&1 || :
fi

%post storage
/sbin/chkconfig --add bacula-sd

%preun storage
if [ "$1" = 0 ]; then
        /sbin/service bacula-sd stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del bacula-sd
fi

%postun storage
if [ "$1" -ge "1" ]; then
        /sbin/service bacula-sd condrestart >/dev/null 2>&1 || :
fi

%endif

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc AUTHORS ChangeLog SUPPORT ReleaseNotes
%defattr(-,root,root,-)
%{_libdir}/libbac-%{version}.so
%{_libdir}/libbaccfg-%{version}.so
%{_libdir}/libbacfind-%{version}.so

%files libs-sql
%defattr(-,root,root,-)
%{_libdir}/libbaccats-mysql-%{version}.so
%{_libdir}/libbaccats-mysql.so
%{_libdir}/libbaccats-postgresql-%{version}.so
%{_libdir}/libbaccats-postgresql.so
%{_libdir}/libbaccats-sqlite3-%{version}.so
%{_libdir}/libbaccats-sqlite3.so
%{_libdir}/libbacsql-%{version}.so

%files common
%defattr(-,root,root,-)
%doc README.Redhat quickstart_*
%config(noreplace) %{_sysconfdir}/logrotate.d/bacula
%dir %{_localstatedir}/log/bacula %attr(750, bacula, bacula)
%dir %{_localstatedir}/spool/bacula %attr(750, bacula, bacula)
%dir %{_libexecdir}/%{name}
%dir %{_sysconfdir}/%{name} %attr(755,root,root)
%{_libexecdir}/%{name}/btraceback.dbx
%{_libexecdir}/%{name}/btraceback.gdb
%{_libexecdir}/%{name}/bacula_config
%{_libexecdir}/%{name}/btraceback.mdb
%{_mandir}/man8/btraceback.8*
# %{_mandir}/man8/bpluginfo.8*
%{_sbindir}/btraceback
# %{_sbindir}/bpluginfo

%files director
%defattr(-,root,root,-)
%doc updatedb examples/sample-query.sql
%config(noreplace) %{_sysconfdir}/bacula/bacula-dir.conf %attr(640,root,bacula)
%config(noreplace) %{_sysconfdir}/bacula/query.sql %attr(640,root,bacula)
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-dir
%{_libexecdir}/%{name}/create_bacula_database
%{_libexecdir}/%{name}/delete_catalog_backup
%{_libexecdir}/%{name}/drop_bacula_database
%{_libexecdir}/%{name}/drop_bacula_tables
%{_libexecdir}/%{name}/grant_bacula_privileges
%{_libexecdir}/%{name}/make_bacula_tables
%{_libexecdir}/%{name}/make_catalog_backup.pl
%{_libexecdir}/%{name}/update_bacula_tables
%{_libexecdir}/%{name}/create_mysql_database
%{_libexecdir}/%{name}/drop_mysql_database
%{_libexecdir}/%{name}/drop_mysql_tables
%{_libexecdir}/%{name}/grant_mysql_privileges
%{_libexecdir}/%{name}/make_mysql_tables
%{_libexecdir}/%{name}/update_mysql_tables
%{_libexecdir}/%{name}/create_sqlite3_database
%{_libexecdir}/%{name}/drop_sqlite3_database
%{_libexecdir}/%{name}/drop_sqlite3_tables
%{_libexecdir}/%{name}/grant_sqlite3_privileges
%{_libexecdir}/%{name}/make_sqlite3_tables
%{_libexecdir}/%{name}/update_sqlite3_tables
%{_libexecdir}/%{name}/create_postgresql_database
%{_libexecdir}/%{name}/drop_postgresql_database
%{_libexecdir}/%{name}/drop_postgresql_tables
%{_libexecdir}/%{name}/grant_postgresql_privileges
%{_libexecdir}/%{name}/make_postgresql_tables
%{_libexecdir}/%{name}/update_postgresql_tables
%{_mandir}/man1/bsmtp.1*
%{_mandir}/man8/bacula-dir.8*
%{_mandir}/man8/bregex.8*
%{_mandir}/man8/bwild.8*
%{_mandir}/man8/dbcheck.8*
%{_sbindir}/bacula-dir
%{_sbindir}/bregex
%{_sbindir}/bsmtp
%{_sbindir}/bwild
%{_sbindir}/dbcheck
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/bacula-dir.service
%else
%{_initrddir}/bacula-dir
%endif

%files logwatch
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/logwatch/conf/logfiles/bacula.conf
%config(noreplace) %{_sysconfdir}/logwatch/conf/services/bacula.conf
%{_sysconfdir}/logwatch/scripts/services/bacula
%{_sysconfdir}/logwatch/scripts/shared/applybaculadate

%files storage
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/bacula/bacula-sd.conf %attr(640,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-sd
%{_libexecdir}/%{name}/disk-changer
%{_libexecdir}/%{name}/dvd-handler
%{_libexecdir}/%{name}/mtx-changer
%{_libexecdir}/%{name}/mtx-changer.conf
%{_mandir}/man8/bacula-sd.8*
%{_mandir}/man8/bcopy.8*
%{_mandir}/man8/bextract.8*
%{_mandir}/man8/bls.8*
%{_mandir}/man8/bscan.8*
%{_mandir}/man8/btape.8*
%{_sbindir}/bacula-sd
%{_sbindir}/bcopy
%{_sbindir}/bextract
%{_sbindir}/bls
%{_sbindir}/bscan
%{_sbindir}/btape
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/bacula-sd.service
%else
%{_initrddir}/bacula-sd
%endif


%files client
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/bacula/bacula-fd.conf %attr(640,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-fd
%{_mandir}/man8/bacula-fd.8*
%{_libdir}/bacula/bpipe-fd.so
%{_sbindir}/bacula-fd
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/bacula-fd.service
%else
%{_initrddir}/bacula-fd
%endif

%files console
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/bacula/bconsole.conf %attr(640,root,root)
%{_mandir}/man8/bconsole.8*
%{_sbindir}/bconsole

%if 0%{?fedora} || 0%{?rhel} >= 6
%files console-bat
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/bacula/bat.conf %attr(640,root,root)
%{_datadir}/applications/bacula-bat.desktop
%{_datadir}/bacula/*.html
%{_datadir}/bacula/*.png
%{_datadir}/pixmaps/bat.png
%{_mandir}/man1/bat.1*
%{_sbindir}/bat

%files traymonitor
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/bacula/tray-monitor.conf %attr(640,root,root)
%{_datadir}/applications/bacula-traymonitor.desktop
%{_datadir}/pixmaps/bacula-tray-monitor.png
%{_mandir}/man1/bacula-tray-monitor.1*
%{_sbindir}/bacula-tray-monitor
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/bacula
%{_libdir}/libbac.so
%{_libdir}/libbaccfg.so
%{_libdir}/libbacfind.so
%{_libdir}/libbacsql.so

%files -n nagios-plugins-bacula
%defattr(-,root,root)
%{_libdir}/nagios/plugins/check_bacula

%changelog
* Fri May 15 2015 Simone Caronni <negativo17@gmail.com> - 7.0.5-7
- Split logwatch files in its own package. Logwatch should be installed
  explicitly by an administrator, and not by defaul. Also, the current logwatch
  package for RHEL 7 has a bug and can not be customized:
  https://bugzilla.redhat.com/show_bug.cgi?id=1221903
  Thanks to Dimitri Maziuk for reporting.

* Tue May 12 2015 Simone Caronni <negativo17@gmail.com> - 7.0.5-6
- Require dejavu-lgc-sans-fonts for graphical programs. Fixes startup of bat on
  headless servers without a desktop installed.

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7.0.5-5
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 02 2015 Simone Caronni <negativo17@gmail.com> - 7.0.5-4
- Fix tray-monitor packaging (again).

* Tue Feb 24 2015 Simone Caronni <negativo17@gmail.com> - 7.0.5-3
- Add license macro.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Simone Caronni <negativo17@gmail.com> - 7.0.5-1
- Update to 7.0.5.

* Thu Jul 24 2014 Simone Caronni <negativo17@gmail.com> - 7.0.4-3
- Remove RPM filters, add back patch inadvertently removed during 7.0 upstream
  release.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Simone Caronni <negativo17@gmail.com> - 7.0.4-1
- Update to 7.0.4.

* Fri May 16 2014 Simone Caronni <negativo17@gmail.com> - 7.0.3-3
- Add versioned library to alternatives system.

* Fri May 16 2014 Simone Caronni <negativo17@gmail.com> - 7.0.3-2
- Filter out libbaccats from auto generated Provides/Obsoletes and add note on
  the libbaccats-x.x.x.so shared object name mess.

* Thu May 15 2014 Simone Caronni <negativo17@gmail.com> - 7.0.3-1
- Update to 7.0.3.

* Thu Apr 24 2014 Simone Caronni <negativo17@gmail.com> - 7.0.2-2
- Bug fixes from upstream.

* Thu Apr 03 2014 Simone Caronni <negativo17@gmail.com> - 7.0.2-1
- Update to 7.0.2, drop upstreamed patches.

* Tue Apr 01 2014 Simone Caronni <negativo17@gmail.com> - 7.0.1-2
- Add patch for Nagios plugin.
- Add missing requirement for Nagios plugin folder.

* Tue Apr 01 2014 Simone Caronni <negativo17@gmail.com> - 7.0.1-1
- Update to 7.0.1; remove Python.
- Drop git patch.

* Sun Mar 30 2014 Simone Caronni <negativo17@gmail.com> - 7.0.0-3
- Update git patch.
- Sort file sections.

* Sun Mar 30 2014 Simone Caronni <negativo17@gmail.com> - 7.0.0-2
- Backport changes from git for QT Tray monitor, Nagios plugin and configure
  script.
- Removed upstream patches.

* Sun Mar 30 2014 Simone Caronni <negativo17@gmail.com> - 7.0.0-1
- Update to 7.0.0.
- Momentarily disable Nagios plugin and QT tray monitor as they don't build
  anymore.

* Tue Aug 06 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-17
- Fix dependencies for devel subpackage.
- Explicitly declare dependency also on libs-sql subpackage where required, so
  we can save one extra cpu cycle during the upgrade (...).
- Bat subpackage used to rely on files in %%_docdir for operation, move them
  elsewhere. Fixes also Fedora 20 unversioned %%_docdir feature.
- Make sure any package combination results in installed license files.

* Tue Aug 06 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-16
- Remove Fedora 17 conditionals, distribution EOL.
- Remove systemd-sysv dependency as per new packaging guidelines.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.2.13-14
- Perl 5.18 rebuild

* Mon Jul 15 2013 Petr Hracek <phracek@redhat.com> - 5.2.13-13
- make dependency of bacula packages on bacula-libs RHEL-7 rpmdiff (#881146)

* Thu Jun 27 2013 Petr Hracek <phracek@redhat.com> - 5.2.13-12
- Correct systemd unitfiles permissions

* Tue May 28 2013 Petr Hracek <phracek@redhat.com> - 5.2.13-11
- Fix for nonfree code (#967417)

* Thu May 16 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-10
- Add aarch64 patch (#925072).
- Add bpluginfo commmand.

* Tue Apr 16 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-9
- Systemd service files cleanup, thanks Michal Schmidt (#952334)

* Mon Apr 08 2013 Petr Hracek <phracek@redhat.com> - 5.2.13-8
- Correcting options and man pages (#948837)

* Mon Apr 08 2013 Petr Hracek <phracek@redhat.com> - 5.2.13-7
- include /var/log/bacula/*.log in logwatch (#924797)

* Mon Mar 04 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-6
- Add mt-st requirement to storage package; update quick start docs.

* Tue Feb 26 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-5
- Improve documentation.

* Mon Feb 25 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-4
- Fix director reload command.
- Adjust to 5.2.13 permission changes.

* Fri Feb 22 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-3
- Renamed README to README.Redhat.

* Thu Feb 21 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-2
- Removed bacula-checkconf stuff.
- Separated postgresql, sqlite3 and mysql how to from README.

* Wed Feb 20 2013 Simone Caronni <negativo17@gmail.com> - 5.2.13-1
- Update to 5.2.13, drop upstreamed patch.
- Remove Fedora 16 (EOL) checks.

* Sun Feb 10 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 5.2.12-9
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247

* Fri Feb 08 2013 Petr Hracek <phracek@redhat.com> - 5.2.12-8
- Fix: (#881146) syntax error in update_postgresql_tables_10_to_11.in

* Mon Feb 04 2013 Petr Hracek <phracek@redhat.com> - 5.2.12-7
- Fix (#905309) e_msg: Process /usr/sbin/bat was killed by signal 11 (SIGSEGV)

* Thu Jan 10 2013 Simone Caronni <negativo17@gmail.com> - 5.2.12-6
- Added missing line in bacula-sd SysV init script.

* Wed Jan 09 2013 Simone Caronni <negativo17@gmail.com> - 5.2.12-5
- Move unversioned libraries into the devel package (#889244).

* Wed Jan 09 2013 Simone Caronni <negativo17@gmail.com> - 5.2.12-4
- Updated SysV init script according to Fedora template:
  https://fedoraproject.org/wiki/Packaging:SysVInitScript

* Wed Oct 17 2012 Simone Caronni <negativo17@gmail.com> - 5.2.12-3
- Add sample-query.sql file to Director's docs.

* Wed Oct 17 2012 Simone Caronni <negativo17@gmail.com> - 5.2.12-2
- Fix fedpkg checks. Requires fedpkg > 1.10:
  http://git.fedorahosted.org/cgit/fedpkg.git/commit/?id=11c46c06a3c9cc2f58d68aea964dd37dc028e349
- Change systemd requirements as per new package guidelines.

* Fri Sep 14 2012 Simone Caronni <negativo17@gmail.com> - 5.2.12-1
- Update to 5.2.12, containing only patches from 5.2.11-4.

* Fri Sep 14 2012 Simone Caronni <negativo17@gmail.com> - 5.2.11-4
- Add a sleep timer for RHEL init scripts restart as Debian does.
  Problems verified on the sd exiting too early on VMs and slow boxes.

* Thu Sep 13 2012 Simone Caronni <negativo17@gmail.com> - 5.2.11-3
- Introduce last minute critical patches.

* Thu Sep 13 2012 Simone Caronni <negativo17@gmail.com> - 5.2.11-2
- Do not remove user on common subpackage uninstall.

* Tue Sep 11 2012 Simone Caronni <negativo17@gmail.com> - 5.2.11-1
- Update to 5.2.11.
- Removed upstreamed patches.
- Updated bat patch.
- Removed useless docs.

* Tue Sep 11 2012 Simone Caronni <negativo17@gmail.com> - 5.2.10-7
- Add Fedora 18 systemd macros.
- Remove old distribution checks.

* Wed Aug 29 2012 Simone Caronni <negativo17@gmail.com> - 5.2.10-6
- Remove user definition during prep so they are not used during the install
  phase (rhbz#852732).
- Enforce permissions in default config files.

* Fri Jul 20 2012 Simone Caronni <negativo17@gmail.com> - 5.2.10-5
- Removed make_catalog_backup bash script, leave only the default perl one (rhbz#456612,665498).

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Simone Caronni <negativo17@gmail.com> - 5.2.10-3
- Updated log path patch (rhbz#837706).

* Tue Jul 10 2012 Simone Caronni <negativo17@gmail.com> - 5.2.10-2
- Add nss-lookup.target as required to service files (rhbz#838828).
- Fix bsmtp upstream bug sending mails to ipv4/ipv6 hosts.

* Mon Jul 02 2012 Simone Caronni <negativo17@gmail.com> - 5.2.10-1
- Update to 5.2.10.

* Tue Jun 19 2012 Simone Caronni <negativo17@gmail.com> - 5.2.9-2
- Remove _isa on BuildRequires.
- Remove useless code in SysV init scripts.

* Tue Jun 12 2012 Simone Caronni <negativo17@gmail.com> - 5.2.9-1
- Update to 5.2.9, remove termlib patch.

* Mon Jun 11 2012 Simone Caronni <negativo17@gmail.com> - 5.2.8-2
- Fix console build on RHEL 5.

* Mon Jun 11 2012 Simone Caronni <negativo17@gmail.com> - 5.2.8-1
- Update to 5.2.8.
- Removed upstram xattr patch.
- Added database backend detection to bacula-libs-sql for upgrades from
  <= 5.0.3-28-fc16 and 5.2.6-1.fc17.

* Fri Jun 08 2012 Simone Caronni <negativo17@gmail.com> - 5.2.7-4
- Make a note about mt-st and mtx (bz#829888).
- Update README.Fedora with current information.
- Fix bacula-sd group on Fedora and RHEL >= 6 (bz#829509).

* Wed Jun 06 2012 Simone Caronni <negativo17@gmail.com> - 5.2.7-3
- Final xattr patch from upstream for bz#819158.
- Switch alternatives to point to the unversioned system libraries.
  Pointed out by the closely related bug #829219.

* Mon Jun 04 2012 Simone Caronni <negativo17@gmail.com> - 5.2.7-2
- Remove python-devel test leftover.
- Updated bat build patch to add support for RHEL 6.

* Mon Jun 04 2012 Simone Caronni <negativo17@gmail.com> - 5.2.7-1
- Updated to 5.2.7, removed patches included upstream.
- Removed python-devel patch, fix included in python package.
- Replaced tabs with blanks in spec file (rpmlint).

* Mon May 28 2012 Simone Caronni <negativo17@gmail.com> - 5.2.6-6
- Even if pulled in by dependencies, re-add explict BR on systemd-units.
- Remove .gz suffix for man pages in file lists as per packaging guidelines.

* Mon May 28 2012 Simone Caronni <negativo17@gmail.com> - 5.2.6-5
- Patch for bug #819158.
- Updated hostname patch with official fix.
- Sorted all BuildRequires and removed useless systemd-units.

* Wed May 23 2012 Simone Caronni <negativo17@gmail.com> - 5.2.6-4
- Added python config workaround for Fedora 16.

* Mon May 21 2012 Simone Caronni <negativo17@gmail.com> - 5.2.6-3
- Removed _install, _mkdir and _make macro.
- Added _isa to BuildRequires.
- Removed lzo-devel option for RHEL 4 (EOL).

* Fri Mar 16 2012 Simone Caronni <negativo17@gmail.com> - 5.2.6-2
- Move libbaccats and libbacsql into bacula-libs-sql package so only
  Director and Storage daemons pull in SQL dependencies:
  http://old.nabble.com/Standalone-client-question-td33495990.html

* Wed Feb 22 2012 Simone Caronni <negativo17@gmail.com> - 5.2.6-1
- Update to 5.2.6.

* Fri Feb 10 2012 Simone Caronni <negativo17@gmail.com> - 5.2.5-3
- WX and gnome console should be upgraded from bconsole, not
  libraries.

* Mon Jan 30 2012 Simone Caronni <negativo17@gmail.com> - 5.2.5-2
- License has changed to AGPLv3 in 5.0.3. Thanks Erinn.
- Fix ldconfig/alternatives symlinks on removal of packages and
  upgrades from recent f15/f16 changes.

* Thu Jan 26 2012 Simone Caronni <negativo17@gmail.com> - 5.2.5-1
- Update to 5.2.5.
- Change the alternative library to the base shared object name
  so the preference set is not lost when changing releases.

* Mon Jan 23 2012 Simone Caronni <negativo17@gmail.com> - 5.2.4-4
- Remove old BuildRequires for bacula-docs.

* Fri Jan 20 2012 Simone Caronni <negativo17@gmail.com> - 5.2.4-3
- Fix for rhbz#728693.

* Fri Jan 20 2012 Simone Caronni <negativo17@gmail.com> - 5.2.4-2
- Close bugs rhbz#708712, rhbz#556669, rhbz#726147

* Wed Jan 18 2012 Simone Caronni <negativo17@gmail.com> - 5.2.4-1
- Update to 5.2.4, rework libbaccats installation as they have
  fixed the soname library problem.

* Thu Jan 12 2012 Simone Caronni <negativo17@gmail.com> - 5.2.3-8
- Fix tray monitor desktop file.

* Wed Jan 11 2012 Simone Caronni <negativo17@gmail.com> - 5.2.3-7
- Split off bacula-docs subpackage.

* Thu Jan 05 2012 Simone Caronni <negativo17@gmail.com> - 5.2.3-6
- Make docs conditional at build for testing.
- Add devel subpackage.

* Tue Jan 03 2012 Simone Caronni <negativo17@gmail.com> - 5.2.3-5
- Trim changelog.
- Merge bacula-director backends and move libbacats alternatives
  to bacula-libs.
- Move bscan to bacula-storage now that is dependent only on
  bacula-libs.
- Added README.Fedora.

* Tue Dec 20 2011 Simone Caronni <negativo17@gmail.com> - 5.2.3-4
- Changing uid from 33 per previous discussion, static uid
  already allocated is 133:
  "cat /usr/share/doc/setup-2.8.36/uidgid | grep bacula"

* Mon Dec 19 2011 Simone Caronni <negativo17@gmail.com> - 5.2.3-3
- Remove fedora-usermgmt entirely, see thread at:
  http://lists.fedoraproject.org/pipermail/packaging/2011-December/008034.html

* Mon Dec 19 2011 Simone Caronni <negativo17@gmail.com> - 5.2.3-2
- Remove leftover users when removing bacula-common.
- Allow building "--without fedora" to avoid RHEL dependency on EPEL:
  http://fedoraproject.org/wiki/PackageUserCreation

* Mon Dec 19 2011 Simone Caronni <negativo17@gmail.com> - 5.2.3-1
- Updated to 5.2.3.
- Remove fedora-usermgmt from libs Requires section.

* Sun Dec 11 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-11
- Add bat html docs so the help button works.
- Minor packaging changes.
- Default permissions on bconsole and bat.
- Use localhost as default on config files instead of patching fake
  example.com hostnames.
- Add QT tray monitor.

* Sat Dec 10 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-10
- Added patch for mysql 5.5.18 from Oliver Falk.

* Wed Dec 07 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-9
- Add sample-query.sql as config file.
- Small log changes.

* Wed Dec 07 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-8
- Fixed building on RHEL/CentOS 4.
- Split out libs package to remove dependency on bacula-common for
  bconsole, bat and check_bacula.
- Fix typo in post scriptlet for director-sqlite.

* Tue Dec 06 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-7
- Added libcap for POSIX.1e capabilities in bacula-fd (5.0.0 feature).
- Allow systemd files to read options set in the sysconfig
  configuration files like SysV scripts to enable capabilities.
- Set capabilities as optional for now.

* Mon Dec 05 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-6
- Removed leftover files and small rpmlint fixes.
- Additional file moves between packages.
- Enabled LZO compression (5.2.1 feature).

* Mon Dec 05 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-5
- Remove redundant user/group in service files.
- Reduce patching for what can be passed through configure.
- Remove dsolink patch, not needed anymore.

* Fri Dec 02 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-4
- Rename storage-common to storage and make it provide storage-common.
- Move bscan to director-common.
- Move storage scripts to storage.
- Add html docs.
- Install dummy catalogue library and mark it as ghost.

* Thu Dec 01 2011 Simone Caronni <negativo17@gmail.com> - 5.2.2-3
- Add missing conditional for bat in the build section.
- Make bat require qt4-devel on build (rhel 5 fix).
- Bumped requirement for qt >= 4.6.2 for 5.2.2.
- Renamed bacula-config.patch to bacula-5.2.2-config.patch as it
  always changes.
- Fix installation of bat and check_bacula binaries. Enabling
  libtool for bpipe-fd.so produces binaries under .libs.
- Removed fedora-usermgmt requirement for director-common.
- Removed examples from docs and make them "noarch".
- Fix bacula-console requirements.
- Fix nagios plugin summary.
- Removed checkconf functions from SysV init files and replace
  the call with the script used in systemd service files. Make
  the script available in all builds.
- Make docs NoArch where supported.

* Thu Dec  1 2011 Tom Callaway <spot@fedoraproject.org> - 5.2.2-2
- resolve broken dependency issues

* Tue Nov 29 2011 Tom Callaway <spot@fedoraproject.org> - 5.2.2-1
- Update to 5.2.2
- minor spec cleanups, conditionalized support for systemd

* Fri Nov 04 2011 Simone Caronni <negativo17@gmail.com> - 5.2.1-1
- Updated to 5.2.1.
- Reworked and removed some patches for 5.2.1 codebase.
- Reworked bat installation.
- Removed sqlite2 support.
- Removed all the fancy database backend rebuilding.
- Disabled libtool for bpipe-fd.so.
- Passed plugins dir as libdir/bacula.
- Added sql libs to alternatives.
- Disabled traymonitor.
- Minor fixes to spec file, rpmlint fixes.
- Nagios patch for Enterprise FDs.
- Removed all gui/web stuff.
- Removed a lot of comments.
- Conditional on Fedora 11 / RHEL 6 for bat build.
- Obsolete bacula-sysconfdir.
- Removed bwxconsole.
