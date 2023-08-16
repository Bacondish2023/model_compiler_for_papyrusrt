##
# @brief Top level build script
#
# @note CMake command line tool is used for os-independent build
#

BUILD_DIR = zzz_build
CODEGEN_DIR = zzz_codegen
ECHO = cmake -E echo
CD = cmake -E chdir
MKDIR = cmake -E make_directory
RM = cmake -E rm

.PHONY: all
all: $(BUILD_DIR)
	$(CD) $(BUILD_DIR) $(MAKE) model_compile
	$(CD) $(BUILD_DIR) $(MAKE) rebuild_cache
#	$(CD) $(BUILD_DIR) $(MAKE) --jobs -O
	$(CD) $(BUILD_DIR) $(MAKE)

$(BUILD_DIR): $(CODEGEN_DIR)
	$(MKDIR) $(BUILD_DIR)
	$(CD) $(BUILD_DIR) cmake -DCMAKE_BUILD_TYPE="Release" -G "Unix Makefiles" ..

$(CODEGEN_DIR):
	$(MKDIR) $(CODEGEN_DIR)
	python -B model_compiler_for_papyrusrt/model_compiler_for_papyrusrt/misc/dummy_cmakelists_generator.py $(CODEGEN_DIR)

.PHONY: clean
clean:
	$(RM) -rf $(CODEGEN_DIR)
	$(RM) -rf $(BUILD_DIR)

.PHONY: help
help:
	$(ECHO) all:    Create target such as executable and library
	$(ECHO) clean:  Removes all deriverables and temporary files
	$(ECHO) help:   Show targets
