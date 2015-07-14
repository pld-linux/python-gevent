
# TODO:
#	- test__core_stat.py fails on 32-bit builds with system libev
#	  investigate/fix that and enable system libev
#
#	- investigate some other failing tests
#	  (now excluded via known_failures-pld.patch)

# Conditional build:
%bcond_without	tests	# do not run tests
%bcond_with	system_libev	# build with system libev (more tests will fail)
%bcond_without	system_c_ares	# build with system c_ares

%define     module  gevent
Summary:	A coroutine-based Python networking library
Name:		python-%{module}
Version:	1.0.2
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://pypi.python.org/packages/source/g/gevent/%{module}-%{version}.tar.gz
# Source0-md5:	117f135d57ca7416203fba3720bf71c1
Patch0:		known_failures-pld.patch
URL:		http://www.gevent.org/
%{?with_system_c_ares:BuildRequires:	c-ares-devel >= 1.10.0}
%{?with_system_libev:BuildRequires:	libev-devel >= 4.11}
#BuildRequires:	python-Cython
BuildRequires:	python-devel
%if %{with tests}
BuildRequires:	python-devel-src
BuildRequires:	python-greenlet >= 0.3.2
BuildRequires:	python-test
BuildRequires:	rpmbuild(macros) >= 1.688
%endif
BuildRequires:	rpm-pythonprov
Requires:	python-greenlet >= 0.3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gevent is a coroutine-based Python networking library.

Features include:

- Fast event loop based on libev.
- Lightweight execution units based on greenlet.
- Familiar API that re-uses concepts from the Python standard library.
- Cooperative sockets with SSL support.
- DNS queries performed through c-ares or a threadpool.
- Ability to use standard library and 3rd party modules written for
  standard blocking sockets

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
# when Cython-generated files are to be rebuilt
# (BR: python-Cython must be enabled then too)
# ln -s Makefile.ext Makefile

CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{?with_system_libev:LIBEV_EMBED=false} \
%{?with_system_c_ares:CARES_EMBED=false} \
%{__python} setup.py build

%if %{with tests}
cd greentest
PYTHONPATH=.. python testrunner.py --config ../known_failures.py
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{?with_system_libev:LIBEV_EMBED=false} \
%{?with_system_c_ares:CARES_EMBED=false} \
%{__python} setup.py install \
    --skip-build \
    --optimize=2 \
    --root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_semaphore.so
%attr(755,root,root) %{py_sitedir}/%{module}/_util.so
%attr(755,root,root) %{py_sitedir}/%{module}/ares.so
%attr(755,root,root) %{py_sitedir}/%{module}/core.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-%{version}-py%{py_ver}.egg-info
%endif
