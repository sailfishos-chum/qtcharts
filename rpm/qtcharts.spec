%global qt_version 5.15.8

Summary: Qt5 - Charts component
Name:    opt-qt5-qtcharts
Version: 5.15.8
Release: 1%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: %{name}-%{version}.tar.bz2

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtdeclarative-devel >= %{qt_version}

%description
Qt Charts module provides a set of easy to use chart components. It uses the Qt Graphics View Framework, therefore charts can be easily
integrated to modern user interfaces. Qt Charts can be used as QWidgets, QGraphicsWidget, or QML types.
Users can easily create impressive graphs by selecting one of the charts themes.

%package devel
Summary: Development files for %{name}
Requires: opt-qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream


%build

export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5}

# have to restart build several times due to bug in sb2
%make_build  -k || chmod -R ugo+r . || true
%make_build

# bug in sb2 leading to 000 permission in some generated plugins.qmltypes files
chmod -R ugo+r .


%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.GPL3
%{_opt_qt5_libdir}/libQt5Charts.so.5*
%{_opt_qt5_qmldir}/QtCharts/

%files devel
%{_opt_qt5_headerdir}/QtCharts/
%{_opt_qt5_libdir}/libQt5Charts.so
%{_opt_qt5_libdir}/libQt5Charts.prl
%{_opt_qt5_libdir}/cmake/Qt5Charts/
%{_opt_qt5_libdir}/pkgconfig/Qt5Charts.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/*
