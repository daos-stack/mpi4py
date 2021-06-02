NAME      := mpi4py
SRC_EXT   := gz

MOCK_OPTIONS := --nocheck

TEST_PACKAGES := mpi4py-common                                              \
	         mpi4py-debuginfo                                           \
	         mpi4py-docs                                                \
	         mpi4py-tests                                               \
	         python$(shell rpm --eval %python3_pkgversion)-mpi4py-mpich

include packaging/Makefile_packaging.mk
