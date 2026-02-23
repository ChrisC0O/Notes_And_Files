find / -perm -4000 -type f 2>/dev/null | while read f; do
    exe="NO"
    write="NO"
    caps="$(getcap "$f" 2>/dev/null)"

    [ -x "$f" ] && exe="YES"
    [ -w "$f" ] && write="YES !!"

    [ -z "$caps" ] && caps="none"

    printf "\n%s\n" "$f"
    printf "  Executable : %s\n" "$exe"
    printf "  Writable   : %s\n" "$write"
    printf "  Capabilities: %s\n" "$caps"
    printf '%s\n' "------------------------------------------------------------"
done
