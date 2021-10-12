%global with_openmpi 0
%global with_mpich 1
%if 0%{?rhel} && 0%{?rhel} <= 6
%ifarch ppc64
%global with_mpich 0
%endif
%endif

%global with_python3 1
%if (0%{?suse_version} >= 1500)
%global python3_pkgversion 3
%global _mpich_load \
 module load gnu-mpich; \
 export CFLAGS="$CFLAGS %{optflags}";
%global _mpich_unload \
 module unload gnu-mpich;
%endif

%global python3_runtime python%{python3_pkgversion}-mpi4py-runtime = %{version}-%{release}
%global python2_runtime mpi4py-runtime = %{version}-%{release}

### TESTSUITE ###
# The testsuite currently fails only on the buildsystem, but works localy.
# So to easily enable/disable the testsuite, the following variables are
# introduced:
#
# * MPICH:     if '1' enable mpich
# * OPENMPI:   if '1' enable openmpi
%ifarch %{arm}
# Disable tests on arm until upstream bug is fixed:
# https://bitbucket.org/mpi4py/mpi4py/issues/145
%global MPICH 0
%else
%global MPICH 1
%global OPENMPI 1
%endif
# Run full testsuite or just with 1 core
%global FULLTESTS 0

#global commit 39ca784226460f9e519507269ebb29635dc8bd90
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:12})}

Name:           mpi4py
Version:        3.0.3
Release:        2%{?commit:.git%{shortcommit}}%{?dist}
Summary:        Python bindings of the Message Passing Interface (MPI)

License:        BSD
URL:            https://mpi4py.readthedocs.io/en/stable/
%if %{defined commit}
Source0:        https://bitbucket.org/mpi4py/mpi4py/get/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://bitbucket.org/mpi4py/mpi4py/downloads/mpi4py-%{version}.tar.gz
%endif
# openmpi at fedora is build without threads. Use that default here too.
# See also #1105902.
Patch1:         mpi4py-2.0.0-openmpi-threading.patch

BuildRequires:  python2-devel
%if (0%{?suse_version} >= 1500)
BuildRequires: lua-lmod
%else
BuildRequires: environment-modules
%endif
BuildRequires:  ed
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  Cython
%else
BuildRequires:  python2-Cython >= 0.22
%endif
%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-Cython >= 0.22
%endif


%description
This package is constructed on top of the MPI-1/MPI-2 specification and
provides an object oriented interface which closely follows MPI-2 C++
bindings. It supports point-to-point (sends, receives) and collective
(broadcasts, scatters, gathers) communications of any picklable Python
object as well as optimized communications of Python object exposing the
single-segment buffer interface (NumPy arrays, built-in bytes/string/array
objects).

%package -n python2-mpi4py
Requires:       %{name}-common = %{version}-%{release}
Summary:        Python 2 bindings of the Message Passing Interface (MPI)
%{?python_provide:%python_provide python2-mpi4py}
%description -n python2-mpi4py
This package is constructed on top of the MPI-1/MPI-2 specification and
provides an object oriented interface which closely follows MPI-2 C++
bindings. It supports point-to-point (sends, receives) and collective
(broadcasts, scatters, gathers) communications of any picklable Python
object as well as optimized communications of Python object exposing the
single-segment buffer interface (NumPy arrays, built-in bytes/string/array
objects).

%package docs
Summary:        Documentation for %{name}
Requires:       %{name}-common = %{version}-%{release}
BuildArch:      noarch
%description docs
This package contains the documentation and examples for %{name}.

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-mpi4py
Requires:       %{name}-common = %{version}-%{release}
Summary:        Python %{python3_version} bindings of the Message Passing Interface (MPI)
%{?python_provide:%python_provide python%{python3_pkgversion}-mpi4py}
%description -n python%{python3_pkgversion}-mpi4py
This package is constructed on top of the MPI-1/MPI-2 specification and
provides an object oriented interface which closely follows MPI-2 C++
bindings. It supports point-to-point (sends, receives) and collective
(broadcasts, scatters, gathers) communications of any picklable Python
object as well as optimized communications of Python object exposing the
single-segment buffer interface (NumPy arrays, built-in bytes/string/array
objects).

%if %{with_openmpi}
%package -n python%{python3_pkgversion}-mpi4py-openmpi
BuildRequires:  openmpi-devel
Requires:       %{name}-common = %{version}-%{release}
Requires:       python%{python3_pkgversion}-openmpi%{?_isa}
Summary:        Python %{python3_version} bindings of MPI, Open MPI version
Provides:       python%{python3_pkgversion}-mpi4py-runtime = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-mpi4py-openmpi}
%description -n python%{python3_pkgversion}-mpi4py-openmpi
This package is constructed on top of the MPI-1/MPI-2 specification and
provides an object oriented interface which closely follows MPI-2 C++
bindings. It supports point-to-point (sends, receives) and collective
(broadcasts, scatters, gathers) communications of any picklable Python
object as well as optimized communications of Python object exposing the
single-segment buffer interface (NumPy arrays, built-in bytes/string/array
objects).

This package contains %{name} compiled against Open MPI.
%endif


%if %{with_mpich}
%package -n python%{python3_pkgversion}-mpi4py-mpich
BuildRequires:  mpich-devel
Requires:       %{name}-common = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires:       python%{python3_pkgversion}-mpich%{?_isa}
%endif
Summary:        Python %{python3_version} bindings of MPI, MPICH version
Provides:       python%{python3_pkgversion}-mpi4py-runtime = %{version}-%{release}
Provides:       python%{python3_pkgversion}-%{name}-mpich2 = %{version}-%{release}
Obsoletes:      python%{python3_pkgversion}-%{name}-mpich2 < 1.3-8
%{?python_provide:%python_provide python%{python3_pkgversion}-mpi4py-mpich}
%description -n python%{python3_pkgversion}-mpi4py-mpich
This package is constructed on top of the MPI-1/MPI-2 specification and
provides an object oriented interface which closely follows MPI-2 C++
bindings. It supports point-to-point (sends, receives) and collective
(broadcasts, scatters, gathers) communications of any picklable Python
object as well as optimized communications of Python object exposing the
single-segment buffer interface (NumPy arrays, built-in bytes/string/array
objects).

This package contains %{name} compiled against MPICH.
%endif
%endif

%package common
Summary:        Common files for mpi4py packages
BuildArch:      noarch
Requires:       %{name}-common = %{version}-%{release}
%description common
This package contains the license file shard between the subpackages of %{name}.

%package -n python2-mpi4py-tests
Summary:        Python 2 tests for mpi4py packages
BuildArch:      noarch
Requires:       %{python2_runtime}
Provides:       %{name}-tests = %{version}-%{release}
Obsoletes:      %{name}-tests < %{version}-%{release}
%description -n python2-mpi4py-tests
This package contains the Python 2 tests for %{name}.

%package -n python%{python3_pkgversion}-mpi4py-tests
Summary:        Python 3 tests for mpi4py packages
BuildArch:      noarch
Requires:       %{python3_runtime}
%description -n python%{python3_pkgversion}-mpi4py-tests
This package contains the Python 3 tests for %{name}.

%if %{with_openmpi}
%package -n python2-mpi4py-openmpi
BuildRequires:  openmpi-devel
Requires:       %{name}-common = %{version}-%{release}
Requires:       python2-openmpi%{?_isa}
Summary:        Python 2 bindings of MPI, Open MPI version
Provides:       mpi4py-runtime = %{version}-%{release}
# Old mpi4py-foo provides added at F24
Provides:       mpi4py-openmpi = %{version}-%{release}
Obsoletes:      mpi4py-openmpi < 1.3.1-16
%{?python_provide:%python_provide python2-mpi4py-openmpi}
%description -n python2-mpi4py-openmpi
This package is constructed on top of the MPI-1/MPI-2 specification and
provides an object oriented interface which closely follows MPI-2 C++
bindings. It supports point-to-point (sends, receives) and collective
(broadcasts, scatters, gathers) communications of any picklable Python
object as well as optimized communications of Python object exposing the
single-segment buffer interface (NumPy arrays, built-in bytes/string/array
objects).

This package contains %{name} compiled against Open MPI.
%endif


%if %{with_mpich}
%package -n python2-mpi4py-mpich
BuildRequires:  mpich-devel
Requires:       %{name}-common = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires:       python2-mpich%{?_isa}
%endif
Summary:        Python 2 bindings of MPI, MPICH version
Provides:       mpi4py-runtime = %{version}-%{release}
Provides:       %{name}-mpich2 = %{version}-%{release}
Obsoletes:      %{name}-mpich2 < 1.3-8
Provides:       mpi4py-mpich = %{version}-%{release}
Obsoletes:      mpi4py-mpich < 1.3.1-16
%{?python_provide:%python_provide python2-mpi4py-mpich}
%description -n python2-mpi4py-mpich
This package is constructed on top of the MPI-1/MPI-2 specification and
provides an object oriented interface which closely follows MPI-2 C++
bindings. It supports point-to-point (sends, receives) and collective
(broadcasts, scatters, gathers) communications of any picklable Python
object as well as optimized communications of Python object exposing the
single-segment buffer interface (NumPy arrays, built-in bytes/string/array
objects).

This package contains %{name} compiled against MPICH.
%endif


%prep
%setup -q %{?commit:-n %{name}-%{name}-%{shortcommit}}
# delete docs/source
# this is just needed to generate docs/*
rm -r docs/source

# work around "wrong-file-end-of-line-encoding"
for file in $(find | grep runtests.bat); do
    sed -i 's/\r//' $file
done

# Save current src/__init__.py for mpich
cp src/mpi4py/__init__.py .__init__mpich.py
%patch1 -p1
cp src/mpi4py/__init__.py .__init__openmpi.py


%build
# Build parallel versions: set compiler variables to MPI wrappers
export CC=mpicc
export CXX=mpicxx

%if %{with_openmpi}
# Build OpenMPI version
%{_openmpi_load}
cp .__init__openmpi.py src/mpi4py/__init__.py
%py2_build
mv build openmpi
%{_openmpi_unload}
%endif

%if %{with_mpich}
# Build mpich version
%{_mpich_load}
cp .__init__mpich.py src/mpi4py/__init__.py
%py2_build
mv build mpich
%{_mpich_unload}
%endif

%if 0%{?with_python3}
# Build parallel versions: set compiler variables to MPI wrappers
export CC=mpicc
export CXX=mpicxx

%if %{with_openmpi}
# Build OpenMPI version
%{_openmpi_load}
cp .__init__openmpi.py src/mpi4py/__init__.py
mv openmpi build
%py3_build
mv build openmpi
%{_openmpi_unload}
%endif

%if %{with_mpich}
# Build mpich version
%{_mpich_load}
cp .__init__mpich.py src/mpi4py/__init__.py
mv mpich build
%py3_build
mv build mpich
%{_mpich_unload}
%endif

%endif


%install
%if %{with_openmpi}
# Install OpenMPI version
%{_openmpi_load}
cp .__init__openmpi.py src/mpi4py/__init__.py
mv openmpi build
%py2_install
mkdir -p %{buildroot}%{python2_sitearch}/openmpi
mv %{buildroot}%{python2_sitearch}/%{name}/ %{buildroot}%{python2_sitearch}/%{name}*.egg-info %{buildroot}%{python2_sitearch}/openmpi
mv build openmpi
%{_openmpi_unload}
%endif

%if %{with_mpich}
# Install MPICH version
%{_mpich_load}
cp .__init__mpich.py src/mpi4py/__init__.py
mv mpich build
%py2_install
mkdir -p %{buildroot}%{python2_sitearch}/mpich
mv %{buildroot}%{python2_sitearch}/%{name}/ %{buildroot}%{python2_sitearch}/%{name}*.egg-info %{buildroot}%{python2_sitearch}/mpich
mv build mpich
%{_mpich_unload}
%endif


%if 0%{?with_python3}
%if %{with_openmpi}
# Install OpenMPI version
%{_openmpi_load}
cp .__init__openmpi.py src/mpi4py/__init__.py
mv openmpi build
%py3_install
mkdir -p %{buildroot}%{python3_sitearch}/openmpi
mv %{buildroot}%{python3_sitearch}/%{name}/ %{buildroot}%{python3_sitearch}/%{name}*.egg-info %{buildroot}%{python3_sitearch}/openmpi
mv build openmpi
%{_openmpi_unload}
%endif

%if %{with_mpich}
# Install MPICH version
%{_mpich_load}
cp .__init__mpich.py src/mpi4py/__init__.py
mv mpich build
%py3_install
mkdir -p %{buildroot}%{python3_sitearch}/mpich
mv %{buildroot}%{python3_sitearch}/%{name}/ %{buildroot}%{python3_sitearch}/%{name}*.egg-info %{buildroot}%{python3_sitearch}/mpich
mv build mpich
%{_mpich_unload}
%endif

for py_site_arch in %{python2_sitearch} %{python3_sitearch}; do
    mkdir -p %{buildroot}/$py_site_arch/%{name}/tests
    install -m 0755 test/test_io.py %{buildroot}/$py_site_arch/%{name}/tests/test_io_daos.py
    for file in mpiunittest arrayimpl; do
        install -m 0644 test/$file.py %{buildroot}/$py_site_arch/%{name}/tests/
    done
    ed <<EOF %{buildroot}/$py_site_arch/%{name}/tests/test_io_daos.py
/^import arrayimpl/a
import uuid
.
/^        if comm.Get_rank() == 0:/a
            fname = str(uuid.uuid4())
            fname = "daos:/"+self.prefix+fname
.
/^            fd, fname = tempfile.mkstemp(prefix=self.prefix)/d
/^            os.close(fd)/d
/^    def testReadWriteShared(self):/;/^$/d
/^    def testIReadIWriteShared(self):/;/^$/d
/^    def testReadWriteOrdered(self):/;/^$/d
/^    def testReadWriteOrderedBeginEnd(self):/;/^$/d
wq
EOF
done
%endif


%check
%if %{with_openmpi}
# test openmpi?
%if 0%{?OPENMPI}
%{_openmpi_load}
cp .__init__openmpi.py src/mpi4py/__init__.py
mv openmpi build
PYTHONPATH=%{buildroot}%{python2_sitearch}/openmpi \
    mpiexec -n 1 python2 test/runtests.py -v --no-builddir --thread-level=serialized -e spawn
%if 0%{?FULLTESTS}
PYTHONPATH=%{buildroot}%{python2_sitearch}/openmpi \
    mpiexec -n 5 python2 test/runtests.py -v --no-builddir -e spawn
PYTHONPATH=%{buildroot}%{python2_sitearch}/openmpi \
    mpiexec -n 8 python2 test/runtests.py -v --no-builddir -e spawn
%endif
mv build openmpi
%{_openmpi_unload}
%endif
%endif

# test mpich?
%if 0%{?MPICH}
%if %{with_mpich}
%{_mpich_load}
cp .__init__mpich.py src/mpi4py/__init__.py
mv mpich build
PYTHONPATH=%{buildroot}%{python2_sitearch}/mpich \
    mpiexec -n 1 python2 test/runtests.py -v --no-builddir -e spawn
%if 0%{?FULLTESTS}
PYTHONPATH=%{buildroot}%{python2_sitearch}/mpich \
    mpiexec -n 5 python2 test/runtests.py -v --no-builddir -e spawn
PYTHONPATH=%{buildroot}%{python2_sitearch}/mpich \
    mpiexec -n 8 python2 test/runtests.py -v --no-builddir -e spawn
%endif
mv build mpich
%{_mpich_unload}
%endif
%endif

%if 0%{?with_python3}
%if %{with_openmpi}
# test openmpi?
%if 0%{?OPENMPI}
%{_openmpi_load}
cp .__init__openmpi.py src/mpi4py/__init__.py
mv openmpi build
PYTHONPATH=%{buildroot}%{python3_sitearch}/openmpi \
    mpiexec -np 1 python3 test/runtests.py -v --no-builddir --thread-level=serialized -e spawn
%if 0%{?FULLTESTS}
PYTHONPATH=%{buildroot}%{python3_sitearch}/openmpi \
    mpiexec -np 5 python3 test/runtests.py -v --no-builddir -e spawn
PYTHONPATH=%{buildroot}%{python3_sitearch}/openmpi \
    mpiexec -np 8 python3 test/runtests.py -v --no-builddir -e spawn
%endif
mv build openmpi
%{_openmpi_unload}
%endif
%endif

# test mpich?
%if 0%{?MPICH}
%if %{with_mpich}
%{_mpich_load}
cp .__init__mpich.py src/mpi4py/__init__.py
mv mpich build
PYTHONPATH=%{buildroot}%{python3_sitearch}/mpich \
    mpiexec -np 1 python3 test/runtests.py -v --no-builddir -e spawn
%if 0%{?FULLTESTS}
PYTHONPATH=%{buildroot}%{python3_sitearch}/mpich \
    mpiexec -np 5 python3 test/runtests.py -v --no-builddir -e spawn
PYTHONPATH=%{buildroot}%{python3_sitearch}/mpich \
    mpiexec -np 8 python3 test/runtests.py -v --no-builddir -e spawn
%endif
mv build mpich
%{_mpich_unload}
%endif
%endif
%endif


%files common
%license LICENSE.rst
%doc CHANGES.rst DESCRIPTION.rst README.rst

%files -n python2-mpi4py-tests
%{python2_sitearch}/%{name}/tests

%files -n python%{python3_pkgversion}-mpi4py-tests
%{python3_sitearch}/%{name}/tests

%if %{with_openmpi}
%files -n python2-mpi4py-openmpi
%{python2_sitearch}/openmpi/%{name}-*.egg-info
%{python2_sitearch}/openmpi/%{name}
%endif

%if %{with_mpich}
%files -n python2-mpi4py-mpich
%{python2_sitearch}/mpich/%{name}-*.egg-info
%{python2_sitearch}/mpich/%{name}
%endif

%if 0%{?with_python3}
%if %{with_openmpi}
%files -n python%{python3_pkgversion}-mpi4py-openmpi
%{python3_sitearch}/openmpi/%{name}-*.egg-info
%{python3_sitearch}/openmpi/%{name}
%endif

%if %{with_mpich}
%files -n python%{python3_pkgversion}-mpi4py-mpich
%{python3_sitearch}/mpich/%{name}-*.egg-info
%{python3_sitearch}/mpich/%{name}
%endif
%endif

%files docs
%doc docs/* demo


%changelog
* Mon May 31 2021 Brian J. Murrell <brian.murrell@intel.com> - 3.0.3-2
- Remove virtual provides
- Package tests for both Python 2 and 3

* Thu Jun 25 2020 Brian J. Murrell <brian.murrell@intel.com> - 3.0.3-1
- Update to new release

* Fri Jun 19 2020 Brian J. Murrell <brian.murrell@intel.com> - 3.0.1-5
- Fix build on Leap 15.1

* Thu Jan 23 2020 Brian J. Murrell <brian.murrell@intel.com> - 3.0.1-4
- Build on Leap 15.1

* Sun Dec 29 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.0.1-3
- Add Provides: %{name}-cart-%{cart_major}-daos-%{daos_major}

* Fri Sep 06 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.0.1-2
- Disable openmpi build
- Add DAOS test
- Create tests subpackage
- BRs environment-modules, {mpich,openmpi}-autoload and ed
- tests needs to Requires: runtime

* Sat Feb 16 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.1-1
- Update to latest bugfix version (#1677683)

* Wed Feb 13 2019 Orion Poplawski <orion@nwra.com> - 3.0.0-6
- Rebuild for openmpi 3.1.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-3
- Rebuilt for Python 3.7

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 11 2017 Thomas Spura <tomspur@fedoraproject.org> - 3.0.0-1
- update to 3.0.0 (#1510901)

* Sun Oct 29 2017 Thomas Spura <tomspur@fedoraproject.org> - 2.0.0-14
- Set threads to serialized in openmpi due to #1105902

* Sun Oct 29 2017 Thomas Spura <tomspur@fedoraproject.org> - 2.0.0-13
- disable tests on openmpi due to #1105902 (#1423965)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Thomas Spura <tomspur@fedoraproject.org> - 2.0.0-10
- Reenable python3 package (#1461023)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 2 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.0-8
- Require appropriate mpi python support packages
- Remove useless provides

* Mon Oct 24 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.0-7
- Use upstream tox commands for tests
- Minor spec cleanup

* Mon Oct 24 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.0-7
- Enable python3 for EPEL

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.0-6
- Rebuild for openmpi 2.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 9 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0.0-2
- Bump obsoletes

* Sat Oct 24 2015 Thomas Spura <tomspur@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Wed Oct 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-16
- Rename mpi4py packages to python2-mpi4py

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 1.3.1-15
- Rebuild for openmpi 1.10.0

* Tue Aug 18 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.1-14
- Rebuild for rpm-mpi-hooks-3-2

* Mon Aug 17 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.1-13
- Rebuild for rpm-mpi-hooks-3-1

* Sat Aug 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.1-12
- Remove requires filtering... not necessary anymore

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> - 1.3.1-11
- Rebuild for RPM MPI Requires Provides Change

* Wed Jul 29 2015 Karsten Hopp <karsten@redhat.com> 1.3.1-10
- mpich is available on ppc64 now

* Mon Jun 29 2015 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-9
- Use new py_build/install macros

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Mar 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-7
- remove %%py3dir
- use python2 macros instead of unversioned ones

* Thu Mar 12 2015 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-6
- Rebuild for changed mpich libraries

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.3.1-3
- Rebuild for Python 3.4

* Mon Feb 24 2014 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-2
- Rebuilt for new mpich-3.1

* Thu Aug  8 2013 Thomas Spura <tomspur@fedoraproject.org> - 1.3.1-1
- update to 1.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Deji Akingunola <dakingun@gmail.com> - 1.3-8
- Rename mpich2 sub-packages to mpich and rebuild for mpich-3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Thomas Spura <tomspur@fedoraproject.org> - 1.3-6
- rebuild for newer mpich2

* Sat Aug  4 2012 Thomas Spura <tomspur@fedoraproject.org> - 1.3-5
- conditionalize mpich2 support, there is no mpich2 on el6-ppc64

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 1.3-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Thomas Spura <tomspur@fedoraproject.org> - 1.3-2
- filter requires in pysitearch/openmpi/mpi4py/lib-pmpi/lib (#741104)

* Fri Jan 20 2012 Thomas Spura <tomspur@fedoraproject.org> - 1.3-1
- update to 1.3
- filter provides in pythonsitearch
- run tests differently

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 30 2011 Deji Akingunola <dakingun@gmail.com> - 1.2.2-6
- Rebuild for mpich2 soname bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010  David Malcolm <dmalcolm@redhat.com> - 1.2.2-4
- rebuild for newer python3

* Tue Oct 19 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.2-3
- rebuild for new mpich2 and openmpi versions

* Wed Sep 29 2010 jkeating - 1.2.2-2
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.2-1
- update to new version

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.1-6
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul  7 2010 Thomas Spura <tomspur@fedoreproject.org> - 1.2.1-4
- doc package needs to require common package, because of licensing

* Sun Apr 11 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.1-3
- also provides python2-mpi4py-*

* Sat Feb 27 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.1-2
- delete R on the main package in docs subpackage
  (main package is empty -> would be an unresolved dependency)

* Sat Feb 27 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.1-1
- new version
- removing of hidden file not needed anymore (done upstream)
- fix spelling error builtin -> built-in

* Fri Feb 26 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2-7
- introduce OPENMPI and MPD macros to easy enable/disable the testsuite

* Tue Feb 16 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2-6
- don't delete *.pyx/*.pyd
- delete docs/source

* Mon Feb  8 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2-5
- disable testsuite

* Sun Feb  7 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2-4
- enable testsuite
- move huge docs into docs subpackage

* Sun Feb  7 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2-3
- delete lam building
- install to correct locations

* Sun Feb  7 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2-2
- compile for different mpi versions

* Sun Feb  7 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2-1
- initial import
