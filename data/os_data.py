from curses.ascii import isdigit
import enum


class os_data(enum.IntEnum):
    # OS Versions, Based off Major Kernel Version
    cheetah =       4 # Actually 1.3.1
    puma =          5
    jaguar =        6
    panther =       7
    tiger =         8
    leopard =       9
    snow_leopard =  10
    lion =          11
    mountain_lion = 12
    mavericks =     13
    yosemite =      14
    el_capitan =    15
    sierra =        16
    high_sierra =   17
    mojave =        18
    catalina =      19
    big_sur =       20
    monterey =      21
    ventura =       22
    max_os =        99


class os_conversion:

    def os_to_kernel(self):
        # Convert OS version to major XNU version
        if self.startswith("10."):
            return int(self.split(".")[1]) + 4
        else:
            return int(self.split(".")[0]) + 9

    def kernel_to_os(self):
        # Convert major XNU version to OS version
        return str(self - 9) if self >= os_data.big_sur else str(f"10.{self - 4}")

    def is_os_newer(self, source_minor, target_major, target_minor):
        # Check if OS version 1 is newer than OS version 2
        if (
            self >= target_major
            and self == target_major
            and source_minor < target_minor
            or self < target_major
        ):
            return True
        elif self == target_major:
            return False

    def convert_kernel_to_marketing_name(self):
        # Convert major XNU version to Marketing Name
        try:
            # Find os_data enum name
            os_name = os_data(self).name

            # Remove "_" from the string
            os_name = os_name.replace("_", " ")

            # Upper case the first letter of each word
            os_name = os_name.title()
        except ValueError:
            # Handle cases where no enum value exists
            # Pass kernel_to_os() as a substitute for a proper OS name
            os_name = os_conversion.kernel_to_os(self)

        return os_name

    def convert_marketing_name_to_kernel(self):
        # Convert Marketing Name to major XNU version
        try:
            # Find os_data enum value
            os_kernel = os_data[self.lower().replace(" ", "_")]
        except KeyError:
            os_kernel = 0

        return os_kernel


    def find_largest_build(self):
        # Find the newest version within an array of versions
        # These builds will have both numbers and letters in the version
        # ex:
        # [
        #    "22A5295i",
        #    "22A5266r",
        #    "22A5286j",
        #    "22A5295h",
        # ]

        max_length =        0  # Length of the longest build
        build_array_split = [] # 'build_array', converted into individual array of elements
        # Convert strings to arrays
        for build in self:
            list_build = list(build)
            if len(list_build) > max_length:
                max_length = len(list_build)
            build_array_split.append(list_build)

        # Pad out each array to same length
        for build in build_array_split:
            while len(build) < max_length:
                build.append("0")

        # Convert all letters to int using ord()
        for build in build_array_split:
            for entry in build:
                if not entry.isdigit():
                    build[build.index(entry)] = ord(entry)

        for build_outer_loop in build_array_split:
            for build_inner_loop in list(build_array_split):
                for i in range(len(build_outer_loop)):
                    # remove any builds that are not the largest
                    if int(build_outer_loop[i]) > int(build_inner_loop[i]):
                        build_array_split.remove(build_inner_loop)
                        break
                    if int(build_outer_loop[i]) < int(build_inner_loop[i]):
                        break

        final_build = "".join(
            chr(entry) if int(entry) > 9 else str(entry)
            for entry in build_array_split[0]
        )
        # Since we pad with 0s, we need to next determine how many 0s to remove
        for build in self:
            if final_build.startswith(build):
                # Handle cases where Apple added a letter to the build
                # ex. "22A5295" vs "22A5295"
                remaining_strings = final_build.split(build)[1]
                # If all remaining strings are 0s, then we can remove the 0s
                if all(char == "0" for char in remaining_strings):
                    final_build = build

        return final_build