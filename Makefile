NAME      := mpi4py
SRC_EXT   := gz

MOCK_OPTIONS := --nocheck

TEST_PACKAGES := mpi4py-common         \
	         mpi4py-debuginfo      \
	         mpi4py-docs           \
	         python2-mpi4py-tests  \
	         python36-mpi4py-mpich

include packaging/Makefile_packaging.mk
