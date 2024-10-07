# SPDX-License-Identifier: BSD-2-Clause-Patent
# Copyright (c) 2019-2024 Intel Corporation

NAME      := mpi4py
SRC_EXT   := gz

MOCK_OPTIONS := --nocheck

TEST_PACKAGES := mpi4py-common         \
	         mpi4py-debuginfo      \
	         mpi4py-docs           \
	         python2-mpi4py-tests  \
	         python36-mpi4py-mpich

include packaging/Makefile_packaging.mk
