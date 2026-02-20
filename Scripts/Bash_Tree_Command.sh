#!/bin/bash

# Usage: ./mytree.sh [directory]
dir="${1:-.}"

# Recursive function to list directories/files with tree lines
list_dir() {
    local path="$1"
    local prefix="$2"

    # Get all items in the current directory
    local entries=("$path"/*)
    local count=${#entries[@]}
    local i=0

    for entry in "${entries[@]}"; do
        # Skip if no files
        [ -e "$entry" ] || continue
        i=$((i + 1))

        # Determine branch symbol
        if [ "$i" -eq "$count" ]; then
            branch="└── "
            new_prefix="$prefix    "
        else
            branch="├── "
            new_prefix="$prefix│   "
        fi

        # Print the entry
        echo "${prefix}${branch}$(basename "$entry")"

        # Recurse if directory
        if [ -d "$entry" ]; then
            list_dir "$entry" "$new_prefix"
        fi
    done
}

# Print the root
echo "$(basename "$dir")"
list_dir "$dir" ""
