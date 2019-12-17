NAME      := mpi4py
SRC_EXT   := gz
SOURCE     = https://bitbucket.org/$(NAME)/$(NAME)/downloads/$(NAME)-$(VERSION).tar.$(SRC_EXT)
PATCHES   := mpi4py-2.0.0-openmpi-threading.patch

include packaging/Makefile_packaging.mk
