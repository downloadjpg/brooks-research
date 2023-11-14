import main
import re
verbose_pattern = main.pattern.pattern
# Replace comments but preserve escaped whitespace
# Remove comments to make it non-verbose
non_verbose_pattern = re.sub(r'#.*$', '', verbose_pattern, flags=re.MULTILINE)
# Remove leading and trailing white spaces on each line
non_verbose_pattern = '\n'.join(line.strip() for line in non_verbose_pattern.split('\n'))
# Remove spaces, except for \- which should become ' '
non_verbose_pattern = re.sub(r'(?<!\\)[ \n]+', '', non_verbose_pattern)
print(non_verbose_pattern)