# Prevent brp-java-repack-jars from being run.
%global __jar_repack %{nil}

%global nb_            netbeans
%global nb_org         %{nb_}.org
%global nb_ver         6.7.1

%global svnCA          svnClientAdapter
%global svnCA_ver      1.6.0

Name:           %{nb_}-svnclientadapter
Version:        %{nb_ver}
Release:        5
Summary:        Subversion Client Adapter

License:        ASL 2.0
Url:            http://subclipse.tigris.org/svnClientAdapter.html
Group:          Development/Java

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export --force --username guest -r4383 \
#     http://subclipse.tigris.org/svn/subclipse/trunk/svnClientAdapter/ \
#     svnClientAdapter-1.6.0
# tar -czvf svnClientAdapter-1.6.0.tar.gz svnClientAdapter-1.6.0
Source0:        %{svnCA}-%{svnCA_ver}.tar.gz
Patch0:         %{svnCA}-%{svnCA_ver}-build.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  ant-junit
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  svn-javahl

Requires:       java >= 0:1.6.0
Requires:       jpackage-utils
Requires:       subversion

%description
SVNClientAdapter is a high-level Java API for Subversion.

%prep
%setup -q -n %{svnCA}-%{svnCA_ver}

# remove all binary libs
find . -name "*.jar" -exec %{__rm} -f {} \;

%patch0 -p1 -b .sav

%{__ln_s} -f %{_javadir}/svnkit-javahl.jar lib/svnjavahl.jar

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java 
ant -verbose svnClientAdapter.jar

%install
%{__rm} -fr %{buildroot}
# jar
%{__install} -d -m 755 %{buildroot}%{_javadir}
%{__install} -m 644 build/lib/svnClientAdapter.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc license.txt readme.txt
%{_javadir}/*

