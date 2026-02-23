find / -perm -4000 -type f 2>/dev/null | while read f; do
    printf "\n[SUID] %s\n" "$f"
    printf "  Run        : %s\n" "$( [ -x "$f" ] && echo YES || echo NO )"
    printf "  Writable   : %s\n" "$( [ -w "$f" ] && echo YES || echo NO )"
    printf "  POSIX Cap  : %s\n" "$(getcap "$f" 2>/dev/null || echo none)"
    printf '%s\n' "----------------------------------------"
done
