
# TODO:
#	- test__core_stat.py fails on 32-bit builds with system libev
#	  investigate/fix that and enable system libev
#
#	- investigate some other failing tests
#	  (now excluded via known_failures-pld.patch)

# Conditional build:
%bcond_without	tests		# do not run tests
%bcond_with	system_libev	# build with system libev [test__core_stat.py test fails]
%bcond_without	system_c_ares	# build with system c_ares
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module

%define	module	gevent
Summary:	A coroutine-based Python 2 networking library
Summary(pl.UTF-8):	Biblioteka sieciowa dla Pythona 2 oparta na korutynach
Name:		python-%{module}
Version:	1.3.4
Release:	1
Epoch:		1
License:	MIT
Group:		Development/Languages
#Source0Download: https://pypi.python.org/simple/gevent
Source0:	https://files.pythonhosted.org/packages/source/g/gevent/%{module}-%{version}.tar.gz
# Source0-md5:	97deaf53196ba430808e8f18b731112a
Patch0:		known_failures-pld.patch
Patch1:		%{name}-tests.patch
URL:		http://www.gevent.org/
%{?with_system_c_ares:BuildRequires:	c-ares-devel >= 1.10.0}
%{?with_system_libev:BuildRequires:	libev-devel >= 4.23}
# if cpython generated files need rebuild
#BuildRequires:	python-Cython >= 0.25.1
%if %{with python2}
BuildRequires:	python-cffi >= 1.3.0
BuildRequires:	python-devel >= 1:2.7
%if %{with tests}
BuildRequires:	python-coverage >= 4.0
BuildRequires:	python-devel-src >= 1:2.7
BuildRequires:	python-greenlet >= 0.4.10
BuildRequires:  python-objgraph
BuildRequires:	python-setuptools
BuildRequires:	python-test
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cffi >= 1.3.0
BuildRequires:	python3-devel >= 1:3.3
%if %{with tests}
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-greenlet >= 0.4.10
BuildRequires:  python3-objgraph
BuildRequires:	python3-setuptools
BuildRequires:	python3-test
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%{?with_system_libev:Requires:	libev >= 4.23}
Requires:	python-greenlet >= 0.4.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gevent is a coroutine-based Python networking library. Features
include:
- Fast event loop based on libev.
- Lightweight execution units based on greenlet.
- Familiar API that re-uses concepts from the Python standard library.
- Cooperative sockets with SSL support.
- DNS queries performed through c-ares or a threadpool.
- Ability to use standard library and 3rd party modules written for
  standard blocking sockets.

%description -l pl.UTF-8
gevent to biblioteka sieciowa dla Pythona oparta na korutynach. Jej
możliwości to m.in.
- szybka pętla zdarzeń oparta na libev
- lekkie jednostki wykonywania oparte na bibliotece greenlet
- znajome API wykorzystujące koncepty biblioteki standardowej Pythona
- gniazda kooperatywne z obsługą SSL
- zapytania DNS wykonywane przez bibliotekę c-ares lub pulę wątków
- możliwość wykorzystania biblioteki standardowej lub modułów innych
  producentów napisanych dla standardowych gniazd blokujących

%package -n python3-%{module}
Summary:	A coroutine-based Python 3 networking library
Summary(pl.UTF-8):	Biblioteka sieciowa dla Pythona 3 oparta na korutynach
Group:		Libraries/Python
%{?with_system_libev:Requires:	libev >= 4.23}
Requires:	python-greenlet >= 0.4.10

%description -n python3-%{module}
gevent is a coroutine-based Python networking library. Features
include:
- Fast event loop based on libev.
- Lightweight execution units based on greenlet.
- Familiar API that re-uses concepts from the Python standard library.
- Cooperative sockets with SSL support.
- DNS queries performed through c-ares or a threadpool.
- Ability to use standard library and 3rd party modules written for
  standard blocking sockets

%description -n python3-%{module} -l pl.UTF-8
gevent to biblioteka sieciowa dla Pythona oparta na korutynach. Jej
możliwości to m.in.
- szybka pętla zdarzeń oparta na libev
- lekkie jednostki wykonywania oparte na bibliotece greenlet
- znajome API wykorzystujące koncepty biblioteki standardowej Pythona
- gniazda kooperatywne z obsługą SSL
- zapytania DNS wykonywane przez bibliotekę c-ares lub pulę wątków
- możliwość wykorzystania biblioteki standardowej lub modułów innych
  producentów napisanych dla standardowych gniazd blokujących

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1 -b .orig

%build
# when Cython-generated files are to be rebuilt
# (BR: python-Cython must be enabled then too)
# ln -s Makefile.ext Makefile

# must be exported to work (py*_build macro is not single invocation)
%{?with_system_libev:export LIBEV_EMBED=false}
%{?with_system_c_ares:export CARES_EMBED=false}

%if %{with python2}
%py_build

%if %{with tests}
PKGDIR=$(echo $PWD/build-2/lib.*)
cd src/greentest
PYTHONPATH=$PKGDIR %{__python} testrunner.py --config known_failures.py
cd ../..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PKGDIR=$(echo $PWD/build-3/lib.*)
cd src/greentest
PYTHONPATH=$PKGDIR %{__python3} testrunner.py --config known_failures.py
cd ../..
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{?with_system_libev:export LIBEV_EMBED=false}
%{?with_system_c_ares:export CARES_EMBED=false}

%if %{with python2}
%py_install

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gevent/*.c
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gevent/*/*.{c,h,pyx}
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/gevent/*.c
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/gevent/*/*.{c,h,pyx}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NOTICE README.rst TODO
%dir %{py_sitedir}/gevent
%attr(755,root,root) %{py_sitedir}/gevent/*.so
%{py_sitedir}/gevent/*.pxd
%{py_sitedir}/gevent/*.py[co]
%dir %{py_sitedir}/gevent/_ffi
%{py_sitedir}/gevent/_ffi/*.py[co]
%dir %{py_sitedir}/gevent/libev
%attr(755,root,root) %{py_sitedir}/gevent/libev/_corecffi.so
%attr(755,root,root) %{py_sitedir}/gevent/libev/corecext.so
%{py_sitedir}/gevent/libev/libev.pxd
%{py_sitedir}/gevent/libev/*.py[co]
%dir %{py_sitedir}/gevent/libuv
%{py_sitedir}/gevent/libuv/*.py[co]
%attr(755,root,root) %{py_sitedir}/gevent/libuv/_corecffi.so
%dir %{py_sitedir}/gevent/resolver
%{py_sitedir}/gevent/resolver/libcares.pxd
%{py_sitedir}/gevent/resolver/*.py[co]
%attr(755,root,root) %{py_sitedir}/gevent/resolver/cares.so
%{py_sitedir}/gevent-%{version}-py%{py_ver}.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NOTICE README.rst TODO
%dir %{py3_sitedir}/gevent
%attr(755,root,root) %{py3_sitedir}/gevent/*.cpython-*.so
%{py3_sitedir}/gevent/__pycache__
%{py3_sitedir}/gevent/*.pxd
%{py3_sitedir}/gevent/*.py
%dir %{py3_sitedir}/gevent/_ffi
%{py3_sitedir}/gevent/_ffi/__pycache__
%{py3_sitedir}/gevent/_ffi/*.py
%dir %{py3_sitedir}/gevent/libuv
%{py3_sitedir}/gevent/libuv/__pycache__
%{py3_sitedir}/gevent/libuv/*.py
%attr(755,root,root) %{py3_sitedir}/gevent/libuv/_corecffi.*.so
%dir %{py3_sitedir}/gevent/libev
%attr(755,root,root) %{py3_sitedir}/gevent/libev/_corecffi.abi3.so
%attr(755,root,root) %{py3_sitedir}/gevent/libev/corecext.cpython-*.so
%{py3_sitedir}/gevent/libev/__pycache__
%{py3_sitedir}/gevent/libev/libev.pxd
%{py3_sitedir}/gevent/libev/*.py
%dir %{py3_sitedir}/gevent/resolver
%{py3_sitedir}/gevent/resolver/__pycache__
%{py3_sitedir}/gevent/resolver/*.py
%{py3_sitedir}/gevent/resolver/libcares.pxd
%attr(755,root,root) %{py3_sitedir}/gevent/resolver/cares.*.so
%{py3_sitedir}/gevent-%{version}-py*.egg-info
%endif
