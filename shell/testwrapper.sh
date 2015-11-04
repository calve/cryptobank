# Return 0 if all testes passes, non-zero otherwise
./command.sh -a &&
if ./command.sh -b; then
    exit 1
fi
if ./command.sh -c; then
    exit 1
fi
if ./command.sh -d; then
    exit 1
fi
exit 0
