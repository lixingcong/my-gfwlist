#! /bin/bash

INVALID_DNS_SERVER=5.4.3.2
DIG="dig @$INVALID_DNS_SERVER +timeout=1 +retries=0"

if [ $# -ne 1 ]; then
    echo "Usage: bash xxx.sh /path/to/domains.txt"
    exit 1
fi

FILENAME=$1

if [ ! -f $FILENAME ]; then
    echo "$FILENAME is not a file"
    exit 1
fi

while read domain; do
    [ -z "$domain" ] && continue
    [[ "$domain" == \#* ]] && continue

    if [[ $domain == :* ]] && [[ $domain == *: ]]; then
        echo "  ignore: $domain"
        continue
    fi

    $DIG $domain > /dev/null 2>&1
    if [ "0" = $? ]; then
        echo "Poisoning: $domain"
    else
        echo "       ok: $domain"
    fi
done < $FILENAME
