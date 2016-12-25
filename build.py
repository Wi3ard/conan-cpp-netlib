from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(visual_versions = [12, 14])
    builder.add_common_builds(shared_option_name="cpp-netlib:shared")
    builder.run()
