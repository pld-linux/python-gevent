
# TODO:
#	- test__core_stat.py fails on 32-bit builds with system libev
#	  investigate/fix that and enable system libev
#
#	- investigate some other failing tests
#	  (now excluded via known_failures-pld.patch)

# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# testing
%bcond_with	system_libev	# system libev [test__core_stat.py test fails]
%bcond_without	system_c_ares	# system c_ares
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module

%define	module	gevent
Summary:	A coroutine-based Python 2 networking library
Summary(pl.UTF-8):	Biblioteka sieciowa dla Pythona 2 oparta na korutynach
Name:		python-%{module}
Version:	21.12.0
Release:	6
Epoch:		1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/gevent/
Source0:	https://files.pythonhosted.org/packages/source/g/gevent/%{module}-%{version}.tar.gz
# Source0-md5:	84014946a25407706cbe9ecb088f1e9c
Patch0:		%{name}-sphinx-python3.patch
Patch1:		known_failures-pld.patch
URL:		http://www.gevent.org/
%{?with_system_c_ares:BuildRequires:	c-ares-devel >= 1.10.0}
%{?with_system_libev:BuildRequires:	libev-devel >= 4.23}
%if %{with python2}
BuildRequires:	python-Cython >= 0.29
BuildRequires:	python-cffi >= 1.12.2
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-greenlet-devel >= 1.1.0
BuildRequires:	python-greenlet-devel < 2
BuildRequires:	python-setuptools >= 1:24.2.0
%if %{with tests}
BuildRequires:	python-coverage >= 4.0
BuildRequires:	python-devel-src >= 1:2.7
BuildRequires:	python-dns >= 1.16.0
BuildRequires:	python-dns < 2
BuildRequires:	python-futures
BuildRequires:	python-greenlet >= 1.1.0
BuildRequires:	python-greenlet < 2
BuildRequires:  python-idna
BuildRequires:  python-mock
BuildRequires:  python-objgraph
BuildRequires:  python-psutil >= 5.7.0
BuildRequires:  python-requests
BuildRequires:	python-test
BuildRequires:	python-zope.event
BuildRequires:	python-zope.interface
%endif
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.29
BuildRequires:	python3-cffi >= 1.12.2
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-greenlet-devel >= 1.1.0
BuildRequires:	python3-greenlet-devel < 2
BuildRequires:	python3-setuptools >= 1:24.2.0
%if %{with tests}
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-dns >= 1.16.0
#BuildRequires:	python3-dns < 2
BuildRequires:	python3-greenlet >= 1.1.0
BuildRequires:	python3-greenlet < 2
BuildRequires:  python3-idna
BuildRequires:  python3-objgraph
BuildRequires:  python3-psutil >= 5.7.0
BuildRequires:  python3-requests
BuildRequires:	python3-test
BuildRequires:	python3-zope.event
BuildRequires:	python3-zope.interface
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	python3-sphinxcontrib-programoutput
BuildRequires:	sphinx-pdg-3
%endif
%{?with_system_libev:Requires:	libev >= 4.23}
Requires:	python-greenlet >= 1.1.0
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
Requires:	python-greenlet >= 1.1.0

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

%package apidocs
Summary:	API documentation for Python gevent module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona gevent
Group:		Documentation

%description apidocs
API documentation for Python gevent module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona gevent.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1
#%patch1 -p1

find . -type f -name '*.orig' | xargs -r %{__rm}

# force rebuild of Cython-generated files
# they depend on specific deps (e.g. greenlet) versions
%{__rm} src/gevent/{*.c,resolver/cares.c}

%build
# must be exported to work (py*_build macro is not single invocation)
%{?with_system_libev:export LIBEV_EMBED=false}
%{?with_system_c_ares:export CARES_EMBED=false}

%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(echo $PWD/build-2/lib.*) \
%{__python} -m gevent.tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $PWD/build-3/lib.*) \
%{__python3} -m gevent.tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(echo $PWD/build-3/lib.*) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{?with_system_libev:export LIBEV_EMBED=false}
%{?with_system_c_ares:export CARES_EMBED=false}

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/gevent/{testing,tests}
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/gevent/{testing,tests}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.rst LICENSE NOTICE README.rst TODO
%dir %{py_sitedir}/gevent
%attr(755,root,root) %{py_sitedir}/gevent/*.so
%{py_sitedir}/gevent/*.py[co]
%dir %{py_sitedir}/gevent/_ffi
%{py_sitedir}/gevent/_ffi/*.py[co]
%dir %{py_sitedir}/gevent/libev
%attr(755,root,root) %{py_sitedir}/gevent/libev/_corecffi.so
%attr(755,root,root) %{py_sitedir}/gevent/libev/corecext.so
%{py_sitedir}/gevent/libev/*.py[co]
%dir %{py_sitedir}/gevent/libuv
%{py_sitedir}/gevent/libuv/*.py[co]
%attr(755,root,root) %{py_sitedir}/gevent/libuv/_corecffi.so
%dir %{py_sitedir}/gevent/resolver
%{py_sitedir}/gevent/resolver/*.py[co]
%attr(755,root,root) %{py_sitedir}/gevent/resolver/cares.so
%{py_sitedir}/gevent-%{version}-py%{py_ver}.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.rst LICENSE NOTICE README.rst TODO
%dir %{py3_sitedir}/gevent
%attr(755,root,root) %{py3_sitedir}/gevent/*.cpython-*.so
%{py3_sitedir}/gevent/__pycache__
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
%{py3_sitedir}/gevent/libev/*.py
%dir %{py3_sitedir}/gevent/resolver
%{py3_sitedir}/gevent/resolver/__pycache__
%{py3_sitedir}/gevent/resolver/*.py
%attr(755,root,root) %{py3_sitedir}/gevent/resolver/cares.*.so
%{py3_sitedir}/gevent-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,development,examples,*.html,*.js}
%endif
